import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from database.postgress.models import User, UnverifiedDetails

pytestmark = pytest.mark.endpoint

@pytest.mark.asyncio
async def test_register_endpoint_success(client: AsyncClient, db_session, init_test_data):
    """Test successful user registration."""
    # Register a test user
    response = await client.post("/auth/register", json={
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "1234567890",
        "address": "123 Test Street",
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securePassword123"
    })
    
    # Assert response
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Verification email sent"
    
    # Verify user was created in DB
    result = await db_session.execute(
        select(User).where(User.email == "testuser@example.com")
    )
    user = result.scalars().first()
    assert user is not None
    assert user.username == "testuser"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    
    # Verify unverified details were created
    result = await db_session.execute(
        select(UnverifiedDetails).where(UnverifiedDetails.user_id == user.id)
    )
    details = result.scalars().first()
    assert details is not None
    assert details.verification_token is not None

@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient, db_session):
    """Test registration with duplicate username."""
    # Try to register with the same username
    response = await client.post("/auth/register", json={
        "first_name": "Another",
        "last_name": "User",
        "phone_number": "9876543210",
        "address": "456 Test Avenue",
        "username": "testuser",  # Same username as previous test
        "email": "another@example.com", 
        "password": "securePassword123"
    })

    # Assert failure response
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "detail" in response.json()
    assert response.json()["detail"] == "Username already taken"

@pytest.mark.asyncio
async def test_login_unverified_user(client: AsyncClient, db_session):
    """Test login with unverified user."""
    # Attempt login with unverified account
    response = await client.post("/auth/login", json={
        "username_or_email": "testuser@example.com",
        "password": "securePassword123"
    })

    # Assert proper error response
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "detail" in response.json()
    assert response.json()["detail"] == "Account not verified"

@pytest.mark.asyncio
async def test_verify_user(client: AsyncClient, db_session):
    """Test user verification process."""
    # Get verification token from DB
    result = await db_session.execute(
        select(UnverifiedDetails)
        .options(joinedload(UnverifiedDetails.user))
        .where(UnverifiedDetails.user.has(User.email == "testuser@example.com"))
    )
    details = result.scalars().first()
    assert details is not None

    # Call verification endpoint
    response = await client.get(f"/auth/verify?code={details.verification_token}")

    # Assert successful verification
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

    # Check verification details were removed
    result = await db_session.execute(
        select(UnverifiedDetails).where(UnverifiedDetails.user_id == details.user_id)
    )
    assert result.scalars().first() is None

@pytest.mark.asyncio
async def test_login_verified_user(client: AsyncClient, db_session):
    """Test login with verified user."""
    # Login with now-verified user
    response = await client.post("/auth/login", json={
        "username_or_email": "testuser@example.com",
        "password": "securePassword123"
    })

    # Assert successful login
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, db_session):
    """Test login with invalid credentials."""
    # Login with wrong password
    response = await client.post("/auth/login", json={
        "username_or_email": "testuser@example.com",
        "password": "wrongPassword"
    })

    # Assert authentication failure
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Login with non-existent user
    response = await client.post("/auth/login", json={
        "username_or_email": "nonexistent@example.com",
        "password": "anyPassword"
    })

    # Assert authentication failure
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_check_username_endpoint(client: AsyncClient, db_session):
    """Test the check_username endpoint."""
    # Check existing username
    response = await client.get("/auth/check_username?username=testuser")

    assert response.status_code == 200
    data = response.json()
    assert "is_available" in data
    assert data["is_available"] is False
    assert "usernames" in data
    assert len(data["usernames"]) > 0

    # Check available username
    response = await client.get("/auth/check_username?username=newusername")

    assert response.status_code == 200
    data = response.json()
    assert data["is_available"] is True
    assert data["usernames"] == ["newusername"]