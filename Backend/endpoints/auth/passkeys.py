from fastapi import APIRouter, HTTPException, Depends, Request, status, Response
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
from server.jwt_config.token_creation import create_token, JWTBearer, set_refresh_cookie
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
    from database.postgress.actions.acc_recovery import get_acc_recovery_by_token
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
