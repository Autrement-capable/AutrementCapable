from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, LargeBinary, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from database.postgress.config import Base

## AUTH

class Role(AsyncAttrs, Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    users: Mapped[list["User"]] = relationship(back_populates="role", lazy="selectin")

class UnverifiedDetails(AsyncAttrs, Base):
    __tablename__ = "unverified_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    verification_token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    token_expires: Mapped[DateTime] = mapped_column(DateTime, nullable=False)  # Add token expiration
    date_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)  # Enforce one-to-one
    user: Mapped["User"] = relationship(back_populates="verification_details", lazy="selectin")

class UserPicture(AsyncAttrs, Base):
    __tablename__ = "user_pictures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    picture_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    date_updated: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    type: Mapped[str] = mapped_column(String, nullable=False)  # Type of picture (e.g., "profile", "cover")

    user: Mapped["User"] = relationship(back_populates="picture", lazy="selectin")

class UserPassion(AsyncAttrs, Base):
    __tablename__ = "user_passions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    passion_text: Mapped[str] = mapped_column(String, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)  # To maintain order of passions (1, 2, 3)

    user: Mapped["User"] = relationship(back_populates="passions", lazy="selectin")

class TermsVersion(AsyncAttrs, Base):
    __tablename__ = "terms_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    version: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    content: Mapped[str] = mapped_column(String, nullable=False)  # Markdown content
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    date_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    user_agreements: Mapped[list["UserTermsAgreement"]] = relationship(
        back_populates="terms_version", lazy="selectin", cascade="all, delete-orphan"
    )

class UserTermsAgreement(AsyncAttrs, Base):
    __tablename__ = "user_terms_agreements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    terms_id: Mapped[int] = mapped_column(ForeignKey("terms_versions.id"), nullable=False)
    date_agreed: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="terms_agreements", lazy="selectin")
    terms_version: Mapped["TermsVersion"] = relationship(back_populates="user_agreements", lazy="selectin")

class User(AsyncAttrs, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)  # Made nullable for passkey users
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)     # Made nullable for passkey users
    password_hash: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_passkey: Mapped[bool] = mapped_column(Boolean, default=False)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Added age field for minimal passkey registration
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)
    onboarding_complete: Mapped[bool] = mapped_column(Boolean, default=False)  # Track if user has completed onboarding

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship(back_populates="users", lazy="selectin")

    # If this is null, the user is verified
    verification_details: Mapped[Optional["UnverifiedDetails"]] = relationship(
        back_populates="user", lazy="selectin", uselist=False, cascade="all, delete-orphan"
    )
    account_recovery: Mapped[list["AccountRecovery"]] = relationship(back_populates="user", lazy="selectin", cascade="all, delete-orphan")
    passkey_credentials: Mapped[list["PasskeyCredential"]] = relationship(back_populates="user", lazy="selectin", cascade="all, delete-orphan")

    # User data
    skills: Mapped[list["UserSkill"]] = relationship(back_populates="user", lazy="selectin", cascade="all, delete-orphan")
    abilities: Mapped[list["UserAbilities"]] = relationship(back_populates="user", lazy="selectin", cascade="all, delete-orphan")

    picture: Mapped[Optional["UserPicture"]] = relationship(
        back_populates="user", lazy="selectin", uselist=False, cascade="all, delete-orphan"
    )
    passions: Mapped[list["UserPassion"]] = relationship(
        back_populates="user", lazy="selectin", cascade="all, delete-orphan"
    )
    terms_agreements: Mapped[list["UserTermsAgreement"]] = relationship(
        back_populates="user", lazy="selectin", cascade="all, delete-orphan"
    )

class AccountRecovery(AsyncAttrs, Base):
    __tablename__ = "account_recovery"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reset_token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    token_expires: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    date_requested: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="account_recovery", lazy="selectin")


class RevokedToken(AsyncAttrs, Base):
    __tablename__ = "revoked_tokens"

    jti: Mapped[str] = mapped_column(String, primary_key=True)
    date_revoked: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    data_expires: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)

class PasskeyCredential(AsyncAttrs, Base):
    __tablename__ = "passkey_credentials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    credential_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    public_key: Mapped[str] = mapped_column(LargeBinary, nullable=False)
    sign_count: Mapped[int] = mapped_column(Integer, default=0)
    device_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    last_used: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="passkey_credentials", lazy="selectin")

## DATA

## Schema may change so we do json instead of individual columns
## Data validation does not exist as a result
class UserSkill(Base):
    __tablename__ = "user_skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    skills_data: Mapped[dict] = mapped_column(JSON, nullable=False, default={})
    # Example:
    # {
    #   "empathie": 10,
    #   "initiative": 8,
    #   "communication": 12,
    #   ...
    # }
    last_updated: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    user: Mapped["User"] = relationship(back_populates="skills")


## same shit schema can change
class UserAbilities(Base):
    __tablename__ = "user_abilities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    abilities_data: Mapped[dict] = mapped_column(JSON, nullable=False, default={})

    # Example:
    # {
    #   "WantToLearn": ["Gestion du stress", ...],
    #   "Unknow": ["Gestion du stress", ...],
    #   "Weak": ["Gestion du stress", ...],
    #   "Strong": ["Gestion du stress", ...],
    #   "Skipped": ["Gestion du stress", ...],
    # }

    last_updated: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    # Relationships
    user: Mapped["User"] = relationship(back_populates="abilities")