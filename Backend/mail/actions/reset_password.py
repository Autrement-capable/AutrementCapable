from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr
from fastapi_mail import MessageSchema
from database.postgress.models.user import User
from database.postgress.models.password_reset import PasswordReset
from mail.config import mail

from os import getenv

template_env = Environment(loader=FileSystemLoader("mail/templates"))

RESET_URL = getenv("RESET_URL", "http://localhost:5000/auth//reset-password")

async def send_reset_password_email(user: User, reset: PasswordReset, email: str = None):
    """
    Send a reset password email to the user.
    """
    if email is None:
        email = user.email
    reset_url = RESET_URL + f"?token={reset.reset_token}"
    template = template_env.get_template("password_reset.html")
    # Render the template with dynamic content
    html_content = template.render(username=user.username, reset_url=reset_url)

    # Create the email message
    message = MessageSchema(
        subject="Reset Your Password",
        recipients=[email],
        body=html_content,
        subtype="html",
    )
    try:
        await mail.send_message(message)
        return True
    except Exception as e:
        print(f"An error occurred while sending the reset password email: {e}")
        return False
    assert False, "Never should reach this line"
