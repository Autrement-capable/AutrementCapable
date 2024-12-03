from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi_another_jwt_auth import AuthJWT
from pydantic import BaseModel, Field
from utils.jwt_exceptions import create_response_dict
from database.postgress.config import GetSession
from database.postgress.actions.user import get_user_by_email
from database.postgress.actions.revoked_jwt_tokens import revoke_token, get_revoked_token_by_jti
from database.postgress.actions.password_reset import get_password_reset_by_token, create_password_reset, del_password_reset
from mail.actions.reset_password import send_reset_password_email

from server.server import AddRouter
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/verify")
async def verify_users(request: Request, code: str, Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(GetSession)):
    """
    Verify a user using their verification code.
    """
    user = await verify_user(session, code)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or the token has expired.")
    access_token = Authorize.create_access_token(subject=user.user_id, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.user_id)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/start-reset-password")
async def try_reset_password(request: Request, email: str, session: AsyncSession = Depends(GetSession)):
    """
    Initiate a password reset for a user.
    """
    user = await get_user_by_email(session, email)
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

@router.get("/is-valid-reset")
async def is_valid_reset(request: Request, token: str, session: AsyncSession = Depends(GetSession)):
    """
    Check if a password reset token is valid.
    """
    reset = await get_password_reset_by_token(session, token)
    if not reset or reset.token_expires < datetime.now():
        return {"valid": False}
    return {"valid": True}

# TODO add the body to the request
@router.post("/reset-password")
async def reset_password(request: Request, token: str, password: str, session: AsyncSession = Depends(GetSession)):
    """
    Reset a user's password.
    """
    reset = await get_password_reset_by_token(session, token)
    if not reset:
        raise HTTPException(status_code=404, detail="Token not found.")
    if reset.token_expires < datetime.now():
        await del_password_reset(session, reset)
        raise HTTPException(status_code=404, detail="Token expired.")
    user = reset.user
    user.password = password
    await del_password_reset(session, reset)
    return {"message": "Password reset."}

AddRouter(router)  # Add the router to the server