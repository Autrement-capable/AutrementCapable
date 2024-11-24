from os import getenv
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, create_engine, Session
from utils.singleton import singleton
from contextlib import asynccontextmanager, contextmanager

DATABASE_URL_ASYNC = (
    f"postgresql+asyncpg://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
    f"@{getenv('POSTGRES_SERVER')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
)

# Use `psycopg2` for the sync engine
DATABASE_URL_SYNC = (
    f"postgresql+psycopg2://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
    f"@{getenv('POSTGRES_SERVER')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
)

@singleton
class Postgress:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL_ASYNC, echo=True if getenv("MODE") == "DEV" else False)
        # only exist for the blasted jwt deny list cause the callback needs to be sync func
        self.sync_engine = create_engine(DATABASE_URL_SYNC, echo=True if getenv("MODE") == "DEV" else False)
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
    @contextmanager
    def GetSessionSync(self):
        """Get a synchronous session on the Sync Engine(diffrent from the async engine)
        For now only exists for the jwt deny list"""
        with Session(self.sync_engine) as session:
            yield session

postgress = Postgress()

__all__ = ["postgress"]