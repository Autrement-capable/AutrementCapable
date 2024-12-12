from fastapi import APIRouter, Depends, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import inspect
from sqlalchemy import text
from server.server import AddRouter
from database.postgress.config import GetSession

example_router = APIRouter(prefix="/dev", tags=["Development"])

@example_router.get("/all-tables")
async def all_tables(DB: AsyncSession = Depends(GetSession)):
    """Get all tables in the database."""
    inspector = inspect(DB.bind)
    tables = await DB.run_sync(inspector.get_table_names)
    return {"tables": tables}

# route used for dropping all tables
@example_router.get("/drop-all-tables")
async def drop_all_tables(DB: AsyncSession = Depends(GetSession)):
    """Drop all tables in the database."""
    inspector = inspect(DB.bind)
    tables = await DB.run_sync(inspector.get_table_names)
    for table in tables:
        await DB.execute(text(f"DROP TABLE {table} CASCADE"))
    await DB.commit()
    return {"message": "All tables dropped"}

@example_router.get("/drop-table/{table_name}")
async def drop_table(table_name: str = Path(..., title="The name of the table to drop."), DB: AsyncSession = Depends(GetSession)):
    """Drop a table in the database."""
    await DB.execute(text(f"DROP TABLE {table_name} CASCADE"))
    await DB.commit()
    return {"message": f"{table_name} dropped"}

@example_router.get("/get-table/{table_name}")
async def get_table(table_name: str = Path(..., title="The name of the table to get."), DB: AsyncSession = Depends(GetSession)):
    """Get a table in the database."""
    inspector = inspect(DB.bind)
    table = await DB.run_sync(inspector.get_table, table_name)
    return {"table": table}

AddRouter(example_router)  # Add the router to the server