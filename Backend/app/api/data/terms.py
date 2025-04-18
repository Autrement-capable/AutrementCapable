from typing import Dict, List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.application import AddRouter
from ...core.security.token_creation import JWTBearer
from ...core.security.decorators import secured_endpoint
from ...db.postgress.engine import getSession
from ...db.postgress.repositories.terms_agreements import (
    get_latest_terms_version,
    get_terms_by_version,
    get_terms_by_id,
    create_terms_version,
    update_terms_version,
    get_user_terms_agreement,
    get_latest_user_terms_agreement,
    create_user_terms_agreement,
    has_user_agreed_to_latest_terms
)

# ============ Pydantic Models for Request/Response ============

class TermsVersionCreate(BaseModel):
    """Model for creating a terms version"""
    version: str = Field(..., description="Version identifier (e.g., 'v1.0')")
    content: str = Field(..., description="Markdown content of the terms")
    is_active: bool = Field(True, description="Whether this is the active version")

class TermsVersionUpdate(BaseModel):
    """Model for updating a terms version"""
    content: Optional[str] = Field(None, description="Markdown content of the terms")
    is_active: Optional[bool] = Field(None, description="Whether this is the active version")

class TermsVersionResponse(BaseModel):
    """Model for terms version response"""
    id: int
    version: str
    content: str
    is_active: bool
    date_created: str

class TermsAgreementResponse(BaseModel):
    """Model for terms agreement response"""
    id: int
    terms_id: int
    terms_version: str
    date_agreed: str

class TermsStatus(BaseModel):
    """Model for terms status response"""
    has_agreed: bool
    latest_terms_id: Optional[int] = None
    latest_terms_version: Optional[str] = None
    agreement_date: Optional[str] = None

# ============ Routers ============

# Public router for getting terms
terms_public_router = APIRouter(prefix="/terms", tags=["Terms and Conditions"])

# Protected router for admin operations on terms
# terms_admin_router = APIRouter(prefix="/admin/terms", tags=["Terms and Conditions Admin"])

# Protected router for user agreements
terms_agreement_router = APIRouter(prefix="/user/terms", tags=["User Terms Agreements"])

# ============ Public Endpoints ============

@terms_public_router.get("", response_model=TermsVersionResponse)
async def get_latest_terms(
    session: AsyncSession = Depends(getSession)
):
    """Get the latest active terms and conditions"""
    terms = await get_latest_terms_version(session)

    if not terms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active terms found"
        )

    return {
        "id": terms.id,
        "version": terms.version,
        "content": terms.content,
        "is_active": terms.is_active,
        "date_created": terms.date_created.isoformat()
    }

@terms_public_router.get("/{version}", response_model=TermsVersionResponse)
async def get_terms_by_version_string(
    version: str = Path(..., description="Terms version identifier"),
    session: AsyncSession = Depends(getSession)
):
    """Get terms and conditions by version string"""
    terms = await get_terms_by_version(session, version)

    if not terms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Terms version '{version}' not found"
        )

    return {
        "id": terms.id,
        "version": terms.version,
        "content": terms.content,
        "is_active": terms.is_active,
        "date_created": terms.date_created.isoformat()
    }

# ============ Admin Endpoints ============

# @terms_admin_router.post("", response_model=TermsVersionResponse, status_code=status.HTTP_201_CREATED)
# @secured_endpoint
# async def create_new_terms_version(
#     terms_data: TermsVersionCreate,
#     session: AsyncSession = Depends(getSession),
#     jwt: dict = Depends(JWTBearer())
# ):
#     """Create a new terms version (admin only)"""
#     # Check if user is admin
#     user_role = jwt["payload"]["role"]
#     if user_role not in [1, 2]:  # Super Admin or Admin roles
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Only administrators can create terms versions"
#         )

#     terms = await create_terms_version(
#         session, terms_data.version, terms_data.content, terms_data.is_active
#     )

