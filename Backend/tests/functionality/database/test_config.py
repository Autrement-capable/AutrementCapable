"""
Tests for database configuration.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database.postgress.config import postgress, getSession, Base

pytestmark = pytest.mark.functionality

@pytest.mark.asyncio
async def test_postgress_singleton():
    """Test that postgress is a singleton."""
    from database.postgress.config import Postgress

    # Create two instances of Postgress
    instance1 = Postgress()
    instance2 = Postgress()

    # Check they are the same object
    assert instance1 is instance2
    assert instance1 is postgress

@pytest.mark.asyncio
async def test_get_async_session():
    """Test getting an async session."""
    session = await getSession()

    try:
        # Check it's an AsyncSession
        assert isinstance(session, AsyncSession)
    finally:
        # Make sure to close the session
        await session.close()

@pytest.mark.asyncio
async def test_get_sync_session():
    """Test getting a sync session."""
    session = postgress.get_SyncSession()

    try:
        # Check it's a regular Session
        assert isinstance(session, Session)
    finally:
        # Make sure to close the session
        session.close()

@pytest.mark.asyncio
async def test_base_metadata():
    """Test base metadata configuration."""
    # Check Base has metadata
    assert hasattr(Base, 'metadata')

    # Check some expected tables
    table_names = [table.name for table in Base.metadata.tables.values()]
    expected_tables = ["users", "roles", "account_recovery", "unverified_details", "revoked_tokens"]

    for table in expected_tables:
        assert table in table_names

@pytest.mark.asyncio
async def test_session_context_manager():
    """Test using session as context manager."""
    async with postgress.Session() as session:
        # Check it's an AsyncSession
        assert isinstance(session, AsyncSession)

        # Try a simple query
        result = await session.execute("SELECT 1")
        value = result.scalar()
        assert value == 1

@pytest.mark.asyncio
async def test_engine_connection():
    """Test direct engine connection."""
    async with postgress.engine.connect() as conn:
        # Try a simple query
        result = await conn.execute("SELECT 1")
        value = result.scalar()
        assert value == 1

@pytest.mark.asyncio
async def test_async_engine_transaction():
    """Test engine transaction."""
    async with postgress.engine.begin() as conn:
        # Within a transaction
        result = await conn.execute("SELECT 1")
        value = result.scalar()
        assert value == 1
        # Transaction will be rolled back automatically since this is a test