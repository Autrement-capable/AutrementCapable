from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr
from fastapi_mail import MessageSchema
from database.postgress.models.unverified_user import UnverifiedUser
from mail.config import mail

template_env = Environment(loader=FileSystemLoader("email_templates"))

VER_URL = "http://localhost:8000/auth/verify"

def send_verification_email(user: UnverifiedUser, email: str = None):
    """
    Send a verification email to the user.
    """
    if email is None:
        email = user.email
    verification_url = VER_URL + f"?code={user.verification_code}"
    template = template_env.get_template("verification.html")
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
        mail.send_message(message)
        return True
    except Exception as e:
        print(f"An error occurred while sending the verification email: {e}")
        return False
    assert false, "Never should reach this line"