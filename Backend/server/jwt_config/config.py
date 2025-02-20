from pydantic import BaseModel
from dotenv import load_dotenv
import yaml
from os import getenv, urandom
from utils.parse_yaml import get_property

load_dotenv()

__config_file__ = "./server/config_files/config.yaml"

class Settings(BaseModel):
    authjwt_secret_key: str
    jwt_access_token_expires: int  # in seconds
    jwt_refresh_token_expires: int  # in seconds
    authjwt_algorithm: str = "HS256"
    authjwt_token_location: list[str] = ["headers"]
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: list[str] = ["access", "refresh"]
    aes_key: bytes
    nonce_size: int = 12

    @classmethod
    def from_yaml(cls, config_path: str):
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        config_vals = get_property(config, "auth", ["access_token_duration", "refresh_token_duration"])

        return cls(
            authjwt_secret_key=getenv("SERVER_SECRET"),
            jwt_access_token_expires=config_vals["access_token_duration"],
            jwt_refresh_token_expires=config_vals["refresh_token_duration"],
            aes_key=getenv("AES_KEY", urandom(32))
        )

def get_config():
    return Settings.from_yaml(__config_file__)