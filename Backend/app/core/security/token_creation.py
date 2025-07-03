import os
import jwt
import datetime
import base64
from uuid import uuid4
from typing import Union, Optional, Dict, Any

from fastapi import HTTPException, status, Depends, Request, Response, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .config import settings as S
from ...db.postgress.engine import getSession
from ...db.postgress.models import RevokedToken

# not 100% sure if this shulbe here or in database.postgress.actions.revoked_jwt_tokens
async def is_token_revoked(session: AsyncSession, jti: str) -> bool:
    """ Check if a token is in the revoked token list
    Args:
    session (AsyncSession): The SQLAlchemy session
    jti (str): The JWT ID of the token

    Returns:
    bool: True if the token is revoked, False otherwise"""
    from ...db.postgress.repositories.revoked_jwt_tokens import get_revoked_token_by_jti

    result = await get_revoked_token_by_jti(session, jti)
    return result is not None

def extract_token_from_header(request: Request) -> str:
    """ Extract JWT token from Authorization header

    Args:
        request (Request): The FastAPI request object

    Returns:
        str: The JWT token
    """
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith(S.auth_schema):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing Authorization header.")
        return auth_header.split(" ")[1]
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error extracting token from header.")

def encrypt_payload(payload: dict) -> bytes:
    """ Encrypt JWT payload using AES-GCM

    Args:
        payload (dict): The JWT payload to be encrypted

    Returns:
        bytes: The nonce and encrypted payload into a single byte string
    """
    aesgcm = AESGCM(S.aes_key)
    nonce = os.urandom(S.nonce_size)  # Generate a unique nonce per encryption
    data = jwt.encode(payload, S.authjwt_secret_key, algorithm=S.authjwt_algorithm).encode()
    encrypted = aesgcm.encrypt(nonce, data, None)
    return nonce + encrypted

def decrypt_payload(encrypted_payload: bytes) -> dict:
    """ Decrypt JWT payload using AES-GCM

    Args:
        encrypted_payload (bytes): The encrypted payload(must include nonce)

    Returns:
        dict: The decrypted payload
    """

    try:
        aesgcm = AESGCM(S.aes_key)
        nonce = encrypted_payload[:S.nonce_size]
        data = encrypted_payload[S.nonce_size:]
        decrypted = aesgcm.decrypt(nonce, data, None).decode()
        payload = jwt.decode(decrypted, S.authjwt_secret_key, algorithms=[S.authjwt_algorithm])
        # because there is some standart i need to follow sub must be str so i convert it back to int
        payload["sub"] = int(payload["sub"])
        return payload
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error decrypting token.")

def create_token(user_id: int, role_id: int, refresh: bool = False, fresh: bool = False) -> str:
    """ Create a JWT (access or refresh) token for the user

    Args:
    user_id (int): The user ID
    role_id (int): The role ID (used for role-based access control)
    refresh (bool): If creating an access token, set to False. If creating a refresh token, set to True. Defaults to False.
    fresh (bool): True if the token is fresh, defaults to False

    Returns:
    str: The JWT token(payload contains the token type and the encrypted data)

    Note:
    **Payload Schema**:
    ```json
    {
        "refresh": bool, //True if refresh token, False if access token
        "payload": bytes
    }
    ```
    """
    # Set the expiration time based on token type
    expires_delta = datetime.timedelta(seconds=S.jwt_refresh_token_expires if refresh else S.jwt_access_token_expires)

    payload = {
        "sub": str(user_id),
        "role": role_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + expires_delta,
        "fresh": fresh,
        "jti": base64.urlsafe_b64encode(uuid4().bytes).decode().rstrip("=")
    }
    encrypted_data = encrypt_payload(payload)
    jwt_payload = {"refresh": refresh, "payload": encrypted_data.hex()}  # Store encrypted data as hex
    return jwt.encode(jwt_payload, S.authjwt_secret_key, algorithm=S.authjwt_algorithm)

def set_refresh_cookie(response: Response, refresh_token: str):
    """
    Set refresh token in an HTTP-only secure cookie

    Args:
        response (Response): FastAPI response object
        refresh_token (str): The refresh token to store
    """
    cookie_settings = {
        "key": "refresh_token",
        "value": refresh_token,
        "httponly": True,
        "secure": S.cookie_secure,  # True in production, can be False in development
        "samesite": "lax",  # Helps prevent CSRF
        "max_age": S.jwt_refresh_token_expires,
        "path": "/auth"  # Limit cookie to auth routes only
    }
    response.set_cookie(**cookie_settings)

