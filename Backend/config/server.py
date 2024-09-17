from fastapi import FastAPI
from fastapi_another_jwt_auth import AuthJWT
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from fastapi.openapi.utils import get_openapi
from config.settings import get_config
from config.cors import init_cors
from config.exception_handlers import authjwt_exception_handler
from modules.utils.singleton import singleton
from os import getenv
import uvicorn

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

        self.port = 5000
        self.host = '0.0.0.0'
        self.log_lvl= "info"

        # Initialize CORS
        init_cors(self.app)

        # Add JWT exception handler
        self.app.add_exception_handler(AuthJWTException, authjwt_exception_handler)

        openapi_tags = [
            {
                "name": "Auth",
                "description": "Operations requiring authentication via ACCESS Token."
            },
            {
                "name": "Auth_refresh",
                "description": "Operations requiring authentication via REFRESH Token."
            }
        ]
        self.app.openapi_tags = openapi_tags
        self.app.openapi = self.__custom_openapi__

        # Initialize and start scheduler
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.__remove_expired_tokens, 'interval', hours=1)
        self.scheduler.start()

    def Run(self):
        try:
            uvicorn.run("app:server.app", host=self.host, port=self.port, log_level=self.log_lvl, reload=True if getenv("MODE") == "DEV" else False)
        except Exception as e:
            print(f"Error: {str(e)}")
            exit(1)

    def __remove_expired_tokens(self):
        # Token removal logic here
        pass

    def __custom_openapi__(self):
        """
        Custom OpenAPI schema for FastAPI app(this is we can test the API in the browser via /docs in Swagger UI)
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

__all__ = ["server", "AddRouter"]
