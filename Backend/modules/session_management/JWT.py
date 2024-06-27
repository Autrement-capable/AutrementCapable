import datetime
from jose import jwt
from os import getenv

def createToken(email: str, Long:bool=False) -> str:
    """Create a JWS token for a given username.

    Args:
        username (str): The username for which the token is created.
        Long (bool): Whether to create a token with extended expiration (30 days). Defaults to False(30 minutes)

    Returns:
        str: The generated JWS token.
    """

    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + (datetime.timedelta(minutes=30) if not Long else datetime.timedelta(days=30))
    }
    secret = getenv('SERVER_SECRET_KEY_PRIVATE')
    algorithm = 'ES256'
    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token

def decodeToken(token: str) -> dict:
    """Decode a JWS token and return the payload.

    Args:
        token (str): The JWS token to decode.

    Returns:
        dict: The decoded payload.
    """
    secret =  getenv('SERVER_SECRET_KEY_PUBLIC')
    return jwt.decode(token, secret, algorithms=['ES256'])

def UnpackToken(token, unpack=False, TokenOverhead="Bearer "):
    """Unpack a JWS token and return the payload.

    Args:
        token (str): The token to unpack.
        unpack (bool): Whether to remove the Bearer overhead. Defaults to False.
        TokenOverhead (str): The Bearer overhead. Defaults to "Bearer ".

    Returns:
        dict or bool: The payload if successful, False otherwise.
    """

    if unpack and token.startswith(TokenOverhead):
        token = token[len(TokenOverhead):]
    try:
        payload = decodeToken(token)
        try:
            if payload["exp"] > int(datetime.datetime.utcnow().timestamp()):
                return payload
            else:
                return False
        except AttributeError:
            return False
    except Exception as e:
        print(e)
        return False