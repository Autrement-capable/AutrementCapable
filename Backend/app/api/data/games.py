# app/api/endpoints/games.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from ...core.application import AddRouter
from ...core.security.decorators import secured_endpoint
from ...db.postgress.engine import getSession
from ...db.postgress.repositories.games_data import (
    get_scenario_game_data,
    get_shape_sequence_game_data,
    get_jobs_game_data,
    get_speed_game_data,
    get_abilities_game_data,
    get_skills_game_data,
    upsert_scenario_game_data,
    upsert_shape_sequence_game_data,
    upsert_jobs_game_data,
    upsert_speed_game_data,
    upsert_abilities_game_data,
    upsert_skills_game_data,
)
from pydantic import BaseModel, Field
from typing import Dict

# === Shared ===
class BaseGamePost(BaseModel):
    completion: float = Field(..., ge=0.0, le=1.0)

# === Scenario Game ===
class ScenarioGamePost(BaseGamePost):
    current_level: int
    traits: Dict = {}
    penalties: Dict = {}

# === Shape Sequence ===
class ShapeSequencePost(BaseGamePost):
    highest_level: int

# === Jobs ===
class JobsPost(BaseGamePost):
    pass

# === Speed ===
class SpeedPost(BaseGamePost):
    wpm: int

# === Abilities ===
class AbilitiesPost(BaseGamePost):
    abilities: Dict

# === Skills ===
class SkillsPost(BaseGamePost):
    skills: Dict

games_router = APIRouter(prefix="/games", tags=["Games"])

# === Scenario Game === /games/scenario
@games_router.get("/scenario", response_model=Dict[str, Any])
@secured_endpoint()
async def get_scenario_data(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_scenario_game_data(session, user_id)
    if not data:
        return {"message": "No scenario game data found", "data": None}

    return {
        "current_level": data.current_level,
        "completion": data.completion,
        "traits": data.traits,
        "penalties": data.penalties,
    }

@games_router.post("/scenario")
@secured_endpoint()
async def post_scenario_data(payload: ScenarioGamePost, jwt: dict, session: AsyncSession = Depends(getSession)):
    data = await upsert_scenario_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Scenario game data saved", "data": data.__dict__}


# === Shape Sequence Game ===
@games_router.get("/shape-sequence", response_model=Dict[str, Any])
@secured_endpoint()
async def get_shape_sequence_data(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_shape_sequence_game_data(session, user_id)
    if not data:
        return {"message": "No shape sequence game data found", "data": None}

    return {
        "completion": data.completion,
        "highest_level": data.highest_level,
    }

@games_router.post("/shape-sequence")
@secured_endpoint()
async def post_shape_sequence_data(payload: ShapeSequencePost, jwt: dict, session: AsyncSession = Depends(getSession)):
    data = await upsert_shape_sequence_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Shape sequence game data saved", "data": data.__dict__}


# === Jobs Game ===
@games_router.get("/jobs", response_model=Dict[str, Any])
@secured_endpoint()
async def get_jobs_data(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_jobs_game_data(session, user_id)
    if not data:
        return {"message": "No jobs game data found", "data": None}

    return {
        "completion": data.completion,
    }

@games_router.post("/jobs")
@secured_endpoint()
async def post_jobs_data(payload: JobsPost, jwt: dict, session: AsyncSession = Depends(getSession)):
    data = await upsert_jobs_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Jobs game data saved", "data": data.__dict__}


# === Speed Game ===
@games_router.get("/speed", response_model=Dict[str, Any])
@secured_endpoint()
async def get_speed_data(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_speed_game_data(session, user_id)
    if not data:
        return {"message": "No speed game data found", "data": None}

    return {
        "completion": data.completion,
        "wpm": data.wpm,
    }

@games_router.post("/speed")
@secured_endpoint()
async def post_speed_data(payload: SpeedPost, jwt: dict, session: AsyncSession = Depends(getSession)):
    data = await upsert_speed_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Speed game data saved", "data": data.__dict__}


# === Abilities Game ===
@games_router.get("/abilities", response_model=Dict[str, Any])
@secured_endpoint()
async def get_abilities_game_data_endpoint(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_abilities_game_data(session, user_id)
    if not data:
        return {"message": "No abilities game data found", "data": None}

    return {
        "completion": data.completion,
        "abilities": data.abilities,
    }

@games_router.post("/abilities")
@secured_endpoint()
async def post_abilities_data(payload: AbilitiesPost, jwt: dict, session: AsyncSession = Depends(getSession)):
    data = await upsert_abilities_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Abilities game data saved", "data": data.__dict__}

# === Skills Game ===
@games_router.get("/skills", response_model=Dict[str, Any])
@secured_endpoint()
async def get_skills_game_data_endpoint(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_skills_game_data(session, user_id)
    if not data:
        return {"message": "No skills game data found", "data": None}

    return {
        "completion": data.completion,
        "skills": data.skills,
    }

@games_router.post("/skills")
@secured_endpoint()
async def post_skills_data(payload: SkillsPost, jwt: dict, session: AsyncSession = Depends(getSession)):
    data = await upsert_skills_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Skills game data saved", "data": data.__dict__}

# Register router
AddRouter(games_router)
