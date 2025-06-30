import asyncio
from typing import Optional, Literal
from datetime import datetime
import yaml

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from faker import Faker
from pydantic import BaseModel

from ..models import User, UnverifiedDetails, UserDetail, UserAvatarInfo
from ..engine import postgress
from .role import get_role_by_name
from ....services.auth.password import verify_password, hash_password
from ....services.auth.verification import generate_verification_code, generate_random_suffix
from ....services.scheduler.base_cron import register_cron_job, BaseCronJob
from ....utils.config_helpers import get_property
from ....core.config import Config

try:
    email_verification_code_duration = Config.get_property(None, "verify", ["email_verification_code_duration"])["email_verification_code_duration"]
except Exception as e: # if the config file is not found
    print(f"Error loading config: {e}")
    email_verification_code_duration = 900
# is_config_loaded = False

# # Cron job functions
@register_cron_job("UnverifiedUserPurgeCron")
class UnverifiedUserPurgeCron(BaseCronJob):
    """Cron job to delete expired unverified users from the database."""
    def __init__(self):
        super().__init__("UnverifiedUserPurgeCron", "verify", ["email_ver_purge_interval"])

    async def run(self, session: AsyncSession):
        """ Delete expired unverified users from the database."""
        try:
            # Select UnverifiedDetails and eagerly load the related User
            statement = (
                select(UnverifiedDetails)
                .where(UnverifiedDetails.token_expires < datetime.utcnow())
                .options(joinedload(UnverifiedDetails.user))  # Eager loading
            )
            result = await session.execute(statement)
            details: list[UnverifiedDetails] = result.scalars().all()

            for detail in details:
                if detail.user:  # Since it's eagerly loaded, this avoids an extra query
                    await session.delete(detail.user)

            await session.commit()
        except Exception as e:
            print(f"Error deleting expired unverified users: {e}")
            await session.rollback()

