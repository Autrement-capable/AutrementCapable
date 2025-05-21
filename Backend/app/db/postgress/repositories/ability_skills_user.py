## DEPRECATED: This file is deprecated and will be removed in future versions.

# from datetime import datetime
# from typing import Dict, Any, Optional, List, Tuple

# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy.exc import IntegrityError, OperationalError

# from ..models.test_model import User, UserSkill, UserAbilities

# # ============ USER SKILLS FUNCTIONS ============

# async def get_user_skills(session: AsyncSession, user_id: int) -> Optional[UserSkill]:
#     """
#     Get the skills for a specific user.

#     Args:
#         session (AsyncSession): The database session
#         user_id (int): The user's ID

#     Returns:
#         Optional[UserSkill]: The user's skills record or None if not found
#     """
#     try:
#         statement = select(UserSkill).where(UserSkill.user_id == user_id)
#         result = await session.execute(statement)
#         return result.scalars().first()
#     except Exception as e:
#         print(f"Error getting user skills: {e}")
#         return None

# async def create_or_update_user_skills(
#     session: AsyncSession, 
#     user_id: int, 
#     skills_data: Dict[str, int], 
#     commit: bool = True
# ) -> Tuple[Optional[UserSkill], bool]:
#     """
#     Create or update the skills for a user.

#     Args:
#         session (AsyncSession): The database session
#         user_id (int): The user's ID
#         skills_data (Dict[str, int]): Dictionary of skills and their values
#         commit (bool, optional): Whether to commit the transaction. Defaults to True.

#     Returns:
#         Tuple[Optional[UserSkill], bool]: The UserSkill object and a boolean indicating whether it was created (True) 
#                                          or updated (False). Returns (None, False) on error.
#     """
#     try:
#         # Check if user exists
#         user_statement = select(User).where(User.id == user_id)
#         user_result = await session.execute(user_statement)
#         user = user_result.scalars().first()

#         if not user:
#             print(f"User with ID {user_id} not found")
#             return None, False

#         # Check if user skills record already exists
#         existing_skills = await get_user_skills(session, user_id)
#         created = False

#         if existing_skills:
#             # Update existing record
#             existing_skills.skills_data = skills_data
#             existing_skills.last_updated = datetime.utcnow()
#             session.add(existing_skills)
#             user_skills = existing_skills
#         else:
#             # Create new record
#             user_skills = UserSkill(
#                 user_id=user_id,
#                 skills_data=skills_data,
#                 last_updated=datetime.utcnow()
#             )
#             session.add(user_skills)
#             created = True

#         if commit:
#             await session.commit()
#             await session.refresh(user_skills)

#         return user_skills, created
#     except IntegrityError:
#         await session.rollback()
#         print(f"Integrity error creating/updating user skills for user {user_id}")
#         return None, False
#     except OperationalError as e:
#         await session.rollback()
#         print(f"Database operation error: {e}")
#         return None, False
#     except Exception as e:
#         await session.rollback()
#         print(f"Unexpected error creating/updating user skills: {e}")
#         return None, False

# async def update_specific_user_skill(
#     session: AsyncSession, 
#     user_id: int, 
#     skill_name: str, 
#     skill_value: int,
#     commit: bool = True
# ) -> Optional[UserSkill]:
#     """
#     Update a specific skill for a user.

#     Args:
#         session (AsyncSession): The database session
#         user_id (int): The user's ID
#         skill_name (str): The name of the skill to update
#         skill_value (int): The new value for the skill
#         commit (bool, optional): Whether to commit the transaction. Defaults to True.

#     Returns:
#         Optional[UserSkill]: The updated UserSkill object or None on error
#     """
#     try:
#         # Get existing skills
#         user_skills = await get_user_skills(session, user_id)

#         if not user_skills:
#             # Create new skills record with the specified skill
#             skills_data = {skill_name: skill_value}
#             user_skills, _ = await create_or_update_user_skills(
#                 session, user_id, skills_data, commit=False
#             )
#         else:
#             # Update existing skills record
#             skills_data = dict(user_skills.skills_data)
#             skills_data[skill_name] = skill_value
#             user_skills.skills_data = skills_data
#             user_skills.last_updated = datetime.utcnow()
#             session.add(user_skills)

#         if commit:
#             await session.commit()
#             await session.refresh(user_skills)

#         return user_skills
#     except Exception as e:
#         await session.rollback()
#         print(f"Error updating user skill: {e}")
#         return None

