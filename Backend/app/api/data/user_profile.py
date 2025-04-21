import os
import json

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...core.application import AddRouter
from ...core.security.token_creation import JWTBearer
from ...core.security.decorators import secured_endpoint
from ...db.postgress.engine import getSession
from ...db.postgress.models import User, UserDetail, UserPassion, UserPicture
from ...db.postgress.repositories.user_passions import get_user_passions, create_user_passion, delete_user_passion
from ...db.postgress.repositories.user_pictures import create_or_update_user_picture

class UserProfileResponse(BaseModel):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    age: Optional[int]
    phone_number: Optional[str]
    address: Optional[str]
    passions: List[Dict[str, Any]]
    has_picture: bool
    onboarding_complete: bool

class ProfileUpdate(BaseModel):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    age: Optional[int]
    phone_number: Optional[str]
    address: Optional[str]
    onboarding_complete: Optional[bool]

profile_router = APIRouter(prefix="/user/profile", tags=["User Profile"])

@profile_router.get("", response_model=UserProfileResponse)
@secured_endpoint
async def get_my_profile(
    session: AsyncSession = Depends(getSession),
    jwt: dict = Depends(JWTBearer())
):
    """Get the current user's profile information"""
    user_id = jwt["payload"]["sub"]

    # Get the user with its detail
    async with session.begin():
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
        "username": user.username,
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
@secured_endpoint
async def update_my_profile(
    profile_data: ProfileUpdate,
    session: AsyncSession = Depends(getSession),
    jwt: dict = Depends(JWTBearer())
):
    """Update the current user's profile information"""
    user_id = jwt["payload"]["sub"]

    async with session.begin():
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
        if profile_data.username is not None:
            user.username = profile_data.username

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

    return {"message": "Profile updated successfully"}

@profile_router.put("/complete-setup")
@secured_endpoint
async def complete_profile_setup(
    username: str = Form(...),
    avatar: Optional[UploadFile] = File(None),
    passions: Optional[str] = Form(None),  # JSON string of passions
    session: AsyncSession = Depends(getSession),
    jwt: dict = Depends(JWTBearer())
):
    """Complete the user profile setup (username, avatar, passions)"""
    user_id = jwt["payload"]["sub"]
    is_dev_mode = os.getenv("MODE") == "DEV"

    # Check if avatar is required
    if not avatar and not is_dev_mode:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avatar image is required"
        )

    # Parse passions
    user_passions = []
    if passions:
        try:
            user_passions = json.loads(passions)
            if not isinstance(user_passions, list) or len(user_passions) > 3:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Passions must be a list with maximum 3 items"
                )
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid passions format, must be a JSON array"
            )

    async with session.begin():
        # Get user
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update username
        user.username = username
        user.onboarding_complete = True
        session.add(user)

        # Process avatar if provided
        if avatar:
            avatar_data = await avatar.read()
            if len(avatar_data) > 2 * 1024 * 1024:  # 2MB limit
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Avatar image must be less than 2MB"
                )

            await create_or_update_user_picture(
                session, user_id, avatar_data, "profile", commit=False
            )

        # Delete existing passions first
        existing_passions = await get_user_passions(session, user_id)
        for passion in existing_passions:
            await session.delete(passion)

        # Create new passions
        for i, passion_text in enumerate(user_passions, 1):
            passion = UserPassion(
                user_id=user_id,
                passion_text=passion_text,
                order=i
            )
            session.add(passion)

    return {"message": "Profile setup completed successfully"}

AddRouter(profile_router)