from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.future import select

from ..models import RevokedToken
from ..engine import postgress
from ....services.scheduler.base_cron import register_cron_job, BaseCronJob
from ....utils.config_helpers import get_property


# Cron jobs

@register_cron_job("TokenPurgeCron")
class TokenPurgeCron(BaseCronJob):
    """Cron job to delete expired tokens from the database."""
    def __init__(self):
        super().__init__("TokenPurgeCron", "auth", ["token_purge_interval"])

    async def run(self, session: AsyncSession):
        """ Delete all expired tokens from the database asynchronously """
        try:
            statement = select(RevokedToken).where(RevokedToken.data_expires < datetime.utcnow())
            result = await session.execute(statement)
            expired_tokens = result.scalars().all()

            for token in expired_tokens:
                await session.delete(token)

            await session.commit()
            return True
        except:
            await session.rollback()
            return False

# Create/Update functions

async def revoke_token(session: AsyncSession, jti: str, expires: datetime, token_type: str, commit=True) -> RevokedToken:
    """ Revoke a token in the database asynchronously

    Args:
        session (AsyncSession): The database session
        jti (str): The JTI of the token
        expires (datetime): The expiration date of the token
        token_type (str): The type of token
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
    """
    try:
        token = RevokedToken(jti=jti, date_revoked=datetime.utcnow(), data_expires=expires, type=token_type)
        session.add(token)
        if commit:
            await session.commit()
        return token
    except IntegrityError:
        await session.rollback()
        print("A token with this JTI already exists.")
        return None
    except OperationalError:
        await session.rollback()
        print("There was an issue with the database operation.")
        return None
    except TypeError as e:
        await session.rollback()
        print(f"Type error: {e}")
        return None

def revoke_token_sync(jti: str, expires: datetime, token_type: str, commit=True) -> RevokedToken:
    """ Revoke a token in the database synchronously """
    session = postgress.SyncSession()
    try:
        token = RevokedToken(jti=jti, date_revoked=datetime.utcnow(), data_expires=expires, type=token_type)
        session.add(token)
        if commit:
            session.commit()
        return token
    except IntegrityError:
        session.rollback()
        print("A token with this JTI already exists.")
        return None
    except OperationalError:
        session.rollback()
        print("There was an issue with the database operation.")
        return None
    except TypeError as e:
        session.rollback()
        print(f"Type error: {e}")
        return None
    finally:
        session.close()

async def get_revoked_token_by_jti(session: AsyncSession, jti: str) -> RevokedToken:
    """ Get a revoked token from the database by JTI asynchronously """
    statement = select(RevokedToken).where(RevokedToken.jti == jti)
    result = await session.execute(statement)
    return result.scalars().first()

def get_revoked_token_by_jti_sync(jti: str) -> RevokedToken:
    """ Get a revoked token from the database by JTI synchronously """
    session = postgress.SyncSession()
    try:
        statement = select(RevokedToken).where(RevokedToken.jti == jti)
        result = session.execute(statement)
        return result.scalars().first()
    finally:
        session.close()