# # ============ USER ABILITIES FUNCTIONS ============

# async def get_user_abilities(session: AsyncSession, user_id: int) -> Optional[UserAbilities]:
#     """
#     Get the abilities for a specific user.

#     Args:
#         session (AsyncSession): The database session
#         user_id (int): The user's ID

#     Returns:
#         Optional[UserAbilities]: The user's abilities record or None if not found
#     """
#     try:
#         statement = select(UserAbilities).where(UserAbilities.user_id == user_id)
#         result = await session.execute(statement)
#         return result.scalars().first()
#     except Exception as e:
#         print(f"Error getting user abilities: {e}")
#         return None

# async def create_or_update_user_abilities(
#     session: AsyncSession, 
#     user_id: int, 
#     abilities_data: Dict[str, List[str]], 
#     commit: bool = True
# ) -> Tuple[Optional[UserAbilities], bool]:
#     """
#     Create or update the abilities for a user.

#     Args:
#         session (AsyncSession): The database session
#         user_id (int): The user's ID
#         abilities_data (Dict[str, List[str]]): Dictionary of ability categories and their values
#         commit (bool, optional): Whether to commit the transaction. Defaults to True.

#     Returns:
#         Tuple[Optional[UserAbilities], bool]: The UserAbilities object and a boolean indicating whether it was created (True) 
#                                              or updated (False). Returns (None, False) on error.
#     """
#     try:
#         # Check if user exists
#         user_statement = select(User).where(User.id == user_id)
#         user_result = await session.execute(user_statement)
#         user = user_result.scalars().first()

#         if not user:
#             print(f"User with ID {user_id} not found")
#             return None, False

#         # Check if user abilities record already exists
#         existing_abilities = await get_user_abilities(session, user_id)
#         created = False

#         if existing_abilities:
#             # Update existing record
#             existing_abilities.abilities_data = abilities_data
#             existing_abilities.last_updated = datetime.utcnow()
#             session.add(existing_abilities)
#             user_abilities = existing_abilities
#         else:
#             # Create new record
#             user_abilities = UserAbilities(
#                 user_id=user_id,
#                 abilities_data=abilities_data,
#                 last_updated=datetime.utcnow()
#             )
#             session.add(user_abilities)
#             created = True

#         if commit:
#             await session.commit()
#             await session.refresh(user_abilities)

#         return user_abilities, created
#     except IntegrityError:
#         await session.rollback()
#         print(f"Integrity error creating/updating user abilities for user {user_id}")
#         return None, False
#     except OperationalError as e:
#         await session.rollback()
#         print(f"Database operation error: {e}")
#         return None, False
#     except Exception as e:
#         await session.rollback()
#         print(f"Unexpected error creating/updating user abilities: {e}")
#         return None, False

# async def update_ability_category(
#     session: AsyncSession, 
#     user_id: int, 
#     category: str, 
#     abilities: List[str],
#     commit: bool = True
# ) -> Optional[UserAbilities]:
#     """
#     Update a specific ability category for a user.

#     Args:
#         session (AsyncSession): The database session
#         user_id (int): The user's ID
#         category (str): The category to update (e.g., "WantToLearn", "Strong", etc.)
#         abilities (List[str]): The list of abilities for the category
#         commit (bool, optional): Whether to commit the transaction. Defaults to True.

#     Returns:
#         Optional[UserAbilities]: The updated UserAbilities object or None on error
#     """
#     try:
#         # Get existing abilities
#         user_abilities = await get_user_abilities(session, user_id)

#         if not user_abilities:
#             # Create new abilities record with the specified category
#             abilities_data = {category: abilities}
#             user_abilities, _ = await create_or_update_user_abilities(
#                 session, user_id, abilities_data, commit=False
#             )
#         else:
#             # Update existing abilities record
#             abilities_data = dict(user_abilities.abilities_data)
#             abilities_data[category] = abilities
#             user_abilities.abilities_data = abilities_data
#             user_abilities.last_updated = datetime.utcnow()
#             session.add(user_abilities)

#         if commit:
#             await session.commit()
#             await session.refresh(user_abilities)

#         return user_abilities
#     except Exception as e:
#         await session.rollback()
#         print(f"Error updating user ability category: {e}")
#         return None

# async def add_ability_to_category(
#     session: AsyncSession, 
#     user_id: int, 
#     category: str, 
#     ability: str,
#     commit: bool = True
# ) -> Optional[UserAbilities]:
#     """
#     Add a single ability to a category for a user.

