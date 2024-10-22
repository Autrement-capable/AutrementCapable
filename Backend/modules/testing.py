from fastapi import APIRouter, Depends, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import inspect
from sqlalchemy import text
from config.server import AddRouter, server

example_router = APIRouter(prefix="/test", tags=["Testing"])

@example_router.get("/all-tables")
async def all_tables(DB: AsyncSession = Depends(server.get_Psession)):
    """Get all tables in the database."""
    inspector = inspect(DB.bind)
    tables = await DB.run_sync(inspector.get_table_names)  # Use run_sync for synchronous calls in async code
    return {"tables": tables}

# route used for dropping all tables
@example_router.get("/drop-all-tables")
async def drop_all_tables(DB: AsyncSession = Depends(server.get_Psession)):
    """Drop all tables in the database."""
    inspector = inspect(DB.bind)
    tables = await DB.run_sync(inspector.get_table_names)  # Use run_sync for synchronous calls
    for table in tables:
        await DB.execute(text(f"DROP TABLE {table} CASCADE"))  # Use await for async DB execution
    await DB.commit()  # Don't forget to commit the transaction after executing the drop commands
    return {"message": "All tables dropped"}

AddRouter(example_router)  # Add the router to the server