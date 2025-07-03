import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from ...core.security.token_creation import create_token, decode_token, set_refresh_cookie, clear_refresh_cookie
from ...core.security.decorators import secured_endpoint, SecurityRequirement
from ...core.errors import create_response_dict
from ...db.postgress.engine import getSession
from ...db.postgress.repositories.revoked_jwt_tokens import revoke_token
from ...core.application import AddRouter
from ...utils import patterns

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Response Models
class LogoutResponse(BaseModel):
    msg: str = Field(..., description="The message")

class RefreshResponse(BaseModel):
    access_token: str = Field(..., description="The new access token")

class MeResponse(BaseModel):
    user_id: int = Field(..., description="The ID of the authenticated user")
    role: str = Field(..., description="The role of the authenticated user")
    msg: str = Field(..., description="A message indicating successful authentication")

@router.post("/refresh",
             response_model=RefreshResponse,
             responses=create_response_dict(AccessToken=False))
@secured_endpoint(security_type=SecurityRequirement.REFRESH_COOKIE)
async def refresh(
    response: Response,
    refresh_jwt: dict,
):
    """
    Refresh the access token. Requires a valid refresh token stored in an HTTP-only cookie.

    The refresh token comes from an HTTP-only cookie, and a new access token is returned in the response body.
    """
    try:
        # Decode the refresh token from the cookie
        jwt_payload = refresh_jwt

        # Create a new access token
        access_token = create_token(jwt_payload["sub"], jwt_payload["role"], refresh=False)

        # Generate a new refresh token for security reasons
        new_refresh_token = create_token(jwt_payload["sub"], jwt_payload["role"], refresh=True)

        # Set the new refresh token as a cookie
        set_refresh_cookie(response, new_refresh_token)

        return {"access_token": access_token}
    except Exception as e:
        # If the token validation fails, clear the cookie
        clear_refresh_cookie(response)
        raise

@router.post("/logout",
             responses=create_response_dict(),
             response_model=LogoutResponse)
@secured_endpoint(security_type=SecurityRequirement.BOTH_TOKENS)
async def logout(
    response: Response,
    jwt: dict,
    refresh_jwt: dict,
    session: AsyncSession = Depends(getSession)
):
    """
    Revoke access and refresh tokens to log out the user.

    The access token is provided in the Authorization header.
    The refresh token is automatically retrieved from the HTTP-only cookie.
    Both tokens are revoked on the server and the refresh cookie is cleared.
    """

    jti_access = jwt["jti"]
    expires_access = datetime.utcfromtimestamp(jwt["exp"])

    # Revoke the access token
    is_ok = await revoke_token(session, jti_access, expires_access, "access", commit=False)
    if not is_ok:
        raise HTTPException(status_code=401, detail="Invalid access token (Already Revoked)")

    # Clear the refresh cookie
    clear_refresh_cookie(response)

    # Revoke the refresh token if it exists

    if refresh_jwt:
        try:
            jti_refresh = refresh_jwt.get("jti")
            expires_refresh = datetime.utcfromtimestamp(refresh_jwt["exp"])
            await revoke_token(session, jti_refresh, expires_refresh, "refresh")
        except Exception:
            # If token is invalid, we just continue as we already cleared the cookie
            pass
    else:
        session.rollback()
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return {"msg": "Successfully logged out"}
# endpoint to check if user is authenticated
@router.get("/status", responses=create_response_dict(AccessToken=False), response_model=MeResponse)
@secured_endpoint(security_type=SecurityRequirement.ACCESS_TOKEN)
async def is_authenticated(
    jwt: dict,
    session: AsyncSession = Depends(getSession)
):
    """
    Check if the user is authenticated.

    This endpoint verifies the access token and returns a success message if valid.
    """
    user_id = jwt.get("sub")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid access token")

    # Optionally, you can check if the user exists in the database
    # user = await session.get("User", user_id)
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")

    return {"msg": "User is authenticated", "user_id": user_id, "role" : jwt.get("role")}

AddRouter(router)