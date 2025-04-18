from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import create_engine, inspect

from ...utils.patterns import singleton

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
        """Close all database connections."""
        # Close the async engine
        if self.engine is not None:
            await self.engine.dispose()

        # Close the sync engine (without await since it's not async)
        if hasattr(self, 'sync_engine') and self.sync_engine is not None:
            self.sync_engine.dispose()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    async def getSession(self) -> AsyncSession:
        return self.Session()

    async def check_all_models_exist(self) -> tuple[bool, dict]:
        """
        Check if all models exist in the database.

        Use 
        Returns:
            - A tuple containing a boolean indicating if all models exist,
              and a dictionary with table names as keys and their existence as values.
        """
        result = {}
        defined_tables = self.Base.metadata.tables.keys()

        async with self.engine.begin() as conn:
            insp = await conn.run_sync(inspect)
            existing_tables = await conn.run_sync(lambda sync_conn: insp.get_table_names())

            for table in defined_tables:
                result[table] = table in existing_tables

        # if all tables exist, return True, dict otherwise return False, dict
        return all(result.values()), result

postgress = Postgress()

async def getSession() -> AsyncSession:
    return await postgress.getSession()

# async def getSession() -> AsyncSession:
#     async with postgress.Session() as session:
#        try:
#           yield session
#        finally:
#           await session.close()

Base = postgress.Base

__all__ = ["postgress", "getSession", "Base"]