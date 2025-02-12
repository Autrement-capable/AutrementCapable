from sqlalchemy import UniqueConstraint, Index, Column, func
from sqlmodel import Field, Relationship, SQLModel, DateTime
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, DateTime
from sqlalchemy import Column, func


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    role_id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(sa_column_kwargs={"unique": True, "nullable": False})
    description: Optional[str] = Field(default=None)

    unverified_users: list["UnverifiedUser"] = Relationship(back_populates="role")
    users: list["User"] = Relationship(back_populates="role")


class PasswordReset(SQLModel, table=True):
    __tablename__ = "password-resets"
    __table_args__ = (
        UniqueConstraint("reset_token", name="uq_reset_token"),
        Index("ix_reset_token", "reset_token"), # faster lookups
    )

    reset_id: Optional[int] = Field(default=None, primary_key=True)
    reset_token: str = Field(nullable=False)
    token_expires: datetime = Field(nullable=False)
    date_requested: datetime = Field(nullable=True, default=None)

    user_id: int = Field(foreign_key="users.user_id", nullable=False)
    user_obj: "User" = Relationship(back_populates="password_resets")


class UnverifiedUser(SQLModel, table=True):
    __tablename__ = "unverified_users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_unverified_email"),
        UniqueConstraint("verification_token", name="uq_verification_token"),
    )

    unverified_user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False)
    email: str = Field(nullable=False)
    password_hash: Optional[str] = Field(default=None)
    is_oauth: bool = Field(default=False)
    is_passkey: bool = Field(default=False)
    verification_token: str = Field(nullable=False, unique=True)
    token_expires: datetime = Field(nullable=False)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    date_created: datetime = Field(sa_column=Column(DateTime, server_default=func.now()))

    pending_role_id: int = Field(nullable=False, foreign_key="roles.role_id")
    role: Optional["Role"] = Relationship(back_populates="unverified_users")

class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False)
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False}) # this is the same as the line above
    password_hash: Optional[str] = Field(default=None)
    is_oauth: bool = Field(default=False)
    is_passkey: bool = Field(default=False)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    date_created: datetime = Field(sa_column=Column(DateTime, server_default=func.now()))
    is_active: bool = Field(default=True)
    last_login: Optional[datetime] = Field(default=None)

    role_id: int = Field(foreign_key="roles.role_id", nullable=False)
    role: Role = Relationship(back_populates="users")
    password_resets: list["PasswordReset"] | None = Relationship(back_populates="user_obj")

## create a model for revoked tokens

class RevokedToken(SQLModel, table=True):
    __tablename__ = "revoked_tokens"

    jti: str = Field(primary_key=True)
    date_revoked:datetime = Field(sa_column=Column(DateTime, server_default=func.now()))
    data_expires:datetime = Field(nullable=False)
    type:str = Field(nullable=False)