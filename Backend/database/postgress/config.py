# Setup for the postgress database
from os import getenv
from sqlmodel import create_engine, SQLModel, Session
from modules.utils.singleton import singleton

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
        print("Creating database and tables")
        self.metadata.create_all(self.engine)

    def GetSession(self):
        with Session(self.engine) as session:
            yield session

postgress = Postgress()

__all__ = ["postgress"]