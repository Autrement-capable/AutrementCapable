import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock, MagicMock
import base64

from app import app
from app.db.postgress.engine import getSession
from app.db.postgress.models import User, UserDetail, PasskeyCredential
from soft_webauthn import SoftWebauthnDevice

def convert_bytes_to_base64(obj):
    """Recursively convert bytes objects to base64 strings for JSON serialization"""
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode('ascii')
    elif isinstance(obj, dict):
        return {k: convert_bytes_to_base64(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_bytes_to_base64(item) for item in obj]
    else:
        return obj


def prepare_options_for_virtual_device(options):
    """Convert string-based WebAuthn options to bytes for SoftWebauthnDevice"""
    options_copy = options.copy()
    
    # Convert challenge from base64url string to bytes
    challenge_str = options_copy["challenge"]
    challenge_padded = challenge_str + '=' * (4 - len(challenge_str) % 4)
    options_copy["challenge"] = base64.urlsafe_b64decode(challenge_padded)
    
    # Convert user.id from base64url string to bytes
    if isinstance(options_copy["user"]["id"], str):
        user_id_str = options_copy["user"]["id"]
        user_id_padded = user_id_str + '=' * (4 - len(user_id_str) % 4)
        options_copy["user"]["id"] = base64.urlsafe_b64decode(user_id_padded)
    
    # Override attestation for SoftWebauthnDevice compatibility
    options_copy["attestation"] = "none"
    
    return options_copy

@pytest.mark.asyncio
async def test_passkey_provisional_account_flow():
    """
    Test the full flow of creating a provisional account with a passkey,
    completing the profile, and then authenticating.
    """
    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.flush = AsyncMock()

    # Mock the session.get method for User
    mock_user = AsyncMock()
    mock_user.id = 1
    mock_user.onboarding_complete = False
    mock_session.get.return_value = mock_user

    # Mock the session.execute method for UserDetail queries
    # The key fix: scalars() should return a regular Mock, not AsyncMock
    mock_result = MagicMock()  # Changed from AsyncMock to MagicMock
    mock_scalars = MagicMock()  # Changed from AsyncMock to MagicMock
    mock_scalars.first.return_value = None  # No existing UserDetail
    mock_result.scalars.return_value = mock_scalars
    mock_session.execute.return_value = mock_result

    # When `flush` is called, simulate the DB assigning an ID to the User object
    async def flush_side_effect(*args, **kwargs):
        for call in mock_session.add.call_args_list:
            added_object = call.args[0]
            if isinstance(added_object, User):
                added_object.id = 1  # Match the real flow
                break

    mock_session.flush.side_effect = flush_side_effect

    # Mock the database session
    app.dependency_overrides[getSession] = lambda: mock_session

    device = SoftWebauthnDevice()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8080") as ac:
        # 1. Start passkey registration (provisional account)
        with patch('app.api.auth.passkeys.get_role_by_name', new_callable=AsyncMock) as mock_get_role_by_name, \
             patch('app.api.auth.passkeys.generate_passkey_registration_options') as mock_generate_options:
            
            # Mock based on your actual response format
            mock_generate_options.return_value = {
                "challenge": "g1x5W9HKwwmfUu82wESi82TvmXVsosCunMPV9UYoHlf2TRudU_PgFmmSZPjhzN5SrUnnBWUnjC2IICIcKYs4Rw",
                "rp": {"name": "Autrement Capable", "id": "localhost"},
                "user": {"id": "MQ", "name": "Autrement Capable", "displayName": "Autrement Capable"},
                "pubKeyCredParams": [
                    {"type": "public-key", "alg": -7},
                    {"type": "public-key", "alg": -8},
                    {"type": "public-key", "alg": -36},
                    {"type": "public-key", "alg": -37},
                    {"type": "public-key", "alg": -38},
                    {"type": "public-key", "alg": -39},
                    {"type": "public-key", "alg": -257},
                    {"type": "public-key", "alg": -258},
                    {"type": "public-key", "alg": -259}
                ],
                "timeout": 60000,
                "excludeCredentials": [],
                "authenticatorSelection": {
                    "authenticatorAttachment": "platform",
                    "residentKey": "preferred",
                    "requireResidentKey": False,
                    "userVerification": "preferred"
                },
                "attestation": "none"  # Changed to "none" for SoftWebauthnDevice
            }

            mock_role = AsyncMock()
            mock_role.id = 1
            mock_get_role_by_name.return_value = mock_role

            # Use the exact payload from your real flow
            response = await ac.post("/auth/passkey/registration/start", 
                                   json={"first_name": None, "last_name": None, "age": None})
            assert response.status_code == 200
            start_data = response.json()
            user_id = start_data["user_id"]
            assert user_id == 1

        # 2. Create credential with the virtual authenticator
        attestation = device.create(
            {"publicKey": prepare_options_for_virtual_device(start_data["options"])},
            "http://localhost:8080"
        )

        attestation_serializable = convert_bytes_to_base64(attestation)
        # 3. Complete the registration
        with patch('app.api.auth.passkeys.verify_passkey_registration') as mock_verify, \
            patch('app.db.postgress.repositories.user.get_user_by_id', new_callable=AsyncMock) as mock_get_user, \
            patch('app.db.postgress.repositories.passkey.register_passkey_credential', new_callable=AsyncMock) as mock_register_cred, \
            patch('app.core.security.token_creation.create_token') as mock_create_token:
            
            # Mock verification result
            mock_verify.return_value = {
                "credential_id": "test_credential_id",
                "public_key": "test_public_key"
            }
            
            # Mock user
            mock_user_for_registration = AsyncMock()
            mock_user_for_registration.id = user_id
            mock_user_for_registration.role_id = 1
            mock_get_user.return_value = mock_user_for_registration
            
            # Mock credential registration
            mock_credential = AsyncMock()
            mock_register_cred.return_value = mock_credential
            
            # Mock token creation
            mock_create_token.return_value = "test_access_token"
            
            response = await ac.post("/auth/passkey/registration/complete", json={
                "user_id": user_id,
                "registration_data": attestation_serializable,
                "challenge": start_data["options"]["challenge"]
            })
            assert response.status_code == 200
            registration_result = response.json()
            assert registration_result["success"] is True
            assert "access_token" in registration_result
            access_token = registration_result["access_token"]

        # 4. Update user profile using the access token
        with patch('app.core.security.decorators.get_jwt_data') as mock_get_jwt:
            # Mock the JWT data to return user info directly (for ACCESS_TOKEN security type)
            mock_get_jwt.return_value = {"sub": user_id, "role": "Young Person"}

            response = await ac.put("/user/profile", 
                                  json={"first_name": "wfwf", "age": 18, "onboarding_complete": True},
                                  headers={"Authorization": f"Bearer {access_token}"})
            assert response.status_code == 200
            assert response.json()["message"] == "Profile updated successfully"

    # Clean up the override
    app.dependency_overrides.clear()