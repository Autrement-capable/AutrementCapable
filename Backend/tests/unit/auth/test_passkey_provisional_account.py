import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock, MagicMock

from app import app  # Assuming your FastAPI app is defined here
from app.db.postgress.engine import getSession
from app.db.postgress.models.test_model import User, UserDetail, PasskeyCredential
from soft_webauthn import SoftWebauthnDevice

from webauthn.helpers import bytes_to_base64url

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

    # When `flush` is called, simulate the DB assigning an ID to the User object
    async def flush_side_effect(*args, **kwargs):
        for call in mock_session.add.call_args_list:
            added_object = call.args[0]
            if isinstance(added_object, User):
                added_object.id = 123  # Assign a mock ID
                break

    mock_session.flush.side_effect = flush_side_effect

    # Mock the database session
    app.dependency_overrides[getSession] = lambda: mock_session

    device = SoftWebauthnDevice()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Start passkey registration (provisional account)
        with patch('app.api.auth.passkeys.get_role_by_name', new_callable=AsyncMock) as mock_get_role_by_name,             patch('app.api.auth.passkeys.generate_passkey_registration_options') as mock_generate_options:
            mock_generate_options.return_value = {
                "challenge": bytes_to_base64url(b"some_challenge_bytes"),  # String, not bytes
                "rp": {"id": "localhost", "name": "Test RP"},
                "user": {
                    "id": bytes_to_base64url(b"123"),  # String, not bytes
                    "name": "testuser", 
                    "displayName": "Test User"
                },
                "pubKeyCredParams": [
                    {"type": "public-key", "alg": -7},
                    {"type": "public-key", "alg": -257}
                ],
                "timeout": 60000,
                "excludeCredentials": [],
                "authenticatorSelection": {
                    "authenticatorAttachment": "platform",
                    "residentKey": "preferred",
                    "requireResidentKey": False,
                    "userVerification": "preferred"
                },
                "attestation": "none"
            }

            mock_role = AsyncMock()
            mock_role.id = 1
            mock_get_role_by_name.return_value = mock_role

            response = await ac.post("/auth/passkey/registration/start", json={})
            assert response.status_code == 200
            start_data = response.json()
            user_id = start_data["user_id"]

        # 2. Create credential with the virtual authenticator
        attestation = await device.create(
            {"publicKey": start_data["options"]},  # Wrap in publicKey object
            "http://localhost:8080" # Match the ORIGIN from .env
        )

        # 3. Complete the registration
        with patch('app.api.auth.passkeys.verify_passkey_registration', return_value=AsyncMock()) as mock_verify:
            response = await ac.post("/auth/passkey/registration/complete", json={
                "user_id": user_id,
                "attestation_response": attestation
            })
            assert response.status_code == 200

        # 4. Update user profile
        with patch('app.api.data.user_profile.get_user_by_id', new_callable=AsyncMock) as mock_get_user:
            mock_user = User(id=user_id, is_provisional=True)
            mock_user_detail = UserDetail(user_id=user_id)
            mock_user.user_detail = mock_user_detail
            mock_get_user.return_value = mock_user

            response = await ac.put(f"/user/profile/{user_id}", json={"first_name": "Test", "age": 30})
            assert response.status_code == 200
            assert mock_user.is_provisional is False
            assert mock_user_detail.first_name == "Test"
            assert mock_user_detail.age == 30

        # 5. Start authentication
        with patch('app.api.auth.passkeys.generate_passkey_authentication_options', return_value={"challenge": "another_challenge"}) as mock_generate_auth_options:
            response = await ac.post("/auth/passkey/authentication/start", json={"user_id": user_id})
            assert response.status_code == 200
            auth_options = response.json()

        # 6. Get assertion with the virtual authenticator
        assertion = await device.get(auth_options, "http://test")

        # 7. Complete the authentication
        with patch('app.api.auth.passkeys.verify_passkey_authentication', new_callable=AsyncMock) as mock_verify_auth:
            mock_user = User(id=user_id, email=f'user_{user_id}@example.com')
            mock_passkey = PasskeyCredential(user_id=user_id, credential_id=device.credential_id, public_key=device.public_key)
            mock_verify_auth.return_value = (mock_user, mock_passkey)

            with patch('app.core.security.token_creation.create_access_token', return_value="test_token") as mock_create_token:
                response = await ac.post("/auth/passkey/authentication/complete", json={
                    "user_id": user_id,
                    "assertion_response": assertion
                })
                assert response.status_code == 200
                assert response.json()["access_token"] == "test_token"

    # Clean up the override
    app.dependency_overrides.clear()