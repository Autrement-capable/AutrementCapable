from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi_another_jwt_auth import AuthJWT
from pydantic import BaseModel, Field
from modules.utils.jwt_exceptions import create_response_dict
from database.postgress.actions.revoked_jwt_tokens import revoke_token, get_revoked_token_by_jti
from config.server import AddRouter, server
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LogoutResponse(BaseModel):
    msg: str = Field(..., description="The message")

class RefreshResponse(BaseModel):
    access_token: str = Field(..., description="The new access token")

class LogoutForm(BaseModel):
    refresh_token: str = Field(..., description="The refresh token. Putting 'Bearer' is optional")

@router.post("/refresh", response_model=RefreshResponse,
             responses=create_response_dict(AccessToken=False),
             tags=["Auth_refresh"])
async def refresh(request: Request, Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(server.get_Psession)):
    """
    This endpoint is used to refresh the access token.

    Note: Send the refresh token in the Authorization header as a Bearer token.
    """
    Authorize.jwt_refresh_token_required()
    user_id = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=user_id, fresh=False)
    return {"access_token": access_token}


@router.post("/logout",
             responses=create_response_dict(),
             response_model=LogoutResponse,
             tags=["Auth", "Auth_refresh"])
async def logout(request: Request, form: LogoutForm, Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(server.get_Psession)):
    """
    This endpoint is used to revoke the access token and refresh token.
    """

    # Revoke the access token
    Authorize.jwt_required()
    print("gets to here")
    jti_access = Authorize.get_raw_jwt()["jti"]
    expires_access = datetime.utcfromtimestamp(Authorize.get_raw_jwt()["exp"])

    # Revoke the access token
    is_ok = await revoke_token(session, jti_access, expires_access, "access", commit=False)
    if not is_ok:
        print("Error here: Access token already revoked")
        raise HTTPException(status_code=401, detail="Invalid access token") # most likely the token is already revoked


    refresh_token = form.refresh_token.replace("Bearer ", "")
    # Verify the refresh token
    try:
        decoded_token = Authorize.get_raw_jwt(refresh_token)
        jti_refresh = decoded_token["jti"]
        expires_refresh = datetime.utcfromtimestamp(decoded_token["exp"])
        await revoke_token(session, jti_refresh, expires_refresh, "refresh")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return {"msg": "Successfully logged out"}

AddRouter(router)  # Add the router to the server