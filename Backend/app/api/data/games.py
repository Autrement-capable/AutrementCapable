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
)

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

# Register router
AddRouter(games_router)
