# Prerequisites and Dependencies

## System Requirements

### Development Environment

#### Minimum Requirements
- **Operating System**: 
  - macOS 10.15+ (Catalina or later)
  - Ubuntu 20.04 LTS or later
  - Windows 10/11 with WSL2
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space for development environment
- **Network**: Stable internet connection for package downloads

#### Recommended Specifications
- **CPU**: Multi-core processor (4+ cores recommended)
- **RAM**: 16GB or more for optimal performance
- **Storage**: SSD with 20GB+ free space
- **Network**: High-speed internet for efficient development

### Production Environment

#### Server Requirements
- **CPU**: 4+ vCPUs
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 50GB+ SSD storage
- **Network**: High-bandwidth connection with low latency
- **OS**: Ubuntu 22.04 LTS (recommended) or compatible Linux distribution

#### Database Requirements
- **PostgreSQL**: Version 15 or later
- **Storage**: Dedicated storage with regular backup capabilities
- **CPU**: 2+ vCPUs for database server
- **RAM**: 4GB minimum, 8GB recommended

## Software Dependencies

### Core Development Tools

#### Node.js and Package Managers
```bash
# Node.js (Required: 18.x or later)
# Installation methods:

# Using Node Version Manager (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18

# Using package managers:
# macOS with Homebrew
brew install node@18

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Windows with Chocolatey
choco install nodejs

# Verify installation
node --version  # Should show v18.x.x or higher
npm --version   # Should show 9.x.x or higher

# Install Yarn (optional but recommended)
npm install -g yarn
yarn --version
```

#### Python Environment
```bash
# Python 3.11+ (Required)
# Installation methods:

# macOS with Homebrew
brew install python@3.11

# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip

# Windows with Chocolatey
choco install python --version=3.11.0

# Verify installation
python3.11 --version  # Should show 3.11.x
pip --version          # Should show pip for Python 3.11

# Create virtual environment
python3.11 -m venv ~/.virtualenvs/autrement-capable
source ~/.virtualenvs/autrement-capable/bin/activate  # macOS/Linux
# ~/.virtualenvs/autrement-capable/Scripts/activate    # Windows
```

#### Git Version Control
```bash
# Git (Required: 2.x or later)
# Installation methods:

# macOS with Homebrew
brew install git

# Ubuntu/Debian
sudo apt install git

# Windows with Chocolatey
choco install git

# Verify installation
git --version  # Should show 2.x.x or higher

# Configure Git (required for development)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
```

### Database Software

#### PostgreSQL
```bash
# PostgreSQL 15+ (Required)
# Installation methods:

# macOS with Homebrew
brew install postgresql@15
brew services start postgresql@15

# Ubuntu/Debian
sudo apt update
sudo apt install postgresql-15 postgresql-client-15 postgresql-contrib-15

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Windows with Chocolatey
choco install postgresql --version=15.0.0

# Verify installation
psql --version  # Should show PostgreSQL 15.x

# Create development database (after installation)
sudo -u postgres createdb autrement_capable_dev
sudo -u postgres createuser autrement_capable_user --pwprompt
```

#### Redis (Optional for Caching)
```bash
# Redis (Optional but recommended for production)
# Installation methods:

# macOS with Homebrew
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Windows with Chocolatey
choco install redis-64

# Verify installation
redis-cli ping  # Should return "PONG"
```

### Containerization Tools

#### Docker and Docker Compose
```bash
# Docker (Required for containerized deployment)
# Installation methods:

# macOS
# Download Docker Desktop from docker.com
# Or with Homebrew:
brew install --cask docker

# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER  # Add user to docker group

# Windows
# Download Docker Desktop from docker.com
# Or with Chocolatey:
choco install docker-desktop

# Verify installation
docker --version          # Should show 20.x.x or higher
docker-compose --version  # Should show 2.x.x or higher

# Test Docker installation
docker run hello-world
```

## Development Dependencies

### Frontend Dependencies

#### Package.json Dependencies
```json
{
  "dependencies": {
    "@azure/identity": "^4.9.1",
    "@mdi/font": "^7.4.47",
    "@simplewebauthn/browser": "^13.1.0",
    "@tresjs/cientos": "^4.1.0",
    "@tresjs/core": "^4.3.3",
    "@vue/runtime-dom": "^3.5.13",
    "apexcharts": "^4.5.0",
    "axios": "^1.7.9",
    "core-js": "^3.8.3",
    "dotenv": "^16.4.7",
    "html2pdf.js": "^0.10.3",
    "mitt": "^3.0.1",
    "openai": "^4.96.0",
    "three": "^0.173.0",
    "vue": "^3.2.13",
    "vue-router": "^4.0.3",
    "vue3-apexcharts": "^1.8.0"
  },
  "devDependencies": {
    "@babel/core": "^7.26.0",
    "@babel/eslint-parser": "^7.25.9",
    "@babel/preset-env": "^7.26.0",
    "@tailwindcss/postcss": "^4.0.3",
    "@types/three": "^0.173.0",
    "@vue/cli-plugin-babel": "~5.0.0",
    "@vue/cli-plugin-eslint": "~5.0.0",
    "@vue/cli-plugin-router": "~5.0.0",
    "@vue/cli-service": "~5.0.0",
    "@vue/eslint-config-prettier": "^10.2.0",
    "autoprefixer": "^10.4.20",
    "babel-eslint": "^10.1.0",
    "eslint": "^7.32.0",
    "eslint-plugin-prettier": "^5.2.5",
    "eslint-plugin-vue": "^8.7.1",
    "postcss": "^8.5.1",
    "prettier": "^3.5.3",
    "tailwindcss": "^4.0.3"
  }
}
```

