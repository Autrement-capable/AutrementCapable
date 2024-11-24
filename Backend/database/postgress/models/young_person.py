from __future__ import annotations
from datetime import date
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from database.postgress.models.user import User


class YoungPerson(SQLModel, table=True):
    __tablename__ = "young_persons"

    young_person_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id", nullable=False, unique=True)
    date_of_birth: Optional[date] = Field(default=None)
    gender: Optional[str] = Field(default=None)
    diagnosis_details: Optional[str] = Field(default=None)
    preferred_communication_method: Optional[str] = Field(default=None)
    sensory_sensitivities: Optional[str] = Field(default=None)
    interests: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
