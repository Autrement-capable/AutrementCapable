from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_another_jwt_auth import AuthJWT
from pydantic import BaseModel
from modules.database.DB import GetUser, GetRevokedTokens
from typing import Dict

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LogoutForm(BaseModel):
    access_token: str

class RefreshResponse(BaseModel):
    access_token: str

@router.post("/refresh", response_model=RefreshResponse)
def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        access_token = Authorize.create_access_token(subject=current_user)
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/logout", response_model=LogoutForm)
def logout(form: LogoutForm, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_required()
        jti = Authorize.get_raw_jwt()['jti']
        # logic goes here
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
