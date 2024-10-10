from fastapi import APIRouter, Depends
from fastapi_another_jwt_auth import AuthJWT
from pydantic import BaseModel, Field
# from modules.database.DB import GetUser, GetRevokedTokens
from modules.utils.jwt_exceptions import create_response_dict
from database.postgress.actions.revoked_jwt_tokens import revoke_token
from config.server import AddRouter, server
from sqlmodel import Session

from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LogoutResponce(BaseModel):
    msg: str = Field(..., description="The message")

class RefreshResponse(BaseModel):
    access_token: str = Field(..., description="The new access token")

@router.post("/refresh", response_model=RefreshResponse,
             responses= create_response_dict(AccessToken=False),
             tags=["Auth_refresh"])
def Refresh(Authorize: AuthJWT = Depends()):
    """
    This endpoint is used to refresh the access token.

    Note: send the refresh token in the Authorization header as a Bearer token.
    """

    Authorize.jwt_refresh_token_required()
    user_id = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=user_id, fresh=False)
    return {"access_token": access_token}


@router.post("/logout",
             responses= create_response_dict(),
             response_model=LogoutResponce,
             tags=["Auth", "Auth_refresh"])
def Logout(Authorize: AuthJWT = Depends(), session: Session = Depends(server.get_Psession)):
    """
    This endpoint is used to revoke the access token and refresh token.
    """

    # Revoke the access token
    Authorize.jwt_required()
    jti_access = Authorize.get_raw_jwt()["jti"]
    expires_access = datetime.utcfromtimestamp(Authorize.get_raw_jwt()["exp"])
    revoke_token(jti_access, expires_access, "access", session, commit=False)

    # Revoke the refresh token
    Authorize.jwt_refresh_token_required()
    jti_refresh = Authorize.get_raw_jwt()["jti"]
    expires_refresh = datetime.utcfromtimestamp(Authorize.get_raw_jwt()["exp"])
    revoke_token(jti_refresh, expires_refresh, "refresh", session)

    return {"msg": "Successfully logged out"}

AddRouter(router) # Add the router to the server