#     if not terms:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Failed to create terms version"
#         )

#     return {
#         "id": terms.id,
#         "version": terms.version,
#         "content": terms.content,
#         "is_active": terms.is_active,
#         "date_created": terms.date_created.isoformat()
#     }

# @terms_admin_router.patch("/{terms_id}", response_model=TermsVersionResponse)
# @secured_endpoint
# async def update_terms_version_admin(
#     terms_update: TermsVersionUpdate,
#     terms_id: int = Path(..., description="Terms ID"),
#     session: AsyncSession = Depends(getSession),
#     jwt: dict = Depends(JWTBearer())
# ):
#     """Update a terms version (admin only)"""
#     # Check if user is admin
#     user_role = jwt["payload"]["role"]
#     if user_role not in [1, 2]:  # Super Admin or Admin roles
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Only administrators can update terms versions"
#         )

#     terms = await update_terms_version(
#         session, terms_id, terms_update.content, terms_update.is_active
#     )

#     if not terms:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Terms version with ID {terms_id} not found"
#         )

#     return {
#         "id": terms.id,
#         "version": terms.version,
#         "content": terms.content,
#         "is_active": terms.is_active,
#         "date_created": terms.date_created.isoformat()
#     }

# ============ User Agreement Endpoints ============

@terms_agreement_router.get("/status", response_model=TermsStatus)
@secured_endpoint
async def check_terms_agreement_status(
    session: AsyncSession = Depends(getSession),
    jwt: dict = Depends(JWTBearer())
):
    """Check if the current user has agreed to the latest terms"""
    user_id = jwt["payload"]["sub"]

    latest_terms = await get_latest_terms_version(session)
    if not latest_terms:
        return {"has_agreed": True}  # No terms to agree to

    has_agreed = await has_user_agreed_to_latest_terms(session, user_id)
    latest_agreement = await get_latest_user_terms_agreement(session, user_id)

    response = {
        "has_agreed": has_agreed,
        "latest_terms_id": latest_terms.id,
        "latest_terms_version": latest_terms.version
    }

    if latest_agreement:
        response["agreement_date"] = latest_agreement.date_agreed.isoformat()

    return response

@terms_agreement_router.post("/{terms_id}/agree", status_code=status.HTTP_201_CREATED)
@secured_endpoint
async def agree_to_terms(
    terms_id: int = Path(..., description="Terms ID to agree to"),
    session: AsyncSession = Depends(getSession),
    jwt: dict = Depends(JWTBearer())
):
    """Record user agreement to a specific terms version"""
    user_id = jwt["payload"]["sub"]

    # Check if terms exist
    terms = await get_terms_by_id(session, terms_id)
    if not terms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Terms version with ID {terms_id} not found"
        )

    agreement, created = await create_user_terms_agreement(session, user_id, terms_id)

    if not agreement:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record agreement"
        )

    status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return {
        "message": "Terms agreement recorded successfully",
        "terms_version": terms.version,
        "date_agreed": agreement.date_agreed.isoformat()
    }

@terms_agreement_router.get("/history", response_model=List[TermsAgreementResponse])
@secured_endpoint
async def get_terms_agreement_history(
    session: AsyncSession = Depends(getSession),
    jwt: dict = Depends(JWTBearer())
):
    """Get the current user's terms agreement history"""
    user_id = jwt["payload"]["sub"]

    agreements = await get_user_terms_agreement(session, user_id)

    # Fetch terms version for each agreement
    result = []
    for agreement in agreements:
        terms = await get_terms_by_id(session, agreement.terms_id)
        if terms:
            result.append({
                "id": agreement.id,
                "terms_id": agreement.terms_id,
                "terms_version": terms.version,
                "date_agreed": agreement.date_agreed.isoformat()
            })

    return result

# Add the routers to the app
AddRouter(terms_public_router)
# AddRouter(terms_admin_router)
AddRouter(terms_agreement_router)