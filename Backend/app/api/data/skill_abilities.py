from typing import Dict, List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.application import AddRouter
from ...core.security.token_creation import JWTBearer
from ...core.security.decorators import secured_endpoint
from ...db.postgress.engine import getSession
from ...db.postgress.repositories.ability_skills_user import (
    get_user_skills,
    create_or_update_user_skills,
    update_specific_user_skill,
    get_user_abilities,
    create_or_update_user_abilities,
    update_ability_category,
    add_ability_to_category,
    remove_ability_from_category,
    move_ability_between_categories
)

# ============ Pydantic Models for Request/Response ============

class SkillsData(BaseModel):
    """Model for skills data with skill names as keys and integer values"""
    skills: Dict[str, int] = Field(..., description="Dictionary of skills with name as key and integer value")

class SkillUpdate(BaseModel):
    """Model for updating a single skill"""
    skill_name: str = Field(..., description="Name of the skill to update")
    skill_value: int = Field(..., description="New value for the skill")

class AbilitiesData(BaseModel):
    """Model for abilities data with category names as keys and lists of abilities as values"""
    abilities: Dict[str, List[str]] = Field(..., description="Dictionary of ability categories with lists of abilities")

class AbilityCategoryUpdate(BaseModel):
    """Model for updating an entire ability category"""
    category: str = Field(..., description="Name of the category to update")
    abilities: List[str] = Field(..., description="List of abilities for this category")

class AbilityUpdate(BaseModel):
    """Model for adding or removing a single ability"""
    category: str = Field(..., description="Category name")
    ability: str = Field(..., description="Ability name")

class AbilityMove(BaseModel):
    """Model for moving an ability between categories"""
    ability: str = Field(..., description="Ability name to move")
    from_category: str = Field(..., description="Source category")
    to_category: str = Field(..., description="Destination category")

# ============ Routers ============

skills_router = APIRouter(prefix="/skills", tags=["Skills"])
abilities_router = APIRouter(prefix="/abilities", tags=["Abilities"])

# ============ Skills Endpoints ============

@skills_router.get("", response_model=Dict[str, Any])
@secured_endpoint
async def get_my_skills(
    session: AsyncSession = Depends(getSession), 
    jwt: dict = Depends(JWTBearer())
):
    """Get the current user's skills"""
    user_id = jwt["payload"]["sub"]
    user_skills = await get_user_skills(session, user_id)

    if not user_skills:
        return {"skills": {}, "last_updated": None}

    return {
        "skills": user_skills.skills_data,
        "last_updated": user_skills.last_updated.isoformat()
    }

@skills_router.put("", response_model=Dict[str, Any])
@secured_endpoint
async def update_my_skills(
    skills_data: SkillsData,
    session: AsyncSession = Depends(getSession), 
    jwt: dict = Depends(JWTBearer())
):
    """Update all skills for the current user"""
    user_id = jwt["payload"]["sub"]
    user_skills, _ = await create_or_update_user_skills(session, user_id, skills_data.skills)

    if not user_skills:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update skills"
        )

    return {
        "message": "Skills updated successfully",
        "skills": user_skills.skills_data,
        "last_updated": user_skills.last_updated.isoformat()
    }

@skills_router.patch("", response_model=Dict[str, Any])
@secured_endpoint
async def update_single_skill(
    skill_update: SkillUpdate,
    session: AsyncSession = Depends(getSession), 
    jwt: dict = Depends(JWTBearer())
):
    """Update a single skill for the current user"""
    user_id = jwt["payload"]["sub"]
    user_skills = await update_specific_user_skill(
        session, user_id, skill_update.skill_name, skill_update.skill_value
    )

    if not user_skills:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update skill"
        )

    return {
        "message": f"Skill '{skill_update.skill_name}' updated successfully",
        "skills": user_skills.skills_data,
        "last_updated": user_skills.last_updated.isoformat()
    }

# ============ Abilities Endpoints ============

