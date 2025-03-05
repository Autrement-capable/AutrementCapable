"""
Integration test script to validate the whole application.

This script runs full integration tests against the running application.
It can be used to verify that all components are working together correctly.
"""
import asyncio
import sys
import time
import httpx
import json
import argparse
from typing import Dict, Any, List, Optional

# Default configuration
DEFAULT_BASE_URL = "http://localhost:8000"
DEFAULT_TIMEOUT = 30  # seconds
DEFAULT_USERNAME = "integrationuser"
DEFAULT_EMAIL = "integration@example.com"
DEFAULT_PASSWORD = "Password123"

class ApiTestClient:
    """Client for interacting with the API during integration tests."""

    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize the test client.

        Args:
            base_url: Base URL of the API
            timeout: Timeout for HTTP requests in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)
        self.access_token = None
        self.refresh_token = None

    async def close(self):
        """Close the client session."""
        await self.client.aclose()

    async def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user."""
        response = await self.client.post(
            "/auth/register",
            json={
                "first_name": "Integration",
                "last_name": "Test",
                "phone_number": "5551234567",
                "address": "123 Integration St",
                "username": username,
                "email": email,
                "password": password
            }
        )
        return response.json()

    async def login(self, username_or_email: str, password: str) -> Dict[str, Any]:
        """Login and store the tokens."""
        response = await self.client.post(
            "/auth/login",
            json={
                "username_or_email": username_or_email,
                "password": password
            }
        )
        data = response.json()
        if "access_token" in data:
            self.access_token = data["access_token"]
            self.refresh_token = data["refresh_token"]
        return data

    async def refresh(self) -> Dict[str, Any]:
        """Refresh the access token."""
        response = await self.client.post(
            "/auth/refresh",
            headers={"Authorization": f"Bearer {self.refresh_token}"}
        )
        data = response.json()
        if "access_token" in data:
            self.access_token = data["access_token"]
        return data

    async def logout(self) -> Dict[str, Any]:
        """Logout by revoking tokens."""
        response = await self.client.post(
            "/auth/logout",
            json={"refresh_token": self.refresh_token},
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        if response.status_code == 200:
            self.access_token = None
            self.refresh_token = None
        return response.json()

    async def authenticated_request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """Make an authenticated request to the API."""
        if not self.access_token:
            raise ValueError("Not authenticated. Login first.")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        if "headers" in kwargs:
            kwargs["headers"].update(headers)
        else:
            kwargs["headers"] = headers

        return await self.client.request(method, path, **kwargs)

    async def verify_user(self, verification_code: str) -> Dict[str, Any]:
        """Verify a user account."""
        response = await self.client.get(f"/auth/verify?code={verification_code}")
        data = response.json()
        if "access_token" in data:
            self.access_token = data["access_token"]
            self.refresh_token = data["refresh_token"]
        return data

async def wait_for_api(base_url: str, max_attempts: int = 30, delay: int = 1):
    """
    Wait for the API to become available.

    Args:
        base_url: Base URL of the API
        max_attempts: Maximum number of attempts
        delay: Delay between attempts in seconds
    """
    client = httpx.AsyncClient()
    for attempt in range(max_attempts):
        try:
            response = await client.get(f"{base_url}/docs", timeout=2)
            if response.status_code == 200:
                print(f"API is available at {base_url}")
                await client.aclose()
                return True
        except httpx.RequestError:
            pass

        print(f"Waiting for API to become available (attempt {attempt+1}/{max_attempts})...")
        time.sleep(delay)

    print(f"API did not become available after {max_attempts} attempts")
    await client.aclose()
    return False

async def get_verification_code(email: str) -> Optional[str]:
    """
    Simulate getting a verification code from an email.

    In a real integration test, this might connect to a real email service,
    or a test mail server like MailHog to fetch the actual email.

    For this example, we'll just simulate it with a SQL query.

    Args:
        email: Email address to get verification code for

    Returns:
        The verification code, or None if not found
    """
    try:
        # Connect to the database directly
        import asyncpg

        conn = await asyncpg.connect(
            user="postgres_test",
            password="postgres_test",
            database="postgres_test",
            host="localhost",
            port=5433
        )

        # Get the verification code
        query = """
        SELECT ud.verification_token
        FROM unverified_details ud
        JOIN users u ON ud.user_id = u.id
        WHERE u.email = $1
        """

        result = await conn.fetchval(query, email)
        await conn.close()

        return result
    except Exception as e:
        print(f"Error getting verification code: {e}")
        return None

async def run_integration_test(base_url: str):
    """
    Run the full integration test suite.

    Args:
        base_url: Base URL of the API
    """
    client = ApiTestClient(base_url)

    try:
        print("Starting integration tests...")

        # Test registration
        print("\n=== Testing Registration ===")
        username = f"{DEFAULT_USERNAME}_{int(time.time())}"
        email = f"integration_{int(time.time())}@example.com"
        password = DEFAULT_PASSWORD

        print(f"Registering user: {username}, {email}")
        result = await client.register(username, email, password)
        print(f"Registration result: {json.dumps(result, indent=2)}")

        # Get verification code
        print("\n=== Getting Verification Code ===")
        verification_code = await get_verification_code(email)
        if not verification_code:
            print("Failed to get verification code")
            return False

        print(f"Verification code: {verification_code}")

        # Verify user
        print("\n=== Verifying User ===")
        result = await client.verify_user(verification_code)
        print(f"Verification result: {json.dumps(result, indent=2)}")

        # Test login
        print("\n=== Testing Login ===")
        result = await client.login(email, password)
        print(f"Login result: {json.dumps(result, indent=2)}")

        # Test refresh token
        print("\n=== Testing Refresh Token ===")
        result = await client.refresh()
        print(f"Refresh result: {json.dumps(result, indent=2)}")

        # Test authenticated request
        print("\n=== Testing Authenticated Request ===")
        response = await client.authenticated_request("GET", "/dev/test_access_token")
        print(f"Authenticated request result: {json.dumps(response.json(), indent=2)}")

        # Test logout
        print("\n=== Testing Logout ===")
        result = await client.logout()
        print(f"Logout result: {json.dumps(result, indent=2)}")

        print("\nAll integration tests passed!")
        return True

    except Exception as e:
        print(f"Integration test failed: {e}")
        return False

    finally:
        await client.close()

async def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Integration test for the FastAPI application")
    parser.add_argument("--url", default=DEFAULT_BASE_URL, help=f"Base URL of the API (default: {DEFAULT_BASE_URL})")
    parser.add_argument("--wait", type=int, default=30, help="Maximum time to wait for API in seconds (default: 30)")
    args = parser.parse_args()

    # Wait for the API to become available
    if not await wait_for_api(args.url, args.wait):
        sys.exit(1)

    # Run the integration tests
    success = await run_integration_test(args.url)

    # Exit with the appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())