from typing import Optional, List
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, LargeBinary, JSON, UniqueConstraint, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

from ..engine import Base
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
    token_expires: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    date_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    
    user_detail_id: Mapped[int] = mapped_column(ForeignKey("user_details.id"), nullable=False, unique=True)
    user_detail: Mapped["UserDetail"] = relationship(back_populates="verification_details", lazy="selectin")

class UserDetail(AsyncAttrs, Base):
    __tablename__ = "user_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    
    # Personal details
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Traditional login details (moved from User)
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="user_detail", lazy="selectin")
    verification_details: Mapped[Optional["UnverifiedDetails"]] = relationship(
        back_populates="user_detail", lazy="selectin", uselist=False, cascade="all, delete-orphan"
    )


class UserPicture(AsyncAttrs, Base):
    __tablename__ = "user_pictures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    picture_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    date_updated: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    type: Mapped[str] = mapped_column(String, nullable=False)  # Type of picture (e.g., "profile", "cover")

    user: Mapped["User"] = relationship(back_populates="picture", lazy="selectin")
    
    # Add composite unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'type', name='unique_user_picture_type'),
    )

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


class UserAvatarInfo(AsyncAttrs, Base):
    __tablename__ = "user_avatar_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    avatarGender: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatarAccessories: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatarColor: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatarPassions: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatarExpression: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class User(AsyncAttrs, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    date_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)
    is_passkey: Mapped[bool] = mapped_column(Boolean, default=True)  # Default to passkey now
    onboarding_complete: Mapped[bool] = mapped_column(Boolean, default=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship(back_populates="users", lazy="selectin")

    # Relationships
    passkey_credentials: Mapped[list["PasskeyCredential"]] = relationship(
        back_populates="user", lazy="selectin", cascade="all, delete-orphan"
    )
    user_detail: Mapped[Optional["UserDetail"]] = relationship(
        back_populates="user", lazy="selectin", uselist=False, cascade="all, delete-orphan"
    )
    picture: Mapped[Optional["UserPicture"]] = relationship(
        back_populates="user", lazy="selectin", uselist=False, cascade="all, delete-orphan"
    )
    passions: Mapped[list["UserPassion"]] = relationship(
        back_populates="user", lazy="selectin", cascade="all, delete-orphan"
    )
    terms_agreements: Mapped[list["UserTermsAgreement"]] = relationship(
        back_populates="user", lazy="selectin", cascade="all, delete-orphan"
    )
    account_recovery: Mapped[list["AccountRecovery"]] = relationship(
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
# class UserSkill(Base): # DEPRECATED
#     __tablename__ = "user_skills"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
#     skills_data: Mapped[dict] = mapped_column(JSON, nullable=False, default={})
#     # Example:
#     # {
#     #   "empathie": 10,
#     #   "initiative": 8,
#     #   "communication": 12,
#     #   ...
#     # }
#     last_updated: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

#     # Relationships
#     user: Mapped["User"] = relationship(back_populates="skills")


# ## same shit schema can change
# class UserAbilities(Base): # DEP
#     __tablename__ = "user_abilities"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
#     abilities_data: Mapped[dict] = mapped_column(JSON, nullable=False, default={})

#     # Example:
#     # {
#     #   "WantToLearn": ["Gestion du stress", ...],
#     #   "Unknow": ["Gestion du stress", ...],
#     #   "Weak": ["Gestion du stress", ...],
#     #   "Strong": ["Gestion du stress", ...],
#     #   "Skipped": ["Gestion du stress", ...],
#     # }

#     last_updated: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
#     # Relationships
#     user: Mapped["User"] = relationship(back_populates="abilities")

## game schemas


##scenario game json example
# {
#   "currentLevel": 3,
#   "completion": 37.5,
#   "traits": {
#     "empathy": 4,
#     "diplomacy": 3,
#     "assertiveness": 2,
#     "pragmatism": 5
#   },
# }
class ScenarioGameData(Base):
    __tablename__ = "scenario_game_data"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)

    current_level = mapped_column(Integer, nullable=False, default=0)
    completion = mapped_column(Float, nullable=False, default=0.0)

    traits = mapped_column(JSON, nullable=False, default={})
    penalties = mapped_column(JSON, nullable=False, default={})

# --- 2️⃣ Shape Sequence Game ---
class ShapeSequenceGameData(Base):
    __tablename__ = "shape_sequence_game_data"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)

    completion = mapped_column(Float, nullable=False, default=0.0)
    levelResults = mapped_column(JSON, nullable=False, default={})

# --- 3️⃣ Jobs Game ---
class JobsGameData(Base):
    __tablename__ = "jobs_game_data"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)

    completion = mapped_column(Float, nullable=False, default=0.0)
    jobChoices = mapped_column(JSON, nullable=False, default={})  # Assuming it's a dict

# --- 4️⃣ Speed Game ---
class SpeedGameData(Base):
    __tablename__ = "speed_game_data"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)

    current_level = mapped_column(Integer, nullable=False, default=0)
    completion = mapped_column(Float, nullable=False, default=0.0)
    levelStats = mapped_column(JSON, nullable=False, default={})

# --- 5️⃣ Abilities Game ---
class AbilitiesGameData(Base):
    __tablename__ = "abilities_game_data"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)

    completion = mapped_column(Float, nullable=False, default=0.0)
    skillAssessment = mapped_column(JSON, nullable=False, default={})  # Assuming it's a dict

# --- 6️⃣ Skills Game ---
class SkillsGameData(Base):
    __tablename__ = "skills_game_data"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)

    completion = mapped_column(Float, nullable=False, default=0.0)
    skillsAssessment = mapped_column(JSON, nullable=False, default={})  # Assuming it's a dict

# --- 7️⃣ Room env ---
class RoomEnvGameData(Base):
    __tablename__ = "room_env_game_data"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)

    completion = mapped_column(Float, nullable=False, default=0.0)
    roomData = mapped_column(JSON, nullable=False, default=list)  # Assuming it's a array of json objects