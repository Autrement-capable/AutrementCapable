from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from fastapi_another_jwt_auth import AuthJWT
from database.postgress.actions.user import create_user, get_user_by_email, login_user, get_user_by_username
from modules.session_management.password import hash_password, verify_password
from config.server import AddRouter, server
import re

router = APIRouter(prefix="/auth", tags=["Authentication"])

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' # should be replaced with a library

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
def login(form: LoginForm, Authorize: AuthJWT = Depends(), Session = Depends(server.get_Psession)):
    """
    Login a user and return an access token and a refresh token
    """
    user = login_user(Session, form.password, form.username_or_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = Authorize.create_access_token(subject=user.user_id, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.user_id)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.get("/check_username")
def check_username(username: str, Session = Depends(server.get_Psession)):
    """ Check if a username is already taken

    Use this when registering a new user to check if the username is already taken
    /auth/check_username?username=example
    """
    user = get_user_by_username(Session, username)
    if user:
        return {"exists": True}
    return {"exists": False}

@router.post("/register", response_model=LoginResponse)
def register(form: RegisterForm, Authorize: AuthJWT = Depends(), Session = Depends(server.get_Psession)):
    """
    NOT FINALLY IMPLEMENTED, currently skips email verification
    Register a new user and return an access token and a refresh
    """
    if not re.fullmatch(email_regex, form.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format")

    user = create_user(Session, form.username, form.email, form.password, first_name=form.first_name, last_name=form.last_name, phone_number=form.phone_number, address=form.address, fresh=True)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    access_token = Authorize.create_access_token(subject=user.user_id, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.user_id)
    return {"access_token": access_token, "refresh_token": refresh_token}

AddRouter(router) # Add the router to the server