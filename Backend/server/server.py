from os import getenv
from fastapi import FastAPI, Depends
from fastapi_another_jwt_auth import AuthJWT
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from fastapi.openapi.utils import get_openapi
from server.jwt_config.settings import get_config
from server.cors.config import init_cors
from server.jwt_config.exception_handlers import authjwt_exception_handler
from server.role_config.roles import init_roles
from utils.singleton import singleton
from database.postgress.config import postgress
from database.postgress.actions.revoked_jwt_tokens import delete_expired_tokens, get_revoked_token_by_jti,  get_revoked_token_by_jti_sync
import uvicorn

# not used becasue jwt deny list does not support async
import asyncio
import anyio
from fastapi.concurrency import run_in_threadpool
from typing import Callable

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

        # Start the async scheduler for deleting expired tokens
        self.scheduler = AsyncIOScheduler()

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
        await self.postgress.create_all()

        # Initialize roles asynchronously
        await self.init_roles()

        self.scheduler.add_job(self.__remove_expired_tokens, 'interval', hours=1)
        self.scheduler.start()

    async def init_roles(self):
        """ Initialize roles asynchronously """
        session = await self.postgress.getSession()
        await init_roles(session)

    async def __remove_expired_tokens(self):
        """ Remove expired tokens from the database asynchronously """
        session = await self.postgress.getSession()
        await delete_expired_tokens(session)

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

# # This function is used to check if a token has been revoked async DOES NOT WORK because the lib does not support async
# @AuthJWT.token_in_denylist_loader
# def check_if_token_in_denylist(decrypted_token):
#     async def check_token():
#         async with postgress.GetSession() as session:
#             jti = decrypted_token['jti']
#             print(f"Checking if jti is revoked: {jti}")
#             token = await get_revoked_token_by_jti(session, jti)
#             print(f"Token found: {token}")  # Debug line
#             return token is not None  # Returns True if token exists (revoked), False if not

#     # Submit the coroutine to the running loop
#     loop = asyncio.get_event_loop()
#     future = asyncio.run_coroutine_threadsafe(check_token(), loop)
#     return future.result()

# Cant use async function because the lib does not support it
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    session = postgress.get_SyncSession()  # Get sync session
    try:
        token = get_revoked_token_by_jti_sync(session, jti)
        return token is not None
    except Exception as e:
        print(f"Error checking token deny list: {e}")
        return True  # Fail-safe: If an error occurs, reject the token
    finally:
        session.close()  # Ensure session is always closed



def AddRouter(router):
    server.app.include_router(router)

def AddCronJob(func: Callable, **kwargs: dict):
    """ Add a cron job to the scheduler """
    server.scheduler.add_job(func, **kwargs)

__all__ = ["server", "AddRouter", "AddCronJob"]