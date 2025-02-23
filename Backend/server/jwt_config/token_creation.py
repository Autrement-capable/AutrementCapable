import jwt
import datetime
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from fastapi import HTTPException, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from server.jwt_config.config import settings as S
from database.postgress.config import getSession
from database.postgress.models import RevokedToken
from typing import Union
from uuid import uuid4
import base64

# not 100% sure if this shulbe here or in database.postgress.actions.revoked_jwt_tokens
async def is_token_revoked(session: AsyncSession, jti: str) -> bool:
    """ Check if a token is in the revoked token list
    Args:
    session (AsyncSession): The SQLAlchemy session
    jti (str): The JWT ID of the token

    Returns:
    bool: True if the token is revoked, False otherwise"""
    from database.postgress.actions.revoked_jwt_tokens import get_revoked_token_by_jti

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
        if not auth_header or not auth_header.startswith(S.Auth_schema):
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
        return jwt.decode(decrypted, S.authjwt_secret_key, algorithms=[S.authjwt_algorithm])
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
    payload = {
        "sub": user_id,
        "role": role_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=S.jwt_access_token_expires),
        "fresh": fresh,
        "jti": base64.urlsafe_b64encode(uuid4().bytes).decode().rstrip("=")
    }
    encrypted_data = encrypt_payload(payload)
    jwt_payload = {"refresh": refresh, "payload": encrypted_data.hex()}  # Store encrypted data as hex
    return jwt.encode(jwt_payload, S.authjwt_secret_key, algorithm=S.authjwt_algorithm)

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
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error decoding token.")

from fastapi import Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

class JWTBearer:
    """ Dependency class for requiring a valid JWT token """

    def __init__(self, is_refresh: bool = False, required_fresh: bool = False):
        """
        Args:
            is_refresh (bool): If True, requires a refresh token instead of an access token.
            required_fresh (bool): If True, ensures the token is fresh.
        """
        self.is_refresh = is_refresh
        self.required_fresh = required_fresh
        self._payload = None  # Stores decoded JWT payload

    async def __call__(self, request: Request, session: AsyncSession = Depends(getSession)):
        """
        Extract, decode, and validate JWT token.

        Args:
            request (Request): Auto-injected FastAPI request object.
            session (AsyncSession): Auto-injected SQLAlchemy session.

        Returns:
            dict: The decoded JWT payload and a boolean indicating if the token is a refresh token.

        Raises:
            HTTPException: If the token is invalid, expired, revoked, or does not meet requirements.

        Note:
          dict schema:
            ```json
            {
                "payload": dict,
                "is_refresh": bool
            }
        """
        self._payload = await decode_token(
            session, request, is_refresh=self.is_refresh, required_fresh=self.required_fresh
        )
        return {"payload": self._payload, is_refresh: self.is_refresh}