from fastapi import APIRouter, Depends
from fastapi_another_jwt_auth import AuthJWT
from pydantic import BaseModel, Field
# from modules.database.DB import GetUser, GetRevokedTokens
from modules.utils.jwt_exceptions import create_response_dict
from config.server import AddRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LogoutForm(BaseModel):
    refresh_token: str = Field(..., description="The refresh token needs to be revoked as well")

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

    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": access_token}


@router.post("/logout", response_model=LogoutForm,
             responses= create_response_dict(RefreshToken=False),
             tags=["Auth"])
def Logout(form: LogoutForm, Authorize: AuthJWT = Depends()):
    """
    This endpoint is used to revoke the access token and refresh token.
    """

    Authorize.access_token_required()
    jti = Authorize.get_raw_jwt()['jti'] # should be the access token jti
    refresh_token = form.refresh_token
    print("access_token", jti)
    print("refresh_token", refresh_token)
    # RevokeToken(jti, refresh_token)
    return {"message": "Successfully logged out"}

AddRouter(router) # Add the router to the server