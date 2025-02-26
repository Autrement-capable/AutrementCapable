from sqlmodel import SQLModel, Field, Relationship, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional, List
import asyncio


# Define ModelB
class ModelB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    model_a_items: List["ModelA"] = Relationship(back_populates="model_b")
    model_c_items: List["ModelC"] = Relationship(back_populates="model_b")


# Define ModelA
class ModelA(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    model_b_id: int = Field(foreign_key="modelb.id")
    model_b: "ModelB" = Relationship(back_populates="model_a_items")


# Define ModelC
class ModelC(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    model_b_id: int = Field(foreign_key="modelb.id")
    model_b: "ModelB" = Relationship(back_populates="model_c_items")


# Async example usage
async def async_main():
    # Initialize async database engine
    sqlite_file_name = "async_database.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{sqlite_file_name}", echo=True)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create instances in async context
    async with AsyncSession(engine) as session:
        # Create a ModelB instance
        model_b = ModelB(name="Shared ModelB")
        session.add(model_b)
        await session.commit()
        await session.refresh(model_b)

        # Create a ModelA instance linked to ModelB
        model_a = ModelA(name="ModelA Instance", model_b=model_b)
        session.add(model_a)
        await session.commit()
        await session.refresh(model_a)

        # Ensure model_a is fully refreshed to load relationships
        await session.refresh(model_a)

        # Create a ModelC instance using the same ModelB instance from ModelA
        model_c = ModelC(description="ModelC Instance", model_b=model_a.model_b)
        session.add(model_c)
        await session.commit()
        await session.refresh(model_c)

        # Query and print to verify
        query = select(ModelC).where(ModelC.id == model_c.id)
        result = await session.execute(query)
        retrieved_model_c = result.scalar_one()
        print(f"ModelC: {retrieved_model_c.description}, Related ModelB: {retrieved_model_c.model_b.name}")


# Run the async main function
if __name__ == "__main__":
    asyncio.run(async_main())
