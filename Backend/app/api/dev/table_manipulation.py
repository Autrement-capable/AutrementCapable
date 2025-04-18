## Debugging endpoints to manipulate tables in the database
## FIY: SHOULD NOT BE USED IN PRODUCTION

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.future import select
from sqlalchemy import text, inspect

from ...core.application import AddRouter
from ...db.postgress.engine import getSession, postgress

example_router = APIRouter(prefix="/dev", tags=["Development"])

# Ensure we have a reference to the async engine
async_engine: AsyncEngine = postgress.engine

@example_router.get("/all-tables")
async def all_tables(DB: AsyncSession = Depends(getSession)):
    """Get all tables in the database."""
    async with async_engine.begin() as conn:
        inspector = inspect(conn)
        tables = inspector.get_table_names()
    return {"tables": tables}

# Route used for dropping all tables
@example_router.get("/drop-all-tables")
async def drop_all_tables(DB: AsyncSession = Depends(getSession)):
    """Drop all tables in the database."""
    async with async_engine.begin() as conn:
        inspector = inspect(conn)
        tables = inspector.get_table_names()
        for table in tables:
            await conn.execute(text(f"DROP TABLE {table} CASCADE"))
    return {"message": "All tables dropped"}

@example_router.get("/drop-table/{table_name}")
async def drop_table(table_name: str = Path(..., title="The name of the table to drop."), DB: AsyncSession = Depends(getSession)):
    """Drop a table in the database."""
    await DB.execute(text(f"DROP TABLE {table_name} CASCADE"))
    await DB.commit()
    return {"message": f"{table_name} dropped"}

AddRouter(example_router)  # Add the router to the server