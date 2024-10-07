from pydantic import BaseModel
from dotenv import load_dotenv
import yaml
from os import getenv

load_dotenv()

__config_file__ = "./config/config.yaml"

class Settings(BaseModel):
    authjwt_secret_key: str
    jwt_access_token_expires: int  # in seconds
    jwt_refresh_token_expires: int  # in seconds
    authjwt_algorithm: str = "HS256"
    authjwt_token_location: list[str] = ["headers"]
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: list[str] = ["access", "refresh"]

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

def get_config():
    return Settings.from_yaml(__config_file__)