"""
Tests for password reset database actions.
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from database.postgress.actions.acc_recovery import (
    create_acc_recovery,
    get_acc_recovery_by_token,
    del_acc_recovery
)
from database.postgress.actions.user import create_user
from database.postgress.models import User, AccountRecovery

pytestmark = pytest.mark.functionality

@pytest.fixture
async def test_user(db_session):
    """Create a test user for password reset tests."""
    # Create a test user
    user_data = await create_user(
        db_session,
        username="resetuser",
        email="resetuser@example.com",
        password="TestPassword123",
        role_name="Young Person"
    )

    if user_data:
        user, _ = user_data
        # Verify user directly to avoid verification details complication
        result = await db_session.execute(
            select(User).where(User.id == user.id)
        )
        db_user = result.scalars().first()

        # Delete verification details if they exist
        if hasattr(db_user, 'verification_details') and db_user.verification_details:
            await db_session.delete(db_user.verification_details)
            await db_session.commit()
            await db_session.refresh(db_user)

        return db_user
    return None

@pytest.mark.asyncio
async def test_create_acc_recovery(db_session, test_user):
    """Test creating a password reset token."""
    # Create password reset
    reset = await create_acc_recovery(db_session, test_user)

    # Check reset was created correctly
    assert reset is not None
    assert reset.user_id == test_user.id
    assert reset.reset_token is not None
    assert reset.token_expires > datetime.utcnow()

    # Check association with user
    assert reset in test_user.account_recovery

@pytest.mark.asyncio
async def test_create_acc_recovery_existing(db_session, test_user):
    """Test creating a password reset when one already exists."""
    # Create first password reset
    first_reset = await create_acc_recovery(db_session, test_user)
    assert first_reset is not None

    # Get the token for comparison
    first_token = first_reset.reset_token

    # Create another password reset
    second_reset = await create_acc_recovery(db_session, test_user)
    assert second_reset is not None

    # Check that we got a new token
    assert second_reset.reset_token != first_token

    # Check that both resets exist in the database
    result = await db_session.execute(
        select(AccountRecovery).where(AccountRecovery.user_id == test_user.id)
    )
    resets = result.scalars().all()
    assert len(resets) == 2

@pytest.mark.asyncio
async def test_get_acc_recovery_by_token(db_session, test_user):
    """Test retrieving a password reset by token."""
    # Create password reset
    reset = await create_acc_recovery(db_session, test_user)
    assert reset is not None

    # Get reset by token
    retrieved_reset = await get_acc_recovery_by_token(db_session, reset.reset_token)

    # Check that we got the right reset
    assert retrieved_reset is not None
    assert retrieved_reset.id == reset.id
    assert retrieved_reset.reset_token == reset.reset_token
    assert retrieved_reset.user_id == test_user.id

    # Check eager loading of user
    assert hasattr(retrieved_reset, 'user')
    assert retrieved_reset.user is not None
    assert retrieved_reset.user.id == test_user.id

    # Try with non-existent token
    non_existent = await get_acc_recovery_by_token(db_session, "non_existent_token")
    assert non_existent is None

@pytest.mark.asyncio
async def test_del_acc_recovery(db_session, test_user):
    """Test deleting a password reset."""
    # Create password reset
    reset = await create_acc_recovery(db_session, test_user)
    assert reset is not None

    # Delete the reset
    result = await del_acc_recovery(db_session, reset)
    assert result is True

    # Check that it's gone from the database
    result = await db_session.execute(
        select(AccountRecovery).where(AccountRecovery.id == reset.id)
    )
    assert result.scalars().first() is None

    # Check that it's removed from the user's resets
    await db_session.refresh(test_user)
    assert reset not in test_user.account_recovery

@pytest.mark.asyncio
async def test_acc_recovery_purge_cron(db_session, test_user):
    """Test the password reset purge cron job."""
    # Import cron job class
    from database.postgress.actions.acc_recovery import AccountRecoveryPurgeCron

    # Create an expired password reset
    expired_reset = AccountRecovery(
        user_id=test_user.id,
        reset_token="expired_token",
        token_expires=datetime.utcnow() - timedelta(hours=1)
    )
    db_session.add(expired_reset)

    # Create a valid password reset
    valid_reset = AccountRecovery(
        user_id=test_user.id,
        reset_token="valid_token",
        token_expires=datetime.utcnow() + timedelta(hours=1)
    )
    db_session.add(valid_reset)

    await db_session.commit()

    # Create and run the cron job
    cron_job = AccountRecoveryPurgeCron()
    await cron_job.run(db_session)

    # Check that expired reset is gone
    result = await db_session.execute(
        select(AccountRecovery).where(AccountRecovery.reset_token == "expired_token")
    )
    assert result.scalars().first() is None

    # Check that valid reset is still there
    result = await db_session.execute(
        select(AccountRecovery).where(AccountRecovery.reset_token == "valid_token")
    )
    assert result.scalars().first() is not None