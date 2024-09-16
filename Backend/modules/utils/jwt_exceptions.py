from fastapi import HTTPException, status
from fastapi_another_jwt_auth.exceptions import (
    MissingTokenError, InvalidHeaderError, JWTDecodeError, CSRFError,
    RevokedTokenError, AccessTokenRequired, RefreshTokenRequired,
    FreshTokenRequired
)
from copy import deepcopy

def handle_jwt_exceptions(
    lambda_func,
    InvalidHeader=True,
    JWTDecode=True,
    CSRF=True,
    MissingToken=True,
    RevokedToken=True,
    AccessToken=True,
    RefreshToken=True,
    FreshToken=True
):
    try:
        return lambda_func()
    except InvalidHeaderError as e:
        if InvalidHeader:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials") from e
        else:
            raise
    except JWTDecodeError as e:
        if JWTDecode:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired") from e
        else:
            raise
    except CSRFError as e:
        if CSRF:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No") from e
        else:
            raise
    except MissingTokenError as e:
        if MissingToken:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials") from e
        else:
            raise
    except RevokedTokenError as e:
        if RevokedToken:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Revoked") from e
        else:
            raise
    except AccessTokenRequired as e:
        if AccessToken:
            raise HTTPException(status_code=status.HTTP_403_UNAUTHORIZED, detail="Access token required") from e
        else:
            raise
    except RefreshTokenRequired as e:
        if RefreshToken:
            raise HTTPException(status_code=status.HTTP_403_UNAUTHORIZED, detail="Refresh token required") from e
        else:
            raise
    except FreshTokenRequired as e:
        if FreshToken:
            raise HTTPException(status_code=status.HTTP_403_UNAUTHORIZED, detail="Fresh token required") from e
        else:
            raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

# create a function takes a responce dict(empty by default) and the bools of the exceptions to handle and returns a dict with the response and the status code

def create_response_dict(response={},
                        InvalidHeader=True,
                        JWTDecode=True,
                        CSRF=True,
                        MissingToken=True,
                        RevokedToken=True,
                        AccessToken=True,
                        RefreshToken=True,
                        FreshToken=True):
    new_response = deepcopy(response)
    if InvalidHeader or CSRF or MissingToken:
        new_response[400] = {"description": "Invalid credentials (CSRF, Invalid Header, Missing Token)"}
    if JWTDecode or RevokedToken:
        new_response[401] = {"description": "Token expired or revoked get a new one"}
    if AccessToken or RefreshToken or FreshToken:
        new_response[403] = {"description": "Access denied (Access token , Fresh token (created by login not refresh), Refresh token required)"}

    new_response[500] = {"description": "Internal server error abnormal behavior"}
    return new_response