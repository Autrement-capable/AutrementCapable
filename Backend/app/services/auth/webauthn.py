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
from webauthn.helpers.structs import (
    AuthenticatorAttachment,
    AuthenticatorSelectionCriteria,
    ResidentKeyRequirement,
    UserVerificationRequirement,
    AttestationConveyancePreference
)
from os import getenv
from datetime import datetime, timedelta

# Get RP name and ID from environment or use defaults
RP_ID = getenv("RP_ID", "localhost")
RP_NAME = getenv("RP_NAME", "Autrement Capable")
ORIGIN = getenv("ORIGIN", f"https://{RP_ID}")

def generate_passkey_registration_options(user_id, username) -> Dict[str, Any]:
    """
    Generate registration options for WebAuthn/Passkey.

    Args:
        user_id (str or int): User ID
        username (str): Username or display name

    Returns:
        Dict[str, Any]: Registration options
    """
    # Convert user_id to string and then to bytes as required by the WebAuthn library
    user_id_str = str(user_id)
    user_id_bytes = user_id_str.encode('utf-8')

    # Generate registration options using proper class instances
    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_id=user_id_bytes,
        user_name=username,
        attestation=AttestationConveyancePreference.DIRECT,
        authenticator_selection=AuthenticatorSelectionCriteria(
            authenticator_attachment=AuthenticatorAttachment.PLATFORM,
            resident_key=ResidentKeyRequirement.PREFERRED,
            user_verification=UserVerificationRequirement.PREFERRED
        )
    )

    # Convert options to dictionary
    try:
        if hasattr(options, 'to_dict'):
            options_dict = options.to_dict()
        elif hasattr(options, 'serialize'):
            options_dict = options.serialize()
        elif hasattr(options, 'asdict'):
            options_dict = options.asdict()
        elif hasattr(options, '__dict__'):
            options_dict = {k: v for k, v in options.__dict__.items() 
                           if not k.startswith('_')}
        else:
            # Manual conversion
            options_dict = {
                'challenge': options.challenge,
                'rp': getattr(options, 'rp', {'name': RP_NAME, 'id': RP_ID}),
                'user': getattr(options, 'user', {'id': user_id_bytes, 'name': username, 'displayName': username}),
                'pubKeyCredParams': getattr(options, 'pub_key_cred_params', []),
                'timeout': getattr(options, 'timeout', 60000),
                'attestation': getattr(options, 'attestation', 'direct'),
                'authenticatorSelection': getattr(options, 'authenticator_selection', {})
            }
    except Exception as e:
        # If conversion fails, create a minimal dictionary with the essentials
        print(f"Error converting options: {e}")
        options_dict = {
            'challenge': options.challenge,
            'rp': {
                'name': RP_NAME,
                'id': RP_ID
            },
            'user': {
                'id': user_id_bytes,
                'name': username,
                'displayName': username
            },
            'pubKeyCredParams': [
                {'type': 'public-key', 'alg': -7},  # ES256
                {'type': 'public-key', 'alg': -257}  # RS256
            ],
            'timeout': 60000,
            'attestation': 'direct',
            'authenticatorSelection': {
                'authenticatorAttachment': 'platform',
                'residentKey': 'preferred',
                'userVerification': 'preferred'
            }
        }

    # Encode challenge as base64url
    options_dict["challenge"] = bytes_to_base64url(options.challenge)

    # Create a new dictionary for the output with the correct structure
    result = {
        'challenge': bytes_to_base64url(options.challenge),
        'rp': {
            'name': options.rp.name,
            'id': options.rp.id
        },
        'user': {
            'id': bytes_to_base64url(options.user.id),
            'name': options.user.name,
            'displayName': options.user.display_name if hasattr(options.user, 'display_name') else options.user.name
        },
        'pubKeyCredParams': [
            {'type': param.type, 'alg': param.alg.value if hasattr(param.alg, 'value') else param.alg}
            for param in options.pub_key_cred_params
        ],
        'timeout': options.timeout,
        'excludeCredentials': [],  # No credentials to exclude for a new user
        'authenticatorSelection': {
            'authenticatorAttachment': options.authenticator_selection.authenticator_attachment.value
                if hasattr(options.authenticator_selection.authenticator_attachment, 'value')
                else options.authenticator_selection.authenticator_attachment,
            'residentKey': options.authenticator_selection.resident_key.value
                if hasattr(options.authenticator_selection.resident_key, 'value')
                else options.authenticator_selection.resident_key,
            'requireResidentKey': options.authenticator_selection.require_resident_key,
            'userVerification': options.authenticator_selection.user_verification.value
                if hasattr(options.authenticator_selection.user_verification, 'value')
                else options.authenticator_selection.user_verification
        },
        'attestation': options.attestation.value if hasattr(options.attestation, 'value') else options.attestation
    }
    return result

def generate_passkey_authentication_options() -> Dict[str, Any]:
    """
    Generate authentication options for WebAuthn/Passkey.

    Returns:
        Dict[str, Any]: Authentication options
    """
    options = generate_authentication_options(
        rp_id=RP_ID,
        user_verification=UserVerificationRequirement.PREFERRED
    )

    # Convert options to dictionary
    try:
        if hasattr(options, 'to_dict'):
            options_dict = options.to_dict()
        elif hasattr(options, 'serialize'):
            options_dict = options.serialize()
        elif hasattr(options, 'asdict'):
            options_dict = options.asdict()
        elif hasattr(options, '__dict__'):
            options_dict = {k: v for k, v in options.__dict__.items() 
                           if not k.startswith('_')}
        else:
            # Manual conversion
            options_dict = {
                'challenge': options.challenge,
                'timeout': getattr(options, 'timeout', 60000),
                'rpId': RP_ID,
                'userVerification': str(UserVerificationRequirement.PREFERRED),
                'allowCredentials': getattr(options, 'allow_credentials', [])
            }
    except Exception as e:
        # Fallback if conversion fails
        print(f"Error converting authentication options: {e}")
        options_dict = {
            'challenge': options.challenge,
            'timeout': 60000,
            'rpId': RP_ID,
            'userVerification': 'preferred',
            'allowCredentials': []
        }

    # Encode challenge as base64url
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
