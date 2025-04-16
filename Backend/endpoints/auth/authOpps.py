from fastapi import APIRouter, Depends, Request, HTTPException, Response, Cookie
from server.jwt_config.token_creation import create_token, decode_token, JWTBearer, set_refresh_cookie, clear_refresh_cookie
from utils import secured_endpoint, SecurityRequirement
from pydantic import BaseModel, Field
from utils.jwt_exceptions import create_response_dict
from database.postgress.config import getSession
from database.postgress.actions.revoked_jwt_tokens import revoke_token
from server.server import AddRouter
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Response Models
class LogoutResponse(BaseModel):
    msg: str = Field(..., description="The message")

class RefreshResponse(BaseModel):
    access_token: str = Field(..., description="The new access token")

@router.post("/refresh",
             response_model=RefreshResponse,
             responses=create_response_dict(AccessToken=False))
@secured_endpoint(security_type=SecurityRequirement.REFRESH_COOKIE)
async def refresh(
    response: Response,
    refresh_token: Optional[str] = Cookie(None, alias="refresh_token"),
    session: AsyncSession = Depends(getSession)
):
    """
    Refresh the access token. Requires a valid refresh token stored in an HTTP-only cookie.

    The refresh token comes from an HTTP-only cookie, and a new access token is returned in the response body.
    """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        # Decode the refresh token from the cookie
        jwt_payload = await decode_token(session, refresh_token, is_refresh=True)

        # Create a new access token
        access_token = create_token(jwt_payload["sub"], jwt_payload["role"], refresh=False)

        # Generate a new refresh token for security reasons
        new_refresh_token = create_token(jwt_payload["sub"], jwt_payload["role"], refresh=True)

        # Set the new refresh token as a cookie
        set_refresh_cookie(response, new_refresh_token)

        return {"access_token": access_token}
    except Exception as e:
        # If the token validation fails, clear the cookie
        clear_refresh_cookie(response)
        raise

@router.post("/logout",
             responses=create_response_dict(),
             response_model=LogoutResponse)
@secured_endpoint(security_type=SecurityRequirement.BOTH_TOKENS)
async def logout(
    response: Response,
    refresh_token: Optional[str] = Cookie(None, alias="refresh_token"),
    session: AsyncSession = Depends(getSession),
    JWT: dict = Depends(JWTBearer())
):
    """
    Revoke access and refresh tokens to log out the user.

    The access token is provided in the Authorization header.
    The refresh token is automatically retrieved from the HTTP-only cookie.
    Both tokens are revoked on the server and the refresh cookie is cleared.
    """
    access_payload = JWT["payload"]
    jti_access = access_payload["jti"]
    expires_access = datetime.utcfromtimestamp(access_payload["exp"])

    # Revoke the access token
    is_ok = await revoke_token(session, jti_access, expires_access, "access", commit=False)
    if not is_ok:
        raise HTTPException(status_code=401, detail="Invalid access token (Already Revoked)")

    # Clear the refresh cookie
    clear_refresh_cookie(response)

    # Revoke the refresh token if it exists
    if refresh_token:
        try:
            refresh_payload = await decode_token(session, refresh_token, is_refresh=True)
            jti_refresh = refresh_payload["jti"]
            expires_refresh = datetime.utcfromtimestamp(refresh_payload["exp"])
            await revoke_token(session, jti_refresh, expires_refresh, "refresh")
        except Exception:
            # If token is invalid, we just continue as we already cleared the cookie
            pass

    return {"msg": "Successfully logged out"}

AddRouter(router)