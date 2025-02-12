from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from database.postgress.config import Base

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

class User(AsyncAttrs, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_oauth: Mapped[bool] = mapped_column(Boolean, default=False)
    is_passkey: Mapped[bool] = mapped_column(Boolean, default=False)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_created: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship(back_populates="users", lazy="selectin")

    # If this is null, the user is verified
    verification_details: Mapped[Optional["UnverifiedDetails"]] = relationship(
        back_populates="user", lazy="selectin", uselist=False, cascade="all, delete-orphan"
    )
    password_resets: Mapped[list["PasswordReset"]] = relationship(back_populates="user", lazy="selectin", cascade="all, delete-orphan")


class PasswordReset(AsyncAttrs, Base):
    __tablename__ = "password_resets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reset_token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    token_expires: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    date_requested: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=func.now())
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="password_resets", lazy="selectin")

class RevokedToken(AsyncAttrs, Base):
    __tablename__ = "revoked_tokens"
    
    jti: Mapped[str] = mapped_column(String, primary_key=True)
    date_revoked: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    data_expires: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)