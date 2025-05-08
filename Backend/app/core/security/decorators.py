## core/security/decorators.py
from functools import wraps
from enum import Enum, auto
from typing import List, Optional, Callable, Dict, Any, TypeVar, Awaitable
import inspect
from inspect import Parameter, Signature

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

    # Return payload directly for simpler access
    if security_type == SecurityRequirement.ACCESS_TOKEN:
        return access_payload  # Return payload directly
    elif security_type == SecurityRequirement.REFRESH_COOKIE:
        return refresh_payload  # Return payload directly
    else:  # BOTH_TOKENS
        # For both tokens, we need to return both payloads
        # but we'll handle this differently in the decorator
        return {"access": access_payload, "refresh": refresh_payload}

def secured_endpoint(security_type: SecurityRequirement = SecurityRequirement.ACCESS_TOKEN, description: Optional[str] = None):
    """
    Decorator that adds JWT authentication to an endpoint.

    This decorator injects JWT data directly into the function parameters:
    - For ACCESS_TOKEN: jwt parameter contains the access token payload
    - For REFRESH_COOKIE: jwt parameter contains the refresh token payload
    - For BOTH_TOKENS: jwt parameter contains access payload, refresh_jwt contains refresh payload

    Args:
        security_type: Type of security requirements
        description: Optional custom description for the security requirement

    Returns:
        A decorator that wraps the endpoint function and properly injects JWT data.
    """
    def decorator(func: Callable):
        # Store security requirements on the function for OpenAPI docs
        func.requires_auth = True
        func.security_type = security_type
        func.security_description = description

        # Get the original function signature
        sig = inspect.signature(func)

        # Create a helper function for dependency injection
        async def jwt_dependency(
            request: Request,
            session: AsyncSession = Depends(getSession)
        ) -> Dict[str, Any]:
            return await get_jwt_data(request, security_type, session)

        # Create a new parameter list with JWT dependency properly injected
        new_params = []

        for name, param in sig.parameters.items():
            if name == "jwt":
                # Replace jwt parameter with our dependency
                new_param = Parameter(
                    name="jwt",
                    kind=param.kind,
                    annotation=dict,
                    default=Depends(jwt_dependency)
                )
                new_params.append(new_param)
            elif name == "refresh_jwt" and security_type == SecurityRequirement.BOTH_TOKENS:
                # For refresh_jwt, we'll inject it in the wrapper
                continue
            else:
                new_params.append(param)

        # Create a new signature with the modified parameters
        new_sig = sig.replace(parameters=new_params)

        # Create a wrapper function
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Handle BOTH_TOKENS case
            if security_type == SecurityRequirement.BOTH_TOKENS and 'jwt' in kwargs:
                combined_data = kwargs['jwt']
                # Split the combined data into separate parameters
                kwargs['jwt'] = combined_data['access']
                if 'refresh_jwt' in sig.parameters:
                    kwargs['refresh_jwt'] = combined_data['refresh']

            return await func(*args, **kwargs)

        # Apply the new signature to our wrapper
        wrapper.__signature__ = new_sig

        return wrapper
    return decorator