#### Installation Commands
```bash
# Navigate to frontend directory
cd website

# Install dependencies using npm
npm install

# Or using yarn (if preferred)
yarn install

# Install global development tools
npm install -g @vue/cli
npm install -g eslint
npm install -g prettier

# Verify frontend setup
npm run lint      # Should pass without errors
npm run serve     # Should start development server
```

### Backend Dependencies

#### Requirements.txt
```txt
# Core Framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0

# Data Validation
pydantic>=2.5.0
pydantic[email]>=2.5.0

# Configuration
python-dotenv>=1.0.0
PyYAML>=6.0.1

# Security
passlib[bcrypt]>=1.7.4
pyjwt>=2.8.0
cryptography>=41.0.7

# File Processing
pymupdf>=1.23.0
pillow>=10.1.0
pillow-avif-plugin>=1.4.0
pdf2image>=3.1.0
fillpdf>=0.6.0

# Task Scheduling
apscheduler>=3.10.4

# HTTP and File Handling
python-multipart>=0.0.6

# Database
asyncpg>=0.29.0
sqlalchemy[asyncio]>=2.0.23
psycopg2-binary>=2.9.9  # For development; use psycopg2 in production

# Testing
pytest>=7.4.3
pytest-asyncio>=0.21.1
httpx>=0.25.2
pytest-order>=1.2.0
pytest-dependency>=0.5.1

# Debugging
debugpy>=1.8.0

# Email
fastapi-mail>=1.4.1

# Templates
Jinja2>=3.1.2

# Fake Data (for testing)
faker>=20.1.0

# WebAuthn/Passkeys
webauthn>=1.11.1
cbor2>=5.4.6

# AI Integration
openai>=1.3.0

# Development Testing (Passkey mocking)
soft-webauthn>=0.1.0
```

#### Installation Commands
```bash
# Navigate to backend directory
cd Backend

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black flake8 isort mypy

# Verify backend setup
python -c "import fastapi; print('FastAPI imported successfully')"
python -c "import sqlalchemy; print('SQLAlchemy imported successfully')"
python -c "import asyncpg; print('AsyncPG imported successfully')"
```

## Optional Dependencies

### Development Tools

#### Code Quality Tools
```bash
# ESLint and Prettier (Frontend)
npm install -g eslint prettier
npm install -g @vue/cli

# Python code quality tools (Backend)
pip install black flake8 isort mypy pylint

# Pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

#### IDE Extensions and Tools
```bash
# VS Code extensions (recommended)
code --install-extension octref.vetur                    # Vue.js support
code --install-extension ms-python.python               # Python support
code --install-extension ms-vscode.vscode-json          # JSON support
code --install-extension bradlc.vscode-tailwindcss      # TailwindCSS support
code --install-extension ms-vscode.vscode-eslint        # ESLint integration
code --install-extension esbenp.prettier-vscode         # Prettier integration
code --install-extension ms-vscode.vscode-typescript-next # TypeScript support
```

### Monitoring and Observability

#### Monitoring Tools (Production)
```bash
# Prometheus and Grafana (for monitoring)
docker pull prom/prometheus:latest
docker pull grafana/grafana:latest

# Log aggregation tools
docker pull elasticsearch:8.11.0
docker pull kibana:8.11.0
docker pull logstash:8.11.0
```

### External Service Dependencies

#### AI Services
```bash
# OpenAI API (for avatar generation)
# Sign up at: https://platform.openai.com/
# Required environment variable: OPENAI_API_KEY
```

#### Email Services (Optional)
```bash
# Email service provider (for notifications)
# Options:
# - Gmail SMTP (for development)
# - SendGrid (for production)
# - AWS SES (for production)
# Required environment variables: EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD
```

## Environment Variables

### Development Environment Variables
```bash
# Backend/.env.development
# Copy this template and fill in your values

# Server Configuration
HOST=0.0.0.0
PORT=5000
DEBUG=True
MODE=DEV
VERSION=0.1.0alpha

