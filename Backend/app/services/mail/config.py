# mail_config.py

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from os import getenv

class MailConfig(BaseModel):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

def get_mail_config():
    if getenv("MODE") == "DEV":
        return MailConfig(
            MAIL_USERNAME=getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=getenv("MAIL_PASSWORD"),
            MAIL_FROM=getenv("MAIL_FROM"),
            MAIL_PORT=int(getenv("MAIL_PORT")),
            MAIL_SERVER=getenv("MAIL_SERVER"),
            MAIL_STARTTLS=getenv("MAIL_STARTTLS", "false").lower() == 'true',
            MAIL_SSL_TLS=getenv("MAIL_SSL_TLS", "false").lower() == 'true'
        )
    else:
        raise ValueError("Email configuration not set for production")

mail_config = get_mail_config()

conf = ConnectionConfig(
    MAIL_USERNAME=mail_config.MAIL_USERNAME,
    MAIL_PASSWORD=mail_config.MAIL_PASSWORD,
    MAIL_FROM=mail_config.MAIL_FROM,
    MAIL_PORT=mail_config.MAIL_PORT,
    MAIL_SERVER=mail_config.MAIL_SERVER,
    MAIL_STARTTLS=mail_config.MAIL_STARTTLS,
    MAIL_SSL_TLS=mail_config.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

mail = FastMail(conf)
