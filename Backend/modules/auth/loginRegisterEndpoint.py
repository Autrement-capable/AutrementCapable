from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from fastapi_another_jwt_auth import AuthJWT
from database.postgress.actions.user import create_user, get_user_by_email, login_user
from database.postgress.models.user import User
from modules.session_management.password import hash_password, verify_password
from config.server import AddRouter, server
import re

router = APIRouter(prefix="/auth", tags=["Authentication"])

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' # should be replaced with a library

class LoginForm(BaseModel):
    username: str
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
    user = login_user(Session, form.username, form.password)
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = Authorize.create_access_token(subject=user["username"])
    refresh_token = Authorize.create_refresh_token(subject=user["username"])
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/register", response_model=LoginResponse)
def register(form: RegisterForm, Authorize: AuthJWT = Depends(), Session = Depends(server.get_Psession)):
    if not re.fullmatch(email_regex, form.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format")

    user = create_user(Session, form.username, form.email, form.password, first_name=form.first_name, last_name=form.last_name, phone_number=form.phone_number, address=form.address, refresh=True)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    access_token = Authorize.create_access_token(subject=user["username"])
    refresh_token = Authorize.create_refresh_token(subject=user["username"])
    return {"access_token": access_token, "refresh_token": refresh_token}

AddRouter(router) # Add the router to the server