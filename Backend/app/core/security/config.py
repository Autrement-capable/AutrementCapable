import os
import base64
from os import getenv, urandom

import yaml
from pydantic import BaseModel
from dotenv import load_dotenv

from ...utils.config_helpers import get_property

load_dotenv()

__config_file__ = "./config/config.yaml"

class Settings(BaseModel):
    authjwt_secret_key: str
    jwt_access_token_expires: int
    jwt_refresh_token_expires: int
    authjwt_algorithm: str
    authjwt_token_location: list[str]
    authjwt_denylist_enabled: bool
    authjwt_denylist_token_checks: list[str]
    aes_key: bytes
    nonce_size: int
    auth_schema: str
    cookie_secure: bool  # Whether to use secure cookies (HTTPS only)

    @classmethod
    def from_yaml(cls, config_path: str):
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        config_vals = get_property(config, "auth", ["access_token_duration", "refresh_token_duration"])

        # Determine if we're in production or development
        is_prod = getenv("MODE", "DEV").upper() != "DEV"

        return cls(
            authjwt_secret_key=getenv("SERVER_SECRET", "default_secret"),
            jwt_access_token_expires=config_vals.get("access_token_duration", 3600),
            jwt_refresh_token_expires=config_vals.get("refresh_token_duration", 86400),
            authjwt_algorithm="HS256",
            authjwt_token_location=["headers", "cookies"],  # Now supporting both headers and cookies
            authjwt_denylist_enabled=True,
            authjwt_denylist_token_checks=["access", "refresh"],
            aes_key=base64.b64decode(getenv("AES_KEY", base64.b64encode(urandom(32)).decode('utf-8'))),
            nonce_size=12,
            auth_schema="Bearer ",
            cookie_secure=is_prod  # Secure cookies in production, non-secure in development
        )

# Load settings from the YAML file during class initialization
__config_file__ = "./config/config.yaml"
settings = Settings.from_yaml(__config_file__)