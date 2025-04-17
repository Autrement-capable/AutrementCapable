from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import Response
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.application import AddRouter
from ...core.security.token_creation import JWTBearer
from ...core.security.decorators import secured_endpoint
from ...db.postgress.engine import getSession
from ...db.postgress.repositories.user_pictures import (
    get_user_picture,
    create_or_update_user_picture,
    delete_user_picture
)

# ============ Router ============

pictures_router = APIRouter(prefix="/user/picture", tags=["User Pictures"])

# ============ Endpoints ============

@pictures_router.get("", response_class=Response)
@secured_endpoint
async def get_my_picture(
    picture_type: str = "profile",
    session: AsyncSession = Depends(getSession), 
    jwt: dict = Depends(JWTBearer())
):
    """Get the current user's picture"""
    user_id = jwt["payload"]["sub"]
    picture = await get_user_picture(session, user_id, picture_type)

    if not picture or not picture.picture_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No picture found"
        )

    # Determine content type (assuming it's always image/jpeg for simplicity)
    return Response(content=picture.picture_data, media_type="image/jpeg")

@pictures_router.post("", status_code=status.HTTP_201_CREATED)
@secured_endpoint
async def upload_picture(
    picture: UploadFile = File(...),
    picture_type: str = Form("profile"),
    session: AsyncSession = Depends(getSession), 
    jwt: dict = Depends(JWTBearer())
):
    """Upload a picture for the current user"""
    user_id = jwt["payload"]["sub"]

    # Validate file type
    if not picture.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )

    # Read the file
    picture_data = await picture.read()

    # Check file size (limit to 2MB)
    if len(picture_data) > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image size must be less than 2MB"
        )

    # Save the picture
    result = await create_or_update_user_picture(
        session, user_id, picture_data, picture_type
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save picture"
        )

    return {"message": f"Picture of type '{picture_type}' uploaded successfully"}

@pictures_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
@secured_endpoint
async def delete_picture(
    picture_type: str = "profile",
    session: AsyncSession = Depends(getSession), 
    jwt: dict = Depends(JWTBearer())
):
    """Delete the current user's picture"""
    user_id = jwt["payload"]["sub"]

    success = await delete_user_picture(session, user_id, picture_type)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No picture found to delete"
        )

# Add the router to the app
AddRouter(pictures_router)