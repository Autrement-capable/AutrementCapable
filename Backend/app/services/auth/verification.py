import hmac
import hashlib
import base64
from os import getenv
from datetime import datetime, timedelta
import random
import string
from typing import Union

SERVER_SECRET = getenv("SERVER_SECRET", "default_secret_key")

def generate_verification_code(data: Union[str, int], expiration_seconds: int = 900) -> tuple[str, datetime]:
    """
    Generate a secure verification code based on either:
      - a string (e.g., email or user ID), or
      - an integer length (random code generation),
    combined with an expiration timestamp to ensure uniqueness.

    Args:
        data (Union[str, int]):
            - str: user identifier (e.g., email)
            - int: desired length of random string
        expiration_seconds (int, optional): Expiration time in seconds. Default is 900 (15 min).

    Returns:
        tuple[str, datetime]: (Generated verification code, expiration timestamp)
    """
    # Determine input base
    if isinstance(data, int):
        base = ''.join(random.choices(string.ascii_letters + string.digits, k=data))
    elif isinstance(data, str):
        base = data
    else:
        raise ValueError("data must be a string (email/identifier) or an integer (length of random code)")

    # Generate expiration datetime
    expiration_dt = datetime.utcnow() + timedelta(seconds=expiration_seconds)
    expiration_str = expiration_dt.isoformat()

    # Create message and HMAC signature
    message = f"{base}:{expiration_str}".encode()
    secret = SERVER_SECRET.encode()
    signature = hmac.new(secret, message, hashlib.sha256).digest()

    # Encode to URL-safe base64 (without padding)
    verification_code = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    return verification_code, expiration_dt


def generate_random_suffix(length: int = 6) -> str:
    """
    Generate a random suffix for a the user's username.(Used to avoid conflicts)

    Args:
        length (int, optional): The length of the suffix. Defaults to 6.
    """
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
