## Debugging endpoints to check if the access token and refresh token are valid
## FIY: SHOULD NOT BE USED IN PRODUCTION

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.application import AddRouter
from ...core.security.decorators import secured_endpoint, SecurityRequirement
from ...db.postgress.engine import getSession as GetSession


auth_test = APIRouter(prefix="/dev", tags=["Development"])

@auth_test.get("/test_access_token")
@secured_endpoint()
async def test_access_token_with_session(
    jwt: dict,
    session: AsyncSession = Depends(GetSession)
):
    return {"msg": "Access Token is valid!", "payload": jwt}

@auth_test.get("/test_refresh_token")
@secured_endpoint(security_type=SecurityRequirement.REFRESH_COOKIE)
async def test_refresh_token_with_session(
    refresh_jwt: dict,
    session: AsyncSession = Depends(GetSession)
):
    return {"msg": "Refresh Token is valid!", "payload": refresh_jwt}

AddRouter(auth_test)
