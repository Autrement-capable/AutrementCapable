from typing import Optional, Tuple
from datetime import datetime
import io

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import UploadFile, HTTPException, status

from ..models import User, UserPicture

async def get_user_picture(session: AsyncSession, user_id: int, picture_type: str = "profile") -> Optional[UserPicture]:
    """Get a user's picture by type."""
    statement = select(UserPicture).where(
        UserPicture.user_id == user_id,
        UserPicture.type == picture_type
    )
    result = await session.execute(statement)
    return result.scalars().first()

async def save_picture_chunk(
    session: AsyncSession,
    chunk: bytes,
    is_first_chunk: bool,
    is_last_chunk: bool,
    user_id: int,
    picture_type: str = "profile",
    commit: bool = False
) -> Optional[UserPicture]:
    """
    Save an image chunk to the database.

    For the first chunk, create or retrieve the picture record.
    For subsequent chunks, append data to the existing record.

    Args:
        session: Database session
        chunk: Binary chunk of picture data
        is_first_chunk: Whether this is the first chunk
        is_last_chunk: Whether this is the last chunk
        user_id: User ID
        picture_type: Type of picture
        commit: Whether to commit after processing

    Returns:
        The UserPicture object
    """
    try:
        # For the first chunk, verify the user exists and create/get the picture record
        if is_first_chunk:
            # Check if user exists
            user_statement = select(User).where(User.id == user_id)
            user_result = await session.execute(user_statement)
            user = user_result.scalars().first()

            if not user:
                raise ValueError(f"User with ID {user_id} not found")

            # Get existing picture or create new one
            existing_picture = await get_user_picture(session, user_id, picture_type)

            if existing_picture:
                # Clear existing data for a new upload
                existing_picture.picture_data = chunk
                existing_picture.date_updated = datetime.utcnow()
                picture = existing_picture
            else:
                # Create new picture with initial chunk
                picture = UserPicture(
                    user_id=user_id,
                    picture_data=chunk,
                    type=picture_type
                )

            session.add(picture)
            # We'll commit only at the end of all chunks

            # Store picture object in session for subsequent chunks
            if hasattr(session, '_custom_attributes'):
                session._custom_attributes['current_picture'] = picture
            else:
                session._custom_attributes = {'current_picture': picture}

            return picture
        else:
            # For subsequent chunks, retrieve picture from session and append data
            if hasattr(session, '_custom_attributes') and 'current_picture' in session._custom_attributes:
                picture = session._custom_attributes['current_picture']

                # Append chunk to existing data
                if picture.picture_data is None:
                    picture.picture_data = chunk
                else:
                    picture.picture_data = picture.picture_data + chunk

                session.add(picture)

                # If this is the last chunk, we can clean up the session attribute
                if is_last_chunk:
                    if hasattr(session, '_custom_attributes'):
                        session._custom_attributes.pop('current_picture', None)

                return picture
            else:
                raise ValueError("No picture found in session for chunked upload")

        # Commit if requested (typically only for the final chunk)
        if commit:
            await session.commit()
            if picture:
                await session.refresh(picture)

        return picture
    except Exception as e:
        if commit:
            await session.rollback()
        print(f"Error saving picture chunk: {e}")
        raise

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
        if commit:
            await session.rollback()
        print(f"Error deleting user picture: {e}")
        return False