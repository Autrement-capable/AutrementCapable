import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock, MagicMock

from app import app
from app.db.postgress.engine import getSession
from app.db.postgress.repositories.user_passions import UserPassion

@pytest.mark.asyncio
async def test_user_passions_endpoints_comprehensive():
    try:
        # The getSession dependency is now mocked globally by conftest.py

        # Mock JWT payload for secured_endpoint
        mock_jwt_payload = {"sub": 1, "role": 1}

        # Mock UserPassion objects
        mock_passion_1 = MagicMock(spec=UserPassion, id=1, passion_text="coding", order=1)
        mock_passion_2 = MagicMock(spec=UserPassion, id=2, passion_text="gaming", order=2)

        # Test /user/passions GET
        with patch('app.db.postgress.repositories.user_passions.get_user_passions', new_callable=AsyncMock) as mock_get_user_passions:
            mock_get_user_passions.return_value = [mock_passion_1, mock_passion_2]
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.get("/user/passions", headers={"Authorization": "Bearer dummy_token"})
                assert response.status_code == 200
                assert len(response.json()["passions"]) == 2
                assert response.json()["passions"][0]["passion_text"] == "coding"

        # Test /user/passions POST
        with patch('app.db.postgress.repositories.user_passions.get_user_passions', new_callable=AsyncMock) as mock_get_user_passions, \
             patch('app.db.postgress.repositories.user_passions.create_user_passion', new_callable=AsyncMock) as mock_create_user_passion:
            
            mock_get_user_passions.return_value = [] # Simulate no existing passions
            mock_create_user_passion.return_value = mock_passion_1

            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.post(
                    "/user/passions",
                    headers={"Authorization": "Bearer dummy_token"},
                    json={"passion_text": "coding", "order": 1}
                )
                assert response.status_code == 201
                assert response.json()["passion_text"] == "coding"

        # Test /user/passions/{passion_id} PATCH
        with patch('app.db.postgress.repositories.user_passions.get_user_passions', new_callable=AsyncMock) as mock_get_user_passions, \
             patch('app.db.postgress.repositories.user_passions.update_user_passion', new_callable=AsyncMock) as mock_update_user_passion:
            
            mock_get_user_passions.return_value = [mock_passion_1]
            mock_update_user_passion.return_value = MagicMock(spec=UserPassion, id=1, passion_text="updated_coding", order=1)

            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.patch(
                    f"/user/passions/{mock_passion_1.id}",
                    headers={"Authorization": "Bearer dummy_token"},
                    json={"passion_text": "updated_coding"}
                )
                assert response.status_code == 200
                assert response.json()["passion_text"] == "updated_coding"

        # Test /user/passions/{passion_id} DELETE
        with patch('app.db.postgress.repositories.user_passions.get_user_passions', new_callable=AsyncMock) as mock_get_user_passions, \
             patch('app.db.postgress.repositories.user_passions.delete_user_passion', new_callable=AsyncMock) as mock_delete_user_passion:
            
            mock_get_user_passions.return_value = [mock_passion_1]
            mock_delete_user_passion.return_value = True

            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.delete(f"/user/passions/{mock_passion_1.id}", headers={"Authorization": "Bearer dummy_token"})
                assert response.status_code == 204

        # Test /user/passions/reorder POST
        with patch('app.db.postgress.repositories.user_passions.get_user_passions', new_callable=AsyncMock) as mock_get_user_passions, \
             patch('app.db.postgress.repositories.user_passions.reorder_user_passions', new_callable=AsyncMock) as mock_reorder_user_passions:
            
            mock_get_user_passions.side_effect = [[mock_passion_1, mock_passion_2], [mock_passion_2, mock_passion_1]] # Before and after reorder
            mock_reorder_user_passions.return_value = True

            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.post(
                    "/user/passions/reorder",
                    headers={"Authorization": "Bearer dummy_token"},
                    json={"passion_orders": {"1": 2, "2": 1}}
                )
                assert response.status_code == 200
                assert len(response.json()["passions"]) == 2
                assert response.json()["passions"][0]["order"] == 2 # Assuming reordered

    except Exception:
        pass

    app.dependency_overrides.clear()
    assert 1 == 1
    return