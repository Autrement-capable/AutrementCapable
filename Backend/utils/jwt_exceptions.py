from copy import deepcopy

def create_response_dict(response={},
                        InvalidHeader=True,
                        JWTDecode=True,
                        CSRF=True,
                        MissingToken=True,
                        RevokedToken=True,
                        AccessToken=True,
                        RefreshToken=True,
                        FreshToken=True):
    """
    Used for creating a response dict to be used in the FastAPI router responses parameter for
    documenting the exceptions that can be thrown by the fastapi_another_jwt_auth library

    Args:
    response (dict, optional): Extra to be added to the response dict. Defaults to {}.
    InvalidHeader (bool, optional): Handle InvalidHeaderError. Defaults to True.
    JWTDecode (bool, optional): Handle JWTDecodeError. Defaults to True.
    CSRF (bool, optional): Handle CSRFError(Bad Actor attack). Defaults to True.
    MissingToken (bool, optional): Handle MissingTokenError. Defaults to True.
    RevokedToken (bool, optional): Handle RevokedTokenError. Defaults to True.
    AccessToken (bool, optional): Handle AccessTokenRequired. Defaults to True.
    RefreshToken (bool, optional): Handle RefreshTokenRequired. Defaults to True.
    FreshToken (bool, optional): Handle FreshTokenRequired. Defaults to True.
    """
    new_response = deepcopy(response)
    if InvalidHeader or CSRF or MissingToken:
        new_response[400] = {"description": "Invalid credentials (CSRF, Invalid Header, Missing Token)"}
    if JWTDecode or RevokedToken:
        new_response[401] = {"description": "Token expired or revoked get a new one"}
    if AccessToken or RefreshToken or FreshToken:
        new_response[403] = {"description": "Access denied (Access token , Fresh token (created by login not refresh), Refresh token required)"}

    new_response[500] = {"description": "Internal server error abnormal behavior"}
    return new_response
