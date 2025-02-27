"""
Tests for mail sending functionality.
"""
import pytest
from datetime import datetime, timedelta
from fastapi_mail import MessageSchema

from mail.actions.verify_account import send_verification_email
from mail.actions.reset_password import send_reset_password_email
from database.postgress.models import User, UnverifiedDetails, PasswordReset

pytestmark = pytest.mark.functionality

class MockFastMail:
    """Mock FastMail class for testing."""
    def __init__(self):
        self.sent_messages = []

    async def send_message(self, message):
        """Mock sending a message."""
        self.sent_messages.append(message)
        return True

@pytest.fixture
def mock_mail(monkeypatch):
    """Fixture to mock mail sending."""
    mock_fastmail = MockFastMail()
    monkeypatch.setattr("mail.config.mail", mock_fastmail)
    return mock_fastmail

@pytest.mark.asyncio
async def test_send_verification_email(mock_mail):
    """Test sending a verification email."""
    # Create test user and details
    user = User(
        id=999,
        username="mailtest",
        email="mailtest@example.com",
        password_hash="hash",
        role_id=1
    )

    details = UnverifiedDetails(
        user_id=999,
        verification_token="test_verification_token",
        token_expires=datetime.utcnow() + timedelta(hours=1)
    )

    # Send the verification email
    result = await send_verification_email(user, details)

    # Check the result
    assert result is True

    # Check that the email was sent with the right parameters
    assert len(mock_mail.sent_messages) == 1
    message = mock_mail.sent_messages[0]

    assert isinstance(message, MessageSchema)
    assert message.subject == "Verify Your Account"
    assert message.recipients == ["mailtest@example.com"]
    assert message.subtype == "html"

    # Check that the email body contains the verification token
    assert "test_verification_token" in message.body
    assert user.username in message.body

@pytest.mark.asyncio
async def test_send_verification_email_alternate_address(mock_mail):
    """Test sending a verification email to an alternate address."""
    # Create test user and details
    user = User(
        id=999,
        username="mailtest",
        email="mailtest@example.com",
        password_hash="hash",
        role_id=1
    )

    details = UnverifiedDetails(
        user_id=999,
        verification_token="test_verification_token",
        token_expires=datetime.utcnow() + timedelta(hours=1)
    )

    # Send to alternate email
    result = await send_verification_email(user, details, email="alternate@example.com")

    # Check the result
    assert result is True

    # Check that the email was sent to the alternate address
    assert len(mock_mail.sent_messages) == 1
    message = mock_mail.sent_messages[0]
    assert message.recipients == ["alternate@example.com"]

@pytest.mark.asyncio
async def test_send_reset_password_email(mock_mail):
    """Test sending a password reset email."""
    # Create test user and reset
    user = User(
        id=999,
        username="resettest",
        email="resettest@example.com",
        password_hash="hash",
        role_id=1
    )

    reset = PasswordReset(
        user_id=999,
        reset_token="test_reset_token",
        token_expires=datetime.utcnow() + timedelta(hours=1)
    )

    # Send the reset email
    result = await send_reset_password_email(user, reset)

    # Check the result
    assert result is True

    # Check that the email was sent with the right parameters
    assert len(mock_mail.sent_messages) == 1
    message = mock_mail.sent_messages[0]

    assert isinstance(message, MessageSchema)
    assert message.subject == "Reset Your Password"
    assert message.recipients == ["resettest@example.com"]
    assert message.subtype == "html"

    # Check that the email body contains the reset token
    assert "test_reset_token" in message.body
    assert user.username in message.body

@pytest.mark.asyncio
async def test_send_reset_password_email_alternate_address(mock_mail):
    """Test sending a password reset email to an alternate address."""
    # Create test user and reset
    user = User(
        id=999,
        username="resettest",
        email="resettest@example.com",
        password_hash="hash",
        role_id=1
    )

    reset = PasswordReset(
        user_id=999,
        reset_token="test_reset_token",
        token_expires=datetime.utcnow() + timedelta(hours=1)
    )

    # Send to alternate email
    result = await send_reset_password_email(user, reset, email="alternate@example.com")

    # Check the result
    assert result is True

    # Check that the email was sent to the alternate address
    assert len(mock_mail.sent_messages) == 1
    message = mock_mail.sent_messages[0]
    assert message.recipients == ["alternate@example.com"]

@pytest.mark.asyncio
async def test_send_email_error_handling(monkeypatch):
    """Test error handling in email sending."""
    # Create a mock that raises an exception
    async def mock_send_message_error(*args, **kwargs):
        raise Exception("Test mail sending error")

    class MockFailingFastMail:
        async def send_message(self, message):
            await mock_send_message_error()

    monkeypatch.setattr("mail.config.mail", MockFailingFastMail())

    # Create test user and details
    user = User(
        id=999,
        username="errortest",
        email="errortest@example.com",
        password_hash="hash",
        role_id=1
    )

    details = UnverifiedDetails(
        user_id=999,
        verification_token="test_token",
        token_expires=datetime.utcnow() + timedelta(hours=1)
    )

    # Try to send email
    result = await send_verification_email(user, details)

    # Should return False on error
    assert result is False
