from fastapi import APIRouter, Depends, Request, HTTPException
from server.jwt_config.token_creation import create_token, decode_token, JWTBearer
from pydantic import BaseModel, Field
from utils.jwt_exceptions import create_response_dict
from database.postgress.config import getSession
from database.postgress.actions.revoked_jwt_tokens import revoke_token
from server.server import AddRouter
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Response Models
class LogoutResponse(BaseModel):
    msg: str = Field(..., description="The message")

class RefreshResponse(BaseModel):
    access_token: str = Field(..., description="The new access token")

class LogoutForm(BaseModel):
    refresh_token: str = Field(..., description="The refresh token. 'Bearer' is optional")

@router.post("/refresh",
             response_model=RefreshResponse,
             responses=create_response_dict(AccessToken=False),
             tags=["Auth_refresh"])
async def refresh(
    jwt: dict = Depends(JWTBearer(is_refresh=True))
):
    """
    Refresh the access token. Requires a valid refresh token.

    - The refresh token is sent in the Authorization header as Bearer {refresh_token}
    """
    jwt = jwt["payload"]
    access_token = create_token(jwt["sub"], jwt["role"], refresh=False)
    return {"access_token": access_token}

@router.post("/logout",
             responses=create_response_dict(),
             response_model=LogoutResponse,
             tags=["Auth", "Auth_refresh"])
async def logout(request: Request, form: LogoutForm = Depends(), session: AsyncSession = Depends(getSession), JWT: dict = Depends(JWTBearer())):
    """
    Revoke access and refresh tokens to log out the user.
    """

    access_payload = JWT["payload"]
    jti_access = access_payload["jti"]
    expires_access = datetime.utcfromtimestamp(access_payload["exp"])

    is_ok = await revoke_token(session, jti_access, expires_access, "access", commit=False)
    if not is_ok:
        raise HTTPException(status_code=401, detail="Invalid access token (Already Revoked)")

    # Revoke Refresh Token
    refresh_token = form.refresh_token.replace("Bearer ", "")
    try:
        refresh_payload = await decode_token(session, refresh_token, is_refresh=True)
        jti_refresh = refresh_payload["jti"]
        expires_refresh = datetime.utcfromtimestamp(refresh_payload["exp"])
        await revoke_token(session, jti_refresh, expires_refresh, "refresh")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return {"msg": "Successfully logged out"}

AddRouter(router)
