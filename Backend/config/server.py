from fastapi import FastAPI, Depends
from fastapi_another_jwt_auth import AuthJWT
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from fastapi.openapi.utils import get_openapi
from config.settings import get_config
from config.cors import init_cors
from config.exception_handlers import authjwt_exception_handler
from config.roles import init_roles
from modules.utils.singleton import singleton
from database.postgress.setup import postgress
from database.postgress.actions.revoked_jwt_tokens import delete_expired_tokens, get_revoked_token_by_jti
import uvicorn
from os import getenv
import asyncio


@AuthJWT.load_config
def load_config():
    return get_config()


@singleton
class Server:
    def __init__(self):
        self.app = FastAPI(
            title="Autrement Capable API Dev Server",
            description="The API for Autrement Capable Backend.",
            version=getenv("VERSION", "0.1.0alpha"),
            docs_url="/docs" if getenv("MODE") == "DEV" else None
        )

        self.port = int(getenv("PORT", 5000))
        self.host = '0.0.0.0'
        self.log_lvl = "info"
        self.postgress = postgress

        # Initialize CORS
        init_cors(self.app)

        # Add JWT exception handler
        self.app.add_exception_handler(AuthJWTException, authjwt_exception_handler)

        # Initialize the database asynchronously in FastAPI startup event
        self.app.add_event_handler("startup", self.on_startup)

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
        await self.postgress.create_db_and_tables()

        # Initialize roles asynchronously
        await self.init_roles()

        # Start the async scheduler for deleting expired tokens
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.__remove_expired_tokens, 'interval', hours=1)
        self.scheduler.start()

    async def init_roles(self):
        """ Initialize roles asynchronously """
        async with self.postgress.GetSession() as session:
            await init_roles(session)

    async def __remove_expired_tokens(self):
        """ Remove expired tokens from the database asynchronously """
        async with self.postgress.GetSession() as session:
            await delete_expired_tokens(session)

    async def get_Psession(self):
        """Get an async session for the postgress database."""
        async with self.postgress.GetSession() as session:
            yield session

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

    def Run(self):
        """ Run the server. """
        try:
            uvicorn.run("app:server.app", host=self.host, port=self.port, log_level=self.log_lvl, reload=True if getenv("MODE") == "DEV" else False)
        except Exception as e:
            print(f"Error: {str(e)}")
            exit(1)


server = Server()

# does not work currently
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    async def check_token():
        async with postgress.GetSession() as session:
            jti = decrypted_token['jti']
            print("the jti is", jti) # gets called
            return await get_revoked_token_by_jti(session, jti) is None

    # Run the async function in the main thread( using async engine so this is necessary)
    return asyncio.create_task(check_token())


def AddRouter(router):
    server.app.include_router(router)

__all__ = ["server", "AddRouter"]