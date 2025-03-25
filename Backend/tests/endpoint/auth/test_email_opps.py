import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta

from database.postgress.models import User, PasswordReset, UnverifiedDetails
from database.postgress.actions.password_reset import create_password_reset

pytestmark = pytest.mark.endpoint

@pytest.fixture
async def test_user_verified(client: AsyncClient, db_session, init_test_data):
    """Create a verified test user."""
    # Register user
    await client.post("/auth/register", json={
        "first_name": "Email",
        "last_name": "Test",
        "phone_number": "5551234567",
        "address": "123 Email St",
        "username": "emailtest",
        "email": "emailtest@example.com",
        "password": "Password123"
    })

    # Get verification token
    result = await db_session.execute(
        select(UnverifiedDetails)
        .options(joinedload(UnverifiedDetails.user))
        .where(UnverifiedDetails.user.has(User.email == "emailtest@example.com"))
    )
    details = result.scalars().first()

    # Verify user
    await client.get(f"/auth/verify?code={details.verification_token}")

    # Get user and return
    result = await db_session.execute(
        select(User).where(User.email == "emailtest@example.com")
    )
    return result.scalars().first()

@pytest.fixture
async def test_user_unverified(client: AsyncClient, db_session, init_test_data):
    """Create an unverified test user."""
    # Register user
    await client.post("/auth/register", json={
        "first_name": "Unverified",
        "last_name": "Test",
        "phone_number": "5557654321",
        "address": "456 Unverified St",
        "username": "unverifiedtest",
        "email": "unverified@example.com",
        "password": "Password123"
    })

    # Get user and return
    result = await db_session.execute(
        select(User).where(User.email == "unverified@example.com")
    )
    return result.scalars().first()

@pytest.mark.asyncio
async def test_verify_endpoint(client: AsyncClient, db_session, test_user_unverified):
    """Test the verify endpoint."""
    # Get verification token
    result = await db_session.execute(
        select(UnverifiedDetails).where(UnverifiedDetails.user_id == test_user_unverified.id)
    )
    details = result.scalars().first()

    # Call verify endpoint
    response = await client.get(f"/auth/verify?code={details.verification_token}")

    # Check response
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

    # Verify user is now verified
    result = await db_session.execute(
        select(UnverifiedDetails).where(UnverifiedDetails.user_id == test_user_unverified.id)
    )
    assert result.scalars().first() is None

@pytest.mark.asyncio
async def test_verify_endpoint_invalid_code(client: AsyncClient, db_session):
    """Test verify endpoint with invalid code."""
    response = await client.get("/auth/verify?code=invalid_code")

    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_start_reset_password(client: AsyncClient, db_session, test_user_verified):
    """Test starting password reset process."""
    # Request password reset
    response = await client.post("/auth/start-reset-password", json={
        "email": "emailtest@example.com"
    })

    # Check response
    assert response.status_code == 200
    assert "message" in response.json()
    assert "reset" in response.json()["message"].lower()

    # Verify reset token was created in database
    result = await db_session.execute(
        select(PasswordReset)
        .where(PasswordReset.user_id == test_user_verified.id)
    )
    reset = result.scalars().first()

    assert reset is not None
    assert reset.reset_token is not None
    assert reset.token_expires > datetime.utcnow()

@pytest.mark.asyncio
async def test_start_reset_password_nonexistent_user(client: AsyncClient, db_session):
    """Test starting password reset for non-existent user."""
    response = await client.post("/auth/start-reset-password", json={
        "email": "nonexistent@example.com"
    })

    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_is_valid_reset_token(client: AsyncClient, db_session, test_user_verified):
    """Test checking if reset token is valid."""
    # Create a password reset
    reset = await create_password_reset(db_session, test_user_verified)

    # Check if token is valid
    response = await client.get(f"/auth/is-valid-reset?token={reset.reset_token}")

    # Should return valid
    assert response.status_code == 200
    assert "valid" in response.json()
    assert response.json()["valid"] is True

    # Check invalid token
    response = await client.get("/auth/is-valid-reset?token=invalid_token")

    # Should return invalid
    assert response.status_code == 404
    assert "valid" in response.json()
    assert response.json()["valid"] is False

    # Check expired token
    # First make the token expired
    reset.token_expires = datetime.utcnow() - timedelta(hours=1)
    db_session.add(reset)
    await db_session.commit()

    # Check if expired token is valid
    response = await client.get(f"/auth/is-valid-reset?token={reset.reset_token}")

    # Should return invalid
    assert response.status_code == 404
    assert "valid" in response.json()
    assert response.json()["valid"] is False

@pytest.mark.asyncio
async def test_reset_password(client: AsyncClient, db_session, test_user_verified):
    """Test resetting password."""
    # Create a password reset
    reset = await create_password_reset(db_session, test_user_verified)

    # Reset password
    response = await client.post("/auth/reset-password", json={
        "password": "NewPassword123",
        "token": reset.reset_token
    })

    # Check response
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

    # Verify reset token was deleted
    result = await db_session.execute(
        select(PasswordReset).where(PasswordReset.reset_token == reset.reset_token)
    )
    assert result.scalars().first() is None

    # Try logging in with new password
    login_response = await client.post("/auth/login", json={
        "username_or_email": "emailtest@example.com",
        "password": "NewPassword123"
    })

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    # Try logging in with old password
    login_response = await client.post("/auth/login", json={
        "username_or_email": "emailtest@example.com",
        "password": "Password123"
    })

    assert login_response.status_code == 401

@pytest.mark.asyncio
async def test_reset_password_invalid_token(client: AsyncClient, db_session):
    """Test resetting password with invalid token."""
    response = await client.post("/auth/reset-password", json={
        "password": "NewPassword123",
        "token": "invalid_token"
    })

    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower() or "expired" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_resend_verification_email(client: AsyncClient, db_session, test_user_unverified):
    """Test resending verification email."""
    # Get original verification details
    result = await db_session.execute(
        select(UnverifiedDetails).where(UnverifiedDetails.user_id == test_user_unverified.id)
    )
    original_details = result.scalars().first()
    original_token = original_details.verification_token

    # Request resend
    response = await client.post("/auth/resend-verification-email", json={
        "email": "unverified@example.com"
    })

    # Check response
    assert response.status_code == 200
    assert "message" in response.json()
    assert "verification email sent" in response.json()["message"].lower()

    # Verify verification details were updated
    result = await db_session.execute(
        select(UnverifiedDetails).where(UnverifiedDetails.user_id == test_user_unverified.id)
    )
    new_details = result.scalars().first()

    assert new_details.verification_token != original_token

@pytest.mark.asyncio
async def test_resend_verification_email_verified_user(client: AsyncClient, db_session, test_user_verified):
    """Test resending verification email for already verified user."""
    response = await client.post("/auth/resend-verification-email", json={
        "email": "emailtest@example.com"
    })

    assert response.status_code == 200
    assert "message" in response.json()
    assert "already verified" in response.json()["message"].lower()

@pytest.mark.asyncio
async def test_resend_verification_email_nonexistent_user(client: AsyncClient, db_session):
    """Test resending verification email for non-existent user."""
    response = await client.post("/auth/resend-verification-email", json={
        "email": "nonexistent@example.com"
    })

    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()