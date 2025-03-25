"""
These tests should only run in development/test mode.
"""
import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.future import select

from database.postgress.models import Role, User

pytestmark = [pytest.mark.endpoint, pytest.mark.dev]

@pytest.fixture
async def auth_tokens(client: AsyncClient, db_session):
    """Create and return auth tokens from a test login."""
    # Create and verify a test user
    await client.post("/auth/register", json={
        "first_name": "Dev",
        "last_name": "Test",
        "phone_number": "5551234567",
        "address": "Test Address",
        "username": "devtestuser",
        "email": "devtest@example.com",
        "password": "Password123"
    })

    # Get verification token
    from database.postgress.models import UnverifiedDetails, User
    from sqlalchemy.orm import joinedload

    result = await db_session.execute(
        select(UnverifiedDetails)
        .options(joinedload(UnverifiedDetails.user))
        .where(UnverifiedDetails.user.has(User.email == "devtest@example.com"))
    )
    details = result.scalars().first()

    # Verify user
    verify_response = await client.get(f"/auth/verify?code={details.verification_token}")

    # Login to get tokens
    login_response = await client.post("/auth/login", json={
        "username_or_email": "devtest@example.com",
        "password": "Password123"
    })

    return login_response.json()

@pytest.mark.asyncio
async def test_test_access_token(client: AsyncClient, auth_tokens):
    """Test the access token test endpoint."""
    access_token = auth_tokens["access_token"]

    # Call test endpoint
    response = await client.get(
        "/dev/test_access_token",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Check response
    assert response.status_code == 200
    assert "msg" in response.json()
    assert response.json()["msg"] == "Access Token is valid!"
    assert "payload" in response.json()

    # Check payload contents
    payload = response.json()["payload"]
    assert "sub" in payload
    assert "role" in payload
    assert "jti" in payload

@pytest.mark.asyncio
async def test_test_refresh_token(client: AsyncClient, auth_tokens):
    """Test the refresh token test endpoint."""
    refresh_token = auth_tokens["refresh_token"]

    # Call test endpoint
    response = await client.get(
        "/dev/test_refresh_token",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )

    # Check response
    assert response.status_code == 200
    assert "msg" in response.json()
    assert response.json()["msg"] == "Refresh Token is valid!"
    assert "payload" in response.json()

    # Check payload contents
    payload = response.json()["payload"]
    assert "sub" in payload
    assert "role" in payload
    assert "jti" in payload

@pytest.mark.asyncio
async def test_all_tables(client: AsyncClient, auth_tokens):
    """Test the all-tables endpoint."""
    access_token = auth_tokens["access_token"]

    response = await client.get(
        "/dev/all-tables",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Check response
    assert response.status_code == 200
    assert "tables" in response.json()

    tables = response.json()["tables"]
    assert isinstance(tables, list)

    # Check for expected tables
    expected_tables = ["roles", "users", "password_resets", "unverified_details", "revoked_tokens"]
    for table in expected_tables:
        assert table in tables

@pytest.mark.asyncio
async def test_drop_table(client: AsyncClient, db_session, auth_tokens):
    """Test the drop-table endpoint (with careful restoration)."""
    access_token = auth_tokens["access_token"]

    # Create a test table specifically for dropping
    # We'll use a temporary role that won't affect the rest of tests
    test_role = Role(role_name="TestDropRole", description="Role to be dropped")
    db_session.add(test_role)
    await db_session.commit()

    # Verify role was created
    result = await db_session.execute(
        select(Role).where(Role.role_name == "TestDropRole")
    )
    assert result.scalars().first() is not None

    # Drop the table
    response = await client.get(
        "/dev/drop-table/roles",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Check response
    assert response.status_code == 200
    assert "message" in response.json()
    assert "roles dropped" in response.json()["message"]

    # Recreate the tables for cleanup
    # This is necessary because dropping tables affects the entire test suite
    from database.postgress.config import Base, postgress
    async with postgress.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Re-initialize roles
    from server.role_config.roles import init_roles
    await init_roles(db_session)
