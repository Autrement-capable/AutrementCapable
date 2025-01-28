from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import UniqueConstraint, Index, Column, func
from sqlmodel import Field, Relationship, SQLModel, DateTime

if TYPE_CHECKING:
    from database.postgress.models.user import User


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
    user_obj:User = Relationship(back_populates="password_resets")