# this file is a draft and not used in the project
# TODO: implement the oauth provider model and see how it would be used in the project
from __future__ import annotations # This is a Python 3.10 feature that allows you to use forward references in type hints.
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import UniqueConstraint, Column, func
from sqlmodel import Field, Relationship, SQLModel, DateTime

if TYPE_CHECKING:
    from database.postgress.models.user import User


class OAuthProvider(SQLModel, table=True):
    __tablename__ = "oauth_providers"
    __table_args__ = (
        UniqueConstraint("provider_name", "provider_user_id", name="uq_provider_user"),
    )

    oauth_provider_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id", nullable=False)
    provider_name: str = Field(nullable=False)
    provider_user_id: str = Field(nullable=False)
    access_token: Optional[str] = Field(default=None)
    refresh_token: Optional[str] = Field(default=None)
    token_expiry: Optional[datetime] = Field(default=None)
    date_linked: datetime = Field(sa_column=Column(DateTime, server_default=func.now()))