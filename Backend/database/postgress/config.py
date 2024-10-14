# Setup for the postgress database
from os import getenv
from sqlmodel import create_engine, SQLModel, Session
from modules.utils.singleton import singleton
from contextlib import contextmanager

DATABASE_URL = (
    f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
    f"@{getenv('POSTGRES_SERVER')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
)

@singleton
class Postgress:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL, echo=True if getenv("MODE") == "DEV" else False)
        self.metadata = SQLModel.metadata
        self.SQLModel = SQLModel

    def create_db_and_tables(self):
        """Create the database and tables"""
        print("Creating database and tables")
        self.metadata.create_all(self.engine)

    @contextmanager
    def GetSession(self):
        session = Session(self.engine)
        try:
            yield session
        finally:
            session.close()

postgress = Postgress()

__all__ = ["postgress"]