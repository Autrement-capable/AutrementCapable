# this file is just a draft and not used in the project
# TODO: implement the passkey model and see how it would be used in the project
from __future__ import annotations # This is a Python 3.10 feature that allows you to use forward references in type hints.
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, DateTime
from sqlalchemy import Column, func

if TYPE_CHECKING:
    from database.postgress.models.user import User


class Passkey(SQLModel, table=True):
    __tablename__ = "passkeys"

    credential_id: str = Field(primary_key=True, nullable=False)
    user_id: int = Field(foreign_key="users.user_id", nullable=False)
    public_key: bytes = Field(sa_column_kwargs={"nullable": False})
    sign_count: int = Field(default=0)
    transports: Optional[str] = Field(default=None)
    created_at: datetime = Field(sa_column=Column(DateTime, server_default=func.now()))
    last_used_at: Optional[datetime] = Field(default=None)
    credential_nickname: Optional[str] = Field(default=None)
