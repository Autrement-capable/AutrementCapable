"""
Tests for role database actions.
"""
import pytest
from sqlalchemy.future import select

from database.postgress.actions.role import (
    create_role,
    get_role_by_name,
    get_role_by_id,
    get_all_roles,
    update_role,
    delete_role
)
from database.postgress.models import Role

pytestmark = pytest.mark.functionality

@pytest.mark.asyncio
async def test_create_role(db_session):
    """Test creating a role."""
    # Create a test role
    role = await create_role(
        db_session,
        name="Test Role",
        desc="A test role",
        commit=True,
        refresh=True
    )

    # Check role was created correctly
    assert role is not None
    assert role.role_name == "Test Role"
    assert role.description == "A test role"
    assert role.id is not None

    # Verify it's in the database
    result = await db_session.execute(
        select(Role).where(Role.role_name == "Test Role")
    )
    db_role = result.scalars().first()
    assert db_role is not None
    assert db_role.id == role.id

@pytest.mark.asyncio
async def test_create_duplicate_role(db_session):
    """Test creating a role with a duplicate name."""
    # Create the first role
    role1 = await create_role(db_session, "Duplicate Role", "First role")
    assert role1 is not None

    # Try to create another role with the same name
    role2 = await create_role(db_session, "Duplicate Role", "Second role")
    assert role2 is None  # Should fail due to integrity error

@pytest.mark.asyncio
async def test_get_role_by_name(db_session):
    """Test retrieving a role by name."""
    # Create a test role
    original = await create_role(db_session, "Get By Name Role", "Role to get by name")
    assert original is not None

    # Get role by name
    retrieved = await get_role_by_name(db_session, "Get By Name Role")

    # Check that we got the right role
    assert retrieved is not None
    assert retrieved.id == original.id
    assert retrieved.role_name == "Get By Name Role"
    assert retrieved.description == "Role to get by name"

    # Try with non-existent name
    non_existent = await get_role_by_name(db_session, "Non Existent Role")
    assert non_existent is None

@pytest.mark.asyncio
async def test_get_role_by_id(db_session):
    """Test retrieving a role by ID."""
    # Create a test role
    original = await create_role(db_session, "Get By ID Role", "Role to get by ID")
    assert original is not None

    # Get role by ID
    retrieved = await get_role_by_id(db_session, original.id)

    # Check that we got the right role
    assert retrieved is not None
    assert retrieved.id == original.id
    assert retrieved.role_name == "Get By ID Role"
    assert retrieved.description == "Role to get by ID"

    # Try with non-existent ID
    non_existent = await get_role_by_id(db_session, 9999)
    assert non_existent is None

@pytest.mark.asyncio
async def test_get_all_roles(db_session):
    """Test retrieving all roles."""
    # Create some test roles
    role1 = await create_role(db_session, "All Roles Test 1", "First test role")
    role2 = await create_role(db_session, "All Roles Test 2", "Second test role")
    role3 = await create_role(db_session, "All Roles Test 3", "Third test role")

    # Get all roles
    roles = await get_all_roles(db_session)

    # Check that we got all roles
    assert roles is not None
    assert isinstance(roles, list)

    # Check that our test roles are in the list
    role_names = [role.role_name for role in roles]
    assert "All Roles Test 1" in role_names
    assert "All Roles Test 2" in role_names
    assert "All Roles Test 3" in role_names

@pytest.mark.asyncio
async def test_update_role(db_session):
    """Test updating a role."""
    # Create a test role
    role = await create_role(db_session, "Update Role Test", "Original description")
    assert role is not None

    # Update the role
    role.description = "Updated description"
    updated = await update_role(db_session, role, commit=True, refresh=True)

    # Check that the role was updated
    assert updated is not None
    assert updated.id == role.id
    assert updated.role_name == "Update Role Test"
    assert updated.description == "Updated description"

    # Verify in the database
    result = await db_session.execute(
        select(Role).where(Role.id == role.id)
    )
    db_role = result.scalars().first()
    assert db_role.description == "Updated description"

@pytest.mark.asyncio
async def test_update_role_name_conflict(db_session):
    """Test updating a role name to an existing name."""
    # Create two test roles
    role1 = await create_role(db_session, "Update Conflict 1", "First role")
    role2 = await create_role(db_session, "Update Conflict 2", "Second role")

    # Try to update role2 to have the same name as role1
    role2.role_name = "Update Conflict 1"
    updated = await update_role(db_session, role2)

    # Should fail due to integrity error
    assert updated is None

    # Verify original name is unchanged
    result = await db_session.execute(
        select(Role).where(Role.id == role2.id)
    )
    db_role = result.scalars().first()
    assert db_role.role_name == "Update Conflict 2"

@pytest.mark.asyncio
async def test_delete_role(db_session):
    """Test deleting a role."""
    # Create a test role
    role = await create_role(db_session, "Delete Role Test", "Role to delete")
    assert role is not None

    # Delete the role
    result = await delete_role(db_session, role)
    assert result is True

    # Verify it's gone from the database
    result = await db_session.execute(
        select(Role).where(Role.id == role.id)
    )
    assert result.scalars().first() is None

@pytest.mark.asyncio
async def test_role_config_init_roles(db_session):
    """Test role initialization from config."""
    from server.role_config.roles import init_roles, roles

    # Clear existing roles first
    result = await db_session.execute(select(Role))
    existing_roles = result.scalars().all()
    for role in existing_roles:
        await db_session.delete(role)
    await db_session.commit()

    # Initialize roles
    success = await init_roles(db_session)
    assert success is True

    # Check that all roles from config are in the database
    result = await db_session.execute(select(Role))
    db_roles = result.scalars().all()

    assert len(db_roles) == len(roles)

    db_role_names = [role.role_name for role in db_roles]
    for role_name in roles.keys():
        assert role_name in db_role_names

    # Run init again to test skipping existing roles
    success = await init_roles(db_session)
    assert success is True

    # Count should be the same
    result = await db_session.execute(select(Role).order_by(Role.id))
    db_roles_after = result.scalars().all()
    assert len(db_roles_after) == len(roles)