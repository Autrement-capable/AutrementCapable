import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime, timedelta

@pytest.fixture(scope="session", autouse=True)
def mock_postgres_initialization():
    """
    Mock the Postgress singleton's __init__ to prevent it from creating
    real database engines during test sessions.
    """
    def mock_init(self):
        self.engine = MagicMock()
        self.sync_engine = MagicMock()
        self.Session = MagicMock(return_value=AsyncMock())
        self.SyncSession = MagicMock(return_value=MagicMock())
        self.Base = MagicMock()
        self.getSession = AsyncMock(return_value=self.Session())

    with patch("app.db.postgress.engine.Postgress.__init__", new=mock_init):
        with patch("app.core.application.postgress.check_all_models_exist", new_callable=AsyncMock, return_value=(True, {})):
            with patch("app.db.postgress.postgress_pool.init_pg_pool", new_callable=AsyncMock):
                yield

@pytest.fixture
def mock_db_session() -> AsyncMock:
    """Provides a mocked async database session."""
    return AsyncMock()

@pytest.fixture(autouse=True)
def mock_security_dependencies():
    """
    Mocks getSession and get_jwt_data for all tests to simulate a logged-in user
    and a working database session.
    """
    mock_session = AsyncMock()
    
    # Mock for getSession
    patch_get_session = patch("app.db.postgress.engine.getSession", return_value=mock_session)
    
    # Mock for get_jwt_data
    mock_jwt_payload = {"sub": 1, "role": 1, "jti": "mock_jti", "exp": (datetime.utcnow() + timedelta(hours=1)).timestamp()}
    mock_refresh_jwt_payload = {"sub": 1, "role": 1, "jti": "mock_refresh_jti", "exp": (datetime.utcnow() + timedelta(days=7)).timestamp()}
    
    patch_get_jwt_data = patch(
        "app.core.security.decorators.get_jwt_data", 
        new_callable=AsyncMock,
        return_value={
            "access": mock_jwt_payload,
            "refresh": mock_refresh_jwt_payload
        }
    )

    with patch_get_session as mock_get_session, patch_get_jwt_data as mock_get_jwt_data:
        yield mock_get_session, mock_get_jwt_data
