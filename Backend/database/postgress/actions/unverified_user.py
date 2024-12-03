from database.postgress.models.user import User
from database.postgress.models.unverified_user import UnverifiedUser
from database.postgress.actions.role import get_role_by_name
from utils.password import verify_password, hash_password
from utils.verifcation_code import generate_verification_code, generate_random_suffix
from database.postgress.actions.user import is_username_taken

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime
import yaml
from utils.parse_yaml import get_property


email_verification_code_duration = 900 # 15 minutes
is_config_loaded = False

def load_config():
    global email_verification_code_duration, is_config_loaded
    if not is_config_loaded:
        __config_file__ = "./server/config_files/config.yaml"
        with open(__config_file__, "r") as file:
            config = yaml.safe_load(file)

        mail_server_config = get_property(config, "verify", ["email_verification_code_duration"])
        email_verification_code_duration = mail_server_config['email_verification_code_duration']
        is_config_loaded = True

try:
    load_config()
except Exception as e:
    print(f"Error loading config: {e}")
    email_verification_code_duration = 900

async def create_unverified_user(session: AsyncSession, username: str, email: str, password: str,
                                 first_name: str = None, last_name: str = None,
                                 role_name: str = "Young Person", phone_number: str = None,
                                 address: str = None, hashed=False, commit=True, fresh=True) -> UnverifiedUser:
    """ Create an unverified user in the database. Registers a confirmation code for the user as well.

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
        fresh (bool, optional): Whether to refresh the user object from DB(usefull if you want to manipulate it). Defaults to True.

        Note: fresh is defaulted because the object is almost always needed after creation."""
    try:
        if not hashed:
            password = hash_password(password)
        role_id = (await get_role_by_name(session, role_name)).role_id
        if not role_id:
            print("Role not found")
            return None
        confirmation_code, expiration = generate_verification_code(email, email_verification_code_duration)
        user = UnverifiedUser(username=username, email=email, password_hash=password,
                              pending_role_id=role_id, verification_token=confirmation_code, token_expires=expiration,
                              first_name=first_name,last_name=last_name, phone_number=phone_number, address=address)
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

async def get_uvf_user_by_email(session: AsyncSession, email: str) -> UnverifiedUser:
    """ Get an unverified user by their email.

    Args:
        session (Session): The database session
        email (str): The user's email

    Returns:
        UnverifiedUser: The unverified user
        None: If the user is not found
    """
    return await session.exec(select(UnverifiedUser).where(UnverifiedUser.email == email))

async def get_uvf_user_by_code(session: AsyncSession, code: str) -> UnverifiedUser:
    """ Get an unverified user by their verification code.

    Args:
        session (AsyncSession): The database session
        code (str): The verification code

    Returns:
        UnverifiedUser: The unverified user
        None: If the user is not found
    """
    try:
        # Execute the query
        result = await session.execute(
            select(UnverifiedUser).where(UnverifiedUser.verification_token == code.strip())
        )
        # Fetch the first scalar result
        user = result.scalars().first()
        return user
    except Exception as e:
        print(f"Error getting user by code: {e}")
        return None

async def verify_user(session: AsyncSession, verification_code: str, commit=True, fresh=False ) -> User:
    """ Verify a user using their verification code.

    Args:
        session (Session): The database session
        verification_code (str): The user's verification code
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        fresh (bool, optional): Whether to refresh the user object from DB(usefull if you want to manipulate it). Defaults to False

    Returns:
        User: The verified user
        None: If the user is not found or the token has expired.
    """
    tmp_user = await get_uvf_user_by_code(session, verification_code)
    if not tmp_user:
        print("User not found")
        return None

    if tmp_user.token_expires < datetime.utcnow():
        print("Token expired")
        return None

    # check if username is taken before creating user(rare case when user that has not been verified has the same username as another user)
    if await is_username_taken(session, tmp_user.username):
        salt = generate_random_suffix()
        tmp_user.username = tmp_user.username + salt

    user = User(username=tmp_user.username, email=tmp_user.email, password_hash=tmp_user.password_hash,
                role_id=tmp_user.pending_role_id, first_name=tmp_user.first_name, last_name=tmp_user.last_name,
                phone_number=tmp_user.phone_number, address=tmp_user.address)

    session.delete(tmp_user)
    session.add(user)

    if commit:
        await session.commit()
    if fresh:
        await session.refresh(user)

    return user

async def del_uvf_user(session: AsyncSession, user: UnverifiedUser, commit=True):
    """ Delete an unverified user from the database.

    Args:
        session (Session): The database session
        user (UnverifiedUser): The user to delete
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
    """
    await session.delete(user)
    if commit:
        await session.commit()

#TODO: Add cron job to delete expired unverified users