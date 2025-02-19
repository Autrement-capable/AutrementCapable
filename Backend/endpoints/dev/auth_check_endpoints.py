## Debugging endpoints to check if the access token and refresh token are valid
## FIY: SHOULD NOT BE USED IN PRODUCTION
from fastapi import APIRouter, Depends, HTTPException
from fastapi_another_jwt_auth import AuthJWT
from database.postgress.config import getSession as GetSession
from sqlalchemy.ext.asyncio import AsyncSession
from server.server import AddRouter

auth_test = APIRouter(prefix="/dev", tags=["Development"])

@auth_test.get("/test_access_token", tags=["Development", "Auth", "Auth_refresh"])
async def test_access_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    decoded_token = Authorize.get_raw_jwt()
    return {
        "message": "Access token is valid",
        "header": decoded_token.get("header"),
        "payload": decoded_token
    }

@auth_test.get("/test_refresh_token", tags=["Development", "Auth"])
async def test_refresh_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    decoded_token = Authorize.get_raw_jwt()
    return {
        "message": "Refresh token is valid",
        "header": decoded_token.get("header"),
        "payload": decoded_token
    }

@auth_test.get("/test_access_token_with_session", tags=["Development", "Auth"])
async def test_access_token_with_session(
    Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(GetSession)
):
    Authorize.jwt_required()
    decoded_token = Authorize.get_raw_jwt()
    return {
        "message": "Access token is valid",
        "header": decoded_token.get("header"),
        "payload": decoded_token
    }

@auth_test.get("/test_refresh_token_with_session", tags=["Development", "Auth", "Auth_refresh"])
async def test_refresh_token_with_session(
    Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(GetSession)
):
    Authorize.jwt_refresh_token_required()
    decoded_token = Authorize.get_raw_jwt()
    return {
        "message": "Refresh token is valid",
        "header": decoded_token.get("header"),
        "payload": decoded_token
    }

AddRouter(auth_test)
