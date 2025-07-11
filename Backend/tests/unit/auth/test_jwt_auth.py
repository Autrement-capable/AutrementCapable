import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock, MagicMock
import time
from datetime import datetime, timedelta
import jwt

from app import app
from app.db.postgress.engine import getSession
from app.core.security.token_creation import create_token
from app.db.postgress.models import RevokedToken

# Helper to create a valid token for tests
def get_test_token(user_id=1, role_id=1, fresh=True, expired=False, is_refresh=False):
    """Create a test token with proper expiration"""
    if expired:
        expires_delta = timedelta(seconds=-1)
    else:
        expires_delta = timedelta(seconds=3600)
    
    return create_token(
        user_id,
        role_id,
        refresh=is_refresh,
        fresh=fresh,
    )

@pytest.mark.asyncio
async def test_refresh_token():
    """
    Test the /auth/refresh endpoint to ensure it returns a new access token
    when provided with a valid refresh token.
    """
    mock_session = AsyncMock()
    app.dependency_overrides[getSession] = lambda: mock_session

    refresh_token = get_test_token(is_refresh=True)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Mock the token revocation check
        with patch('app.core.security.token_creation.is_token_revoked', new_callable=AsyncMock) as mock_is_revoked:
            mock_is_revoked.return_value = False  # Token is not revoked
            
            response = await ac.post("/auth/refresh", cookies={"refresh_token": refresh_token})

            assert response.status_code == 200
            response_data = response.json()
            assert "access_token" in response_data
            
            # Verify we can use the new access token to call /auth/status
            access_token = response_data["access_token"]
            status_response = await ac.get("/auth/status", 
                                         headers={"Authorization": f"Bearer {access_token}"})
            assert status_response.status_code == 200
            status_data = status_response.json()
            assert "user_id" in status_data
            assert status_data["user_id"] == 1

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_logout():
    """
    Test the /auth/logout endpoint to ensure it revokes both access and refresh tokens.
    """
    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    
    app.dependency_overrides[getSession] = lambda: mock_session

    access_token = get_test_token()
    refresh_token = get_test_token(is_refresh=True)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Mock the token revocation check and the actual revoke function
        with patch('app.core.security.token_creation.is_token_revoked', new_callable=AsyncMock) as mock_is_revoked, \
             patch('app.api.auth.auth_operations.revoke_token', new_callable=AsyncMock) as mock_revoke:
            
            mock_is_revoked.return_value = False  # Tokens are not revoked initially
            mock_revoke.return_value = MagicMock()  # Return a mock RevokedToken object
            
            response = await ac.post("/auth/logout", 
                                   headers={"Authorization": f"Bearer {access_token}"},
                                   cookies={"refresh_token": refresh_token})
            
            assert response.status_code == 200
            response_data = response.json()
            assert "msg" in response_data
            assert "logged out" in response_data["msg"].lower()
            
            # Verify that revoke_token was called (might be once or twice depending on implementation)
            assert mock_revoke.call_count >= 1

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_token_blacklisting():
    """
    Test that a revoked token cannot be used.
    """
    mock_session = AsyncMock()
    app.dependency_overrides[getSession] = lambda: mock_session

    access_token = get_test_token()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        with patch('app.core.security.token_creation.is_token_revoked', new_callable=AsyncMock) as mock_is_revoked:
            # Mark the token as revoked
            mock_is_revoked.return_value = True

            response = await ac.get("/auth/status", headers={"Authorization": f"Bearer {access_token}"})
            
            assert response.status_code == 401
            response_data = response.json()
            assert "Token has been revoked" in response_data["detail"]

    app.dependency_overrides.clear()

# Helper to create a valid token for tests
def get_test_token(user_id=1, role_id=1, fresh=True, expired=False, is_refresh=False):
    """Create a test token with proper expiration"""
    # Create token first
    token = create_token(
        user_id,
        role_id,
        refresh=is_refresh,
        fresh=fresh,
    )
    
    # If we want an expired token, we need to manually create one with past expiration
    if expired:
        import jwt as jose_jwt
        from app.core.security.config import get_secret_key
        
        # Decode the token to get the payload
        secret_key = get_secret_key()
        payload = jose_jwt.decode(token, secret_key, algorithms=["HS256"], options={"verify_exp": False})
        
        # Set expiration to past time
        payload["exp"] = int(time.time()) - 3600  # 1 hour ago
        
        # Re-encode with expired timestamp
        token = jose_jwt.encode(payload, secret_key, algorithm="HS256")
    
    return token

@pytest.mark.asyncio
async def test_expired_token():
    """
    Test that an expired token cannot be used.
    """
    mock_session = AsyncMock()
    app.dependency_overrides[getSession] = lambda: mock_session

    # Create an expired token
    expired_token = get_test_token(expired=True)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        with patch('app.core.security.token_creation.is_token_revoked', new_callable=AsyncMock) as mock_is_revoked:
            mock_is_revoked.return_value = False  # Token is not revoked, just expired
            
            response = await ac.get("/auth/status", headers={"Authorization": f"Bearer {expired_token}"})
            
            assert response.status_code == 401
            response_data = response.json()
            # Check for various possible error messages
            detail = response_data.get("detail", "").lower()
            assert any(word in detail for word in ["expired", "invalid", "signature"])

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_valid_token_auth_status():
    """
    Test that a valid token can access the /auth/status endpoint.
    """
    mock_session = AsyncMock()
    app.dependency_overrides[getSession] = lambda: mock_session

    access_token = get_test_token()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        with patch('app.core.security.token_creation.is_token_revoked', new_callable=AsyncMock) as mock_is_revoked:
            mock_is_revoked.return_value = False  # Token is valid
            
            response = await ac.get("/auth/status", headers={"Authorization": f"Bearer {access_token}"})
            
            assert response.status_code == 200
            response_data = response.json()
            assert "user_id" in response_data
            assert response_data["user_id"] == 1
            assert "role" in response_data
            assert response_data["msg"] == "User is authenticated"

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_missing_token():
    """
    Test that requests without tokens are rejected.
    """
    mock_session = AsyncMock()
    app.dependency_overrides[getSession] = lambda: mock_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/auth/status")
        
        assert response.status_code == 401
        response_data = response.json()
        assert "missing" in response_data["detail"].lower() or "invalid" in response_data["detail"].lower()

    app.dependency_overrides.clear()