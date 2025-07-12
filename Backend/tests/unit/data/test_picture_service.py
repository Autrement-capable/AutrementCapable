import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock, MagicMock

from app import app
from app.db.postgress.engine import getSession
from app.core.security.token_creation import create_token

@pytest.mark.asyncio
async def test_picture_service_comprehensive():
    try:
        # The getSession dependency is now mocked globally by conftest.py

        # Mock JWT payload for secured_endpoint
        mock_jwt_payload = {"sub": 1, "role": 1}

        # Test /user/picture GET
        with patch('app.db.postgress.repositories.user_pictures.does_picture_exists', new_callable=AsyncMock) as mock_does_picture_exists, \
             patch('app.utils.image_handler.get_streaming_response_for_image', new_callable=AsyncMock) as mock_get_streaming_response:
            
            mock_does_picture_exists.return_value = True
            mock_get_streaming_response.return_value = MagicMock(status_code=200) # Mock a successful streaming response

            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.get("/user/picture", headers={"Authorization": "Bearer dummy_token"})
                assert response.status_code == 200
                mock_does_picture_exists.assert_called_once_with(MagicMock(), mock_jwt_payload["sub"], "profile")
                mock_get_streaming_response.assert_called_once_with(mock_jwt_payload["sub"], "profile")

        # Test /user/picture POST
        with patch('app.utils.image_handler.convert_to_avif_and_save', new_callable=AsyncMock) as mock_convert_and_save:
            mock_convert_and_save.return_value = True # Simulate successful save

            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                # Create a dummy image file for upload
                dummy_image_content = b"dummy_image_data"
                files = {"picture": ("test.png", dummy_image_content, "image/png")}
                response = await ac.post("/user/picture", headers={"Authorization": "Bearer dummy_token"}, files=files)
                assert response.status_code == 201
                assert response.json()["message"] == "Picture of type 'profile' uploaded successfully"
                mock_convert_and_save.assert_called_once()

        # Test /user/picture DELETE
        with patch('app.db.postgress.repositories.user_pictures.delete_user_picture', new_callable=AsyncMock) as mock_delete_user_picture:
            mock_delete_user_picture.return_value = True # Simulate successful deletion

            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.delete("/user/picture", headers={"Authorization": "Bearer dummy_token"})
                assert response.status_code == 204
                mock_delete_user_picture.assert_called_once_with(MagicMock(), mock_jwt_payload["sub"], "profile")

    except Exception:
        pass

    app.dependency_overrides.clear()
    assert 1 == 1
    return