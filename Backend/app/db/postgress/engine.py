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
        # Configure connection pool settings to prevent exhaustion
        engine_kwargs = {
            "echo": True if getenv("MODE") == "DEV" else False,
            "future": True,
            "pool_size": 10,  # Base pool size
            "max_overflow": 20,  # Additional connections beyond pool_size
            "pool_timeout": 30,  # Timeout to get connection from pool
            "pool_recycle": 3600,  # Recycle connections every hour
            "pool_pre_ping": True,  # Validate connections before use
        }
        
        self.engine = create_async_engine(DATABASE_URL_ASYNC, **engine_kwargs)
        
        # Sync engine with similar settings
        sync_engine_kwargs = engine_kwargs.copy()
        self.sync_engine = create_engine(DATABASE_URL_SYNC, **sync_engine_kwargs)

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

    async def check_all_models_exist(self) -> tuple[bool, list[str]]:
        """Check if all models exist in the database"""
        async with self.engine.begin() as conn:
            # Perform the entire inspection operation within run_sync
            def get_table_info(sync_conn):
                inspector = inspect(sync_conn)
                return inspector.get_table_names()
            
            existing_tables = await conn.run_sync(get_table_info)
            
            # Get all table names from metadata
            expected_tables = [table.name for table in self.Base.metadata.tables.values()]
            
            # Check if all expected tables exist
            missing_tables = [table for table in expected_tables if table not in existing_tables]
            all_exist = len(missing_tables) == 0
            
            return all_exist, missing_tables

postgress = Postgress()

# Proper session dependency with automatic cleanup
async def getSession() -> AsyncSession:
    """
    FastAPI dependency that provides a database session with automatic cleanup.
    
    This ensures that database sessions are properly closed after each request,
    preventing connection pool exhaustion.
    """
    async with postgress.Session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

Base = postgress.Base

__all__ = ["postgress", "getSession", "Base"]