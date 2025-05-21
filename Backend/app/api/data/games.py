
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

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
    get_room_env_game_data,
    upsert_scenario_game_data,
    upsert_shape_sequence_game_data,
    upsert_jobs_game_data,
    upsert_speed_game_data,
    upsert_abilities_game_data,
    upsert_skills_game_data,
    upsert_room_env_game_data,
)
from pydantic import BaseModel, Field
from typing import Dict, Optional

# === Shared ===
class BaseGamePost(BaseModel):
    completion: float = Field(..., ge=0.0, le=1.0)

class BaseGameResponse(BaseModel):
    completion: float = Field(..., description="Game completion percentage (0.0 to 1.0)")
    message: str = Field("Success", description="Response message")


# === Scenario Game ===
class ScenarioGamePost(BaseGamePost):
    current_level: int
    traits: Dict = {}
    penalties: Dict = {}

# === Shape Sequence ===
class ShapeSequencePost(BaseGamePost):
    levelResults: Dict = {}

# === Jobs ===
class JobsPost(BaseGamePost):
    jobChoices: Dict = {}

# === Speed ===
class SpeedPost(BaseGamePost):
    current_level: int = 0
    levelStats: Dict = {}

# === Abilities ===
class AbilitiesPost(BaseGamePost):
    skillAssessment: Dict = {}

# === Skills ===
class SkillsPost(BaseGamePost):
    skillsAssessment: Dict = {}

class RoomEnvPost(BaseGamePost):
    roomData: List[Dict] = Field(default_factory=list, description="Room environment configuration items")

## === Response Models ===
class ScenarioGameResponse(BaseGameResponse):
    current_level: int = Field(..., description="Current level in the scenario game")
    traits: Dict[str, int] = Field(default_factory=dict, description="Player traits and their values")
    penalties: Dict[str, Any] = Field(default_factory=dict, description="Penalty information")
    
class ShapeSequenceResponse(BaseGameResponse):
    levelResults: Dict[str, Any] = Field(default_factory=dict, description="Results for each completed level")
    current_level: int = Field(..., description="Current level in the shape sequence game")
class JobsGameResponse(BaseGameResponse):
    jobChoices: Dict[str, Any] = Field(default_factory=dict, description="User's job selections and preferences")
    
class SpeedGameResponse(BaseGameResponse):
    current_level: int = Field(0, description="Current level in the speed game")
    levelStats: Dict[str, Any] = Field(default_factory=dict, description="Statistics for each completed level")
    
class AbilitiesGameResponse(BaseGameResponse):
    skillAssessment: Dict[str, Any] = Field(default_factory=dict, description="User's ability self-assessment")
    
class SkillsGameResponse(BaseGameResponse):
    skillsAssessment: Dict[str, Any] = Field(default_factory=dict, description="User's skills assessment data")

class RoomEnvGameResponse(BaseGameResponse):
    roomData: List[Dict[str, Any]] = Field(default_factory=list, description="Room environment configuration items")


games_router = APIRouter(prefix="/games", tags=["Games"])

