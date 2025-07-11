# Autrement Capable - Backend

This is the FastAPI backend for the Autrement Capable platform - providing secure, scalable APIs for an inclusive self-discovery platform for neurodivergent youth.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Docker and Docker Compose (recommended)

### Installation
```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup
```bash
# Option 1: Docker (Recommended)
docker-compose up -d db

# Option 2: Local PostgreSQL
createdb autrement_capable_dev
createuser autrement_capable_user --pwprompt
```

### Configuration
```bash
# Copy environment template
cp .env.example .env
# Edit .env with your database credentials and settings
```

### Development
```bash
# Start the development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

# API will be available at:
# - API: http://localhost:5000
# - Documentation: http://localhost:5000/docs
# - Alternative docs: http://localhost:5000/redoc
```

## 🛠️ Development

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

### Code Quality
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/

# Import sorting
isort app/
```

## 📁 Project Structure

```
app/
├── api/                    # API endpoints
│   ├── auth/              # Authentication endpoints
│   ├── data/              # Game data endpoints
│   └── dev/               # Development endpoints
├── core/                  # Core application configuration
│   ├── application.py     # FastAPI app setup
│   ├── config.py          # Configuration management
│   ├── security/          # Security middleware
│   └── cors/              # CORS configuration
├── db/                    # Database layer
│   ├── models/            # SQLAlchemy models
│   ├── repositories/      # Data access layer
│   └── postgress/         # PostgreSQL specific code
├── services/              # Business logic services
│   ├── auth/              # Authentication services
│   ├── scheduler/         # Background tasks
│   └── content/           # Content management
└── utils/                 # Utility functions
```

## 🔧 Key Features

- **FastAPI Framework**: High-performance async API framework
- **PostgreSQL**: Robust relational database with async support
- **WebAuthn/Passkeys**: Passwordless authentication implementation
- **SQLAlchemy 2.0**: Modern async ORM with type safety
- **OpenAPI Integration**: Automatic API documentation
- **Background Tasks**: Async task scheduling with APScheduler
- **Security First**: JWT tokens, CORS, input validation

## 🗄️ Database

### Models
- **Users**: User accounts and authentication
- **Game Data**: Results from 6 self-discovery mini-games
- **Profiles**: User preferences and personalization
- **Terms**: Legal compliance and user agreements

### Migrations
```bash
# Create migration (when models change)
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# View migration history
alembic history
```

## 🔐 Security

### Authentication
- **WebAuthn/Passkeys**: Hardware-backed authentication
- **JWT Tokens**: Stateless session management
- **Password Hashing**: Bcrypt for traditional auth (fallback)

### Data Protection
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **CORS Protection**: Configured cross-origin resource sharing
- **Rate Limiting**: Built-in request throttling

## 🚀 Deployment

### Docker
```bash
# Build and run with Docker Compose
docker-compose up -d --build

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Production
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or use the production Docker configuration
docker-compose -f docker-compose.prod.yml up -d
```

## 📊 Monitoring

### Health Checks
- **Health Endpoint**: `GET /health`
- **Database Status**: Included in health check
- **Service Dependencies**: External service status

### Logging
- **Structured Logging**: JSON format for log aggregation
- **Request Logging**: Automatic API request logging
- **Error Tracking**: Comprehensive error reporting

## 🧪 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

### Key Endpoints
- `POST /auth/register` - User registration with WebAuthn
- `POST /auth/login` - User authentication
- `GET /games/{game_type}/{user_id}` - Get game data
- `POST /games/{game_type}` - Submit game results
- `GET /profile/{user_id}` - Get user profile
- `PUT /profile/{user_id}` - Update user profile

## 📚 Documentation

- **[Complete Documentation](../docs/README.md)**: Comprehensive project documentation
- **[API Architecture](../docs/04-technical-architecture.md)**: Technical system design
- **[Data Model](../docs/03-data-model.md)**: Database schema and relationships
- **[Local Development](../docs/08-local-development.md)**: Complete setup guide
- **[Deployment Guide](../docs/10-deployment.md)**: Production deployment

## 🤝 Contributing

1. **Setup**: Follow the [local development guide](../docs/08-local-development.md)
2. **Standards**: Read the [developer guide](../docs/07-developer-getting-started.md)
3. **Testing**: Write tests for new endpoints and services
4. **Security**: Follow security best practices for all changes

## 🔍 Troubleshooting

### Common Issues

#### Database Connection
```bash
# Check PostgreSQL status
docker-compose ps db

# Test connection
psql -h localhost -U autrement_capable_user -d autrement_capable_dev
```

#### Python Environment
```bash
# Recreate virtual environment
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Import Errors
```bash
# Ensure PYTHONPATH includes app directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)/app"

# Or install in development mode
pip install -e .
```

## 📞 Support

- **Documentation**: Check the [comprehensive docs](../docs/README.md)
- **Issues**: Report bugs in the GitHub repository
- **Development**: Join team discussions for technical questions

---

*Providing secure, accessible APIs for an inclusive future.*