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
    RoomEnvGameData,
)

# === Scenario Game ===
async def get_scenario_game_data(session: AsyncSession, user_id: int) -> Optional[ScenarioGameData]:
    try:
        stmt = select(ScenarioGameData).where(ScenarioGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting scenario game data: {e}")
        return None
    
async def upsert_scenario_game_data(session: AsyncSession, user_id: int, payload: dict):
    stmt = select(ScenarioGameData).where(ScenarioGameData.user_id == user_id)
    result = await session.execute(stmt)
    data = result.scalars().first()

    if data:
        for key, value in payload.items():
            setattr(data, key, value)
    else:
        data = ScenarioGameData(user_id=user_id, **payload)
        session.add(data)

    await session.commit()
    return data

# === Shape Sequence Game ===
async def get_shape_sequence_game_data(session: AsyncSession, user_id: int) -> Optional[ShapeSequenceGameData]:
    try:
        stmt = select(ShapeSequenceGameData).where(ShapeSequenceGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting shape sequence game data: {e}")
        return None
    
async def upsert_shape_sequence_game_data(session: AsyncSession, user_id: int, payload: dict):
    stmt = select(ShapeSequenceGameData).where(ShapeSequenceGameData.user_id == user_id)
    result = await session.execute(stmt)
    data = result.scalars().first()

    if data:
        for key, value in payload.items():
            setattr(data, key, value)
    else:
        data = ShapeSequenceGameData(user_id=user_id, **payload)
        session.add(data)

    await session.commit()
    return data

# === Jobs Game ===
async def get_jobs_game_data(session: AsyncSession, user_id: int) -> Optional[JobsGameData]:
    try:
        stmt = select(JobsGameData).where(JobsGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting jobs game data: {e}")
        return None
    
async def upsert_jobs_game_data(session: AsyncSession, user_id: int, payload: dict):
    stmt = select(JobsGameData).where(JobsGameData.user_id == user_id)
    result = await session.execute(stmt)
    data = result.scalars().first()

    if data:
        for key, value in payload.items():
            setattr(data, key, value)
    else:
        data = JobsGameData(user_id=user_id, **payload)
        session.add(data)

    await session.commit()
    return data

# === Speed Game ===
async def get_speed_game_data(session: AsyncSession, user_id: int) -> Optional[SpeedGameData]:
    try:
        stmt = select(SpeedGameData).where(SpeedGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting speed game data: {e}")
        return None
    
async def upsert_speed_game_data(session: AsyncSession, user_id: int, payload: dict):
    stmt = select(SpeedGameData).where(SpeedGameData.user_id == user_id)
    result = await session.execute(stmt)
    data = result.scalars().first()

    if data:
        for key, value in payload.items():
            setattr(data, key, value)
    else:
        data = SpeedGameData(user_id=user_id, **payload)
        session.add(data)

    await session.commit()
    return data

# === Abilities Game ===
async def get_abilities_game_data(session: AsyncSession, user_id: int) -> Optional[AbilitiesGameData]:
    try:
        stmt = select(AbilitiesGameData).where(AbilitiesGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting abilities game data: {e}")
        return None
    
async def upsert_abilities_game_data(session: AsyncSession, user_id: int, payload: dict):
    stmt = select(AbilitiesGameData).where(AbilitiesGameData.user_id == user_id)
    result = await session.execute(stmt)
    data = result.scalars().first()

    if data:
        for key, value in payload.items():
            setattr(data, key, value)
    else:
        data = AbilitiesGameData(user_id=user_id, **payload)
        session.add(data)

    await session.commit()
    return data

# === Skills Game ===
async def get_skills_game_data(session: AsyncSession, user_id: int) -> Optional[SkillsGameData]:
    try:
        stmt = select(SkillsGameData).where(SkillsGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting skills game data: {e}")
        return None
    
async def upsert_skills_game_data(session: AsyncSession, user_id: int, payload: dict):
    stmt = select(SkillsGameData).where(SkillsGameData.user_id == user_id)
    result = await session.execute(stmt)
    data = result.scalars().first()

    if data:
        for key, value in payload.items():
            setattr(data, key, value)
    else:
        data = SkillsGameData(user_id=user_id, **payload)
        session.add(data)

    await session.commit()
    return data

# === Room Environment Game ===
async def get_room_env_game_data(session: AsyncSession, user_id: int) -> Optional[RoomEnvGameData]:
    try:
        stmt = select(RoomEnvGameData).where(RoomEnvGameData.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        print(f"Error getting room environment game data: {e}")
        return None

async def upsert_room_env_game_data(session: AsyncSession, user_id: int, payload: dict):
    stmt = select(RoomEnvGameData).where(RoomEnvGameData.user_id == user_id)
    result = await session.execute(stmt)
    data = result.scalars().first()

    if data:
        for key, value in payload.items():
            setattr(data, key, value)
    else:
        data = RoomEnvGameData(user_id=user_id, **payload)
        session.add(data)

    await session.commit()
    return data