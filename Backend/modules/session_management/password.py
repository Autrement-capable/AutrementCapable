from passlib.hash import pbkdf2_sha256
from functools import wraps
import secrets
import inspect

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