async def create_user(session: AsyncSession, username: str, email: str, password: str,
                     first_name: str = None, last_name: str = None,
                     role_name: str = "Young Person", phone_number: str = None,
                     address: str = None, hashed=False, commit=True, fresh=True) -> tuple[User, UnverifiedDetails] | None:
    """Create a user with traditional login in the database asynchronously

    Args:
        session (AsyncSession): The database session
        username (str): The user's username
        email (str): The user's email
        password (str): The user's password
        first_name (str, optional): The user's first name. Defaults to None.
        last_name (str, optional): The user's last name. Defaults to None.
        role_name (str, optional): The user's role. Defaults to "Young Person".
        phone_number (str, optional): The user's phone number. Defaults to None.
        address (str, optional): The user's address. Defaults to None.
        hashed (bool, optional): Whether the password is already hashed. Defaults to False.
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        fresh (bool, optional): Whether to return a fresh object. Defaults to True.

    Returns:
        tuple[User, UnverifiedDetails] | None: A tuple containing the created user and unverified details if successful, None otherwise
    """
    try:
        if not hashed:
            password = hash_password(password)

        role = await get_role_by_name(session, role_name)
        if not role:
            print("Role not found")
            return None

        # Create base user
        user = User(
            username=username,
            is_passkey=False,  # This is a traditional login user
            role_id=role.id,
            role=role
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        # Create verification token
        verification_token, expiration = generate_verification_code(email, email_verification_code_duration)

        # Create user detail with email/password
        user_detail = UserDetail(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            email=email,
            password_hash=password
        )
        session.add(user_detail)
        await session.commit()
        await session.refresh(user_detail)

        # Create unverified details linked to user_detail
        unverified_details = UnverifiedDetails(
            user_detail_id=user_detail.id,
            verification_token=verification_token,
            token_expires=expiration
        )
        session.add(unverified_details)

        if commit:
            await session.commit()

        if fresh:
            await asyncio.gather(
                session.refresh(user), 
                session.refresh(user_detail),
                session.refresh(unverified_details)
            )

        return user, unverified_details
    except IntegrityError:
        await session.rollback()
        print("A user with this email or username already exists.")
        return None
    except Exception as e:
        await session.rollback()
        print(f"Error creating user: {e}")
        return None

async def get_user_by_email(session: AsyncSession, email: str, load_type: Literal["lazy", "eager"] = "lazy") -> User | None:
    """ Get a user by their email asynchronously

    Args:
        session (AsyncSession): The database session
        email (str): The user's email
        load_type (Literal["lazy", "eager"], optional): The type of loading to use. Defaults to "lazy".

    Returns:
        User | None: The user object if found, None otherwise
    """
    if load_type == "lazy":
        statement = select(User).where(User.email == email)
    elif load_type == "eager":
        statement = (select(User)
        .where(User.email == email)
        .options(joinedload(User.account_recovery), joinedload(User.verification_details)))
    else:
        raise ValueError("Invalid load type")

    result = await session.execute(statement)
    result = result.scalars().first()
    if not result:
        print("User not found")
        return None
    return result

async def get_user_by_id(session: AsyncSession, user_id: int, load_type: Literal["lazy", "eager"] = "lazy") -> User | None:
    """ Get a user by their ID asynchronously

    Args:
        session (AsyncSession): The database session
        user_id (int): The user's ID
        load_type (Literal["lazy", "eager"], optional): The type of loading to use. Defaults to "lazy".

    Returns:
        User | None: The user object if found, None otherwise
    """
    if load_type == "lazy":
        statement = select(User).where(User.id == user_id)
    elif load_type == "eager":
        statement = (select(User)
        .where(User.id == user_id)
        .options(joinedload(User.account_recovery), joinedload(User.verification_details), 
                 joinedload(User.passkey_credentials)))
    else:
        raise ValueError("Invalid load type")

    result = await session.execute(statement)
    result = result.scalars().first()
    if not result:
        print("User not found")
        return None
    return result

async def verify_user(session: AsyncSession, verification_code: str, commit=True, fresh=True) -> User:
    """Verify a user using their verification code.

    Args:
        session (AsyncSession): The database session
        verification_code (str): The verification code
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        fresh (bool, optional): Whether to return a fresh object. Defaults to True.
    Returns:
        User | None: The user object if successful, None otherwise
    """
    statement = (
        select(UnverifiedDetails)
        .where(UnverifiedDetails.verification_token == verification_code.strip())
        .options(joinedload(UnverifiedDetails.user_detail))
    )
    result = await session.execute(statement)
    unverified_details = result.scalars().first()

    if not unverified_details:
        print("Verification details not found")
        return None

    if unverified_details.token_expires < datetime.utcnow():
        print("Token expired")
        return None

    user_detail = unverified_details.user_detail
    if not user_detail:
        print("User detail not found")
        return None

    # Get the user from user_detail
    statement = select(User).where(User.id == user_detail.user_id)
    result = await session.execute(statement)
    user = result.scalars().first()

    if user:
        await session.delete(unverified_details)
        if commit:
            await session.commit()
        if fresh:
            await session.refresh(user)

    return user

async def del_uvf_user(session: AsyncSession, user: User, commit=True) -> bool:
    """ Delete a user from the database asynchronously

    Args:
        session (AsyncSession): The database session
        user (User): The user object
        commit (bool, optional): Whether to commit the transaction. Defaults to True.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        await session.delete(user)
        if commit:
            await session.commit()
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        await session.rollback()
        return False

async def login_user(session: AsyncSession, password: str, username_or_email: str) -> User | None:
    """Login a user asynchronously with traditional credentials

    Args:
        session (AsyncSession): The database session
        password (str): The user's password
        username_or_email (str): The user's username or email
    Returns:
        User | None: The user object if successful, None otherwise
    """
    # First try username lookup
    statement = select(User).where(User.username == username_or_email)
    result = await session.execute(statement)
    user = result.scalars().first()

    if not user:
        # Try email lookup in UserDetail
        statement = (
            select(User)
            .join(UserDetail, User.id == UserDetail.user_id)
            .where(UserDetail.email == username_or_email)
        )
        result = await session.execute(statement)
        user = result.scalars().first()

    if not user:
        return None

    # Get user details to check password
    statement = select(UserDetail).where(UserDetail.user_id == user.id)
    result = await session.execute(statement)
    user_detail = result.scalars().first()

    if not user_detail or not user_detail.password_hash:
        return None

    if not verify_password(password, user_detail.password_hash):
        return None

    # Update last login timestamp
    user.last_login = datetime.utcnow()
    await session.commit()

    return user

fake = Faker()

async def get_available_usernames(session: AsyncSession, username: str, num_similars=3) -> tuple[bool, list[str]]:
    """ Check if a username is available in the database asynchronously.
        If taken, return a list of similar available usernames.

    Args:
        session (AsyncSession): The database session.
        username (str): The desired username.
        num_similars (int, optional): Number of alternative usernames to suggest. Defaults to 3.

    Returns:
        tuple[bool, list[str]]: A tuple containing a boolean indicating if the username is available
        and a list of suggested usernames if the username is taken.
    """
    # Check if username exists
    statement = select(User.username).where(User.username == username)
    result = await session.execute(statement)
    taken_usernames = set(result.scalars().all())

    if username not in taken_usernames:
        return True, [username]  # Username is available

    if num_similars < 1:
        return False, []  # No suggestions needed

    suggestions = set()
    attempt_size = num_similars + 5  # Generate a few extra usernames

    # FIY: this has the unlikely possibility of generating the same username multiple times and that
    # username being taken, but the chances are very low
    while len(suggestions) < num_similars:
        generated_usernames = {fake.user_name() for _ in range(attempt_size)}
        statement = select(User.username).where(User.username.in_(generated_usernames))
        result = await session.execute(statement)
        taken_usernames = set(result.scalars().all())
        available_usernames = generated_usernames - taken_usernames
        suggestions.update(available_usernames)

    return False, list(suggestions)[:num_similars]

async def update_ver_details(session: AsyncSession, user: User, eagerly_loaded:bool = False, commit=True,) -> UnverifiedDetails:
    """ Update a user's verification details asynchronously

    Args:
        session (AsyncSession): The database session
        user (User): The user object
        eagerly_loaded (bool): Whether the user object is eagerly loaded (defaults to false)
        commit (bool, optional): Whether to commit the transaction. Defaults to True.

    Note: if you dont know if the user object is eagerly loaded, set eagerly_loaded to False
    Returns:
        UnverifiedDetails | None: The updated unverified details object if successful, None otherwise
    """
    if not eagerly_loaded:
        statement = select(UnverifiedDetails).where(UnverifiedDetails.user_id == user.id)
        result = await session.execute(statement)
        unverified_details = result.scalars().first()
    else:
        unverified_details = user.verification_details
    try:
        verification_token, expiration = generate_verification_code(user.email, email_verification_code_duration)
        unverified_details.verification_token = verification_token
        unverified_details.token_expires = expiration
        session.add(unverified_details)
        if commit:
            await session.commit()
        return unverified_details
    except Exception as e:
        print(f"Error updating verification details: {e}")
        await session.rollback()
        return None

## User avatar data storage
class AvatarInfo(BaseModel):
    """ Pydantic model for avatar information """
    avatarGender: Optional[str] = None
    avatarAccessories: Optional[str] = None
    avatarColor: Optional[str] = None
    avatarPassions: Optional[str] = None
    avatarExpression: Optional[str] = None

async def store_avatar_info(session: AsyncSession, user_id: int, data:dict | AvatarInfo, fresh=True, commit=True) -> UserAvatarInfo | None:
    """ Store avatar information in the database asynchronously(IF already exists overwrite it)

    Args:
        session (AsyncSession): The database session
        user_id (int): The user's ID
        data (dict): The avatar information

    Returns:
        UserAvatarInfo | None: The created avatar info object if successful, None otherwise
    """
    if isinstance(data, dict):
        # If data is a dict, convert it to AvatarInfo model
        try:
            data = AvatarInfo(**data)
        except Exception as e:
            print(f"Invalid avatar data: {e}")
            return None
    elif isinstance(data, AvatarInfo):
        # If data is already an AvatarInfo model, use it directly
        pass
    try:
        # Check if the user already has avatar info
        statement = select(UserAvatarInfo).where(UserAvatarInfo.user_id == user_id)
        result = await session.execute(statement)
        avatar_info = result.scalars().first()

        if avatar_info:
            # Update existing avatar info
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(avatar_info, key, value)
            session.add(avatar_info)
        else:
            # Create new avatar info
            avatar_info = UserAvatarInfo(user_id=user_id, **data.model_dump())
            session.add(avatar_info)

        if commit:
            await session.commit()
        if fresh:
            await session.refresh(avatar_info)
        return avatar_info
    except IntegrityError:
        await session.rollback()
        print("A user with this email or username already exists.")
        return None
    except Exception as e:
        await session.rollback()
        print(f"Error storing avatar info: {e}")
        return None

async def get_avatar_info(session: AsyncSession, user_id: int) -> UserAvatarInfo | None:
    """ Get avatar information for a user asynchronously
    Args:
        session (AsyncSession): The database session
        user_id (int): The user's ID
    Returns:
        UserAvatarInfo | None: The avatar info object if found, None otherwise
    """
    statement = select(UserAvatarInfo).where(UserAvatarInfo.user_id == user_id)
    result = await session.execute(statement)
    avatar_info = result.scalars().first()
    if not avatar_info:
        print("Avatar info not found")
        return None
    return avatar_info

