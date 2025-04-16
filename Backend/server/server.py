from dotenv import load_dotenv
load_dotenv()

from os import getenv
from fastapi import FastAPI, Depends
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.openapi.utils import get_openapi
from server.cors.config import init_cors
from server.misc_config.roles import init_roles
from server.misc_config.init_terms import init_terms
from utils.singleton import singleton
from database.postgress.config import postgress
from database.postgress.actions.revoked_jwt_tokens import get_revoked_token_by_jti,  get_revoked_token_by_jti_sync
import uvicorn
from .cron_jobs.factory import CronJobFactory

# not used becasue jwt deny list does not support async
import asyncio
import anyio
from fastapi.concurrency import run_in_threadpool
from contextlib import asynccontextmanager
from typing import Callable

@singleton
class Server:
    def __init__(self):
        # Acording the fast api docs this better than using on_event(deprecated)
        # I disagree but need to make the code compatible with the rest of the code
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Startup
            CronJobFactory.set_add_cron_job(AddCronJob)

            # Check if tables exist and initialize data if needed
            exists, _ = await self.postgress.check_all_models_exist()
            if not exists:
                await self.postgress.create_all()
                await self.init_roles()
                await init_terms()

            # Start scheduler
            self.scheduler.start()
            CronJobFactory.register_jobs()

            yield  # This is where FastAPI serves requests

            # Shutdown
            if hasattr(self, 'scheduler') and self.scheduler is not None:
                await self.scheduler.shutdown()
            else:
                print("Scheduler was already shut down or was None")

            if hasattr(self.postgress, 'engine') and self.postgress.engine is not None:
                print("Closing database connections...")
                await self.postgress.close()

        self.app = FastAPI(
            title="Autrement Capable API Dev Server",
            description="The API for Autrement Capable Backend.",
            version=getenv("VERSION", "0.1.0alpha"),
            docs_url="/docs" if getenv("MODE") == "DEV" else None,
            lifespan=lifespan,
        )

        self.port = int(getenv("PORT", 5000))
        self.host = '0.0.0.0'
        self.log_lvl = "info"
        self.postgress = postgress

        # Start the async scheduler for deleting expired tokens
        self.scheduler = AsyncIOScheduler()

        # Initialize CORS
        init_cors(self.app)

        # Set up custom OpenAPI
        self.app.openapi_tags = self.get_openapi_tags()
        self.app.openapi = self.__custom_openapi__

    def get_openapi_tags(self):
        return [
            {
                "name": "Auth",
                "description": "Operations requiring authentication via ACCESS Token."
            },
            {
                "name": "Auth_refresh",
                "description": "Operations requiring authentication via REFRESH Token."
            }
        ]

    async def on_startup(self):
        """ This function runs during startup of FastAPI application. """
        # Initialize the database and create tables asynchronously
        exists, _ = await self.postgress.check_all_models_exist()
        if not exists: # if tables do not exist, create them and init data
            await self.postgress.create_all()

            # Initialize roles asynchronously
            await self.init_roles()

            # Initialize Terms creation
            await init_terms()

        server.scheduler.start()
        CronJobFactory.register_jobs()

    @staticmethod
    async def run_job_with_session(func:Callable):
        """Executes a cron job with a managed AsyncSession."""
        async with postgress.Session() as session:
            try:
                await func(session)
            except Exception as e:
                print(f"[TaskScheduler] Error running {func.__name__}: {e}")
                await session.rollback()
            finally:
                await session.close()

    async def init_roles(self):
        """ Initialize roles asynchronously """
        session = await self.postgress.getSession()
        await init_roles(session)

    def __custom_openapi__(self):
        """
        Custom OpenAPI schema for FastAPI app.
        """
        if self.app.openapi_schema:
            return self.app.openapi_schema

        openapi_schema = get_openapi(
            title="Autrement Capable API Dev Server",
            version=getenv("VERSION", "0.1.0alpha"),
            description="The API for Autrement Capable Backend.",
            routes=self.app.routes,
            tags=self.app.openapi_tags
        )

        openapi_schema["components"]["securitySchemes"] = {
            "Authorization": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT Authorization header using the Bearer scheme (FYI: do not include 'Bearer ' in the value)",
            }
        }

        for path, path_item in openapi_schema["paths"].items():
            for method, operation in path_item.items():
                tags = operation.get("tags", [])
                if "Auth" in tags or "Auth_refresh" in tags:
                    operation["security"] = [{"Authorization": []}]

        self.app.openapi_schema = openapi_schema
        return self.app.openapi_schema

server = Server()

def AddRouter(router):
    server.app.include_router(router)

def AddCronJob(func: Callable, **kwargs: dict):
    """ Add a cron job to the scheduler """
    server.scheduler.add_job(server.run_job_with_session, args=[func], **kwargs)

__all__ = ["server", "AddRouter", "AddCronJob"]
