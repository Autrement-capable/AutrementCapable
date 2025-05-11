from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.test_model import (
    ScenarioGameData,
    ShapeSequenceGameData,
    JobsGameData,
    SpeedGameData,
    AbilitiesGameData,
    SkillsGameData,
)

# new styling for python 3.11
# Option[thing] == thing | None

# === Scenario Game ===
async def get_scenario_game_data(session: AsyncSession, user_id: int) -> Optional[ScenarioGameData]:
    try:
        stmt = select(ScenarioGameData).where(ScenarioGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting scenario game data: {e}")
        return None

# === Shape Sequence Game ===
async def get_shape_sequence_game_data(session: AsyncSession, user_id: int) -> Optional[ShapeSequenceGameData]:
    try:
        stmt = select(ShapeSequenceGameData).where(ShapeSequenceGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting shape sequence game data: {e}")
        return None

# === Jobs Game ===
async def get_jobs_game_data(session: AsyncSession, user_id: int) -> Optional[JobsGameData]:
    try:
        stmt = select(JobsGameData).where(JobsGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting jobs game data: {e}")
        return None

# === Speed Game ===
async def get_speed_game_data(session: AsyncSession, user_id: int) -> Optional[SpeedGameData]:
    try:
        stmt = select(SpeedGameData).where(SpeedGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting speed game data: {e}")
        return None

# === Abilities Game ===
async def get_abilities_game_data(session: AsyncSession, user_id: int) -> Optional[AbilitiesGameData]:
    try:
        stmt = select(AbilitiesGameData).where(AbilitiesGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting abilities game data: {e}")
        return None

# === Skills Game ===
async def get_skills_game_data(session: AsyncSession, user_id: int) -> Optional[SkillsGameData]:
    try:
        stmt = select(SkillsGameData).where(SkillsGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting skills game data: {e}")
        return None
