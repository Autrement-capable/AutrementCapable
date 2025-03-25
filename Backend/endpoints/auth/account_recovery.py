from fastapi import APIRouter, Depends, Request, HTTPException
from server.jwt_config.token_creation import create_token, JWTBearer
from pydantic import BaseModel, Field, EmailStr
from utils.password import hash_password
from database.postgress.config import getSession as GetSession
from database.postgress.actions.password_reset import get_acc_recovery_by_token, del_acc_recovery

from server.server import AddRouter
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from os import getenv

router = APIRouter(prefix="/recovery", tags=["Account Recovery"])

class ResetForm(BaseModel):
    password: str = Field(..., title="The new password.", description="The new password for the user.")
    token: str = Field(..., title="The password reset token.", description="The password reset token.")

class TokenResponse(BaseModel):
    access_token: str = Field(..., title="The access token.", description="The access token for the user.")
    refresh_token: str = Field(..., title="The refresh token.", description="The refresh token for the user.")

@router.get("/is-valid-reset", response_model=dict, responses={200: {"valid": True}, 404: {"valid": False}})
async def is_valid_reset(request: Request, token: str, session: AsyncSession = Depends(GetSession)):
    """
    Check if a password reset token is valid.
    This should be called first by the frontend to check if the token is valid before allowing the user to reset their password.
    """
    reset = await get_acc_recovery_by_token(session, token)
    if not reset or reset.token_expires < datetime.now():
        return {"valid": False}, 404
    return {"valid": True}

@router.post("/reset-password", response_model=TokenResponse)
async def reset_password(request: Request, form: ResetForm, session: AsyncSession = Depends(GetSession)):
    """
    Reset a user's password.
    """
    reset = await get_acc_recovery_by_token(session, form.token)
    if not reset or reset.token_expires < datetime.now():
        raise HTTPException(status_code=404, detail="Token not found or has expired.")
    user = reset.user
    user.password_hash = hash_password(form.password)

    try:
        user.account_recovery = [] # should work cause of cascade set to orphab-delete
        session.add(user)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the user's password.")

    access_token = create_token(user.id, user.role_id, refresh=False, fresh=True)
    refresh_token = create_token(user.id, user.role_id, refresh=True, fresh=True)
    await del_acc_recovery(session, reset)
    return {"access_token": access_token, "refresh_token": refresh_token}

## WIP in the future will require fresh access token. i need to figure out how to make
## that work with passkeys
@router.get("/create-account-recovery", response_model=dict,
responses={200: {"message": "Account recovery created."}}, tags=["Auth"])
async def create_account_recovery(request: Request, session: AsyncSession = Depends(GetSession), JWT: dict = Depends(JWTBearer())):
    """
    Create an account recovery for a user. (Used when tranfering to a new device that does not have registered passkeys)
    """
    payload = JWT["payload"]
    user_id = payload["sub"]
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.account_recovery: # dont know if this is the right way to check if the user has an account recovery
        raise HTTPException(status_code=400, detail="Account recovery already exists.")
    recovery_code = await create_acc_recovery(session, user)
    if not recovery_code:
        raise HTTPException(status_code=500, detail="An error occurred while creating the account recovery.")
    return {"recover_code": recovery_code} # WIP, for now just return the recovery code
AddRouter(router)