# Database Configuration
POSTGRES_SERVER=localhost
POSTGRES_USER=autrement_capable_user
POSTGRES_PASSWORD=your_dev_password_here
POSTGRES_DB=autrement_capable_dev
POSTGRES_PORT=5432

# Security Configuration (use strong values even in development)
SERVER_SECRET=your_super_secret_development_key_minimum_32_characters
AES_KEY=your_32_character_aes_key_here_base64

# WebAuthn Configuration
RP_ID=localhost
ORIGIN=http://localhost

# Optional: AI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Debug Configuration
DEBUG_PORT=5678
```

```bash
# website/.env.development
# Frontend environment variables

VUE_APP_SERVER_URL=http://localhost:5000
VUE_APP_ENVIRONMENT=development
VUE_APP_DEBUG=true
```

### Production Environment Variables
```bash
# Production environment variables (secure these!)
# Use environment variable management tools like:
# - AWS Secrets Manager
# - Azure Key Vault  
# - HashiCorp Vault
# - Docker secrets

# Critical: Never commit production values to version control!
```

## Dependency Management

### Keeping Dependencies Updated

#### Automated Dependency Updates
```bash
# Frontend dependency updates
npx npm-check-updates -u  # Check for updates
npm audit                 # Check for security vulnerabilities
npm audit fix             # Fix vulnerabilities automatically

# Backend dependency updates
pip list --outdated       # Check for outdated packages
pip-review --local --auto # Update packages (install pip-tools first)

# Security scanning
npm audit                 # Frontend security audit
pip-audit                 # Backend security audit (install pip-audit first)
```

#### Manual Dependency Review
```bash
# Regular dependency maintenance (monthly)
# 1. Review package.json and requirements.txt
# 2. Check for major version updates
# 3. Test compatibility with new versions
# 4. Update documentation if needed
# 5. Run full test suite after updates
```

### Dependency Troubleshooting

#### Common Issues and Solutions
```bash
# Node.js version conflicts
nvm use 18                # Switch to correct Node.js version
npm cache clean --force   # Clear npm cache
rm -rf node_modules package-lock.json
npm install              # Reinstall dependencies

# Python dependency conflicts
pip install --upgrade pip
pip install --force-reinstall -r requirements.txt
# Or recreate virtual environment:
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database connection issues
# Check PostgreSQL is running:
sudo systemctl status postgresql
# Check connection:
psql -h localhost -U autrement_capable_user -d autrement_capable_dev

# Docker issues
docker system prune       # Clean up Docker resources
docker-compose down -v    # Remove volumes
docker-compose up -d      # Restart containers
```

## Verification Checklist

### Development Environment Setup Verification
```bash
# Run this checklist after completing setup:

# 1. Verify core tools
[ ] node --version (>= 18.x)
[ ] python3.11 --version (>= 3.11.x)
[ ] git --version (>= 2.x)
[ ] docker --version (>= 20.x)
[ ] psql --version (>= 15.x)

# 2. Verify database connectivity
[ ] Can connect to PostgreSQL
[ ] Development database exists
[ ] Database user has proper permissions

# 3. Verify backend setup
[ ] Virtual environment activated
[ ] All Python dependencies installed
[ ] Backend starts without errors
[ ] Can access http://localhost:5000/health

# 4. Verify frontend setup
[ ] Node dependencies installed
[ ] Frontend builds without errors
[ ] Development server starts
[ ] Can access http://localhost:8080

# 5. Verify integration
[ ] Frontend can communicate with backend
[ ] Database connections work
[ ] Basic authentication flow functions

# 6. Verify development tools
[ ] Code linting works (frontend and backend)
[ ] Tests can be run
[ ] Pre-commit hooks installed (if used)
```

### Quick Setup Script
```bash
#!/bin/bash
# quick-setup.sh - Automated environment setup

set -e

echo "🚀 Setting up Autrement Capable development environment..."

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed."; exit 1; }
command -v python3.11 >/dev/null 2>&1 || { echo "❌ Python 3.11 is required but not installed."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git is required but not installed."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }

echo "✅ Prerequisites check passed"

# Backend setup
echo "🐍 Setting up backend..."
cd Backend
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Frontend setup
echo "🌐 Setting up frontend..."
cd ../website
npm install

# Database setup
echo "🗄️ Setting up database..."
cd ../Backend
docker-compose up -d db
sleep 10  # Wait for database to start

echo "✅ Development environment setup complete!"
echo "📖 Next steps:"
echo "1. Copy .env.example to .env and configure your settings"
echo "2. Run 'cd Backend && source venv/bin/activate && python -m uvicorn app.main:app --reload'"
echo "3. In another terminal: 'cd website && npm run serve'"
```

---

*This prerequisites guide ensures you have everything needed to contribute effectively to the Autrement Capable project. If you encounter any issues, refer to the troubleshooting section or ask for help from the team.*