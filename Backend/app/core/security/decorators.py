from functools import wraps
from enum import Enum, auto
from typing import List, Optional, Callable, Dict, Any, TypeVar, Awaitable

from fastapi import Request, Response, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .token_creation import decode_token
from ...db.postgress.engine import getSession

class SecurityRequirement(Enum):
    ACCESS_TOKEN = auto()      # Bearer token in Authorization header
    REFRESH_COOKIE = auto()    # Refresh token in HTTP-only cookie
    BOTH_TOKENS = auto()       # Requires both access token and refresh cookie

def extract_token_from_header(request: Request) -> str:
    """Extract JWT token from Authorization header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or missing Authorization header."
        )
    return auth_header.split(" ")[1]

# Define a dependency for getting JWT data
async def get_jwt_data(
    request: Request,
    security_type: SecurityRequirement = SecurityRequirement.ACCESS_TOKEN,
    session: AsyncSession = Depends(getSession)
):
    """Get JWT data based on security requirements"""
    # Handle different token requirements
    access_payload = None
    refresh_payload = None

    # Get access token if needed
    if security_type in [SecurityRequirement.ACCESS_TOKEN, SecurityRequirement.BOTH_TOKENS]:
        try:
            token = extract_token_from_header(request)
            access_payload = await decode_token(session, token, is_refresh=False)
        except HTTPException as e:
            if security_type == SecurityRequirement.ACCESS_TOKEN:
                raise  # Re-raise if access token is required

    # Get refresh token if needed
    if security_type in [SecurityRequirement.REFRESH_COOKIE, SecurityRequirement.BOTH_TOKENS]:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token missing"
            )
        try:
            refresh_payload = await decode_token(session, refresh_token, is_refresh=True)
        except HTTPException:
            raise  # Always re-raise for refresh token

    # Make sure we have all required tokens
    if security_type == SecurityRequirement.BOTH_TOKENS and (not access_payload or not refresh_payload):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Both access and refresh tokens are required"
        )

    # Return appropriate payload(s)
    if security_type == SecurityRequirement.ACCESS_TOKEN:
        return {"jwt": access_payload}
    elif security_type == SecurityRequirement.REFRESH_COOKIE:
        return {"jwt": refresh_payload}
    else:  # BOTH_TOKENS
        return {"jwt": access_payload, "refresh_jwt": refresh_payload}

def secured_endpoint(security_type: SecurityRequirement = SecurityRequirement.ACCESS_TOKEN, description: Optional[str] = None):
    """
    Decorator that adds JWT authentication to an endpoint.

    Instead of injecting parameters directly, it uses a dependency approach
    that's compatible with FastAPI's response model generation.

    Args:
        security_type: Type of security requirements
        description: Optional custom description for the security requirement

    Returns:
        A decorator that wraps the endpoint function.

        decorrator sets the following params of the endpoint function based on SecurityRequirement:
        - jwt: JWT payload from the access token
        - refresh_jwt: JWT payload from the refresh token (if required)
    """
    def decorator(func: Callable):
        # Store security requirements on the function for OpenAPI docs
        func.requires_auth = True
        func.security_type = security_type
        func.security_description = description

        # Explicitly set response_model=None to prevent FastAPI from trying
        # to generate a response model from the function signature
        if hasattr(func, "__annotations__") and "return" in func.__annotations__:
            # Function has a return type annotation, we should keep it
            pass
        else:
            # No return type annotation, mark explicitly to not generate response model
            func.response_model = None

        # Create dependency that FastAPI will properly handle
        async def jwt_dependency(request: Request):
            jwt_data = await get_jwt_data(request, security_type)
            return jwt_data

        # Store the dependency on the function
        if not hasattr(func, "dependencies"):
            func.dependencies = []
        func.dependencies.append(Depends(jwt_dependency))

        # Use normal FastAPI dependency injection - this is cleaner and works with OpenAPI
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract JWT data from kwargs if injected by FastAPI
            jwt_data = {}
            if "jwt" in kwargs:
                jwt_data["jwt"] = kwargs["jwt"]
            if "refresh_jwt" in kwargs:
                jwt_data["refresh_jwt"] = kwargs["refresh_jwt"]

            # Call the function
            return await func(*args, **kwargs)

        return wrapper
    return decorator