from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth.exceptions import (
    AuthJWTException, InvalidHeaderError, JWTDecodeError, CSRFError,
    MissingTokenError, RevokedTokenError, AccessTokenRequired, RefreshTokenRequired,
    FreshTokenRequired
)

def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    if isinstance(exc, InvalidHeaderError):
        print("Invalid Header error msg" + str(exc))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid credentials"}
        )
    elif isinstance(exc, JWTDecodeError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token expired"}
        )
    elif isinstance(exc, CSRFError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "No"}
        )
    elif isinstance(exc, MissingTokenError):
        print("Missing Token error msg" + str(exc))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid credentials"}
        )
    elif isinstance(exc, RevokedTokenError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token Revoked"}
        )
    elif isinstance(exc, AccessTokenRequired):
        return JSONResponse(
            status_code=status.HTTP_403_UNAUTHORIZED,
            content={"detail": "Access token required"}
        )
    elif isinstance(exc, RefreshTokenRequired):
        return JSONResponse(
            status_code=status.HTTP_403_UNAUTHORIZED,
            content={"detail": "Refresh token required"}
        )
    elif isinstance(exc, FreshTokenRequired):
        return JSONResponse(
            status_code=status.HTTP_403_UNAUTHORIZED,
            content={"detail": "Fresh token required"}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)}
        )
