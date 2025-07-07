import os
import json
import secrets
from typing import Dict, Any, Optional, List

from fastapi import APIRouter, HTTPException, Depends, Request, status, Response, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.application import AddRouter
from ...core.security.token_creation import create_token, set_refresh_cookie
from ...db.postgress.engine import getSession
from ...db.postgress.models import User, UserDetail, UserPicture, UserPassion
from ...db.postgress.repositories.passkey import (
    create_passkey_user, #needs to be fixxed
    register_passkey_credential,
    get_user_by_credential_id, #needs to be fixxed
    get_credential_by_id,
    update_credential_counter,
    update_user_profile #needs to be fixxed
)
from ...db.postgress.repositories.role import get_role_by_name
from ...services.auth.webauthn import (
    generate_passkey_registration_options,
    verify_passkey_registration,
    generate_passkey_authentication_options,
    verify_passkey_authentication
)

router = APIRouter(prefix="/auth/passkey", tags=["Passkey Authentication"])

# ----- Data Models -----

class PasskeyRegistrationStart(BaseModel):
    first_name: Optional[str] = Field(None, description="User's first name")
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
    access_token: str = Field(..., description="JWT access token")
    message: str = Field("Registration successful", description="Success message")

class PasskeyAuthenticationStart(BaseModel):
    credential_id: Optional[str] = Field(None, description="Credential ID (if known)")

class PasskeyAuthenticationOptions(BaseModel):
    options: Dict[str, Any] = Field(..., description="WebAuthn authentication options")

class PasskeyAuthenticationComplete(BaseModel):
    authentication_data: Dict[str, Any] = Field(..., description="WebAuthn authentication data")
    challenge: str = Field(..., description="Authentication challenge")

class PasskeyAuthenticationResult(BaseModel):
    success: bool = Field(..., description="Whether authentication was successful")
    access_token: str = Field(..., description="JWT access token")
    user_id: int = Field(..., description="User ID")
    is_new_user: bool = Field(..., description="Whether this is a new user")
    onboarding_complete: bool = Field(..., description="Whether onboarding is complete")
    message: str = Field("Authentication successful", description="Success message")

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
    
    All fields are optional, allowing the creation of a dummy empty account
    that can be populated with user data later.
    """
    try:
        # Transaction for creating user and related data
        # 1. Create the base user with default role
        role = await get_role_by_name(session, "Young Person")
        if not role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Default role not found"
            )

        # Generate a random username as placeholder
        random_suffix = secrets.token_hex(8)
        temp_username = f"user_{random_suffix}"

        user = User(
            username=temp_username,
            is_passkey=True,
            role_id=role.id,
            onboarding_complete=False
        )
        session.add(user)
        await session.flush()  # Get the user ID

        # 2. Create the user detail entry (all fields optional)
        user_detail = UserDetail(
            user_id=user.id,
            first_name=data.first_name,
            last_name=data.last_name,
            age=data.age
        )
        session.add(user_detail)
        await session.flush()  # Ensure user_detail is created
        # Generate registration options with appropriate display name
        display_name = "Autrement Capable"
        if data.first_name:
            display_name = f"{data.first_name}"
            if data.last_name:
                display_name += f" {data.last_name}"
                
        options = generate_passkey_registration_options(user.id, display_name)

        await session.commit()  # Commit the transaction
        return {
            "options": options,
            "user_id": user.id
        }
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"Error in passkey registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user profile"
        )

@router.post("/registration/complete", response_model=PasskeyRegistrationResult)
async def complete_passkey_registration(
    data: PasskeyRegistrationComplete,
    response: Response,
    session: AsyncSession = Depends(getSession)
):
    """
    Complete the passkey registration process by verifying the registration response
    and storing the credential.

    The refresh token is automatically stored in an HTTP-only cookie.
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
    from ...db.postgress.repositories.user import get_user_by_id
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

    # Set refresh token in HTTP-only cookie
    set_refresh_cookie(response, refresh_token)

    return {
        "success": True,
        "access_token": access_token,
        "message": "Passkey registration successful"
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
    response: Response,
    session: AsyncSession = Depends(getSession)
):
    """
    Complete the passkey authentication process by verifying the authentication response.

    The refresh token is automatically stored in an HTTP-only cookie.
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

    # Set refresh token in HTTP-only cookie
    set_refresh_cookie(response, refresh_token)

    return {
        "success": True,
        "access_token": access_token,
        "user_id": user.id,
        "is_new_user": not user.onboarding_complete,
        "onboarding_complete": user.onboarding_complete,
        "message": "Passkey authentication successful"
    }

# Handle passkeys registration to an existing account
@router.post("/rec-acc-passkey", response_model=PasskeyRegistrationOptions)
async def rec_acc_passkey(
    code: str,
    session: AsyncSession = Depends(getSession)
):
    """
    Create a new passkey for existing account using a recovery code.
    you must follow up with a call to /auth/passkey/registration/complete to
    complete the registration of new passkey (old passkey does not get deleted)
    """
    # Get the user from the recovery code
    from ...db.postgress.repositories.acc_recovery import get_acc_recovery_by_token
    recovery = await get_acc_recovery_by_token(session, code)
    if not recovery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recovery code not found"
        )
    user = recovery.user

    # Generate registration options
    options = generate_passkey_registration_options(user.id, user.first_name)

    return {
        "options": options,
        "user_id": user.id
    }

# Add router to the server
AddRouter(router)
