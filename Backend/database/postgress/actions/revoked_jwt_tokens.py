from database.postgress.models.revokedTokens import RevokedToken
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime
from sqlmodel import select

# Create/Update functions

async def revoke_token(session: AsyncSession, jti: str, expires: datetime, token_type: str, commit=True) -> RevokedToken:
    """ Revoke a token in the database asynchronously

    Args:
        session (AsyncSession): The database session
        jti (str): The token's JTI
        expires (datetime): The token's expiration date
        token_type (str): The token's type
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

# Cron job functions

async def delete_expired_tokens(session: AsyncSession, commit=True) -> bool:
    """ Delete all expired tokens from the database asynchronously

    Args:
        session (AsyncSession): The database session
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
    """
    try:
        statement = select(RevokedToken).where(RevokedToken.data_expires < datetime.utcnow())
        results = await session.exec(statement)
        expired_tokens = results.all()

        for token in expired_tokens:
            await session.delete(token)
        
        if commit:
            await session.commit()

        return True
    except:
        await session.rollback()
        return False

# Get functions

async def get_revoked_token_by_jti(session: AsyncSession, jti: str) -> RevokedToken:
    """ Get a revoked token from the database by JTI asynchronously

    Args:
        session (AsyncSession): The database session
        jti (str): The token's JTI
    """
    statement = select(RevokedToken).where(RevokedToken.jti == jti)
    result = await session.exec(statement)
    return result.first()