import os

from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr
from fastapi_mail import MessageSchema

from ....db.postgress.models.test_model import User, UnverifiedDetails
from ..config import mail

current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up one level to the mail directory, then to templates
template_path = os.path.join(current_dir, "..", "templates")
template_env = Environment(loader=FileSystemLoader(template_path))

VER_URL = os.getenv("VER_URL", "http://localhost:5000/auth/verify")

async def send_verification_email(user: User, details: UnverifiedDetails, email: str = None):
    """
    Send a verification email to the user.
    """
    if email is None:
        email = user.email
    verification_url = VER_URL + f"?code={details.verification_token}"
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