@abilities_router.get("", response_model=Dict[str, Any])
@secured_endpoint
async def get_my_abilities(
    session: AsyncSession = Depends(getSession), 
    jwt: dict = Depends(JWTBearer())
):
    """Get the current user's abilities"""
    user_id = jwt["payload"]["sub"]
    user_abilities = await get_user_abilities(session, user_id)

    if not user_abilities:
        return {"abilities": {}, "last_updated": None}

    return {
        "abilities": user_abilities.abilities_data,
        "last_updated": user_abilities.last_updated.isoformat()
    }

@abilities_router.put("", response_model=Dict[str, Any])
@secured_endpoint
async def update_my_abilities(
    abilities_data: AbilitiesData,
    session: AsyncSession = Depends(getSession), 
    jwt: dict = Depends(JWTBearer())
):
    """Update all abilities for the current user"""
    user_id = jwt["payload"]["sub"]
    user_abilities, _ = await create_or_update_user_abilities(session, user_id, abilities_data.abilities)

    if not user_abilities:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update abilities"
        )

    return {
        "message": "Abilities updated successfully",
        "abilities": user_abilities.abilities_data,
        "last_updated": user_abilities.last_updated.isoformat()
    }

@abilities_router.put("/category", response_model=Dict[str, Any])
@secured_endpoint
async def update_category(
    category_update: AbilityCategoryUpdate,
    session: AsyncSession = Depends(getSession), 
    jwt: dict = Depends(JWTBearer())
):
    """Update a complete category of abilities for the current user"""
    user_id = jwt["payload"]["sub"]
    user_abilities = await update_ability_category(
        session, user_id, category_update.category, category_update.abilities
    )

    if not user_abilities:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update ability category"
        )

    return {
        "message": f"Category '{category_update.category}' updated successfully",
        "abilities": user_abilities.abilities_data,
        "last_updated": user_abilities.last_updated.isoformat()
    }

@abilities_router.post("/add", response_model=Dict[str, Any])
@secured_endpoint
async def add_ability(
    ability_update: AbilityUpdate,
    session: AsyncSession = Depends(getSession), 
    jwt: dict = Depends(JWTBearer())
):
    """Add an ability to a category for the current user"""
    user_id = jwt["payload"]["sub"]
    user_abilities = await add_ability_to_category(
        session, user_id, ability_update.category, ability_update.ability
    )

    if not user_abilities:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add ability"
        )

    return {
        "message": f"Added '{ability_update.ability}' to category '{ability_update.category}'",
        "abilities": user_abilities.abilities_data,
        "last_updated": user_abilities.last_updated.isoformat()
    }

@abilities_router.post("/remove", response_model=Dict[str, Any])
@secured_endpoint
async def remove_ability(
    ability_update: AbilityUpdate,
    session: AsyncSession = Depends(getSession), 
    jwt: dict = Depends(JWTBearer())
):
    """Remove an ability from a category for the current user"""
    user_id = jwt["payload"]["sub"]
    user_abilities = await remove_ability_from_category(
        session, user_id, ability_update.category, ability_update.ability
    )

    if not user_abilities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ability or category not found"
        )

    return {
        "message": f"Removed '{ability_update.ability}' from category '{ability_update.category}'",
        "abilities": user_abilities.abilities_data,
        "last_updated": user_abilities.last_updated.isoformat()
    }

@abilities_router.post("/move", response_model=Dict[str, Any])
@secured_endpoint
async def move_ability(
    ability_move: AbilityMove,
    session: AsyncSession = Depends(getSession), 
    jwt: dict = Depends(JWTBearer())
):
    """Move an ability from one category to another for the current user"""
    user_id = jwt["payload"]["sub"]
    user_abilities = await move_ability_between_categories(
        session, 
        user_id, 
        ability_move.ability,
        ability_move.from_category, 
        ability_move.to_category
    )

    if not user_abilities:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to move ability"
        )

    return {
        "message": f"Moved '{ability_move.ability}' from '{ability_move.from_category}' to '{ability_move.to_category}'",
        "abilities": user_abilities.abilities_data,
        "last_updated": user_abilities.last_updated.isoformat()
    }

# Add routers to the application
AddRouter(skills_router)
AddRouter(abilities_router)