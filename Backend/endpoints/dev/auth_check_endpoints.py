## Debugging endpoints to check if the access token and refresh token are valid
## FIY: SHOULD NOT BE USED IN PRODUCTION
from fastapi import APIRouter, Depends, HTTPException
from server.jwt_config.token_creation import JWTBearer
from database.postgress.config import getSession as GetSession
from sqlalchemy.ext.asyncio import AsyncSession
from server.server import AddRouter

auth_test = APIRouter(prefix="/dev", tags=["Development"])

@auth_test.get("/test_access_token", tags=["Development", "Auth"])
async def test_access_token_with_session(
    session: AsyncSession = Depends(GetSession), token: dict = Depends(JWTBearer())
):
    return {"msg": "Access Token is valid!", "payload": token["payload"]}

@auth_test.get("/test_refresh_token", tags=["Development", "Auth", "Auth_refresh"])
async def test_refresh_token_with_session(
    session: AsyncSession = Depends(GetSession), token: dict = Depends(JWTBearer(is_refresh=True))
):
    return {"msg": "Refresh Token is valid!", "payload": token["payload"]}

AddRouter(auth_test)
