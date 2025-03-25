import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.future import select
from datetime import datetime

from database.postgress.models import RevokedToken
from server.jwt_config.token_creation import decode_token

pytestmark = pytest.mark.endpoint

@pytest.fixture
async def auth_tokens(client: AsyncClient, db_session):
    """Create and return auth tokens from a test login."""
    # Register and verify a user first
    await client.post("/auth/register", json={
        "first_name": "Auth",
        "last_name": "Test",
        "phone_number": "5551234567",
        "address": "Auth Test Address",
        "username": "authuser",
        "email": "authuser@example.com",
        "password": "Password123"
    })

    # Get verification token
    from database.postgress.models import UnverifiedDetails, User
    from sqlalchemy.orm import joinedload

    result = await db_session.execute(
        select(UnverifiedDetails)
        .options(joinedload(UnverifiedDetails.user))
        .where(UnverifiedDetails.user.has(User.email == "authuser@example.com"))
    )
    details = result.scalars().first()

    # Verify user
    verify_response = await client.get(f"/auth/verify?code={details.verification_token}")

    # Login to get tokens
    login_response = await client.post("/auth/login", json={
        "username_or_email": "authuser@example.com",
        "password": "Password123"
    })

    return login_response.json()

@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient, db_session, auth_tokens):
    """Test successful token refresh."""
    refresh_token = auth_tokens["refresh_token"]

    # Call refresh endpoint
    response = await client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )

    # Assert successful response
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Validate new access token
    new_access_token = response.json()["access_token"]
    decoded = await decode_token(db_session, new_access_token, is_refresh=False)

    # Ensure token contains expected fields
    assert "sub" in decoded
    assert "role" in decoded
    assert "jti" in decoded
    assert "exp" in decoded

    # Ensure token is not expired
    assert datetime.utcfromtimestamp(decoded["exp"]) > datetime.utcnow()

@pytest.mark.asyncio
async def test_refresh_with_access_token(client: AsyncClient, db_session, auth_tokens):
    """Test refresh endpoint with an access token (should fail)."""
    access_token = auth_tokens["access_token"]

    # Try to use access token on refresh endpoint
    response = await client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assert proper error
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient, db_session, auth_tokens):
    """Test successful logout."""
    access_token = auth_tokens["access_token"]
    refresh_token = auth_tokens["refresh_token"]

    # Call logout endpoint
    response = await client.post(
        "/auth/logout",
        json={"refresh_token": refresh_token},
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assert successful logout
    assert response.status_code == 200
    assert "msg" in response.json()
    assert response.json()["msg"] == "Successfully logged out"

    # Verify tokens are revoked in DB
    # Get access token JTI
    access_payload = await decode_token(db_session, access_token, is_refresh=False)
    access_jti = access_payload["jti"]

    # Verify access token is revoked
    result = await db_session.execute(
        select(RevokedToken).where(RevokedToken.jti == access_jti)
    )
    revoked_access = result.scalars().first()
    assert revoked_access is not None
    assert revoked_access.type == "access"

    # Get refresh token JTI
    refresh_payload = await decode_token(db_session, refresh_token, is_refresh=True)
    refresh_jti = refresh_payload["jti"]

    # Verify refresh token is revoked
    result = await db_session.execute(
        select(RevokedToken).where(RevokedToken.jti == refresh_jti)
    )
    revoked_refresh = result.scalars().first()
    assert revoked_refresh is not None
    assert revoked_refresh.type == "refresh"

    # Try to use revoked tokens
    # Try refresh
    refresh_response = await client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try access
    access_response = await client.post(
        "/auth/logout",
        json={"refresh_token": "any_token"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert access_response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_logout_invalid_refresh(client: AsyncClient, db_session, auth_tokens):
    """Test logout with invalid refresh token."""
    access_token = auth_tokens["access_token"]

    # Call logout with invalid refresh token
    response = await client.post(
        "/auth/logout",
        json={"refresh_token": "invalid_refresh_token"},
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Assert proper error
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()