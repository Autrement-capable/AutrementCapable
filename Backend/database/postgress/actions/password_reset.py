from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from datetime import datetime, timedelta
import yaml
from database.postgress.models import User, PasswordReset
from database.postgress.config import postgress
from utils.verifcation_code import generate_verification_code
from server.server import AddCronJob
from utils.Config_loader import Config
import asyncio
from server.cron_jobs.base_cron import register_cron_job, BaseCronJob

try:
    password_reset_code_duration = Config.get_property(None, "verify", ["password_reset_code_duration"])
except Exception as e: # if the config file is not found
    print(f"Error loading config: {e}")
# is_config_loaded = False

# # Cron job functions
# async def delete_expired_password_resets() -> bool:
#     """ Delete all expired password resets from the database asynchronously """
#     async with postgress.getSession() as session:
#         try:
#             statement = select(PasswordReset).where(PasswordReset.token_expires < datetime.utcnow())
#             result = await session.execute(statement)
#             resets = result.scalars().all()
#             for reset in resets:
#                 await session.delete(reset)
#             await session.commit()
#         except Exception as e:
#             print(f"Error deleting expired password resets: {e}")
#             await session.rollback()
#             return False

# def load_config():
#     global password_reset_code_duration, is_config_loaded
#     if not is_config_loaded:
#         __config_file__ = "./server/config_files/config.yaml"
#         with open(__config_file__, "r") as file:
#             config = yaml.safe_load(file)

#         mail_server_config = get_property(config, "verify", ["password_reset_code_duration", "password_reset_purge_interval"])
#         password_reset_code_duration = mail_server_config['password_reset_code_duration']
#         prune_interval = mail_server_config['password_reset_purge_interval']
#         AddCronJob(delete_expired_password_resets, trigger="interval", seconds=prune_interval)
#         is_config_loaded = True

# try:
#     load_config()
# except Exception as e:
#     print(f"Error loading config: {e}")
#     password_reset_code_duration = 900

@register_cron_job("PasswordResetPurgeCron")
class PasswordResetPurgeCron(BaseCronJob):
    """Cron job to delete expired password resets from the database."""
    def __init__(self):
        super().__init__("PasswordResetPurgeCron", "verify", ["password_reset_purge_interval"])

    async def run(self, session: AsyncSession):
        """ Delete all expired password resets from the database asynchronously """
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

async def create_password_reset(session: AsyncSession, user: User, commit=True, fresh=True) -> PasswordReset | None:
    """ Create a password reset entry for a user. """
    try:
        reset_token, token_expire = generate_verification_code(32, password_reset_code_duration)
        password_reset = PasswordReset(user_id=user.id, reset_token=reset_token, token_expires=token_expire)
        session.add(password_reset)
        if commit:
            await session.commit()
        if fresh:
            await asyncio.gather(session.refresh(password_reset), session.refresh(user))
        return password_reset
    except IntegrityError:
        await session.rollback()
        return None
    except OperationalError:
        await session.rollback()
        return None

async def get_password_reset_by_token(session: AsyncSession, reset_token: str) -> PasswordReset | None:
    """ Get a password reset entry by its token. """
    try:
        statement = select(PasswordReset).where(PasswordReset.reset_token == reset_token).options(joinedload(PasswordReset.user))
        result = await session.execute(statement)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting password reset by token: {e}")
        return None

async def del_password_reset(session: AsyncSession, reset: PasswordReset, commit=True):
    """ Delete a password reset entry from the database. """
    try:
        await session.delete(reset)
        if commit:
            await session.commit()
    except Exception as e:
        await session.rollback()
        print(f"Error deleting password reset: {e}")
        return False
    return True
