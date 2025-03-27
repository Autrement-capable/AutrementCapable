"""
Tests for cron job functionality.
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.future import select

from server.cron_jobs.base_cron import CronJobRegistry
from database.postgress.models import AccountRecovery, RevokedToken, User, UnverifiedDetails
from database.postgress.actions.user import create_user
from database.postgress.actions.role import get_role_by_name, create_role

pytestmark = pytest.mark.functionality

@pytest.mark.asyncio
async def test_acc_recovery_purge_cron(db_session, init_test_data):
    """Test the password reset purge cron job."""
    # Create a test user if needed
    role = await get_role_by_name(db_session, "Young Person")
    if not role:
        role = await create_role(db_session, "Young Person", "Role for user", commit=True)

    user_result = await db_session.execute(
        select(User).where(User.username == "cronuser")
    )
    user = user_result.scalars().first()

    if not user:
        user_data = await create_user(
            db_session,
            username="cronuser",
            email="cronuser@example.com",
            password="Password123",
            role_name="Young Person"
        )
        user, _ = user_data

    # Create an expired password reset
    expired_reset = AccountRecovery(
        user_id=user.id,
        reset_token="expired_token",
        token_expires=datetime.utcnow() - timedelta(hours=1)
    )
    db_session.add(expired_reset)

    # Create a valid password reset
    valid_reset = AccountRecovery(
        user_id=user.id,
        reset_token="valid_token",
        token_expires=datetime.utcnow() + timedelta(hours=1)
    )
    db_session.add(valid_reset)

    await db_session.commit()

    # Get the cron job class and create an instance
    acc_recovery_purge_cron = None
    for job_cls in CronJobRegistry.get_registered_jobs():
        if job_cls.__name__ == "AccountRecoveryPurgeCron":
            acc_recovery_purge_cron = job_cls()
            break

    assert acc_recovery_purge_cron is not None

    # Run the cron job
    await acc_recovery_purge_cron.run(db_session)

    # Verify expired reset is deleted
    result = await db_session.execute(
        select(AccountRecovery).where(AccountRecovery.reset_token == "expired_token")
    )
    assert result.scalars().first() is None

    # Verify valid reset is still there
    result = await db_session.execute(
        select(AccountRecovery).where(AccountRecovery.reset_token == "valid_token")
    )
    assert result.scalars().first() is not None

@pytest.mark.asyncio
async def test_token_purge_cron(db_session):
    """Test the token purge cron job."""
    # Create expired token
    expired_token = RevokedToken(
        jti="expired_jti",
        date_revoked=datetime.utcnow() - timedelta(hours=2),
        data_expires=datetime.utcnow() - timedelta(hours=1),
        type="access"
    )
    db_session.add(expired_token)

    # Create valid token
    valid_token = RevokedToken(
        jti="valid_jti",
        date_revoked=datetime.utcnow(),
        data_expires=datetime.utcnow() + timedelta(hours=1),
        type="refresh"
    )
    db_session.add(valid_token)

    await db_session.commit()

    # Get the cron job class and create an instance
    token_purge_cron = None
    for job_cls in CronJobRegistry.get_registered_jobs():
        if job_cls.__name__ == "TokenPurgeCron":
            token_purge_cron = job_cls()
            break

    assert token_purge_cron is not None

    # Run the cron job
    await token_purge_cron.run(db_session)

    # Verify expired token is deleted
    result = await db_session.execute(
        select(RevokedToken).where(RevokedToken.jti == "expired_jti")
    )
    assert result.scalars().first() is None

    # Verify valid token is still there
    result = await db_session.execute(
        select(RevokedToken).where(RevokedToken.jti == "valid_jti")
    )
    assert result.scalars().first() is not None

@pytest.mark.asyncio
async def test_unverified_user_purge_cron(db_session, init_test_data):
    """Test the unverified user purge cron job."""
    # Create an expired unverified user
    result = await create_user(
        db_session,
        username="expireduser",
        email="expireduser@example.com",
        password="Password123",
        role_name="Young Person",
        commit=False  # Don't commit yet
    )
    assert result is not None
    expired_user, expired_details = result

    # Set the verification token to be expired
    expired_details.token_expires = datetime.utcnow() - timedelta(hours=1)
    db_session.add(expired_details)

    # Create a valid unverified user
    result = await create_user(
        db_session,
        username="validuser",
        email="validuser@example.com",
        password="Password123",
        role_name="Young Person"
    )
    assert result is not None
    valid_user, valid_details = result

    await db_session.commit()

    # Get the cron job class and create an instance
    unverified_user_purge_cron = None
    for job_cls in CronJobRegistry.get_registered_jobs():
        if job_cls.__name__ == "UnverifiedUserPurgeCron":
            unverified_user_purge_cron = job_cls()
            break

    assert unverified_user_purge_cron is not None

    # Run the cron job
    await unverified_user_purge_cron.run(db_session)

    # Verify expired user is deleted
    result = await db_session.execute(
        select(User).where(User.id == expired_user.id)
    )
    assert result.scalars().first() is None

    # Verify valid user is still there
    result = await db_session.execute(
        select(User).where(User.id == valid_user.id)
    )
    assert result.scalars().first() is not None
