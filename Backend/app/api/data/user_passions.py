from typing import Dict, List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.application import AddRouter
from ...core.security.decorators import secured_endpoint
from ...db.postgress.engine import getSession
from ...db.postgress.repositories.user_passions import (
    get_user_passions,
    create_user_passion,
    update_user_passion,
    delete_user_passion,
    reorder_user_passions
)
# ============ Pydantic Models for Request/Response ============

class PassionCreate(BaseModel):
    """Model for creating a passion"""
    passion_text: str = Field(..., description="Text describing the passion")
    order: int = Field(..., description="Order of the passion (1, 2, 3)")

class PassionUpdate(BaseModel):
    """Model for updating a passion"""
    passion_text: Optional[str] = Field(None, description="Text describing the passion")
    order: Optional[int] = Field(None, description="Order of the passion (1, 2, 3)")

class PassionResponse(BaseModel):
    """Model for passion response"""
    id: int
    passion_text: str
    order: int

class PassionList(BaseModel):
    """Model for list of passions"""
    passions: List[PassionResponse]

class PassionReorder(BaseModel):
    """Model for reordering passions"""
    passion_orders: Dict[int, int] = Field(..., description="Dictionary of passion IDs to new orders")

# ============ Router ============

passions_router = APIRouter(prefix="/user/passions", tags=["User Passions"])

# ============ Endpoints ============

@passions_router.get("", response_model=PassionList)
@secured_endpoint()
async def get_my_passions(
    jwt: dict,
    session: AsyncSession = Depends(getSession)
):
    """Get the current user's passions"""
    user_id = jwt["sub"]
    passions = await get_user_passions(session, user_id)

    return {"passions": [
        {"id": p.id, "passion_text": p.passion_text, "order": p.order}
        for p in passions
    ]}

@passions_router.post("", response_model=PassionResponse, status_code=status.HTTP_201_CREATED)
@secured_endpoint()
async def create_passion(
    passion: PassionCreate,
    jwt: dict,
    session: AsyncSession = Depends(getSession)
):
    """Create a new passion for the current user"""
    user_id = jwt["sub"]

    # Check if they already have 3 passions
    existing_passions = await get_user_passions(session, user_id)
    if len(existing_passions) >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum of 3 passions allowed"
        )

    # Create the passion
    new_passion = await create_user_passion(
        session, user_id, passion.passion_text, passion.order
    )

    if not new_passion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create passion. Order may already be in use."
        )

    return {
        "id": new_passion.id,
        "passion_text": new_passion.passion_text,
        "order": new_passion.order
    }

@passions_router.patch("/{passion_id}", response_model=PassionResponse)
@secured_endpoint()
async def update_passion(
    passion_update: PassionUpdate,
    jwt: dict,
    session: AsyncSession = Depends(getSession),
    passion_id: int = Path(..., description="The ID of the passion to update"),
):
    """Update a passion for the current user"""
    user_id = jwt["sub"]

    # Verify the passion belongs to the user
    passions = await get_user_passions(session, user_id)
    if not any(p.id == passion_id for p in passions):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Passion not found"
        )

    # Update the passion
    updated_passion = await update_user_passion(
        session, passion_id, passion_update.passion_text, passion_update.order
    )

    if not updated_passion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update passion. Order may already be in use."
        )

    return {
        "id": updated_passion.id,
        "passion_text": updated_passion.passion_text,
        "order": updated_passion.order
    }

@passions_router.delete("/{passion_id}", status_code=status.HTTP_204_NO_CONTENT)
@secured_endpoint()
async def delete_passion(
    jwt: dict,
    session: AsyncSession = Depends(getSession),
    passion_id: int = Path(..., description="The ID of the passion to delete"),
):
    """Delete a passion for the current user"""
    user_id = jwt["sub"]

    # Verify the passion belongs to the user
    passions = await get_user_passions(session, user_id)
    if not any(p.id == passion_id for p in passions):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Passion not found"
        )

    # Delete the passion
    success = await delete_user_passion(session, passion_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete passion"
        )

@passions_router.post("/reorder", response_model=PassionList)
@secured_endpoint()
async def reorder_passions(
    reorder_data: PassionReorder,
    jwt: dict,
    session: AsyncSession = Depends(getSession),
):
    """Reorder passions for the current user"""
    user_id = jwt["sub"]

    # Verify all passions belong to the user
    passions = await get_user_passions(session, user_id)
    passion_ids = {p.id for p in passions}

    for passion_id in reorder_data.passion_orders.keys():
        if passion_id not in passion_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Passion with ID {passion_id} not found"
            )

    # Reorder the passions
    success = await reorder_user_passions(
        session, user_id, reorder_data.passion_orders
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reorder passions"
        )

    # Get updated passions
    updated_passions = await get_user_passions(session, user_id)

    return {"passions": [
        {"id": p.id, "passion_text": p.passion_text, "order": p.order}
        for p in updated_passions
    ]}

# Add the router to the app
AddRouter(passions_router)