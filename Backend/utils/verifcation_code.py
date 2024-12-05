import hmac
import hashlib
import base64
from os import getenv
from datetime import datetime, timedelta
import random
import string

SERVER_SECRET = getenv("SERVER_SECRET", "default_secret_key")

def generate_verification_code(email: str, expiration_seconds: int = 900) -> tuple[str, datetime]:
    """
    Generate a secure verification code based on email and expiration time.

    Args:
        email (str): The email to generate the verification code for.
        expiration_seconds (int, optional): The expiration time in seconds. Defaults to 900(15 minutes).

    Returns:
        tuple[str, datetime]: The generated verification code and the expiration time.
    """
    expiration = (datetime.utcnow() + timedelta(seconds=expiration_seconds)).isoformat()
    message = f"{email}:{expiration}".encode()
    secret = SERVER_SECRET.encode()
    signature = hmac.new(secret, message, hashlib.sha256).digest()
    verification_code = base64.urlsafe_b64encode(signature).decode().rstrip("=") # Remove padding
    expiration = datetime.fromisoformat(expiration)
    return verification_code, expiration

def generate_random_suffix(length: int = 6) -> str:
    """
    Generate a random suffix for a the user's username.(Used to avoid conflicts)

    Args:
        length (int, optional): The length of the suffix. Defaults to 6.
    """
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))