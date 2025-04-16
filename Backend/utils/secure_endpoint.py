from functools import wraps
from enum import Enum, auto
from typing import List, Optional

class SecurityRequirement(Enum):
    ACCESS_TOKEN = auto()      # Bearer token in Authorization header
    REFRESH_COOKIE = auto()    # Refresh token in HTTP-only cookie
    BOTH_TOKENS = auto()       # Requires both access token and refresh cookie

def secured_endpoint(security_type: SecurityRequirement = SecurityRequirement.ACCESS_TOKEN, description: Optional[str] = None):
    """
    Decorator to mark an endpoint as requiring specific authentication in the OpenAPI docs.

    Args:
        security_type: Type of security requirements (access token, refresh cookie, or both)
        description: Optional custom description for the security requirement
    """
    def decorator(func):
        # Store security requirements on the function
        func.requires_auth = True
        func.security_type = security_type
        func.security_description = description

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        # Transfer attributes to the wrapper
        wrapper.requires_auth = True
        wrapper.security_type = security_type
        wrapper.security_description = description

        return wrapper
    return decorator