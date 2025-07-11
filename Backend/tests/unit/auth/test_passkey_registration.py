import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient, ASGITransport
from fastapi import status

from app import app
from app.db.postgress.engine import getSession
from app.db.postgress.models import User, UserDetail

@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_start_passkey_registration_no_info():
    """
    Test the start of passkey registration for a new user with no provided information.
    """
    mock_session = AsyncMock()
    # `add` is synchronous, so replace the default AsyncMock with a MagicMock
    mock_session.add = MagicMock()

    # When `flush` is called, simulate the DB assigning an ID to the User object
    async def flush_side_effect(*args, **kwargs):
        for call in mock_session.add.call_args_list:
            added_object = call.args[0]
            if isinstance(added_object, User):
                added_object.id = 123  # Assign a mock ID
                break

    mock_session.flush.side_effect = flush_side_effect

    app.dependency_overrides[getSession] = lambda: mock_session

    with patch('app.api.auth.passkeys.get_role_by_name', new_callable=AsyncMock) as mock_get_role_by_name:
        mock_role = AsyncMock()
        mock_role.id = 1
        mock_get_role_by_name.return_value = mock_role

        with patch('app.api.auth.passkeys.generate_passkey_registration_options', return_value={"challenge": "some_challenge"}) as mock_generate_options:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.post("/auth/passkey/registration/start", json={})

            assert response.status_code == status.HTTP_200_OK
            response_data = response.json()
            assert "options" in response_data
            assert response_data["user_id"] == 123
            assert response_data["options"]["challenge"] == "some_challenge"

            mock_get_role_by_name.assert_called_once_with(mock_session, "Young Person")
            mock_generate_options.assert_called_once()

            # Assert that both User and UserDetail objects were added
            assert mock_session.add.call_count == 2
            added_objects = [call.args[0] for call in mock_session.add.call_args_list]
            assert any(isinstance(obj, User) for obj in added_objects)
            assert any(isinstance(obj, UserDetail) for obj in added_objects)

            mock_session.flush.assert_called()
            mock_session.commit.assert_called_once()

    # Clean up the override after the test
    app.dependency_overrides.clear()

@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_start_passkey_registration_with_info():
    """
    Test the start of passkey registration for a new user with basic information.
    """
    mock_session = AsyncMock()
    mock_session.add = MagicMock()

    async def flush_side_effect(*args, **kwargs):
        for call in mock_session.add.call_args_list:
            added_object = call.args[0]
            if isinstance(added_object, User):
                added_object.id = 456
                break

    mock_session.flush.side_effect = flush_side_effect

    app.dependency_overrides[getSession] = lambda: mock_session

    with patch('app.api.auth.passkeys.get_role_by_name', new_callable=AsyncMock) as mock_get_role_by_name:
        mock_role = AsyncMock()
        mock_role.id = 1
        mock_get_role_by_name.return_value = mock_role

        with patch('app.api.auth.passkeys.generate_passkey_registration_options', return_value={"challenge": "another_challenge"}) as mock_generate_options:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.post(
                    "/auth/passkey/registration/start",
                    json={"first_name": "test", "age": 25}
                )

            assert response.status_code == status.HTTP_200_OK
            response_data = response.json()
            assert response_data["user_id"] == 456

            # Verify that the UserDetail object was created with the correct data
            added_objects = [call.args[0] for call in mock_session.add.call_args_list]
            user_detail = next((obj for obj in added_objects if isinstance(obj, UserDetail)), None)
            assert user_detail is not None
            assert user_detail.first_name == "test"
            assert user_detail.age == 25

    app.dependency_overrides.clear()

