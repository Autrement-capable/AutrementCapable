from flask import request, jsonify, make_response
from functools import wraps
from os import getenv
from passlib.hash import pbkdf2_sha256
from modules.session_management.JWT import UnpackToken
from modules.database.Opps import GetUser, IsTokenRevoked # may use user object returns istead of the payload
from functools import wraps
import secrets
import inspect

def login_required(func):
    """Decorator to check if the user is logged in.
    This decorator checks if the user is logged in by checking the JWT token in the Authorization header.
    If the token is valid, the user object and/or the token are passed to the method if it needs them.
    Note: NB: This decorator should be after @marshal_with decorator if you are using it. To
    be safe put it last.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        token_overhead= getenv("JWT_OVERHEAD")
        if token and IsTokenRevoked(token) == False:
            payload = UnpackToken(token, unpack=True, TokenOverhead=token_overhead)
            if payload:
                user = GetUser(payload["email"])
                if user:
                    arg_names = inspect.getfullargspec(func).args # get the args of the function
                    if "user" in arg_names: # if the function needs the user object send it
                        kwargs["user"] = user
                    if "token" in arg_names: # if the function needs the payload object send it
                        kwargs["token"] = token[len(token_overhead):]
                    return func(*args, **kwargs)
                else:
                    if getenv("MODE") == "DEV":
                        return make_response(jsonify({"message": "User Not Found"}), 403)
                    return make_response(jsonify({"message": "Invalid Credentials"}), 403)
            else:
                if getenv("MODE") == "DEV":
                    return make_response(jsonify({"message": "Token Expired"}), 403)
                return make_response(jsonify({"message": "Invalid Credentials"}), 403)
        else:
            if getenv("MODE") == "DEV":
                return make_response(jsonify({"message": "Token Missing in Headers send or revoked"}), 403)
            return make_response(jsonify({"message": "Invalid Credentials"}), 403)
    return wrapper

def hash_password(password) -> str:
    """Hash a password using pbkdf2_sha256.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    salt = secrets.token_hex(16)
    # convert the salt to bytes
    salt = salt.encode('utf-8')
    hash_value = pbkdf2_sha256.hash(password, salt=salt)
    return f"{hash_value}"

def verify_password(password, hash) -> bool:
    """Verify a password against a hash.

    Args:
        password (str): The password to verify.
        hash (str): The hash to verify against.

    Returns:
        bool: Whether the password is valid or not.
    """
    try:
        return pbkdf2_sha256.verify(password, hash)
    except Exception as e:
        print(e)
        return False