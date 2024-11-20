from fastapi import APIRouter, Depends, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import inspect
from sqlalchemy import text
from server.server import AddRouter
from database.postgress.setup import postgress

example_router = APIRouter(prefix="/dev", tags=["Development"])

@example_router.get("/all-tables")
async def all_tables(DB: AsyncSession = Depends(postgress.GetSession)):
    """Get all tables in the database."""
    inspector = inspect(DB.bind)
    tables = await DB.run_sync(inspector.get_table_names)
    return {"tables": tables}

# route used for dropping all tables
@example_router.get("/drop-all-tables")
async def drop_all_tables(DB: AsyncSession = Depends(postgress.GetSession)):
    """Drop all tables in the database."""
    inspector = inspect(DB.bind)
    tables = await DB.run_sync(inspector.get_table_names)
    for table in tables:
        await DB.execute(text(f"DROP TABLE {table} CASCADE"))
    await DB.commit()
    return {"message": "All tables dropped"}

AddRouter(example_router)  # Add the router to the server