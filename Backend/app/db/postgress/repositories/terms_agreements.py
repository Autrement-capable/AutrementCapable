from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Tuple
from datetime import datetime

from database.postgress.models import User, TermsVersion, UserTermsAgreement

async def get_latest_terms_version(session: AsyncSession) -> Optional[TermsVersion]:
    """Get the latest active terms version."""
    statement = select(TermsVersion).where(TermsVersion.is_active == True).order_by(TermsVersion.date_created.desc())
    result = await session.execute(statement)
    return result.scalars().first()

async def get_terms_by_version(session: AsyncSession, version: str) -> Optional[TermsVersion]:
    """Get terms by version string."""
    statement = select(TermsVersion).where(TermsVersion.version == version)
    result = await session.execute(statement)
    return result.scalars().first()

async def get_terms_by_id(session: AsyncSession, terms_id: int) -> Optional[TermsVersion]:
    """Get terms by ID."""
    statement = select(TermsVersion).where(TermsVersion.id == terms_id)
    result = await session.execute(statement)
    return result.scalars().first()

async def create_terms_version(
    session: AsyncSession, 
    version: str,
    content: str,
    is_active: bool = True,
    commit: bool = True
) -> Optional[TermsVersion]:
    """Create a new terms version."""
    try:
        # If new version is active, deactivate all other versions
        if is_active:
            await deactivate_all_terms(session, commit=False)

        terms = TermsVersion(
            version=version,
            content=content,
            is_active=is_active
        )
        session.add(terms)

        if commit:
            await session.commit()
            await session.refresh(terms)

        return terms
    except Exception as e:
        await session.rollback()
        print(f"Error creating terms version: {e}")
        return None

async def deactivate_all_terms(session: AsyncSession, commit: bool = True) -> bool:
    """Deactivate all terms versions."""
    try:
        statement = select(TermsVersion).where(TermsVersion.is_active == True)
        result = await session.execute(statement)
        terms_versions = result.scalars().all()

        for terms in terms_versions:
            terms.is_active = False
            session.add(terms)

        if commit:
            await session.commit()

        return True
    except Exception as e:
        if commit:
            await session.rollback()
        print(f"Error deactivating terms: {e}")
        return False

async def update_terms_version(
    session: AsyncSession,
    terms_id: int,
    content: str = None,
    is_active: bool = None,
    commit: bool = True
) -> Optional[TermsVersion]:
    """Update a terms version."""
    try:
        statement = select(TermsVersion).where(TermsVersion.id == terms_id)
        result = await session.execute(statement)
        terms = result.scalars().first()

        if not terms:
            print(f"Terms with ID {terms_id} not found")
            return None

        if content is not None:
            terms.content = content

        if is_active is not None and is_active != terms.is_active:
            if is_active:
                # If activating this version, deactivate all others
                await deactivate_all_terms(session, commit=False)
            terms.is_active = is_active

        session.add(terms)

        if commit:
            await session.commit()
            await session.refresh(terms)

        return terms
    except Exception as e:
        await session.rollback()
        print(f"Error updating terms version: {e}")
        return None

async def get_user_terms_agreement(session: AsyncSession, user_id: int) -> List[UserTermsAgreement]:
    """Get a user's terms agreements."""
    statement = (
        select(UserTermsAgreement)
        .where(UserTermsAgreement.user_id == user_id)
        .order_by(UserTermsAgreement.date_agreed.desc())
    )
    result = await session.execute(statement)
    return result.scalars().all()

async def get_latest_user_terms_agreement(session: AsyncSession, user_id: int) -> Optional[UserTermsAgreement]:
    """Get a user's most recent terms agreement."""
    statement = (
        select(UserTermsAgreement)
        .where(UserTermsAgreement.user_id == user_id)
        .order_by(UserTermsAgreement.date_agreed.desc())
    )
    result = await session.execute(statement)
    return result.scalars().first()

async def create_user_terms_agreement(
    session: AsyncSession,
    user_id: int,
    terms_id: int,
    commit: bool = True
) -> Tuple[Optional[UserTermsAgreement], bool]:
    """Create a new user terms agreement."""
    try:
        # Check if user exists
        user_statement = select(User).where(User.id == user_id)
        user_result = await session.execute(user_statement)
        user = user_result.scalars().first()

        if not user:
            print(f"User with ID {user_id} not found")
            return None, False

        # Check if terms exists
        terms_statement = select(TermsVersion).where(TermsVersion.id == terms_id)
        terms_result = await session.execute(terms_statement)
        terms = terms_result.scalars().first()

        if not terms:
            print(f"Terms with ID {terms_id} not found")
            return None, False

        # Check if user already agreed to these terms
        existing_agreement = await get_user_specific_agreement(session, user_id, terms_id)
        if existing_agreement:
            return existing_agreement, False

        agreement = UserTermsAgreement(
            user_id=user_id,
            terms_id=terms_id,
            date_agreed=datetime.utcnow()
        )
        session.add(agreement)

        if commit:
            await session.commit()
            await session.refresh(agreement)

        return agreement, True
    except Exception as e:
        await session.rollback()
        print(f"Error creating user terms agreement: {e}")
        return None, False

async def get_user_specific_agreement(session: AsyncSession, user_id: int, terms_id: int) -> Optional[UserTermsAgreement]:
    """Get a specific user-terms agreement."""
    statement = select(UserTermsAgreement).where(
        UserTermsAgreement.user_id == user_id,
        UserTermsAgreement.terms_id == terms_id
    )
    result = await session.execute(statement)
    return result.scalars().first()

async def has_user_agreed_to_latest_terms(session: AsyncSession, user_id: int) -> bool:
    """Check if a user has agreed to the latest terms."""
    latest_terms = await get_latest_terms_version(session)
    if not latest_terms:
        return False

    agreement = await get_user_specific_agreement(session, user_id, latest_terms.id)
    return agreement is not None