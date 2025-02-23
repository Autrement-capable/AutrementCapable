from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.future import select
from datetime import datetime
from sqlalchemy.orm import joinedload
import yaml
from database.postgress.models import User, UnverifiedDetails
from database.postgress.config import postgress
from database.postgress.actions.role import get_role_by_name
from utils.password import verify_password, hash_password
from utils.verifcation_code import generate_verification_code, generate_random_suffix
from server.cron_jobs.base_cron import register_cron_job, BaseCronJob
from utils.parse_yaml import get_property
from utils.Config_loader import Config
from faker import Faker
from typing import Optional, Literal
import asyncio

try:
    email_verification_code_duration = Config.get_property(None, "verify", ["email_verification_code_duration"])
except Exception as e: # if the config file is not found
    print(f"Error loading config: {e}")
    email_verification_code_duration = 900
# is_config_loaded = False

# # Cron job functions

# async def delete_expired_unverified_users() -> bool:
#     """ Delete expired unverified users from the database."""
#     async with postgress.getSession() as session:
#         try:
#             # Select UnverifiedDetails and eagerly load the related User
#             statement = (
#                 select(UnverifiedDetails)
#                 .where(UnverifiedDetails.token_expires < datetime.utcnow())
#                 .options(joinedload(UnverifiedDetails.user))  # Eager loading
#             )
#             result = await session.execute(statement)
#             details: list[UnverifiedDetails] = result.scalars().all()

#             for detail in details:
#                 if detail.user:  # Since it's eagerly loaded, this avoids an extra query
#                     await session.delete(detail.user)

#             await session.commit()
#             return True
#         except Exception as e:
#             print(f"Error deleting expired unverified users: {e}")
#             await session.rollback()
#             return False


# def load_config():
#     global email_verification_code_duration, is_config_loaded
#     if not is_config_loaded:
#         __config_file__ = "./server/config_files/config.yaml"
#         with open(__config_file__, "r") as file:
#             config = yaml.safe_load(file)

#         mail_server_config = get_property(config, "verify", ["email_verification_code_duration", "email_ver_purge_interval"])
#         email_verification_code_duration = mail_server_config['email_verification_code_duration']
#         prune_interval = mail_server_config['email_ver_purge_interval']
#         AddCronJob(delete_expired_unverified_users, trigger="interval", seconds=prune_interval)
#         is_config_loaded = True

# try:
#     load_config()
# except Exception as e:
#     print(f"Error loading config: {e}")
#     email_verification_code_duration = 900

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
    """ Create a user in the database asynchronously

    Args:
        session (AsyncSession): The database session
        username (str): The user's username
        email (str): The user's email
        password (str): The user's password
        first_name (str, optional): The user's first name. Defaults to None.
        last_name (str, optional): The user's last name. Defaults to None.
        role_name (str, optional): The user's role name. Defaults to "Young Person".
        phone_number (str, optional): The user's phone number. Defaults to None.
        address (str, optional): The user's address. Defaults to None.
        hashed (bool, optional): Whether the password is hashed. Defaults to False.
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        fresh (bool, optional): Whether to refresh the user object from DB. Defaults to True.

        Returns:
        tuple[User, UnverifiedDetails] | None: A tuple containing the user and unverified details objects if successful, None otherwise

            FIY: the user object is lazily loaded with selectin strategy"""
    try:
        if not hashed:
            password = hash_password(password)
        role = await get_role_by_name(session, role_name)
        if not role:
            print("Role not found")
            return None
        verification_token, expiration = generate_verification_code(email, email_verification_code_duration)
        user = User(username=username, email=email, password_hash=password,
                    role_id=role.id, first_name=first_name, last_name=last_name,
                    phone_number=phone_number, address=address, role=role)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        unverified_details = UnverifiedDetails(user_id=user.id, verification_token=verification_token, token_expires=expiration)
        session.add(unverified_details)
        if commit:
            await session.commit()
        if fresh:
            await asyncio.gather(session.refresh(user), session.refresh(unverified_details))
        return user, unverified_details
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
        .options(joinedload(User.password_resets), joinedload(User.verification_details)))
    else:
        raise ValueError("Invalid load type")
    
    result = await session.execute(statement)
    result = result.scalars().first()
    if not result:
        print("User not found")
        return None
    return result

async def verify_user(session: AsyncSession, verification_code: str, commit=True, fresh=True) -> User:
    """ Verify a user using their verification code.

    Args:
        session (AsyncSession): The database session
        verification_code (str): The code that we will verify that is legit
        commit (bool): whether to commit on change (defaults to true)
        fresh (bool): whether to give fresh object back (defaults to true)
        
    Returns:
        User | None: The user object if found, None otherwise
    """
    statement = (select(UnverifiedDetails)
    .where(UnverifiedDetails.verification_token == verification_code.strip())
    .options(joinedload(UnverifiedDetails.user))) # Eager loading
    result = await session.execute(statement)
    unverified_details = result.scalars().first()
    if not unverified_details:
        print("User not found")
        return None
    if unverified_details.token_expires < datetime.utcnow():
        print("Token expired")
        return None
    user = unverified_details.user
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
    """ Login a user asynchronously

    Args:
        session (AsyncSession): The database session
        password (str): The user's password
        username_or_email (str): The user's username or email

    Returns:
        User | None: The user object if found, None otherwise
    """
    statement = select(User).where(User.username == username_or_email)
    result = await session.execute(statement)
    user = result.scalars().first()

    if not user:
        statement = select(User).where(User.email == username_or_email)
        result = await session.execute(statement)
        user = result.scalars().first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

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
