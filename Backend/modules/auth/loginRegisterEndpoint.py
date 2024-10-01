from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from fastapi_another_jwt_auth import AuthJWT
# from modules.database.DB import GetUser, AddUser
from modules.session_management.password import hash_password, verify_password
from config.server import AddRouter
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
    name: str
    username: str
    email: EmailStr
    password: str

@router.post("/login", response_model=LoginResponse)
def login(form: LoginForm, Authorize: AuthJWT = Depends()):
    # user = GetUser(form.username)
    # if not user or not verify_password(form.password, user["password"]):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = Authorize.create_access_token(subject=user["username"])
    refresh_token = Authorize.create_refresh_token(subject=user["username"])
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/register", response_model=LoginResponse)
def register(form: RegisterForm, Authorize: AuthJWT = Depends()):
    pass
    # if not re.fullmatch(email_regex, form.email):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format")

    # user = AddUser(form.name, form.username, form.email, hash_password(form.password))
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")

    # access_token = Authorize.create_access_token(subject=user["username"])
    # refresh_token = Authorize.create_refresh_token(subject=user["username"])
    # return {"access_token": access_token, "refresh_token": refresh_token}

AddRouter(router) # Add the router to the server