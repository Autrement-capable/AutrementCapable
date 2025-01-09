from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr
from fastapi_mail import MessageSchema
from database.postgress.models.test_model import UnverifiedUser
from mail.config import mail

from os import getenv

template_env = Environment(loader=FileSystemLoader("mail/templates"))

VER_URL = getenv("VER_URL", "http://localhost:5000/auth/verify")


async def send_verification_email(user: UnverifiedUser, email: str = None):
    """
    Send a verification email to the user.
    """
    if email is None:
        email = user.email
    verification_url = VER_URL + f"?code={user.verification_token}"
    template = template_env.get_template("account_verification.html")
    # Render the template with dynamic content
    html_content = template.render(username=user.username, verification_url=verification_url)

    # Create the email message
    message = MessageSchema(
        subject="Verify Your Account",
        recipients=[email],
        body=html_content,
        subtype="html",
    )
    try:
        await mail.send_message(message)
        return True
    except Exception as e:
        print(f"An error occurred while sending the verification email: {e}")
        return False
    assert False, "Never should reach this line"