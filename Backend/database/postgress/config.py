from os import getenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import create_engine
from utils.singleton import singleton

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
        self.engine = create_async_engine(DATABASE_URL_ASYNC, echo=True if getenv("MODE") == "DEV" else False, future=True)
        self.sync_engine = create_engine(DATABASE_URL_SYNC, echo=True if getenv("MODE") == "DEV" else False, future=True)

        self.Session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        self.SyncSession = sessionmaker(self.sync_engine, expire_on_commit=False)

        self.Base = declarative_base()

    def get_SyncSession(self) -> Session:
        return self.SyncSession()

    async def close(self):
        await self.engine.dispose()
        await self.sync_engine.dispose()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    async def getSession(self) -> AsyncSession:
        return self.Session()

postgress = Postgress()

async def getSession() -> AsyncSession:
    return await postgress.getSession()

# async def getSession() -> AsyncSession:
#     async with postgress.Session() as session:
#         yield session

Base = postgress.Base

__all__ = ["postgress", "getSession", "Base"]