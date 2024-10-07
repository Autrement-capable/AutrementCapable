# models/user.py

from __future__ import annotations # This is a Python 3.10 feature that allows you to use forward references in type hints.
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, DateTime
from sqlalchemy import Column, func

if TYPE_CHECKING:
    from database.postgress.models.oauth_provider import OAuthProvider
    from database.postgress.models.passkey import Passkey
    from database.postgress.models.password_reset import PasswordReset
    from database.postgress.models.young_person import YoungPerson
    from database.postgress.models.role import Role


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str] = Field(default=None)
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False})
    password_hash: Optional[str] = Field(default=None)
    is_oauth: bool = Field(default=False)
    is_passkey: bool = Field(default=False)
    role_id: int = Field(foreign_key="roles.role_id", nullable=False)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    date_created: datetime = Field(sa_column=Column(DateTime, server_default=func.now()))
    is_active: bool = Field(default=True)
    last_login: Optional[datetime] = Field(default=None)

    # Relationships
    role: "Role" = Relationship(back_populates="users")
    oauth_providers: List["OAuthProvider"] = Relationship(back_populates="user")
    passkeys: List["Passkey"] = Relationship(back_populates="user")
    password_resets: List["PasswordReset"] = Relationship(back_populates="user")
    young_person: Optional["YoungPerson"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )
