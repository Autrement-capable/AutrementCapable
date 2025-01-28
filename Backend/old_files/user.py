# models/user.py

from __future__ import annotations # This is a Python 3.10 feature that allows you to use forward references in type hints.
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, DateTime
from sqlalchemy import Column, func

if TYPE_CHECKING:
    from database.postgress.models.role import Role
    from database.postgress.models.password_reset import PasswordReset


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
    password_resets: list["PasswordReset"] = Relationship(back_populates="user_obj")