def clear_refresh_cookie(response: Response):
    """
    Clear the refresh token cookie

    Args:
        response (Response): FastAPI response object
    """
    response.delete_cookie(key="refresh_token", path="/auth")

    # Also clear from root path to be thorough
    response.delete_cookie(
        key="refresh_token",
        path="/",
        secure=True,
        httponly=True,
        samesite="lax"
    )

async def decode_token(session: AsyncSession, token_source: Union[Request, str], is_refresh: bool = False, required_fresh: bool = False) -> dict:
    """ Extract, decode, and verify JWT token from request header or JWT string

    Args:
    session (AsyncSession): The SQLAlchemy session
    token_source (Request | JWT (str)): The FastAPI request object | The JWT token string
    is_refresh (bool): True if decoding a refresh token, False if decoding an access token, defaults to False
    required_fresh (bool): True if the token must be fresh, defaults to False

    Returns:
    dict: The decoded payload

    Raises:
    - If the token is invalid, expired, or revoked, an HTTPException is raised
    - If the token is not fresh, an HTTPException is raised if required_fresh is True

    Note:
    **Decrypted Payload Schema**:
    ```json
    {
        "sub": int, // The user ID
        "role": int, // The role ID
        "iat": datetime, // The issued at time
        "exp": datetime, // The expiration time
        "fresh": bool, // True if the token is fresh
        "jti": str // The JWT ID
    }
        ```
    """
    if isinstance(token_source, str):
        token = token_source
    else:
        token = extract_token_from_header(token_source)
    try:
        payload = jwt.decode(token, S.authjwt_secret_key, algorithms=[S.authjwt_algorithm])
        if "refresh" not in payload or "payload" not in payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format.")

        if payload["refresh"] != is_refresh:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type.")

        decrypted_payload = decrypt_payload(bytes.fromhex(payload["payload"]))

        if required_fresh and not decrypted_payload.get("fresh", False):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not fresh.")

        if await is_token_revoked(session, decrypted_payload["jti"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked.")

        return decrypted_payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
    except HTTPException:
        raise # Re-raise HTTPException
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error decoding token.")

# HTTP bearer scheme for access token extraction
http_bearer = HTTPBearer(auto_error=False)

import warnings

class JWTBearer:
    """DEPRECATED: This class is deprecated and will be removed in future versions.

    Please use the `secured_endpoint` decorator instead:
    ```python
    from app.core.security.decorators import secured_endpoint

    @router.get("/protected-route")
    @secured_endpoint()  # Use parameters like secured_endpoint(fresh=True) if needed
    async def protected_endpoint(jwt, session): # jwt and session are auto-injected
        # jwtP["sub"] is the user ID
        # jwtP["role"] is the role ID
        return {"message": "Success"}
    ```
    """

    def __init__(self, is_refresh: bool = False, required_fresh: bool = False):
        """
        Args:
            is_refresh (bool): If True, requires a refresh token instead of an access token.
            required_fresh (bool): If True, ensures the token is fresh.
        """
        warnings.warn(
            "JWTBearer is deprecated. Use secured_endpoint instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self.is_refresh = is_refresh
        self.required_fresh = required_fresh
        self._payload = None  # Stores decoded JWT payload

    async def __call__(
        self, 
        request: Request, 
        response: Response = None,
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
        refresh_token: Optional[str] = Cookie(None, alias="refresh_token"),
        session: AsyncSession = Depends(getSession)
    ):
        """
        Extract, decode, and validate JWT token from either header (access token) or cookie (refresh token).

        Args:
            request (Request): Auto-injected FastAPI request object.
            response (Response, optional): Auto-injected FastAPI response object.
            credentials (HTTPAuthorizationCredentials, optional): Access token extracted from header.
            refresh_token (str, optional): Refresh token extracted from cookie.
            session (AsyncSession): Auto-injected SQLAlchemy session.

        Returns:
            dict: The decoded JWT payload and a boolean indicating if the token is a refresh token.

        Raises:
            HTTPException: If the token is invalid, expired, revoked, or does not meet requirements.
        """
        if self.is_refresh:
            # For refresh tokens, check the cookie
            if not refresh_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Refresh token missing. Please login again."
                )
            token = refresh_token
            # Decode directly from the string
            self._payload = await decode_token(
                session, token, is_refresh=True, required_fresh=self.required_fresh
            )
        else:
            # For access tokens, check the Authorization header
            if not credentials:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Access token missing. Please login again."
                )
            # Decode from the header
            self._payload = await decode_token(
                session, credentials.credentials, is_refresh=False, required_fresh=self.required_fresh
            )

        return {"payload": self._payload, "refresh": self.is_refresh}