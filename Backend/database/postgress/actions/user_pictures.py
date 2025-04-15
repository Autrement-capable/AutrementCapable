from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional
from datetime import datetime

from database.postgress.models import User, UserPicture

async def get_user_picture(session: AsyncSession, user_id: int, picture_type: str = "profile") -> Optional[UserPicture]:
    """Get a user's picture by type."""
    statement = select(UserPicture).where(
        UserPicture.user_id == user_id,
        UserPicture.type == picture_type
    )
    result = await session.execute(statement)
    return result.scalars().first()

async def create_or_update_user_picture(
    session: AsyncSession, 
    user_id: int, 
    picture_data: bytes,
    picture_type: str = "profile",
    commit: bool = True
) -> Optional[UserPicture]:
    """Create or update a user's picture."""
    try:
        # Check if user exists
        user_statement = select(User).where(User.id == user_id)
        user_result = await session.execute(user_statement)
        user = user_result.scalars().first()

        if not user:
            print(f"User with ID {user_id} not found")
            return None

        # Check if picture already exists
        existing_picture = await get_user_picture(session, user_id, picture_type)

        if existing_picture:
            # Update existing picture
            existing_picture.picture_data = picture_data
            existing_picture.date_updated = datetime.utcnow()
            session.add(existing_picture)
            picture = existing_picture
        else:
            # Create new picture
            picture = UserPicture(
                user_id=user_id,
                picture_data=picture_data,
                type=picture_type
            )
            session.add(picture)

        if commit:
            await session.commit()
            await session.refresh(picture)

        return picture
    except Exception as e:
        await session.rollback()
        print(f"Error creating/updating user picture: {e}")
        return None

async def delete_user_picture(
    session: AsyncSession, 
    user_id: int,
    picture_type: str = "profile",
    commit: bool = True
) -> bool:
    """Delete a user's picture."""
    try:
        picture = await get_user_picture(session, user_id, picture_type)

        if not picture:
            print(f"Picture not found for user {user_id} with type {picture_type}")
            return False

        await session.delete(picture)

        if commit:
            await session.commit()

        return True
    except Exception as e:
        await session.rollback()
        print(f"Error deleting user picture: {e}")
        return False