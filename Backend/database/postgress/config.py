from os import getenv
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from modules.utils.singleton import singleton
from contextlib import asynccontextmanager

DATABASE_URL = (
    f"postgresql+asyncpg://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
    f"@{getenv('POSTGRES_SERVER')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
)

@singleton
class Postgress:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL, echo=True if getenv("MODE") == "DEV" else False)
        self.metadata = SQLModel.metadata
        self.SQLModel = SQLModel

    async def create_db_and_tables(self):
        """Create the database and tables"""
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.create_all)

    @asynccontextmanager
    async def GetSession(self):
        async with AsyncSession(self.engine) as session:
            yield session

postgress = Postgress()

__all__ = ["postgress"]