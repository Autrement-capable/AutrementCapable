"""
Tests for user database actions.
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from database.postgress.actions.user import (
    create_user,
    get_user_by_email,
    verify_user,
    login_user,
    get_available_usernames,
    update_ver_details,
    del_uvf_user
)
from database.postgress.models import User, UnverifiedDetails

pytestmark = pytest.mark.functionality

@pytest.mark.asyncio
async def test_create_user(db_session, init_test_data):
    """Test user creation functionality."""
    # Create a test user
    result = await create_user(
        db_session,
        username="functionuser",
        email="functionuser@example.com",
        password="TestPassword123",
        first_name="Function",
        last_name="User",
        role_name="Young Person"
    )

    assert result is not None
    user, details = result

    # Verify user properties
    assert user.username == "functionuser"
    assert user.email == "functionuser@example.com"
    assert user.first_name == "Function"
    assert user.last_name == "User"
    assert user.role.role_name == "Young Person"
    assert user.password_hash is not None
    assert user.password_hash != "TestPassword123"  # Should be hashed

    # Verify unverified details
    assert details.user_id == user.id
    assert details.verification_token is not None
    assert details.token_expires > datetime.utcnow()

@pytest.mark.asyncio
async def test_create_user_duplicate(db_session):
    """Test creating a user with duplicate username or email."""
    # Try to create user with same email
    result = await create_user(
        db_session,
        username="anotherfunctionuser",
        email="functionuser@example.com",  # Same email as previous test
        password="TestPassword123"
    )

    assert result is None

    # Try to create user with same username
    result = await create_user(
        db_session,
        username="functionuser",  # Same username as previous test
        email="different@example.com",
        password="TestPassword123"
    )

    assert result is None

@pytest.mark.asyncio
async def test_get_user_by_email(db_session):
    """Test retrieving a user by email."""
    # Get existing user
    user = await get_user_by_email(db_session, "functionuser@example.com")

    assert user is not None
    assert user.email == "functionuser@example.com"
    assert user.username == "functionuser"

    # Try with non-existent email
    user = await get_user_by_email(db_session, "nonexistent@example.com")
    assert user is None

    # Test eager loading
    user = await get_user_by_email(db_session, "functionuser@example.com", load_type="eager")
    assert user is not None
    assert hasattr(user, "verification_details")
    assert hasattr(user, "password_resets")

@pytest.mark.asyncio
async def test_verify_user(db_session):
    """Test user verification."""
    # Get unverified details
    result = await db_session.execute(
        select(UnverifiedDetails)
        .options(joinedload(UnverifiedDetails.user))
        .where(UnverifiedDetails.user.has(User.email == "functionuser@example.com"))
    )
    details = result.scalars().first()
    assert details is not None

    # Verify user
    user = await verify_user(db_session, details.verification_token)

    assert user is not None
    assert user.id == details.user_id

    # Check that verification details are removed
    result = await db_session.execute(
        select(UnverifiedDetails).where(UnverifiedDetails.user_id == user.id)
    )
    assert result.scalars().first() is None

    # Try with invalid token
    user = await verify_user(db_session, "invalid_token")
    assert user is None

    # Try with expired token
    # First create a new user
    new_user_data = await create_user(
        db_session,
        username="expireduser",
        email="expired@example.com",
        password="TestPassword123"
    )
    assert new_user_data is not None
    new_user, new_details = new_user_data

    # Manually set token to expired
    new_details.token_expires = datetime.utcnow() - timedelta(hours=1)
    db_session.add(new_details)
    await db_session.commit()

    # Try to verify with expired token
    user = await verify_user(db_session, new_details.verification_token)
    assert user is None

@pytest.mark.asyncio
async def test_login_user(db_session):
    """Test user login."""
    # Login with correct credentials
    user = await login_user(db_session, "TestPassword123", "functionuser@example.com")

    assert user is not None
    assert user.email == "functionuser@example.com"

    # Login with correct credentials using username
    user = await login_user(db_session, "TestPassword123", "functionuser")

    assert user is not None
    assert user.username == "functionuser"

    # Login with incorrect password
    user = await login_user(db_session, "WrongPassword", "functionuser@example.com")
    assert user is None

    # Login with non-existent user
    user = await login_user(db_session, "TestPassword123", "nonexistent@example.com")
    assert user is None

@pytest.mark.asyncio
async def test_get_available_usernames(db_session):
    """Test checking for available usernames."""
    # Check available username
    is_available, suggestions = await get_available_usernames(db_session, "newusername")

    assert is_available is True
    assert suggestions == ["newusername"]

    # Check taken username
    is_available, suggestions = await get_available_usernames(db_session, "functionuser")

    assert is_available is False
    assert len(suggestions) == 3  # Default is 3 suggestions
    assert all(suggestion != "functionuser" for suggestion in suggestions)

@pytest.mark.asyncio
async def test_update_ver_details(db_session):
    """Test updating verification details."""
    # Create a new user for this test
    user_data = await create_user(
        db_session,
        username="updateuser",
        email="updateuser@example.com",
        password="TestPassword123"
    )
    assert user_data is not None
    user, details = user_data

    # Store original token
    original_token = details.verification_token
    original_expires = details.token_expires

    # Update verification details
    updated_details = await update_ver_details(db_session, user)

    assert updated_details is not None
    assert updated_details.verification_token != original_token
    assert updated_details.token_expires != original_expires
    assert updated_details.token_expires > datetime.utcnow()

@pytest.mark.asyncio
async def test_del_uvf_user(db_session):
    """Test deleting an unverified user."""
    # Create a user to delete
    user_data = await create_user(
        db_session,
        username="deleteuser",
        email="deleteuser@example.com",
        password="TestPassword123"
    )
    assert user_data is not None
    user, _ = user_data

    # Delete the user
    result = await del_uvf_user(db_session, user)

    assert result is True

    # Verify user is deleted
    result = await db_session.execute(
        select(User).where(User.id == user.id)
    )
    assert result.scalars().first() is None