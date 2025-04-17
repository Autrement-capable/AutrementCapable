from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime
from database.postgress.models import Role

# Create functions

async def create_role(session: AsyncSession, name: str, desc: str, commit=True, refresh=False) -> Role:
    """ Create a role in the database asynchronously

    Args:
        session (AsyncSession): The database session
        name (str): The role's name
        desc (str): The role's description
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        refresh (bool, optional): Whether to refresh the role object from DB. Defaults to False.
    """
    try:
        role = Role(role_name=name, description=desc)
        session.add(role)
        if commit:
            await session.commit()
        if refresh:
            await session.refresh(role)
        return role
    except IntegrityError:
        await session.rollback()
        print("Role already exists.")
        return None
    except OperationalError:
        await session.rollback()
        print("Database operation failed.")
        return None

# Get functions

async def get_role_by_name(session: AsyncSession, name: str) -> Role | None:
    """ Get a role from the database by name asynchronously """
    statement = select(Role).where(Role.role_name == name)
    result = await session.execute(statement)
    return result.scalars().first()

async def get_role_by_id(session: AsyncSession, role_id: int) -> Role | None:
    """ Get a role from the database by ID asynchronously """
    statement = select(Role).where(Role.id == role_id)
    result = await session.execute(statement)
    return result.scalars().first()

async def get_all_roles(session: AsyncSession) -> list[Role]:
    """ Get all roles from the database asynchronously """
    statement = select(Role)
    result = await session.execute(statement)
    return result.scalars().all()

# Update functions

async def update_role(session: AsyncSession, role: Role, commit=True, refresh=False) -> Role:
    """ Update a role in the database asynchronously

    Args:
        session (AsyncSession): The database session
        role (Role): The role object
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        refresh (bool, optional): Whether to refresh the role object from DB. Defaults to False.
    """
    try:
        session.add(role)
        if commit:
            await session.commit()
        if refresh:
            await session.refresh(role)
        return role
    except IntegrityError:
        await session.rollback()
        print("A role with this name already exists.")
        return None
    except OperationalError:
        await session.rollback()
        print("There was an issue with the database operation.")
        return None

# Delete functions

async def delete_role(session: AsyncSession, role: Role, commit=True) -> bool:
    """ Delete a role from the database asynchronously

    Args:
        session (AsyncSession): The database session
        role (Role): The role object
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
    """
    try:
        await session.delete(role)
        if commit:
            await session.commit()
        return True
    except Exception:
        await session.rollback()
        print("Failed to delete the role.")
        return False
