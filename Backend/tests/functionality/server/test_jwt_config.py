"""
Tests for JWT token functionality.
"""
import pytest
from datetime import datetime, timedelta
import jwt
import os

from server.jwt_config.token_creation import (
    create_token,
    decode_token,
    encrypt_payload,
    decrypt_payload
)
from server.jwt_config.config import settings
from database.postgress.actions.revoked_jwt_tokens import revoke_token, get_revoked_token_by_jti

pytestmark = pytest.mark.functionality

@pytest.mark.asyncio
async def test_create_token(db_session):
    """Test token creation."""
    # Create access token
    access_token = create_token(
        user_id=999,
        role_id=1,
        refresh=False,
        fresh=True
    )

    assert isinstance(access_token, str)

    # Decode using PyJWT to verify structure
    payload = jwt.decode(
        access_token,
        settings.authjwt_secret_key,
        algorithms=[settings.authjwt_algorithm]
    )

    assert "refresh" in payload
    assert payload["refresh"] is False
    assert "payload" in payload

    # Create refresh token
    refresh_token = create_token(
        user_id=999,
        role_id=1,
        refresh=True,
        fresh=True
    )

    assert isinstance(refresh_token, str)

    # Decode using PyJWT to verify structure
    payload = jwt.decode(
        refresh_token,
        settings.authjwt_secret_key,
        algorithms=[settings.authjwt_algorithm]
    )

    assert "refresh" in payload
    assert payload["refresh"] is True
    assert "payload" in payload

@pytest.mark.asyncio
async def test_encrypt_decrypt_payload():
    """Test payload encryption and decryption."""
    # Create a test payload
    test_payload = {
        "sub": "999",
        "role": 1,
        "iat": int(datetime.utcnow().timestamp()),
        "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp()),
        "fresh": True,
        "jti": "test_jti"
    }

    # Encrypt the payload
    encrypted = encrypt_payload(test_payload)

    assert isinstance(encrypted, bytes)

    # Decrypt the payload
    decrypted = decrypt_payload(encrypted)

    # Verify decrypted payload matches original
    assert decrypted["sub"] == 999  # Converted to int
    assert decrypted["role"] == test_payload["role"]
    assert decrypted["fresh"] is test_payload["fresh"]
    assert decrypted["jti"] == test_payload["jti"]

@pytest.mark.asyncio
async def test_decode_token(db_session):
    """Test token decoding."""
    # Create tokens for testing
    access_token = create_token(999, 1, refresh=False, fresh=True)
    refresh_token = create_token(999, 1, refresh=True, fresh=True)

    # Decode access token
    access_payload = await decode_token(db_session, access_token, is_refresh=False)

    assert access_payload["sub"] == 999
    assert access_payload["role"] == 1
    assert access_payload["fresh"] is True
    assert "jti" in access_payload
    assert "exp" in access_payload

    # Decode refresh token
    refresh_payload = await decode_token(db_session, refresh_token, is_refresh=True)

    assert refresh_payload["sub"] == 999
    assert refresh_payload["role"] == 1
    assert refresh_payload["fresh"] is True
    assert "jti" in refresh_payload
    assert "exp" in refresh_payload

    # Test decoding with wrong token type
    with pytest.raises(Exception):
        await decode_token(db_session, access_token, is_refresh=True)

    with pytest.raises(Exception):
        await decode_token(db_session, refresh_token, is_refresh=False)

@pytest.mark.asyncio
async def test_token_revocation(db_session):
    """Test token revocation."""
    # Create a token
    access_token = create_token(999, 1, refresh=False, fresh=True)

    # Decode to get jti and expiration
    access_payload = await decode_token(db_session, access_token, is_refresh=False)
    jti = access_payload["jti"]
    expires = datetime.utcfromtimestamp(access_payload["exp"])

    # Revoke the token
    revoked_token = await revoke_token(db_session, jti, expires, "access")

    assert revoked_token is not None
    assert revoked_token.jti == jti
    assert revoked_token.type == "access"

    # Verify it's in the database
    db_token = await get_revoked_token_by_jti(db_session, jti)
    assert db_token is not None
    assert db_token.jti == jti

    # Try to decode the revoked token
    with pytest.raises(Exception):
        await decode_token(db_session, access_token, is_refresh=False)

@pytest.mark.asyncio
async def test_fresh_token_requirement(db_session):
    """Test fresh token requirement."""
    # Create tokens
    fresh_token = create_token(999, 1, refresh=False, fresh=True)
    non_fresh_token = create_token(999, 1, refresh=False, fresh=False)

    # Decode with fresh requirement - should work for fresh token
    payload = await decode_token(db_session, fresh_token, is_refresh=False, required_fresh=True)
    assert payload["fresh"] is True

    # Decode with fresh requirement - should fail for non-fresh token
    with pytest.raises(Exception):
        await decode_token(db_session, non_fresh_token, is_refresh=False, required_fresh=True)

    # Should work without fresh requirement
    payload = await decode_token(db_session, non_fresh_token, is_refresh=False, required_fresh=False)
    assert payload["fresh"] is False
