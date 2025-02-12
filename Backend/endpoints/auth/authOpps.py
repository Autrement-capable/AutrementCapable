from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi_another_jwt_auth import AuthJWT
from pydantic import BaseModel, Field
from utils.jwt_exceptions import create_response_dict
from database.postgress.config import getSession  # Uses AsyncSession from SQLAlchemy
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

@router.post("/refresh", response_model=RefreshResponse,
             responses=create_response_dict(AccessToken=False),
             tags=["Auth_refresh"])
async def refresh(request: Request, Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(getSession)):
    """
    Refresh the access token. Requires a valid refresh token.
    """
    Authorize.jwt_refresh_token_required()
    user_id = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=user_id, fresh=False)
    return {"access_token": access_token}

@router.post("/logout",
             responses=create_response_dict(),
             response_model=LogoutResponse,
             tags=["Auth", "Auth_refresh"])
async def logout(request: Request, form: LogoutForm, Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(getSession)):
    """
    Revoke access and refresh tokens to log out the user.
    """

    # Revoke Access Token
    Authorize.jwt_required()
    jti_access = Authorize.get_raw_jwt()["jti"]
    expires_access = datetime.utcfromtimestamp(Authorize.get_raw_jwt()["exp"])

    is_ok = await revoke_token(session, jti_access, expires_access, "access", commit=False)
    if not is_ok:
        raise HTTPException(status_code=401, detail="Invalid access token (Already Revoked)")

    # Revoke Refresh Token
    refresh_token = form.refresh_token.replace("Bearer ", "")
    try:
        decoded_token = Authorize.get_raw_jwt(refresh_token)
        jti_refresh = decoded_token["jti"]
        expires_refresh = datetime.utcfromtimestamp(decoded_token["exp"])

        await revoke_token(session, jti_refresh, expires_refresh, "refresh")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return {"msg": "Successfully logged out"}

AddRouter(router)
