from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from server.jwt_config.token_creation import create_token, decode_token, JWTBearer
from pydantic import BaseModel, Field, EmailStr
from utils.password import hash_password
from utils.jwt_exceptions import create_response_dict
from database.postgress.config import getSession as GetSession
from database.postgress.actions.user import get_user_by_email
from database.postgress.actions.revoked_jwt_tokens import revoke_token, get_revoked_token_by_jti
from database.postgress.actions.password_reset import get_password_reset_by_token, create_password_reset, del_password_reset
from database.postgress.actions.user import verify_user, update_ver_details
from mail.actions.reset_password import send_reset_password_email

from server.server import AddRouter
from sqlalchemy.ext.asyncio import AsyncSession
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

class ResendRequestForm(BaseModel):
    email: EmailStr = Field(..., title="The email of the user.", description="The email of the user.")

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/verify", response_model=TokenResponse)
async def verify_users(request: Request, code: str, session: AsyncSession = Depends(GetSession)):
    """
    Verify a user using their verification code.
    """
    user = await verify_user(session, code, fresh=True)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or the token has expired.")
    access_token = create_token(user.id, user.role_id, is_refresh=False, fresh=True)
    refresh_token = create_token(user.id, user.role_id, is_refresh=True, fresh=True)
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

@router.post("/reset-password", response_model=TokenResponse)
async def reset_password(request: Request, form: ResetForm, session: AsyncSession = Depends(GetSession)):
    """
    Reset a user's password.
    """
    reset = await get_password_reset_by_token(session, form.token)
    if not reset or reset.token_expires < datetime.now():
        raise HTTPException(status_code=404, detail="Token not found or has expired.")
    user = reset.user
    user.password_hash = hash_password(form.password)

    try:
        user.password_resets = [] # should work cause of cascade set to orphab-delete
        session.add(user)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the user's password.")

    access_token = create_token(user.id, user.role_id, is_refresh=False, fresh=True)
    refresh_token = create_token(user.id, user.role_id, is_refresh=True, fresh=True)
    await del_password_reset(session, reset)
    return {"access_token": access_token, "refresh_token": refresh_token}


AddRouter(router)  # Add the router to the server

@router.post("/resend-verification-email", response_model=dict,
responses={200: {"message": "Verification email sent."}})
async def resend_verification_email(request: Request, form: ResendRequestForm, session: AsyncSession = Depends(GetSession)):
    """
    Resend the verification email to a user.
    """
    user = await get_user_by_email(session, form.email, load_type="eager")
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.verified:
        return {"message": "User is already verified."}
    try:
        if not await send_verification_email(user, user.verification_details):
            raise HTTPException(status_code=500, detail="An error occurred while sending the verification email.")
    except Exception as e:
        if getenv("MODE", False) == "DEV":
            raise # propagate the error
    user.verification_details
    return {"message": "Verification email sent."}
