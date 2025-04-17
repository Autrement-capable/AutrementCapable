import yaml
import asyncio
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select

from ..models import User, AccountRecovery
from ..engine import postgress
from ....services.auth.verification import generate_verification_code
from ....core.config import Config
from ....services.scheduler.base_cron import register_cron_job, BaseCronJob

try:
    password_reset_code_duration = Config.get_property(None, "verify", ["password_reset_code_duration"])['password_reset_code_duration']
except Exception as e: # if the config file is not found
    print(f"Error loading config: {e}")
# is_config_loaded = False

@register_cron_job("AccountRecoveryPurgeCron")
class AccountRecoveryPurgeCron(BaseCronJob):
    """Cron job to delete expired password resets from the database."""
    def __init__(self):
        super().__init__("AccountRecoveryPurgeCron", "verify", ["password_reset_purge_interval"])

    async def run(self, session: AsyncSession):
        """ Delete all expired password resets from the database asynchronously """
        try:
            statement = select(AccountRecovery).where(AccountRecovery.token_expires < datetime.utcnow())
            result = await session.execute(statement)
            resets = result.scalars().all()
            for reset in resets:
                await session.delete(reset)
            await session.commit()
        except Exception as e:
            print(f"Error deleting expired password resets: {e}")
            await session.rollback()

async def create_acc_recovery(session: AsyncSession, user: User, commit=True, fresh=True) -> AccountRecovery | None:
    """ Create a password reset entry for a user. """
    try:
        reset_token, token_expire = generate_verification_code(32, password_reset_code_duration)
        password_reset = AccountRecovery(user_id=user.id, reset_token=reset_token, token_expires=token_expire)
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

async def get_acc_recovery_by_token(session: AsyncSession, reset_token: str) -> AccountRecovery | None:
    """ Get a password reset entry by its token. (LOADS USER) """
    try:
        statement = select(AccountRecovery).where(AccountRecovery.reset_token == reset_token).options(joinedload(AccountRecovery.user))
        result = await session.execute(statement)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting password reset by token: {e}")
        return None

async def del_acc_recovery(session: AsyncSession, reset: AccountRecovery, commit=True):
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
