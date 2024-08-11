from fastapi import FastAPI
from fastapi_another_jwt_auth import AuthJWT
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from modules.utils.singleton import singleton
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel
import uvicorn
from os import getenv
import yaml

load_dotenv()
__config_file__ = "./config/config.yaml"
class Settings(BaseModel):
    authjwt_secret_key: str
    jwt_access_token_expires: int  # in seconds
    jwt_refresh_token_expires: int  # in seconds

    @classmethod
    def from_yaml(cls, config_path: str):
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        auth_config = config.get("auth", {})
        access_token_duration = auth_config.get("access_token_duration", {})
        refresh_token_duration = auth_config.get("refresh_token_duration", {})

        access_token_seconds = (
            access_token_duration.get("hours", 0) * 3600 +
            access_token_duration.get("minutes", 0) * 60 +
            access_token_duration.get("seconds", 0)
        )

        refresh_token_seconds = (
            refresh_token_duration.get("days", 0) * 86400 +
            refresh_token_duration.get("hours", 0) * 3600 +
            refresh_token_duration.get("minutes", 0) * 60 +
            refresh_token_duration.get("seconds", 0)
        )

        return cls(
            authjwt_secret_key=getenv("SERVER_SECRET"),
            jwt_access_token_expires=access_token_seconds,
            jwt_refresh_token_expires=refresh_token_seconds,
        )


@AuthJWT.load_config
def get_config():
    return Settings.from_yaml(__config_file__)

@singleton
class Server:
    def __init__(self):
        self.app = FastAPI(
            title="Autrement Capable API Dev Server",
            description="The API for the DrumGan project Monetization.",
            version=getenv("VERSION", "0.1.0alpha"),
            docs_url="/docs" if getenv("MODE") == "DEV" else None
        )

        self.port = 5000
        self.host = '0.0.0.0'
        self.log_lvl= "info"

        self.__init_cors()

        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.__remove_expired_tokens, 'interval', hours=1)
        self.scheduler.start()


    def __init_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def Run(self):
        try:
            uvicorn.run(self.app, host=self.host, port=self.port, log_level=self.log_lvl)
        except Exception as e:
            print(f"Error: {str(e)}")
            exit(1)

    def __remove_expired_tokens(self):
        # Token removal logic here
        pass

server = Server()

__all__ = ["server"]