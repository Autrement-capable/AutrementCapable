## create a model for revoked tokens

from datetime import datetime
from sqlmodel import Field, SQLModel, DateTime
from sqlalchemy import Column, func

class RevokedToken(SQLModel, table=True):
    __tablename__ = "revoked_tokens"

    jti: str = Field(primary_key=True)
    date_revoked:datetime = Field(sa_column=Column(DateTime, server_default=func.now()))
    data_expires:datetime = Field(nullable=False)
    type:str = Field(nullable=False)