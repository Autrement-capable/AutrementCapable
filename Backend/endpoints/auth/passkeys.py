from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgress.config import getSession
from database.postgress.actions.passkey import (
    create_passkey_user,
    register_passkey_credential,
    get_user_by_credential_id,
    get_credential_by_id,
    update_credential_counter,
    update_user_profile
)
from utils.webauthn_utils import (
    generate_passkey_registration_options,
    verify_passkey_registration,
    generate_passkey_authentication_options,
    verify_passkey_authentication
)
from server.jwt_config.token_creation import create_token, JWTBearer
from server.server import AddRouter

router = APIRouter(prefix="/auth/passkey", tags=["Passkey Authentication"])

# ----- Data Models -----

class PasskeyRegistrationStart(BaseModel):
    first_name: str = Field(..., description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    age: Optional[int] = Field(None, description="User's age")

class PasskeyRegistrationOptions(BaseModel):
    options: Dict[str, Any] = Field(..., description="WebAuthn registration options")
    user_id: int = Field(..., description="User ID")

class PasskeyRegistrationComplete(BaseModel):
    user_id: int = Field(..., description="User ID")
    registration_data: Dict[str, Any] = Field(..., description="WebAuthn registration data")
    challenge: str = Field(..., description="Registration challenge")

class PasskeyRegistrationResult(BaseModel):
    success: bool = Field(..., description="Whether registration was successful")
    access_token: Optional[str] = Field(None, description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="JWT refresh token")

class PasskeyAuthenticationStart(BaseModel):
    credential_id: Optional[str] = Field(None, description="Credential ID (if known)")

class PasskeyAuthenticationOptions(BaseModel):
    options: Dict[str, Any] = Field(..., description="WebAuthn authentication options")

class PasskeyAuthenticationComplete(BaseModel):
    authentication_data: Dict[str, Any] = Field(..., description="WebAuthn authentication data")
    challenge: str = Field(..., description="Authentication challenge")

class PasskeyAuthenticationResult(BaseModel):
    success: bool = Field(..., description="Whether authentication was successful")
    access_token: Optional[str] = Field(None, description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="JWT refresh token")
    user_id: Optional[int] = Field(None, description="User ID")
    is_new_user: Optional[bool] = Field(None, description="Whether this is a new user")
    onboarding_complete: Optional[bool] = Field(None, description="Whether onboarding is complete")

class UpdateUserProfile(BaseModel):
    username: Optional[str] = Field(None, description="Username")
    email: Optional[str] = Field(None, description="Email")
    phone_number: Optional[str] = Field(None, description="Phone number")
    address: Optional[str] = Field(None, description="Address")
    onboarding_complete: Optional[bool] = Field(None, description="Whether onboarding is complete")

# ----- Endpoints -----

@router.post("/registration/start", response_model=PasskeyRegistrationOptions)
async def start_passkey_registration(
    data: PasskeyRegistrationStart,
    session: AsyncSession = Depends(getSession)
):
    """
    Start the passkey registration process by creating a minimal user profile
    and generating WebAuthn registration options.
    """
    # Create a user with minimal information
    user = await create_passkey_user(
        session=session,
        first_name=data.first_name,
        last_name=data.last_name,
        age=data.age
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

    # Generate registration options
    display_name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
    options = generate_passkey_registration_options(user.id, display_name)

    return {
        "options": options,
        "user_id": user.id
    }

@router.post("/registration/complete", response_model=PasskeyRegistrationResult)
async def complete_passkey_registration(
    data: PasskeyRegistrationComplete,
    session: AsyncSession = Depends(getSession)
):
    """
    Complete the passkey registration process by verifying the registration response
    and storing the credential.
    """
    # Verify registration response
    verification = verify_passkey_registration(
        user_id=data.user_id,
        options_challenge=data.challenge,
        registration_data=data.registration_data
    )

    if not verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to verify registration"
        )

    # Get the user
    from database.postgress.actions.user import get_user_by_id
    user = await get_user_by_id(session, data.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Register credential
    credential = await register_passkey_credential(
        session=session,
        user=user,
        credential_id=verification["credential_id"],
        public_key=verification["public_key"],
        device_type="platform"  # Assuming this is a platform passkey
    )

    if not credential:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register credential"
        )

    # Create tokens
    access_token = create_token(user.id, user.role_id, refresh=False, fresh=True)
    refresh_token = create_token(user.id, user.role_id, refresh=True, fresh=True)

    return {
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@router.post("/authentication/start", response_model=PasskeyAuthenticationOptions)
async def start_passkey_authentication(
    data: PasskeyAuthenticationStart = None,
    session: AsyncSession = Depends(getSession)
):
    """
    Start the passkey authentication process by generating WebAuthn authentication options.
    """
    # Generate authentication options
    options = generate_passkey_authentication_options()

    return {
        "options": options
    }

@router.post("/authentication/complete", response_model=PasskeyAuthenticationResult)
async def complete_passkey_authentication(
    data: PasskeyAuthenticationComplete,
    session: AsyncSession = Depends(getSession)
):
    """
    Complete the passkey authentication process by verifying the authentication response.
    """
    # Extract credential ID from authentication data
    credential_id = data.authentication_data.get("id")

    if not credential_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing credential ID"
        )

    # Get credential from database
    credential = await get_credential_by_id(session, credential_id)

    if not credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credential not found"
        )

    # Get user
    user = credential.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verify authentication response
    verification = verify_passkey_authentication(
        credential_id=credential.credential_id,
        public_key=credential.public_key,
        current_sign_count=credential.sign_count,
        options_challenge=data.challenge,
        authentication_data=data.authentication_data
    )

    if not verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to verify authentication"
        )

    # Update sign count
    await update_credential_counter(
        session=session,
        credential=credential,
        new_sign_count=verification["new_sign_count"]
    )

    # Create tokens
    access_token = create_token(user.id, user.role_id, refresh=False, fresh=True)
    refresh_token = create_token(user.id, user.role_id, refresh=True, fresh=True)

    return {
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user.id,
        "is_new_user": not user.onboarding_complete,
        "onboarding_complete": user.onboarding_complete
    }

@router.put("/user/{user_id}/profile", tags=["Passkey User Profile"])
async def update_profile(
    user_id: int,
    data: UpdateUserProfile,
    session: AsyncSession = Depends(getSession),
    jwt: dict = Depends(JWTBearer())
):
    """
    Update a user's profile information.
    """
    # Get the user from JWT
    if user_id != jwt["payload"]["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized"
        )
    from database.postgress.actions.user import get_user_by_id
    user = await get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update user profile
    updated_user = await update_user_profile(
        session=session,
        user=user,
        username=data.username,
        email=data.email,
        phone_number=data.phone_number,
        address=data.address,
        onboarding_complete=data.onboarding_complete
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )

    return {
        "success": True,
        "user": {
            "id": updated_user.id,
            "username": updated_user.username,
            "email": updated_user.email,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "age": updated_user.age,
            "onboarding_complete": updated_user.onboarding_complete
        }
    }


# WIP
@router.post("/rec-acc-passkey", response_model=PasskeyAuthenticationResult)
async def rec_acc_passkey():
    pass

# Add router to the server
AddRouter(router)
