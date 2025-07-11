import pytest
from unittest.mock import patch, AsyncMock, MagicMock

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