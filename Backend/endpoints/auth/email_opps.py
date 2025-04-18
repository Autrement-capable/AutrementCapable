from fastapi import APIRouter, Depends, Request, HTTPException, Response, Cookie, status, Query
from fastapi.responses import RedirectResponse
from server.jwt_config.token_creation import create_token, decode_token, set_refresh_cookie, clear_refresh_cookie
from pydantic import BaseModel, Field, EmailStr
from utils.password import hash_password
from utils.jwt_exceptions import create_response_dict
from database.postgress.config import getSession as GetSession
from database.postgress.actions.user import get_user_by_email
from database.postgress.actions.revoked_jwt_tokens import revoke_token, get_revoked_token_by_jti
from database.postgress.actions.acc_recovery import get_acc_recovery_by_token, create_acc_recovery, del_acc_recovery
from database.postgress.actions.user import verify_user, update_ver_details
from mail.actions.reset_password import send_reset_password_email

from server.server import AddRouter
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from os import getenv

class ResetRequestForm(BaseModel):
    email: EmailStr

class ResendRequestForm(BaseModel):
    email: EmailStr = Field(..., title="The email of the user.", description="The email of the user.")

router = APIRouter(prefix="/recovery", tags=["Account Recovery"])

@router.post("/request-password-reset", responses={200: {"message": "Password reset email sent."}})
async def try_reset_password(request: Request, form: ResetRequestForm, session: AsyncSession = Depends(GetSession)):
    """
    Initiate a password reset for a user.
    """
    user = await get_user_by_email(session, form.email, lazy=False)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    reset = await create_acc_recovery(session, user)
    if not reset:
        raise HTTPException(status_code=500, detail="An error occurred while creating the password reset.")
    try:
        await send_reset_password_email(user, reset)
    except Exception as e:
        await del_acc_recovery(session, reset)
        if getenv("MODE", False) == "DEV":
            raise # propagate the error
        raise HTTPException(status_code=500, detail="An error occurred while sending the password reset email.")
    return {"message": "Password reset email sent."}

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

AddRouter(router)  # Add the router to the server

router = APIRouter(prefix="/auth", tags=["Email Verification"])

class VerificationResponse(BaseModel):
    message: str = Field(..., description="Verification message")
    access_token: str = Field(None, description="JWT access token if auto-login is enabled")

# Verification endpoint for email link click
@router.get("/verify", response_model=VerificationResponse)
async def verify_email(
    code: str = Query(..., description="Verification code sent to user's email"),
    auto_login: bool = Query(False, description="Whether to automatically log in the user after verification"),
    redirect_url: str = Query(None, description="URL to redirect to after verification"),
    session: AsyncSession = Depends(GetSession),
    response: Response = None
):
    """
    Verify a user's email address using the verification code sent to their email.

    - If auto_login is True, returns access token and sets refresh token cookie
    - If redirect_url is provided, redirects to that URL after verification
    """
    # Verify the user using the verification code
    user = await verify_user(session, code)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )

    result = {"message": "Email verified successfully"}

    # Auto-login if requested
    if auto_login:
        access_token = create_token(user.id, user.role_id, refresh=False, fresh=True)
        refresh_token = create_token(user.id, user.role_id, refresh=True, fresh=True)

        # Set refresh token in HTTP-only cookie
        if response:
            set_refresh_cookie(response, refresh_token)

        result["access_token"] = access_token

    # Redirect if URL provided
    if redirect_url:
        # Build redirect URL with query parameters
        query_params = f"verified=true"
        if auto_login and "access_token" in result:
            query_params += f"&access_token={result['access_token']}"

        redirect_to = f"{redirect_url}?{query_params}"
        return RedirectResponse(url=redirect_to)

    return result

# Alternative endpoint for frontend verification (AJAX calls)
@router.post("/verify-code", response_model=VerificationResponse)
async def verify_email_code(
    code: str = Query(..., description="Verification code sent to user's email"),
    auto_login: bool = Query(True, description="Whether to automatically log in the user after verification"),
    session: AsyncSession = Depends(GetSession),
    response: Response = None
):
    """
    Verify a user's email address using the verification code.
    This endpoint is meant for frontend applications to verify email through AJAX calls.

    If auto_login is True (default), returns access token and sets refresh token cookie.
    """
    # Verify the user using the verification code
    user = await verify_user(session, code)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )

    result = {"message": "Email verified successfully"}

    # Auto-login if requested
    if auto_login:
        access_token = create_token(user.id, user.role_id, refresh=False, fresh=True)
        refresh_token = create_token(user.id, user.role_id, refresh=True, fresh=True)

        # Set refresh token in HTTP-only cookie
        if response:
            set_refresh_cookie(response, refresh_token)

        result["access_token"] = access_token

    return result

AddRouter(router)
