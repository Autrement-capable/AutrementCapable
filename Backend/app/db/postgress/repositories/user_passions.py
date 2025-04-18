from typing import List, Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from ..models import User, UserPassion


async def get_user_passions(session: AsyncSession, user_id: int) -> List[UserPassion]:
    """Get all passions for a user ordered by their defined order."""
    statement = select(UserPassion).where(UserPassion.user_id == user_id).order_by(UserPassion.order)
    result = await session.execute(statement)
    return result.scalars().all()

async def create_user_passion(
    session: AsyncSession, 
    user_id: int, 
    passion_text: str, 
    order: int,
    commit: bool = True
) -> Optional[UserPassion]:
    """Create a new passion for a user."""
    try:
        # Check if user exists
        user_statement = select(User).where(User.id == user_id)
        user_result = await session.execute(user_statement)
        user = user_result.scalars().first()

        if not user:
            print(f"User with ID {user_id} not found")
            return None

        # Check if order is already used
        existing_passion = await get_passion_by_order(session, user_id, order)
        if existing_passion:
            print(f"Order {order} is already used for user {user_id}")
            return None

        passion = UserPassion(
            user_id=user_id,
            passion_text=passion_text,
            order=order
        )
        session.add(passion)

        if commit:
            await session.commit()
            await session.refresh(passion)

        return passion
    except Exception as e:
        await session.rollback()
        print(f"Error creating user passion: {e}")
        return None

async def get_passion_by_order(session: AsyncSession, user_id: int, order: int) -> Optional[UserPassion]:
    """Get a specific passion by its order for a user."""
    statement = select(UserPassion).where(
        UserPassion.user_id == user_id,
        UserPassion.order == order
    )
    result = await session.execute(statement)
    return result.scalars().first()

async def update_user_passion(
    session: AsyncSession, 
    passion_id: int, 
    passion_text: str = None,
    order: int = None,
    commit: bool = True
) -> Optional[UserPassion]:
    """Update an existing passion."""
    try:
        statement = select(UserPassion).where(UserPassion.id == passion_id)
        result = await session.execute(statement)
        passion = result.scalars().first()

        if not passion:
            print(f"Passion with ID {passion_id} not found")
            return None

        if passion_text is not None:
            passion.passion_text = passion_text

        if order is not None and order != passion.order:
            # Check if new order is already used
            existing_passion = await get_passion_by_order(session, passion.user_id, order)
            if existing_passion and existing_passion.id != passion_id:
                print(f"Order {order} is already used")
                return None
            passion.order = order

        session.add(passion)

        if commit:
            await session.commit()
            await session.refresh(passion)

        return passion
    except Exception as e:
        await session.rollback()
        print(f"Error updating user passion: {e}")
        return None

async def delete_user_passion(
    session: AsyncSession, 
    passion_id: int,
    commit: bool = True
) -> bool:
    """Delete a user passion."""
    try:
        statement = select(UserPassion).where(UserPassion.id == passion_id)
        result = await session.execute(statement)
        passion = result.scalars().first()

        if not passion:
            print(f"Passion with ID {passion_id} not found")
            return False

        await session.delete(passion)

        if commit:
            await session.commit()

        return True
    except Exception as e:
        await session.rollback()
        print(f"Error deleting user passion: {e}")
        return False

async def reorder_user_passions(
    session: AsyncSession,
    user_id: int,
    passion_orders: dict,  # {passion_id: new_order}
    commit: bool = True
) -> bool:
    """Reorder multiple passions for a user at once."""
    try:
        # Get all passions for the user
        statement = select(UserPassion).where(UserPassion.user_id == user_id)
        result = await session.execute(statement)
        passions = {p.id: p for p in result.scalars().all()}

        # Update orders
        for passion_id, new_order in passion_orders.items():
            if passion_id in passions:
                passions[passion_id].order = new_order
                session.add(passions[passion_id])

        if commit:
            await session.commit()

        return True
    except Exception as e:
        await session.rollback()
        print(f"Error reordering passions: {e}")
        return False