import pytest
from fastapi.testclient import TestClient
from fastapi import status
from httpx import AsyncClient

from config.server import server

# Test the synchronous login endpoint using TestClient
client = TestClient(server.app)

@pytest.mark.asyncio
async def test_register():
    async with AsyncClient(app=server.app, base_url="http://test") as ac:
        # Make a POST request to the /register endpoint with valid data
        response = await ac.post("/auth/register", json={
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "address": "123 Main St",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "password": "supersecurepassword"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

@pytest.mark.asyncio
async def test_register_invalid_email():
    async with AsyncClient(app=server.app, base_url="http://test") as ac:
        # Make a POST request to the /register endpoint with an invalid email
        response = await ac.post("/auth/register", json={
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "address": "123 Main St",
            "username": "johndoe",
            "email": "invalid-email",
            "password": "supersecurepassword"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=server.app, base_url="http://test") as ac:
        # Ensure user already registered for login
        response = await ac.post("/auth/login", json={
            "username_or_email": "johndoe",
            "password": "supersecurepassword"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

@pytest.mark.asyncio
async def test_check_username():
    async with AsyncClient(app=server.app, base_url="http://test") as ac:
        # Check if the username 'johndoe' is taken
        response = await ac.get("/auth/check_username?username=johndoe")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["exists"] == True
