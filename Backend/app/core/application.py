from os import getenv
import atexit
from contextlib import asynccontextmanager
from typing import Callable

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

from ..utils.patterns import singleton
from ..db.postgress.engine import postgress
from ..services.scheduler.factory import CronJobFactory
from ..services.auth.roles import init_roles
from ..services.content.terms import init_terms
from .cors.config import init_cors
from .security.decorators import SecurityRequirement

@singleton
class Server:
    def AddCronJob(self, func: Callable, **kwargs: dict):
        """ Add a cron job to the scheduler """
        self.scheduler.add_job(self.run_job_with_session, args=[func], **kwargs)

    def __init__(self):
        # First, initialize your properties
        self.port = int(getenv("PORT", 5000))
        self.host = '0.0.0.0'
        self.log_lvl = "info"
        self.postgress = postgress
        # Initialize scheduler before setting up lifespan so we dont get stupid errors
        self.scheduler = AsyncIOScheduler()

        # Acording the fast api docs this better than using on_event(deprecated)
        # I disagree but need to make the code compatible with the rest of the code
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Startup
            CronJobFactory.set_add_cron_job(self.AddCronJob)

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
            try:
                if self.scheduler and hasattr(self.scheduler, 'running') and self.scheduler.running:
                    print("Shutting down scheduler...")
                    self.scheduler.shutdown(wait=False)
            except Exception as e:
                print(f"Error shutting down scheduler: {e}")

            try:
                if self.postgress:
                    print("Closing database connections...")
                    await self.postgress.close()
            except Exception as e:
                print(f"Error closing database connections: {e}")

        self.app = FastAPI(
            title="Autrement Capable API Dev Server",
            description="The API for Autrement Capable Backend.",
            version=getenv("VERSION", "0.1.0alpha"),
            docs_url="/docs" if getenv("MODE") == "DEV" else None,
            redoc_url="/redoc" if getenv("MODE") == "DEV" else None,
            lifespan=lifespan,
        )

        # Initialize CORS
        init_cors(self.app)

        # Set up custom OpenAPI
        self.app.openapi = self.__custom_openapi__

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
        )

        # Define security schemes
        openapi_schema["components"]["securitySchemes"] = {
            "Authorization": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT Authorization header using the Bearer scheme"
            },
            "RefreshCookie": {
                "type": "apiKey",
                "in": "cookie",
                "name": "refresh_token",
                "description": "JWT Refresh token stored in HTTP-only cookie"
            }
        }

        # Add security requirements to endpoints based on their decorators
        for path, path_item in openapi_schema["paths"].items():
            for method, operation in path_item.items():
                for route in self.app.routes:
                    if hasattr(route, "endpoint") and route.path == path and method.upper() in route.methods:
                        endpoint = route.endpoint

                        # Find the original function if wrapped
                        while hasattr(endpoint, "__wrapped__"):
                            endpoint = endpoint.__wrapped__

                        if hasattr(endpoint, "requires_auth") and endpoint.requires_auth:
                            security_type = getattr(endpoint, "security_type", SecurityRequirement.ACCESS_TOKEN)

                            if security_type == SecurityRequirement.ACCESS_TOKEN:
                                operation["security"] = [{"Authorization": []}]
                            elif security_type == SecurityRequirement.REFRESH_COOKIE:
                                operation["security"] = [{"RefreshCookie": []}]
                            elif security_type == SecurityRequirement.BOTH_TOKENS:
                                operation["security"] = [{"Authorization": [], "RefreshCookie": []}]
                            else:
                                operation["security"] = [{"Authorization": []}]

                            # Add custom description if provided
                            custom_desc = getattr(endpoint, "security_description", None)
                            if custom_desc:
                                if "description" not in operation:
                                    operation["description"] = ""
                                operation["description"] += f"\n\n**Auth:** {custom_desc}"

        self.app.openapi_schema = openapi_schema
        return self.app.openapi_schema

server = Server()

def AddRouter(router):
    server.app.include_router(router)

__all__ = ["server", "AddRouter"]
