from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from datetime import datetime
from database.postgress.models import User, PasskeyCredential, Role
from database.postgress.actions.role import get_role_by_name
import base64
import secrets
import json
import asyncio

async def create_passkey_user(
    session: AsyncSession, 
    first_name: str, 
    last_name: str = None, 
    age: int = None,
    role_name: str = "Young Person", 
    commit: bool = True, 
    fresh: bool = True
) -> User:
    """
    Create a new user with minimal information for passkey registration.

    Args:
        session (AsyncSession): Database session
        first_name (str): User's first name
        last_name (str): User's last name (optional)
        age (int): User's age (optional)
        role_name (str): Role name (defaults to "Young Person")
        commit (bool): Whether to commit the transaction
        fresh (bool): Whether to refresh the user from DB

    Returns:
        User: The created user or None if there was an error
    """
    try:
        role = await get_role_by_name(session, role_name)
        if not role:
            print("Role not found")
            return None

        # Generate a random username to use as a placeholder
        random_suffix = secrets.token_hex(8)
        temp_username = f"user_{random_suffix}"

        user = User(
            first_name=first_name,
            last_name=last_name,
            age=age,
            username=temp_username,  # Temporary username that will be updated later
            is_passkey=True,
            role_id=role.id,
            role=role,
            onboarding_complete=False  # User has not completed onboarding yet
        )

        session.add(user)
        await session.commit()

        if fresh:
            await session.refresh(user)

        return user
    except IntegrityError:
        await session.rollback()
        print("Integration error creating passkey user")
        return None
    except OperationalError as e:
        await session.rollback()
        print(f"Database operation error: {e}")
        return None
    except Exception as e:
        await session.rollback()
        print(f"Unexpected error creating passkey user: {e}")
        return None

async def register_passkey_credential(
    session: AsyncSession,
    user: User,
    credential_id: str,
    public_key: bytes,
    device_type: str = None,
    commit: bool = True,
    fresh: bool = True
) -> PasskeyCredential:
    """
    Register a new passkey credential for a user.

    Args:
        session (AsyncSession): Database session
        user (User): The user to register the credential for
        credential_id (str): WebAuthn credential ID
        public_key (bytes): WebAuthn public key
        device_type (str): Type of device (optional)
        commit (bool): Whether to commit the transaction
        fresh (bool): Whether to refresh the credential from DB

    Returns:
        PasskeyCredential: The registered credential or None if there was an error
    """
    try:
        credential = PasskeyCredential(
            user_id=user.id,
            credential_id=credential_id,
            public_key=public_key,
            device_type=device_type,
            sign_count=0,
            date_created=datetime.utcnow(),
            last_used=datetime.utcnow()
        )

        session.add(credential)

        if commit:
            await session.commit()

        if fresh:
            await session.refresh(credential)

        return credential
    except IntegrityError:
        await session.rollback()
        print("A credential with this ID already exists")
        return None
    except Exception as e:
        await session.rollback()
        print(f"Error registering passkey credential: {e}")
        return None

async def get_user_by_credential_id(session: AsyncSession, credential_id: str) -> User:
    """
    Get a user by their credential ID.

    Args:
        session (AsyncSession): Database session
        credential_id (str): WebAuthn credential ID

    Returns:
        User: The user associated with the credential or None if not found
    """
    try:
        # Query for the credential and eager load the user
        statement = (
            select(PasskeyCredential)
            .where(PasskeyCredential.credential_id == credential_id)
            .options(joinedload(PasskeyCredential.user))
        )
        result = await session.execute(statement)
        credential = result.scalars().first()

        if not credential:
            return None

        # Update the last_used timestamp
        credential.last_used = datetime.utcnow()
        await session.commit()

        return credential.user
    except Exception as e:
        print(f"Error getting user by credential ID: {e}")
        return None

async def get_credential_by_id(session: AsyncSession, credential_id: str) -> PasskeyCredential:
    """
    Get a credential by its ID.

    Args:
        session (AsyncSession): Database session
        credential_id (str): WebAuthn credential ID

    Returns:
        PasskeyCredential: The credential or None if not found
    """
    try:
        statement = select(PasskeyCredential).where(PasskeyCredential.credential_id == credential_id)
        result = await session.execute(statement)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting credential by ID: {e}")
        return None

async def update_credential_counter(
    session: AsyncSession,
    credential: PasskeyCredential,
    new_sign_count: int,
    commit: bool = True
) -> bool:
    """
    Update the sign counter for a credential.

    Args:
        session (AsyncSession): Database session
        credential (PasskeyCredential): The credential to update
        new_sign_count (int): The new sign count
        commit (bool): Whether to commit the transaction

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        credential.sign_count = new_sign_count
        credential.last_used = datetime.utcnow()

        if commit:
            await session.commit()

        return True
    except Exception as e:
        await session.rollback()
        print(f"Error updating credential counter: {e}")
        return False

async def get_passkey_credentials_for_user(session: AsyncSession, user_id: int) -> list[PasskeyCredential]:
    """
    Get all passkey credentials for a user.

    Args:
        session (AsyncSession): Database session
        user_id (int): User ID

    Returns:
        list[PasskeyCredential]: List of credentials
    """
    try:
        statement = select(PasskeyCredential).where(PasskeyCredential.user_id == user_id)
        result = await session.execute(statement)
        return result.scalars().all()
    except Exception as e:
        print(f"Error getting passkey credentials for user: {e}")
        return []

async def delete_credential(session: AsyncSession, credential: PasskeyCredential, commit: bool = True) -> bool:
    """
    Delete a passkey credential.

    Args:
        session (AsyncSession): Database session
        credential (PasskeyCredential): The credential to delete
        commit (bool): Whether to commit the transaction

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        await session.delete(credential)

        if commit:
            await session.commit()

        return True
    except Exception as e:
        await session.rollback()
        print(f"Error deleting credential: {e}")
        return False

async def update_user_profile(
    session: AsyncSession,
    user: User,
    username: str = None,
    email: str = None,
    phone_number: str = None,
    address: str = None,
    onboarding_complete: bool = None,
    commit: bool = True,
    fresh: bool = True
) -> User:
    """
    Update a user's profile information.

    Args:
        session (AsyncSession): Database session
        user (User): The user to update
        username (str): New username (optional)
        email (str): New email (optional)
        phone_number (str): New phone number (optional)
        address (str): New address (optional)
        onboarding_complete (bool): Whether onboarding is complete (optional)
        commit (bool): Whether to commit the transaction
        fresh (bool): Whether to refresh the user from DB

    Returns:
        User: The updated user or None if there was an error
    """
    try:
        if username is not None:
            user.username = username

        if email is not None:
            user.email = email

        if phone_number is not None:
            user.phone_number = phone_number

        if address is not None:
            user.address = address

        if onboarding_complete is not None:
            user.onboarding_complete = onboarding_complete

        session.add(user)

        if commit:
            await session.commit()

        if fresh:
            await session.refresh(user)

        return user
    except IntegrityError:
        await session.rollback()
        print("A user with this username or email already exists")
        return None
    except Exception as e:
        await session.rollback()
        print(f"Error updating user profile: {e}")
        return None

# async def create_acc_recovery(session: AsyncSession, user: User):
    