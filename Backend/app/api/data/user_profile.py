import os
import json

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...core.application import AddRouter
from ...core.security.decorators import secured_endpoint
from ...db.postgress.engine import getSession
from ...db.postgress.models import User, UserDetail, UserPassion, UserPicture
from ...db.postgress.repositories.user_passions import get_user_passions, create_user_passion, delete_user_passion
from ...db.postgress.repositories.user import store_avatar_info, get_avatar_info, AvatarInfo

class UserProfileResponse(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    passions: Optional[List[Dict[str, Any]]] = []
    has_picture: bool
    onboarding_complete: bool

class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    onboarding_complete: Optional[bool] = None

profile_router = APIRouter(prefix="/user/profile", tags=["User Profile"])

@profile_router.get("", response_model=UserProfileResponse)
@secured_endpoint()
async def get_my_profile(
    jwt: dict,
    session: AsyncSession = Depends(getSession)
):
    """Get the current user's profile information"""
    user_id = jwt["sub"]

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get user detail
    stmt = select(UserDetail).where(UserDetail.user_id == user_id)
    result = await session.execute(stmt)
    user_detail = result.scalars().first()

    # Get user passions
    passions = await get_user_passions(session, user_id)

    # Check if user has a picture
    stmt = select(UserPicture).where(UserPicture.user_id == user_id)
    result = await session.execute(stmt)
    user_picture = result.scalars().first()

    return {
        "username": user.username if user.username else None,
        "first_name": user_detail.first_name if user_detail else None,
        "last_name": user_detail.last_name if user_detail else None,
        "email": user_detail.email if user_detail else None,
        "age": user_detail.age if user_detail else None,
        "phone_number": user_detail.phone_number if user_detail else None,
        "address": user_detail.address if user_detail else None,
        "passions": [
            {"id": p.id, "text": p.passion_text, "order": p.order}
            for p in passions
        ],
        "has_picture": bool(user_picture and user_picture.picture_data),
        "onboarding_complete": user.onboarding_complete
    }

@profile_router.put("")
@secured_endpoint()
async def update_my_profile(
    profile_data: ProfileUpdate,
    jwt: dict,
    session: AsyncSession = Depends(getSession)
):
    """Update the current user's profile information"""
    user_id = jwt["sub"]

    # Get user
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get or create user detail
    stmt = select(UserDetail).where(UserDetail.user_id == user_id)
    result = await session.execute(stmt)
    user_detail = result.scalars().first()

    if not user_detail:
        user_detail = UserDetail(user_id=user_id)
        session.add(user_detail)

    # Update user fields
    # Note: Username is typically immutable in many systems, so this is commented out.
    # if profile_data.username is not None:
    #     user.username = profile_data.username

    if profile_data.onboarding_complete is not None:
        user.onboarding_complete = profile_data.onboarding_complete

    # Update user detail fields
    if profile_data.first_name is not None:
        user_detail.first_name = profile_data.first_name

    if profile_data.last_name is not None:
        user_detail.last_name = profile_data.last_name

    if profile_data.email is not None:
        user_detail.email = profile_data.email

    if profile_data.age is not None:
        user_detail.age = profile_data.age

    if profile_data.phone_number is not None:
        user_detail.phone_number = profile_data.phone_number

    if profile_data.address is not None:
        user_detail.address = profile_data.address

    session.add(user)
    session.add(user_detail)
    await session.commit()

    return {"message": "Profile updated successfully"}


## avatar data
@profile_router.post("/avatar-creation-data")
@secured_endpoint()
async def process_avatar_creation_data(
    data: AvatarInfo,
    jwt: dict,
    session: AsyncSession = Depends(getSession)
):
    """Process avatar creation data"""
    user_id = jwt["sub"]

    try:
        await store_avatar_info(session, user_id, data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing avatar creation data"
        )

    return {"message": "Avatar creation data processed successfully"}

@profile_router.get("/avatar-creation-data", response_model=AvatarInfo)
@secured_endpoint()
async def get_avatar_creation_data(
    jwt: dict,
    session: AsyncSession = Depends(getSession)
):
    """Get avatar creation data"""
    user_id = jwt["sub"]

    async with session.begin():
        # Get user
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Get avatar info
        avatar_info = await get_avatar_info(session, user_id)

        if not avatar_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Avatar creation data not found"
            )
    avatar_info = {
        "avatarGender" : avatar_info.avatarGender,
        "avatarAccessories" : avatar_info.avatarAccessories,
        "avatarColor" : avatar_info.avatarColor,
        "avatarPassions" : avatar_info.avatarPassions,
        "avatarExpression" : avatar_info.avatarExpression,
    }
    return avatar_info

AddRouter(profile_router)