from database.postgress.models.test_model import PasswordReset
from database.postgress.models.test_model import User
from utils.verifcation_code import generate_verification_code
from database.postgress.setup import postgress
from server.server import AddCronJob

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime, timedelta
import yaml
from utils.parse_yaml import get_property

password_reset_code_duration = 900 # 15 minutes
is_config_loaded = False

# Cron job functions
async def delete_expired_password_resets() -> bool:
    """ Delete all expired password resets from the database asynchronously

    Args:
        session (AsyncSession): The database session
        commit (bool, optional): Whether to commit the transaction. Defaults to True."""

    async with postgress.GetSession() as session:
        try:
            statement = select(PasswordReset).where(PasswordReset.token_expires < datetime.utcnow())
            result = await session.execute(statement)
            resets = result.scalars().all()
            for reset in resets:
                await session.delete(reset)
            await session.commit()
        except Exception as e:
            print(f"Error deleting expired password resets: {e}")
            await session.rollback()
            return False


def load_config():
    global password_reset_code_duration, is_config_loaded
    if not is_config_loaded:
        __config_file__ = "./server/config_files/config.yaml"
        with open(__config_file__, "r") as file:
            config = yaml.safe_load(file)

        mail_server_config = get_property(config, "verify", ["password_reset_code_duration", "password_reset_purge_interval"])
        password_reset_code_duration = mail_server_config['password_reset_code_duration']
        prune_interval = mail_server_config['password_reset_purge_interval']
        AddCronJob(delete_expired_password_resets, trigger="interval", seconds=prune_interval) # cron job to delete expired password resets
        is_config_loaded = True

try:
    load_config()
except Exception as e:
    print(f"Error loading config: {e}")
    password_reset_code_duration = 900

async def create_password_reset(session: AsyncSession, user:User, commit = True, fresh = True) -> PasswordReset|None:
    """ Create a password reset for a user in the database. Registers a confirmation code for the user as well.

    Args:
        session (Session): The database session
        user (User): The user to reset the password for
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        fresh (bool, optional): Whether to refresh the user object from DB(usefull if you want to manipulate it). Defaults to False.

        Note: fresh is defaulted because the object is almost always needed after creation."""
    try:
        reset_token, token_expire = generate_verification_code(32, password_reset_code_duration)
        password_reset = PasswordReset(user_id=user.user_id, reset_token=reset_token, token_expires=token_expire, user=user)
        session.add(password_reset)
        if commit:
            await session.commit()
        if fresh:
            await session.refresh(password_reset)
        return password_reset
    except IntegrityError as e:
        await session.rollback()
        return None
    except OperationalError as e:
        await session.rollback()
        return None

async def get_password_reset_by_token(session: AsyncSession, reset_token: str) -> PasswordReset|None:
    """ Get a password reset by its token

    Args:
        session (Session): The database session
        reset_token (str): The token to search for"""
    try:
        statement = select(PasswordReset).where(PasswordReset.reset_token == reset_token)
        result = await session.execute(statement)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting password reset by token: {e}")
        return None

async def del_password_reset(session: AsyncSession, reset: PasswordReset, commit = True):
    """ Delete a password reset from the database

    Args:
        session (Session): The database session
        reset (PasswordReset): The password reset to delete
        commit (bool, optional): Whether to commit the transaction. Defaults to True."""
    try:
        await session.delete(reset)
        if commit:
            await session.commit()
    except Exception as e:
        await session.rollback()
        print(f"Error deleting password reset: {e}")
        return False
    return True
