from database.postgress.models.revokedTokens import RevokedToken

from sqlmodel import Session
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime , timedelta

# Create/Update functions

def revoke_token(session: Session, jti: str, expires: datetime, token_type: str, commit = True) -> RevokedToken:
    """ Revoke a token in the database

    Args:
        session (Session): The database session
        jti (str): The token's JTI
        expires (datetime): The token's expiration date
        token_type (str): The token's type
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
    """
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

# Cron job functions

def delete_expired_tokens(session: Session, commit=True) -> bool:
    """ Delete all expired tokens from the database

    Args:
        session (Session): The database session
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
    """
    try:
        session.query(RevokedToken).filter(RevokedToken.data_expires < datetime.utcnow()).delete()
        if commit:
            session.commit()
        return True
    except:
        session.rollback()
        return False

# get functions

def get_revoked_token_by_jti(session: Session, jti: str) -> RevokedToken:
    """ Get a revoked token from the database by JTI

    Args:
        session (Session): The database session
        jti (str): The token's JTI
    """
    return session.query(RevokedToken).filter(RevokedToken.jti == jti).first()