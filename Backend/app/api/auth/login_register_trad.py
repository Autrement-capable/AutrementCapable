import os

from fastapi import APIRouter, HTTPException, Depends, status, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.application import AddRouter
from ...core.security.token_creation import create_token, set_refresh_cookie
from ...db.postgress.engine import getSession as GetSession
from ...db.postgress.repositories.user import create_user, login_user, get_available_usernames, del_uvf_user, DuplicateUserError, RoleNotFoundError, UserCreationError
from ...services.mail.repositories.verify_account import send_verification_email

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginForm(BaseModel):
    username_or_email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    message: str = "Login successful"

class RegisterForm(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    address: str
    username: str
    email: EmailStr
    password: str

@router.post("/login", response_model=LoginResponse)
async def login(form: LoginForm, response: Response, session: AsyncSession = Depends(GetSession)):
    """
    Login a user and return an access token.
    The refresh token is automatically stored in an HTTP-only cookie.
    """
    user = await login_user(session, form.password, form.username_or_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if user.verification_details is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account not verified")

    # Create tokens
    access_token = create_token(user.id, user.role_id, refresh=False, fresh=True)
    refresh_token = create_token(user.id, user.role_id, refresh=True, fresh=True)

    # Set refresh token in HTTP-only cookie
    set_refresh_cookie(response, refresh_token)

    return {"access_token": access_token, "message": "Login successful"}

@router.post("/register")
async def register(form: RegisterForm, session: AsyncSession = Depends(GetSession)):
    """
    Register a new user and send verification email
    """
    test,_ = await get_available_usernames(session, form.username, 0)
    if not test:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username already taken")

    try:
        tmp_user, details = await create_user(session, form.username,form.email,
                                                form.password, first_name=form.first_name,
                                                last_name=form.last_name, phone_number=form.phone_number,
                                                address=form.address, fresh=True)
    except DuplicateUserError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except RoleNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except UserCreationError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    try:
        if not await send_verification_email(tmp_user, details):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send verification email")
    except Exception as e: # if the email sending fails, delete the user
        await del_uvf_user(session, tmp_user)
        if os.getenv("MODE", False) == "DEV":
            raise # propagate the error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send verification email")
    return {"message": "Verification email sent"}

@router.get("/check_username")
async def check_username(username: str, session:AsyncSession = Depends(GetSession)):
    """ Check if a username is already taken

    Use this when registering a new user to check if the username is already taken,
    before attempting to create the user.
    this also gives suggestions for similar usernames.
    /auth/check_username?username=example
    """
    is_available, usernames = await get_available_usernames(session, username)

    return {"is_available": is_available, "usernames": usernames}

AddRouter(router)
