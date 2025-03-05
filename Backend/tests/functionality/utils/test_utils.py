"""
Tests for utility functions.
"""
import pytest
import os
import tempfile
import yaml
from datetime import datetime, timedelta

from utils.Config_loader import Config
from utils.password import hash_password, verify_password
from utils.verifcation_code import generate_verification_code, generate_random_suffix
from utils.jwt_exceptions import create_response_dict
from utils.singleton import singleton

pytestmark = pytest.mark.functionality

class TestConfigLoader:
    """Tests for the Config loader utility."""

    def test_load_config(self):
        """Test loading a config file."""
        # Create a temporary YAML file
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.yaml', delete=False) as temp:
            temp.write("""
test_section:
  test_key: test_value
  time_key:
    minutes: 30
    seconds: 15
            """)
            temp_filename = temp.name

        try:
            # Load the config
            config = Config.load_config(temp_filename)

            # Check the config contents
            assert "test_section" in config
            assert "test_key" in config["test_section"]
            assert config["test_section"]["test_key"] == "test_value"

            # Check time conversion
            assert "time_key" in config["test_section"]
            assert isinstance(config["test_section"]["time_key"], int)
            assert config["test_section"]["time_key"] == 30 * 60 + 15  # 30 minutes + 15 seconds in seconds
        finally:
            # Clean up
            os.unlink(temp_filename)

    def test_get_property(self):
        """Test retrieving properties from config."""
        # Create a temporary YAML file
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.yaml', delete=False) as temp:
            temp.write("""
section1:
  key1: value1
  key2: value2
  time_value:
    hours: 2
    minutes: 30
section2:
  key3: value3
            """)
            temp_filename = temp.name

        try:
            # Set default config file for testing
            Config.__default_config_file__ = temp_filename

            # Get property with file path
            props = Config.get_property(temp_filename, "section1", ["key1", "key2"])
            assert "key1" in props
            assert "key2" in props
            assert props["key1"] == "value1"
            assert props["key2"] == "value2"

            # Get property with default file path
            props = Config.get_property(None, "section2", ["key3"])
            assert "key3" in props
            assert props["key3"] == "value3"

            # Get entire section
            section = Config.get_property(temp_filename, "section1")
            assert "key1" in section
            assert "key2" in section
            assert "time_value" in section

            # Get time value
            props = Config.get_property(temp_filename, "section1", ["time_value"])
            assert "time_value" in props
            assert props["time_value"] == 2 * 3600 + 30 * 60  # 2 hours + 30 minutes in seconds
        finally:
            # Clean up
            os.unlink(temp_filename)

    def test_get_property_nonexistent(self):
        """Test getting non-existent properties."""
        # Create a temporary YAML file
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.yaml', delete=False) as temp:
            temp.write("""
section:
  key: value
            """)
            temp_filename = temp.name

        try:
            # Try to get non-existent section
            with pytest.raises(KeyError):
                Config.get_property(temp_filename, "nonexistent", ["key"])

            # Try to get non-existent key
            with pytest.raises(KeyError):
                Config.get_property(temp_filename, "section", ["nonexistent"])
        finally:
            # Clean up
            os.unlink(temp_filename)

class TestPasswordUtils:
    """Tests for password utilities."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "secure_password"

        # Hash the password
        hashed = hash_password(password)

        # Verify the hash is not the original password
        assert hashed != password

        # Verify the hash format (pbkdf2_sha256)
        assert hashed.startswith("$pbkdf2-sha256$")

    def test_verify_password(self):
        """Test password verification."""
        password = "test_password"

        # Hash the password
        hashed = hash_password(password)

        # Verify correct password
        assert verify_password(password, hashed) is True

        # Verify incorrect password
        assert verify_password("wrong_password", hashed) is False

    def test_verify_invalid_hash(self):
        """Test verification with invalid hash."""
        # This should not raise an exception, just return False
        assert verify_password("password", "invalid_hash") is False

class TestVerificationCode:
    """Tests for verification code utilities."""

    def test_generate_verification_code(self):
        """Test verification code generation."""
        email = "test@example.com"
        expiration_seconds = 900  # 15 minutes

        # Generate verification code
        code, expires = generate_verification_code(email, expiration_seconds)

        # Check that code is a string
        assert isinstance(code, str)

        # Check that expiration is a datetime
        assert isinstance(expires, datetime)

        # Check expiration time is correct
        now = datetime.utcnow()
        expected_expiry = now + timedelta(seconds=expiration_seconds)
        difference = abs((expires - expected_expiry).total_seconds())
        assert difference < 5  # Allow for small timing differences

        # Generate another code and ensure it's different
        code2, _ = generate_verification_code(email, expiration_seconds)
        assert code != code2

    def test_generate_random_suffix(self):
        """Test random suffix generation."""
        # Generate suffix with default length
        suffix = generate_random_suffix()
        assert isinstance(suffix, str)
        assert len(suffix) == 6

        # Generate suffix with custom length
        custom_length = 10
        suffix = generate_random_suffix(custom_length)
        assert len(suffix) == custom_length

        # Generate another suffix and ensure it's different
        suffix2 = generate_random_suffix(custom_length)
        assert suffix != suffix2

class TestJwtExceptions:
    """Tests for JWT exception utilities."""

    def test_create_response_dict(self):
        """Test creating response dictionary for JWT exceptions."""
        # Create default response dict
        response_dict = create_response_dict()

        # Check that all default status codes are present
        assert 400 in response_dict
        assert 401 in response_dict
        assert 403 in response_dict
        assert 500 in response_dict

        # Check specific error descriptions
        assert "Invalid credentials" in response_dict[400]["description"]
        assert "Token expired or revoked" in response_dict[401]["description"]
        assert "Access denied" in response_dict[403]["description"]

        # Create custom response dict with some options disabled
        response_dict = create_response_dict(
            InvalidHeader=False,
            JWTDecode=False,
            response={200: {"description": "Success"}}
        )

        # Check that custom success response is present
        assert 200 in response_dict
        assert response_dict[200]["description"] == "Success"

        # Should still have error codes even if some are disabled
        assert 400 in response_dict
        assert 401 in response_dict

class TestSingleton:
    """Tests for singleton decorator."""

    def test_singleton_decorator(self):
        """Test that singleton decorator creates only one instance."""
        # Create a class with singleton decorator
        @singleton
        class TestClass:
            def __init__(self):
                self.value = 0

            def increment(self):
                self.value += 1
                return self.value

        # Get two instances
        instance1 = TestClass()
        instance2 = TestClass()

        # Check that they are the same object
        assert instance1 is instance2

        # Modify one instance and check that the other is affected
        instance1.increment()
        assert instance2.value == 1

        instance2.increment()
        assert instance1.value == 2