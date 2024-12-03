from datetime import datetime
from typing import Optional

from sqlalchemy import UniqueConstraint, Column, func
from sqlmodel import Field, SQLModel, DateTime, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.postgress.models.role import Role

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
    pending_role_id: int = Field(nullable=False, foreign_key="roles.role_id")
    is_oauth: bool = Field(default=False)
    is_passkey: bool = Field(default=False)
    verification_token: str = Field(nullable=False, unique=True)
    token_expires: datetime = Field(nullable=False)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    date_created: datetime = Field(sa_column=Column(DateTime, server_default=func.now()))