#     Args:
#         session (AsyncSession): The database session
#         user_id (int): The user's ID
#         category (str): The category to update
#         ability (str): The ability to add
#         commit (bool, optional): Whether to commit the transaction. Defaults to True.

#     Returns:
#         Optional[UserAbilities]: The updated UserAbilities object or None on error
#     """
#     try:
#         # Get existing abilities
#         user_abilities = await get_user_abilities(session, user_id)

#         if not user_abilities:
#             # Create new abilities record with the specified category and ability
#             abilities_data = {category: [ability]}
#             user_abilities, _ = await create_or_update_user_abilities(
#                 session, user_id, abilities_data, commit=False
#             )
#         else:
#             # Update existing abilities record
#             abilities_data = dict(user_abilities.abilities_data)
#             if category not in abilities_data:
#                 abilities_data[category] = []

#             # Only add if not already in the list
#             if ability not in abilities_data[category]:
#                 abilities_data[category].append(ability)

#             user_abilities.abilities_data = abilities_data
#             user_abilities.last_updated = datetime.utcnow()
#             session.add(user_abilities)

#         if commit:
#             await session.commit()
#             await session.refresh(user_abilities)

#         return user_abilities
#     except Exception as e:
#         await session.rollback()
#         print(f"Error adding ability to category: {e}")
#         return None

# async def remove_ability_from_category(
#     session: AsyncSession, 
#     user_id: int, 
#     category: str, 
#     ability: str,
#     commit: bool = True
# ) -> Optional[UserAbilities]:
#     """
#     Remove a single ability from a category for a user.

#     Args:
#         session (AsyncSession): The database session
#         user_id (int): The user's ID
#         category (str): The category to update
#         ability (str): The ability to remove
#         commit (bool, optional): Whether to commit the transaction. Defaults to True.

#     Returns:
#         Optional[UserAbilities]: The updated UserAbilities object or None on error
#     """
#     try:
#         # Get existing abilities
#         user_abilities = await get_user_abilities(session, user_id)

#         if not user_abilities or category not in user_abilities.abilities_data:
#             # Nothing to remove
#             return user_abilities

#         # Update existing abilities record
#         abilities_data = dict(user_abilities.abilities_data)
#         if ability in abilities_data[category]:
#             abilities_data[category].remove(ability)

#         user_abilities.abilities_data = abilities_data
#         user_abilities.last_updated = datetime.utcnow()
#         session.add(user_abilities)

#         if commit:
#             await session.commit()
#             await session.refresh(user_abilities)

#         return user_abilities
#     except Exception as e:
#         await session.rollback()
#         print(f"Error removing ability from category: {e}")
#         return None

# async def move_ability_between_categories(
#     session: AsyncSession, 
#     user_id: int, 
#     ability: str,
#     from_category: str, 
#     to_category: str,
#     commit: bool = True
# ) -> Optional[UserAbilities]:
#     """
#     Move an ability from one category to another.

#     Args:
#         session (AsyncSession): The database session
#         user_id (int): The user's ID
#         ability (str): The ability to move
#         from_category (str): The source category
#         to_category (str): The destination category
#         commit (bool, optional): Whether to commit the transaction. Defaults to True.

#     Returns:
#         Optional[UserAbilities]: The updated UserAbilities object or None on error
#     """
#     try:
#         # Get existing abilities
#         user_abilities = await get_user_abilities(session, user_id)

#         if not user_abilities:
#             # Create new abilities record with the ability in the destination category
#             abilities_data = {to_category: [ability]}
#             user_abilities, _ = await create_or_update_user_abilities(
#                 session, user_id, abilities_data, commit=False
#             )
#             return user_abilities

#         # Update existing abilities record
#         abilities_data = dict(user_abilities.abilities_data)

#         # Remove from source category if it exists
#         if from_category in abilities_data and ability in abilities_data[from_category]:
#             abilities_data[from_category].remove(ability)

#         # Add to destination category
#         if to_category not in abilities_data:
#             abilities_data[to_category] = []

#         if ability not in abilities_data[to_category]:
#             abilities_data[to_category].append(ability)

#         user_abilities.abilities_data = abilities_data
#         user_abilities.last_updated = datetime.utcnow()
#         session.add(user_abilities)

#         if commit:
#             await session.commit()
#             await session.refresh(user_abilities)

#         return user_abilities
#     except Exception as e:
#         await session.rollback()
#         print(f"Error moving ability between categories: {e}")
#         return None

