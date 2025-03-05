import base64
import os
import json
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives import serialization
import cbor2
from webauthn.helpers import bytes_to_base64url, base64url_to_bytes
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response
)
from os import getenv
from datetime import datetime, timedelta

# Get RP name and ID from environment or use defaults
RP_ID = getenv("RP_ID", "localhost")
RP_NAME = getenv("RP_NAME", "Autrement Capable")
ORIGIN = getenv("ORIGIN", f"https://{RP_ID}")

def generate_passkey_registration_options(user_id: str, username: str) -> Dict[str, Any]:
    """
    Generate registration options for WebAuthn/Passkey.

    Args:
        user_id (str): User ID
        username (str): Username or display name

    Returns:
        Dict[str, Any]: Registration options
    """
    # Convert user_id to string if it's not already
    user_id_str = str(user_id)

    # Generate registration options
    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_id=user_id_str,
        user_name=username,
        attestation="direct",
        authenticator_selection={
            "authenticatorAttachment": "platform",  # platform = passkey, cross-platform = security key
            "residentKey": "preferred",
            "userVerification": "preferred"
        }
    )

    # Encode challenge as base64url (required for serialization)
    options_dict = options.asdict()
    options_dict["challenge"] = bytes_to_base64url(options.challenge)

    return options_dict

def verify_passkey_registration(
    user_id: str,
    options_challenge: str,
    registration_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Verify WebAuthn/Passkey registration response.

    Args:
        user_id (str): User ID
        options_challenge (str): Challenge from registration options (base64url)
        registration_data (Dict[str, Any]): Registration data from client

    Returns:
        Optional[Dict[str, Any]]: Verified credential data if successful, None if failed
    """
    try:
        # Convert user_id to string if it's not already
        user_id_str = str(user_id)

        # Convert base64url challenge to bytes
        challenge_bytes = base64url_to_bytes(options_challenge)

        # Verify registration response
        verification = verify_registration_response(
            credential=registration_data,
            expected_challenge=challenge_bytes,
            expected_origin=ORIGIN,
            expected_rp_id=RP_ID,
        )

        # If verification successful, return credential data
        if verification and verification.credential_id:
            return {
                "credential_id": bytes_to_base64url(verification.credential_id),
                "public_key": verification.credential_public_key,
                "sign_count": verification.sign_count
            }

        return None
    except Exception as e:
        print(f"Error verifying passkey registration: {e}")
        return None

def generate_passkey_authentication_options() -> Dict[str, Any]:
    """
    Generate authentication options for WebAuthn/Passkey.

    Returns:
        Dict[str, Any]: Authentication options
    """
    options = generate_authentication_options(
        rp_id=RP_ID,
        user_verification="preferred"
    )

    # Encode challenge as base64url
    options_dict = options.asdict()
    options_dict["challenge"] = bytes_to_base64url(options.challenge)

    return options_dict

def verify_passkey_authentication(
    credential_id: str,
    public_key: bytes,
    current_sign_count: int,
    options_challenge: str,
    authentication_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Verify WebAuthn/Passkey authentication response.

    Args:
        credential_id (str): Credential ID (base64url)
        public_key (bytes): Public key
        current_sign_count (int): Current sign count
        options_challenge (str): Challenge from authentication options (base64url)
        authentication_data (Dict[str, Any]): Authentication data from client

    Returns:
        Optional[Dict[str, Any]]: Verification result if successful, None if failed
    """
    try:
        # Convert base64url challenge to bytes
        challenge_bytes = base64url_to_bytes(options_challenge)

        # Verify authentication response
        verification = verify_authentication_response(
            credential=authentication_data,
            expected_challenge=challenge_bytes,
            expected_origin=ORIGIN,
            expected_rp_id=RP_ID,
            credential_public_key=public_key,
            credential_current_sign_count=current_sign_count
        )

        # If verification successful, return new sign count
        if verification:
            return {
                "verified": True,
                "new_sign_count": verification.new_sign_count
            }

        return None
    except Exception as e:
        print(f"Error verifying passkey authentication: {e}")
        return None