# === Scenario Game === /games/scenario
@games_router.get("/scenario", response_model=ScenarioGameResponse)
@secured_endpoint()
async def get_scenario_data(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_scenario_game_data(session, user_id)
    if not data:
        return ScenarioGameResponse(
            message="No scenario game data found",
            current_level=0,
            completion=0.0,
            traits={},
            penalties={}
        )

    return ScenarioGameResponse(
        current_level=data.current_level,
        completion=data.completion,
        traits=data.traits,
        penalties=data.penalties,
    )

@games_router.post("/scenario")
@secured_endpoint()
async def post_scenario_data(payload: ScenarioGamePost, jwt: dict, session: AsyncSession = Depends(getSession)):
    data = await upsert_scenario_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Scenario game data saved", "data": data.__dict__}


# === Shape Sequence Game ===
@games_router.get("/shape-sequence", response_model=ShapeSequenceResponse)
@secured_endpoint()
async def get_shape_sequence_data(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_shape_sequence_game_data(session, user_id)
    if not data:
        return ShapeSequenceResponse(
            message="No shape sequence game data found",
            completion=0.0,
            levelResults={}
        )

    return ShapeSequenceResponse(
        completion=data.completion,
        levelResults=data.levelResults,
        current_level=data.current_level,
    )

@games_router.post("/shape-sequence")
@secured_endpoint()
async def post_shape_sequence_data(payload: ShapeSequencePost, jwt: dict, session: AsyncSession = Depends(getSession)):
    data = await upsert_shape_sequence_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Shape sequence game data saved", "data": data.__dict__}


# === Jobs Game ===
@games_router.get("/jobs", response_model=JobsGameResponse)
@secured_endpoint()
async def get_jobs_data(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_jobs_game_data(session, user_id)
    if not data:
        return JobsGameResponse(
            message="No jobs game data found",
            completion=0.0,
            jobChoices={}
        )

    return JobsGameResponse(
        completion=data.completion,
        jobChoices=data.jobChoices,
    )

@games_router.post("/jobs")
@secured_endpoint()
async def post_jobs_data(payload: JobsPost, jwt: dict, session: AsyncSession = Depends(getSession)):
    data = await upsert_jobs_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Jobs game data saved", "data": data.__dict__}


# === Speed Game ===
@games_router.get("/speed", response_model=SpeedGameResponse)
@secured_endpoint()
async def get_speed_data(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_speed_game_data(session, user_id)
    if not data:
        return SpeedGameResponse(
            message="No speed game data found",
            completion=0.0,
            current_level=0,
            levelStats={}
        )

    return SpeedGameResponse(
        completion=data.completion,
        current_level=data.current_level,
        levelStats=data.levelStats,
    )


@games_router.post("/speed")
@secured_endpoint()
async def post_speed_data(payload: SpeedPost, jwt: dict, session: AsyncSession = Depends(getSession)):
    data = await upsert_speed_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Speed game data saved", "data": data.__dict__}


# === Abilities Game ===
@games_router.get("/abilities", response_model=AbilitiesGameResponse)
@secured_endpoint()
async def get_abilities_game_data_endpoint(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_abilities_game_data(session, user_id)
    if not data:
        return AbilitiesGameResponse(
            message="No abilities game data found",
            completion=0.0,
            skillAssessment={}
        )

    return AbilitiesGameResponse(
        completion=data.completion,
        skillAssessment=data.skillAssessment,
    )

@games_router.post("/abilities")
@secured_endpoint()
async def post_abilities_data(payload: AbilitiesPost, jwt: dict, session: AsyncSession = Depends(getSession)):
    data = await upsert_abilities_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Abilities game data saved", "data": data.__dict__}

# === Skills Game ===
@games_router.get("/skills", response_model=SkillsGameResponse)
@secured_endpoint()
async def get_skills_game_data_endpoint(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_skills_game_data(session, user_id)
    if not data:
        return SkillsGameResponse(
            message="No skills game data found",
            completion=0.0,
            skillsAssessment={}
        )

    return SkillsGameResponse(
        completion=data.completion,
        skillsAssessment=data.skillsAssessment,
    )

@games_router.post("/skills")
@secured_endpoint()
async def post_skills_data(payload: SkillsPost, jwt: dict, session: AsyncSession = Depends(getSession)):
    data = await upsert_skills_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Skills game data saved", "data": data.__dict__}

# Add the RoomEnv game endpoint
@games_router.get("/room-env", response_model=RoomEnvGameResponse)
@secured_endpoint()
async def get_room_env_data(jwt: dict, session: AsyncSession = Depends(getSession)):
    user_id = jwt["sub"]
    data = await get_room_env_game_data(session, user_id)
    if not data:
        return RoomEnvGameResponse(
            message="No room environment data found",
            completion=0.0,
            roomData=[]
        )

    return RoomEnvGameResponse(
        completion=data.completion,
        roomData=data.roomData,
    )

@games_router.post("/room-env")
@secured_endpoint()
async def post_room_env_data(payload: RoomEnvPost, jwt: dict, session: AsyncSession = Depends(getSession)):
    # You'll need to implement this repository function
    data = await upsert_room_env_game_data(session, jwt["sub"], payload.model_dump())
    return {"message": "Room environment data saved", "data": data.__dict__}

# Register the router with the main application
AddRouter(games_router)