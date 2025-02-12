from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from fastapi_another_jwt_auth import AuthJWT
from database.postgress.actions.user import create_user, login_user, get_available_usernames, del_uvf_user
from mail.actions.verify_account import send_verification_email
from server.server import AddRouter
from database.postgress.config import getSession as GetSession
from sqlalchemy.ext.asyncio import AsyncSession
from database.postgress.setup import postgress

from os import getenv

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginForm(BaseModel):
    username_or_email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

class RegisterForm(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    address: str
    username: str
    email: EmailStr
    password: str

@router.post("/login", response_model=LoginResponse)
async def login(form: LoginForm, Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(GetSession)):
    """
    Login a user and return an access token and a refresh token
    """

    user = await login_user(session, form.password, form.username_or_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    access_token = Authorize.create_access_token(subject=user.user_id, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.user_id)
    return {"access_token": access_token, "refresh_token": refresh_token}

# @router.post("/register", response_model=LoginResponse)
# async def register(form: RegisterForm, Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(GetSession)):
#     """
#     NOT FINALLY IMPLEMENTED, currently skips email verification
#     Register a new user and return an access token and a refresh token
#     """
#     user = await create_user(session, form.username, form.email, form.password, first_name=form.first_name, last_name=form.last_name, phone_number=form.phone_number, address=form.address, fresh=True)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
#     access_token = Authorize.create_access_token(subject=user.user_id, fresh=True)
#     refresh_token = Authorize.create_refresh_token(subject=user.user_id)
#     return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/register")
async def register(form: RegisterForm, Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(GetSession)):
    """
    Register a new user and return an access token and a refresh token
    """
    tmp_user, details = await create_user(session, form.username,form.email,
                                            form.password, first_name=form.first_name,
                                            last_name=form.last_name, phone_number=form.phone_number,
                                            address=form.address, fresh=True)
    if not tmp_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    #Note we might want to handle failed email sending and delete the tmp user form db
    try:
        if not await send_verification_email(tmp_user, details):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send verification email")
    except Exception as e: # if the email sending fails, delete the user
        await del_uvf_user(session, tmp_user)
        if getenv("MODE", False) == "DEV":
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
