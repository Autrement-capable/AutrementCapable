"""
Core PostgreSQL connection pool manager.
"""
from typing import Optional, Dict, Any, AsyncGenerator
import asyncpg
from asyncpg.pool import Pool
from os import getenv

from ...core.config import Config

# Cache the connection pool
_pg_pool: Optional[Pool] = None
_pg_config: Optional[Dict[str, Any]] = None

def get_pool_config() -> Dict[str, Any]:
    """
    Get PostgreSQL pool configuration from environment variables and config file.

    Returns:
        Dict[str, Any]: Pool configuration
    """
    global _pg_config

    if _pg_config is None:
        # Get config from file
        config = Config.get_property(None, "database", ["connection_pool"])
        pool_config = config.get("connection_pool", {})

        # Default values
        _pg_config = {
            "min_size": pool_config.get("min_size", 2),
            "max_size": pool_config.get("max_size", 10),
            "max_queries": pool_config.get("max_queries", 50000),
            "max_inactive_connection_lifetime": pool_config.get("max_inactive_connection_lifetime", 300),
            "timeout": pool_config.get("timeout", 60),
            "command_timeout": pool_config.get("command_timeout", 60),
            "statement_cache_size": pool_config.get("statement_cache_size", 100),
        }

    return _pg_config

def get_connection_string() -> str:
    """
    Get PostgreSQL connection string from environment variables.

    Returns:
        str: Connection string
    """
    return (
        f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
        f"@{getenv('POSTGRES_SERVER')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
    )

async def init_pg_pool() -> Pool:
    """
    Initialize the PostgreSQL connection pool.

    Returns:
        Pool: AsyncPG connection pool
    """
    global _pg_pool

    if _pg_pool is None:
        # Get connection string and pool config
        pg_conn_string = get_connection_string()
        pool_config = get_pool_config()

        # Create pool
        print(f"Initializing PostgreSQL connection pool (max_size: {pool_config['max_size']})")
        _pg_pool = await asyncpg.create_pool(
            pg_conn_string,
            min_size=pool_config["min_size"],
            max_size=pool_config["max_size"],
            max_queries=pool_config["max_queries"],
            max_inactive_connection_lifetime=pool_config["max_inactive_connection_lifetime"],
            timeout=pool_config["timeout"],
            command_timeout=pool_config["command_timeout"],
            statement_cache_size=pool_config["statement_cache_size"],
        )

    return _pg_pool

async def close_pg_pool() -> None:
    """Close the PostgreSQL connection pool."""
    global _pg_pool

    if _pg_pool is not None:
        print("Closing PostgreSQL connection pool")
        await _pg_pool.close()
        _pg_pool = None

async def get_pg_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Get a PostgreSQL connection from the pool.

    Yields:
        Connection: AsyncPG connection
    """
    pool = await init_pg_pool()

    async with pool.acquire() as conn:
        yield conn
