# Setup for the postgress database
from os import getenv
from database.postgress.models import *
from sqlmodel import create_engine, SQLModel

DATABASE_URL = (
    f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
    f"@{getenv('POSTGRES_SERVER')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
)


def create_Pengine():
    """Create the postgress engine"""
    return create_engine(DATABASE_URL, echo=True if getenv("MODE") == "DEV" else False)

def create_db_and_tables(engine):
    """Create the database and all tables"""
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables(engine):
    """Drop the database and all tables. Should only be used for testing."""
    SQLModel.metadata.drop_all(engine)