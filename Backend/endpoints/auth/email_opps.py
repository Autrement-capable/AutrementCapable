from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi_another_jwt_auth import AuthJWT
from pydantic import BaseModel, Field, EmailStr
from utils.password import hash_password
from utils.jwt_exceptions import create_response_dict
from database.postgress.config import GetSession
from database.postgress.actions.user import get_user_by_email, update_user, get_user_by_id
from database.postgress.actions.revoked_jwt_tokens import revoke_token, get_revoked_token_by_jti
from database.postgress.actions.password_reset import get_password_reset_by_token, create_password_reset, del_password_reset
from database.postgress.actions.unverified_user import verify_user
from mail.actions.reset_password import send_reset_password_email

from server.server import AddRouter
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from os import getenv


class ResetForm(BaseModel):
    password: str = Field(..., title="The new password.", description="The new password for the user.")
    token: str = Field(..., title="The password reset token.", description="The password reset token.")

class TokenResponse(BaseModel):
    access_token: str = Field(..., title="The access token.", description="The access token for the user.")
    refresh_token: str = Field(..., title="The refresh token.", description="The refresh token for the user.")

class ResetRequestForm(BaseModel):
    email: EmailStr

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/verify", response_model=TokenResponse)
async def verify_users(request: Request, code: str, Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(GetSession)):
    """
    Verify a user using their verification code.
    """
    user = await verify_user(session, code, fresh=True)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or the token has expired.")
    access_token = Authorize.create_access_token(subject=user.user_id, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.user_id)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/start-reset-password", responses={200: {"message": "Password reset email sent."}})
async def try_reset_password(request: Request, form: ResetRequestForm, session: AsyncSession = Depends(GetSession)):
    """
    Initiate a password reset for a user.
    """
    user = await get_user_by_email(session, form.email, lazy=False)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    reset = await create_password_reset(session, user)
    if not reset:
        raise HTTPException(status_code=500, detail="An error occurred while creating the password reset.")
    try:
        # because of a unique interagtion between the async engine and the relationship
        # between the user and the password reset, the user objects gets detached from the session
        # so we need to refresh the user object to get the password reset relationship
        # so it is also valid to say user = reset.user (relationship is already loaded cause the reset object is fresh)
        await session.refresh(user)
        await send_reset_password_email(user, reset)
    except Exception as e:
        await del_password_reset(session, reset)
        if getenv("MODE", False) == "DEV":
            raise # propagate the error
        raise HTTPException(status_code=500, detail="An error occurred while sending the password reset email.")
    return {"message": "Password reset email sent."}

@router.get("/is-valid-reset", response_model=dict, responses={200: {"valid": True}, 404: {"valid": False}})
async def is_valid_reset(request: Request, token: str, session: AsyncSession = Depends(GetSession)):
    """
    Check if a password reset token is valid.
    This should be called first by the frontend to check if the token is valid before allowing the user to reset their password.
    """
    reset = await get_password_reset_by_token(session, token)
    if not reset or reset.token_expires < datetime.now():
        return {"valid": False}, 404
    return {"valid": True}

# @router.post("/reset-password", response_model=TokenResponse)
# async def reset_password(request: Request, form: ResetForm, session: AsyncSession = Depends(GetSession), Authorize: AuthJWT = Depends()):
#     """
#     Reset a user's password.
#     """
#     reset = await get_password_reset_by_token(session, form.token)
#     if not reset or reset.token_expires < datetime.now():
#         raise HTTPException(status_code=404, detail="Token not found or has expired.")
#     user = reset.user
#     session.refresh(user)
#     print(user)
#     user.password_hash = hash_password(form.password)
#     if not await update_user(session, user):
#         raise HTTPException(status_code=500, detail="An error occurred while updating the user.")
#     access_token = Authorize.create_access_token(subject=user.user_id, fresh=True)
#     refresh_token = Authorize.create_refresh_token(subject=user.user_id)
#     await del_password_reset(session, reset)
#     return {"access_token": access_token, "refresh_token": refresh_token}

# TODO: for now we will not use the relationship between the user and the password reset
@router.post("/reset-password", response_model=TokenResponse)
async def reset_password(request: Request, form: ResetForm, session: AsyncSession = Depends(GetSession), Authorize: AuthJWT = Depends()):
    """
    Reset a user's password.
    """
    reset = await get_password_reset_by_token(session, form.token)
    if not reset or reset.token_expires < datetime.now():
        raise HTTPException(status_code=404, detail="Token not found or has expired.")
    user = await get_user_by_id(session, reset.user_id)
    # session.refresh(user)
    # print(user)
    user.password_hash = hash_password(form.password)
    if not await update_user(session, user, commit=False):
        raise HTTPException(status_code=500, detail="An error occurred while updating the user.")
    access_token = Authorize.create_access_token(subject=user.user_id, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.user_id)
    await del_password_reset(session, reset)
    return {"access_token": access_token, "refresh_token": refresh_token}


AddRouter(router)  # Add the router to the server
