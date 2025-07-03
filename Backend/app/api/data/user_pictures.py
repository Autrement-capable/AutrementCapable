from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.application import AddRouter
from ...core.security.decorators import secured_endpoint
from ...core.picture_config import picture_config
from ...db.postgress.engine import getSession
from ...db.postgress.repositories.user_pictures import (
    save_picture_chunk,
    delete_user_picture,
    does_picture_exists
)
from ...utils.image_handler import (
    stream_avif_to_db,
    convert_to_avif_and_save,
    validate_image,
    get_streaming_response_for_image
)

# ============ Router ============

pictures_router = APIRouter(prefix="/user/picture", tags=["User Pictures"])

# ============ Endpoints ============

@pictures_router.get("")
@secured_endpoint()
async def get_my_picture(
    jwt: dict,
    picture_type: str = "profile",
    session: AsyncSession = Depends(getSession)
):
    """
    Get the current user's picture with memory-efficient streaming

    The image is streamed directly from the database to the client
    without loading the entire image into memory at once.
    """
    user_id = jwt["sub"]

    try:
        # Create streaming response using core pool
        if not await does_picture_exists(session,user_id, picture_type):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No picture found for type '{picture_type}'"
            )
        return await get_streaming_response_for_image(user_id, picture_type)
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving image: {str(e)}"
        )

@pictures_router.post("", status_code=status.HTTP_201_CREATED)
@secured_endpoint()
async def upload_picture(
    jwt: dict,
    session: AsyncSession = Depends(getSession),
    picture: UploadFile = File(...),
    picture_type: str = Form("profile"),
    is_avif: bool = Form(False),
    quality: Optional[int] = Form(None),
):
    """
    Upload a picture for the current user with memory-efficient streaming

    Args:
        picture: The image file to upload
        picture_type: Type of picture (profile, cover, etc.)
        is_avif: Whether the image is already in AVIF format (converted client-side)
        quality: AVIF quality (0-100), defaults to the configuration value
    """
    user_id = jwt["sub"]

    # Use specified quality or fallback to config
    avif_quality = quality if quality is not None else picture_config.avif_quality

    # Process the image based on whether it's already AVIF or needs conversion
    if is_avif and picture.content_type == 'image/avif':
        # Direct streaming of AVIF image
        result = await stream_avif_to_db(
            session, 
            picture, 
            save_picture_chunk,
            user_id,
            picture_type
        )
    else:
        # Convert to AVIF and save
        result = await convert_to_avif_and_save(
            session, 
            picture, 
            save_picture_chunk,
            user_id,
            picture_type,
            quality=avif_quality
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save picture"
        )

    return {
        "message": f"Picture of type '{picture_type}' uploaded successfully",
        "picture_type": picture_type,
        "is_avif": True,
        "dimensions": {
            "max_width": picture_config.max_width,
            "max_height": picture_config.max_height
        }
    }

@pictures_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
@secured_endpoint()
async def delete_picture(
    jwt: dict,
    session: AsyncSession = Depends(getSession),
    picture_type: str = "profile",
):
    """Delete the current user's picture"""
    user_id = jwt["sub"]

    success = await delete_user_picture(session, user_id, picture_type)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No picture found to delete"
        )

# Add the router to the app
AddRouter(pictures_router)