# models/role.py

from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.postgress.models.user import User
    from database.postgress.models.unverified_user import UnverifiedUser

class Role(SQLModel, table=True):
    __tablename__ = "roles"

    role_id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(sa_column_kwargs={"unique": True, "nullable": False})
    description: Optional[str] = Field(default=None)

    # Relationships
    users: List["User"] = Relationship(back_populates="role")
    unverified_users: List["UnverifiedUser"] = Relationship(back_populates="role")
