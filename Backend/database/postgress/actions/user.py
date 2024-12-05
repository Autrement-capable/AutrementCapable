from database.postgress.models.user import User
from database.postgress.actions.role import get_role_by_name
from utils.password import verify_password, hash_password

from sqlalchemy.orm import joinedload, selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime

# Create functions

async def create_user(session: AsyncSession, username: str, email: str, password: str, first_name: str = None, last_name: str = None, role_name: str = "Young Person", phone_number: str = None, address: str = None, hashed=False, commit=True, fresh=False) -> User:
    """ Create a user in the database via standard registration (Password) Async

    Args:
        session (Session): The database session
        email (str): The user's email
        username (str): The user's username
        password (str): The user's password
        first_name (str, optional): The user's first name. Defaults to None.
        last_name (str, optional): The user's last name. Defaults to None.
        role_name (str, optional): The user's role. Defaults to "Young Person".
        phone_number (str, optional): The user's phone number. Defaults to None.
        address (str, optional): The user's address. Defaults to None.
        hashed (bool, optional): Whether the password given is hashed. Defaults to False.
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        fresh (bool, optional): Whether to refresh the user object from DB(usefull if you want to manipulate it). Defaults to False."""
    try:
        if not hashed:
            password = hash_password(password)
        role_id = (await get_role_by_name(session, role_name)).role_id
        if not role_id:
            print("Role not found")
            return None
        user = User(username=username, email=email, password_hash=password, role_id=role_id, first_name=first_name, last_name=last_name, phone_number=phone_number, address=address)
        session.add(user)
        if commit:
            await session.commit()
        if fresh:
            await session.refresh(user)
        return user
    except IntegrityError:
        await session.rollback()
        print("A user with this email already exists.")
        return None
    except OperationalError:
        await session.rollback()
        print("There was an issue with the database operation.")
        return None
    except TypeError as e:
        await session.rollback()
        print(f"Type error: {e}")
        return None

# Oauth and passkey to be implemented

# Get functions

async def get_user_by_email(session: AsyncSession, email: str, lazy=True) -> User:
    """ Get a user by email async.
    Args:
        session (Session): The database session.
        email (str): The user's email.
        lazy (bool, optional): Whether to load the email object lazily. Defaults to True.
    """
    query = select(User).where(User.email == email)
    result = await session.exec(query)
    user = result.first()

    if not lazy:
        await session.refresh(user)  # Ensure all attributes are loaded

    return user

async def get_user_by_username(session: AsyncSession, username: str) -> User:
    """ Get a user by username async """
    result = await session.exec(select(User).where(User.username == username))
    return result.first()

async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    """ Get a user by id async """
    result = await session.exec(select(User).where(User.user_id == user_id))
    return result.first()

async def get_all_usernames(session: AsyncSession) -> list[str]:
    """ Get all usernames async """
    result = await session.exec(select(User.username))
    return result.all()

async def is_username_taken(session: AsyncSession, username: str) -> bool:
    """ Check if a username is taken async
    Returns:
        True if the username is taken, False otherwise
    """
    result = await session.execute(
        select(User).where(User.username == username)
    )  # Execute the query
    user = result.first()  # Fetch the first result (already scalar)
    return user is not None

async def login_user(session: AsyncSession, password: str, username_email: str, hashed=False) -> User:
    """ Login a user async

    Args:
        session (Session): The database session
        password (str): The user's password
        username_email (str): The user's username or email
        hashed (bool, optional): Whether the password given is hashed. Defaults to False.

    Returns:
        User: The user object if successful, None otherwise"""
    query = select(User).where((User.username == username_email) | (User.email == username_email))
    result = await session.exec(query)
    user = result.first()

    if not user:
        return None

    if (not hashed and not verify_password(password, user.password_hash)) or \
       (hashed and password != user.password_hash):
        return None

    return user

# Update functions
async def update_user(session: AsyncSession, user: User, commit=True, fresh=False) -> User:
    """ Update a user in the database async

    Args:
        session (Session): The database session
        user (User): The user object
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        fresh (bool, optional): Whether to refresh the user object from DB(usefull if you want to manipulate it). Defaults to False.

        Returns:
            User: The updated user object if successful, None otherwise"""
    try:
        session.add(user)
        if commit:
            await session.commit()
        if fresh:
            await session.refresh(user)
        return user
    except IntegrityError:
        await session.rollback()
        print("A user with this email already exists.")
        return None
    except OperationalError:
        await session.rollback()
        print("There was an issue with the database operation.")
        return None
    except TypeError as e:
        await session.rollback()
        print(f"Type error: {e}")
        return None

# Delete functions
async def delete_user(session: AsyncSession, user: User, commit=True) -> bool:
    """ Delete a user from the database async

    Args:
        session (Session): The database session
        user (User): The user object
        commit (bool, optional): Whether to commit the transaction. Defaults to True.

        Returns:
            bool: True if successful, False otherwise"""
    try:
        session.delete(user)
        if commit:
            await session.commit()
        return True
    except IntegrityError:
        await session.rollback()
        print("A user with this email already exists.")
        return False
    except OperationalError:
        await session.rollback()
        print("There was an issue with the database operation.")
        return False
    except TypeError as e:
        await session.rollback()
        print(f"Type error: {e}")
        return False
    except Exception as e:
        await session.rollback()
        print(f"Error: {e}")
        return False