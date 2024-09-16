from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi_another_jwt_auth import AuthJWT
from pydantic import BaseModel, Field
from modules.database.DB import GetUser, GetRevokedTokens
from modules.utils.jwt_exceptions import handle_jwt_exceptions, create_response_dict
from config.server import AddRouter
from typing import Dict

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LogoutForm(BaseModel):
    access_token: str = Field(..., description="The access token to be revoked")

class RefreshResponse(BaseModel):
    access_token: str = Field(..., description="The new access token")

@router.post("/refresh", response_model=RefreshResponse, responses= create_response_dict(AccessToken=False))
def refresh(Authorize: AuthJWT = Depends(), authorization: str = Header(None)):
    """
    This endpoint is used to refresh the access token.

    Note: send the refresh token in the Authorization header as a Bearer token.
    """
    def refresh_logic():
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        access_token = Authorize.create_access_token(subject=current_user)
        return {"access_token": access_token}

    handle_jwt_exceptions(refresh_logic, AccessToken=False)

@router.post("/logout", response_model=LogoutForm, responses= create_response_dict(RefreshToken=False))
def logout(form: LogoutForm, Authorize: AuthJWT = Depends(), authorization: str = Header(None)):
    """
    This endpoint is used to revoke the access token and refresh token.
    """
    def logout_logic():
        Authorize.jwt_refresh_required()
        jti = Authorize.get_raw_jwt()['jti']
        # logic goes here
        return {"message": "Successfully logged out"}

    handle_jwt_exceptions(logout_logic, RefreshToken=False)

AddRouter(router) # Add the router to the server