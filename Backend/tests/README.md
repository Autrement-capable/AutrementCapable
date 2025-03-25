# Guide on how to run and implement tests


## Overview

Tests are divided into two main categories:

1. **Endpoint Tests**: Test API endpoints and their responses.
2. **Functionality Tests**: Test functions and classes that don't have endpoints (config loaders, cron jobs, database operations, etc.).

## Setup

### Requirements

- Docker and Docker Compose
- Python 3.10+

### Directory Structure

```
tests/
├── conftest.py                # Common fixtures and configurations
├── docker-compose.test.yml    # Docker setup for testing
├── Dockerfile.test            # Dedicated testing Dockerfile
├── pytest.ini                 # Pytest configuration
├── requirements.test.txt      # Test-specific dependencies
├── run_tests.sh               # Script to run tests with Docker
├── endpoint/                  # API endpoint tests
│   ├── auth/                  # Auth-related endpoint tests
│   └── dev/                   # Development endpoint tests
└── functionality(not done)/   # Non-endpoint component tests
    ├── database/              # Database tests
    ├── mail/                  # Mail functionality tests
    ├── server/                # Server component tests
    └── utils/                 # Utility function tests
```

## Running Tests

### Using Docker (Recommended)

The easiest way to run tests is using the provided script:

```bash
# Run all tests
./tests/run_tests.sh

# Run only endpoint tests
./tests/run_tests.sh endpoint

# Run only functionality tests
./tests/run_tests.sh functionality

# Run specific test file
./tests/run_tests.sh tests/endpoint/auth/test_login_register.py

# Run with specific pytest options
./tests/run_tests.sh -v --no-cov
```

### Manually

If you prefer to run tests manually:

1. Start a test database:

```bash
docker-compose -f tests/docker-compose.test.yml up -d db_test mailhog
```

2. Install test dependencies:

```bash
pip install -r requirements.txt -r tests/requirements.test.txt
```

3. Run tests:

```bash
python -m pytest tests/
```

## Test Configurations

### Environment Variables

The test environment uses the following environment variables:

- `POSTGRES_USER=postgres_test`
- `POSTGRES_PASSWORD=postgres_test`
- `POSTGRES_DB=postgres_test`
- `POSTGRES_SERVER=db_test` (or `localhost` when running manually)
- `POSTGRES_PORT=5432`
- `MODE=TEST`
- `SERVER_SECRET=test_secret_key`

These variables are configured in `docker-compose.test.yml` for Docker-based tests.

### Database Setup

The test database is automatically created, migrated, and cleaned up for each test session. Each test function gets a fresh transaction that is rolled back after the test completes.

### Email Testing

The test environment uses MailHog for email testing. When running with Docker, MailHog is available at http://localhost:8025 to view emails sent during tests.

## Writing Tests

### Endpoint Tests

Create endpoint tests in the `tests/endpoint/` directory. Use the `@pytest.mark.endpoint` decorator:

```python
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.endpoint

@pytest.mark.asyncio
async def test_my_endpoint(client: AsyncClient):
    response = await client.get("/my-endpoint")
    assert response.status_code == 200
    assert "data" in response.json()
```

### Functionality Tests

Create functionality tests in the `tests/functionality/` directory. Use the `@pytest.mark.functionality` decorator:

```python
import pytest
from my_module import my_function

pytestmark = pytest.mark.functionality

@pytest.mark.asyncio
async def test_my_function(db_session):
    result = await my_function(db_session, "test")
    assert result is not None
```

### Test Fixtures

Common fixtures are defined in `conftest.py`:

- `db_session`: Async SQLAlchemy session for database operations
- `test_app`: The FastAPI application with test configuration
- `client`: AsyncClient for making HTTP requests
- `init_test_data`: Initializes common test data

### Mocking

For mailing and external services, use pytest's monkeypatch or pytest-mock:

```python
@pytest.mark.asyncio
async def test_with_mock(monkeypatch):
    # Mock external function
    async def mock_function(*args, **kwargs):
        return "mocked result"

    monkeypatch.setattr("my_module.external_function", mock_function)

    # Test your function that uses the external function
    result = await my_function()
    assert result == "mocked result"
```

## Code Coverage

Tests generate coverage reports in the `coverage/` directory. View HTML reports at `coverage/index.html` after running tests.

## Compatibility

This testing framework is compatible with:

- **Alembic**: Database migrations are supported via SQLAlchemy models.
- **Prometheus/Sentry**: Monitoring systems can be integrated by adding fixtures in `conftest.py`.

To add Prometheus metrics to your tests, install the `prometheus-client` package and add metrics in your test fixtures.

## Extending the Framework

To add more test types or configurations:

1. Add new markers in `pytest.ini`
2. Create appropriate directories and files
3. Update the `run_tests.sh` script if needed