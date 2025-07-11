# Local Development Setup

## Quick Start

### Minimal Setup (Recommended for New Developers)
```bash
# Clone and navigate
git clone https://github.com/Autrement-capable/AutrementCapable.git
cd AutrementCapable

# Use Docker for easy setup
cd Backend
docker-compose up -d

# Frontend in separate terminal
cd ../website
npm install
npm run serve
```

### Manual Setup (For Full Control)
Follow this guide for a complete local development environment with all services running natively.

## Prerequisites

### System Requirements
- **OS**: macOS 10.15+, Ubuntu 20.04+, Windows 10+ with WSL2
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 10GB free space for dependencies and data
- **Network**: Internet connection for package downloads

### Required Software

#### Core Development Tools
```bash
# Check current versions
node --version    # Need: 18.x or higher
python --version  # Need: 3.11 or higher
git --version     # Need: 2.x or higher
```

#### Installation by Platform

**macOS (using Homebrew)**
```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install development tools
brew install node python@3.11 postgresql@15 redis git
brew install --cask docker
```

**Ubuntu/Debian**
```bash
# Update package list
sudo apt update

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# Install PostgreSQL 15
sudo apt install postgresql-15 postgresql-client-15

# Install Redis (optional)
sudo apt install redis-server

# Install Docker
sudo apt install docker.io docker-compose

# Install Git
sudo apt install git
```

**Windows (using Chocolatey)**
```bash
# Install Chocolatey (run as Administrator)
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install development tools
choco install nodejs python postgresql docker-desktop git
```

#### Verify Installations
```bash
# Verify all tools are installed correctly
node --version     # Should show v18.x.x or higher
npm --version      # Should show 9.x.x or higher
python --version   # Should show 3.11.x or higher
pip --version      # Should show 23.x.x or higher
psql --version     # Should show 15.x
docker --version   # Should show 20.x.x or higher
git --version      # Should show 2.x.x
```

## Database Setup

### Option 1: Docker PostgreSQL (Recommended)
```bash
cd Backend

# Start PostgreSQL with Docker
docker-compose up -d db

# Verify database is running
docker-compose ps

# Connect to database (optional, for verification)
docker-compose exec db psql -U postgres -d autrement_capable_dev
```

### Option 2: Native PostgreSQL Installation

#### Initial PostgreSQL Configuration
```bash
# Start PostgreSQL service
# macOS
brew services start postgresql@15

# Ubuntu/Debian
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Windows (if using native PostgreSQL)
# Use Services.msc to start PostgreSQL service
```

#### Create Development Database
```bash
# Switch to postgres user (Linux only)
sudo -u postgres psql

# Or connect directly (macOS/Windows)
psql postgres

# Create database and user
CREATE DATABASE autrement_capable_dev;
CREATE USER autrement_capable_user WITH PASSWORD 'dev_password_123';
GRANT ALL PRIVILEGES ON DATABASE autrement_capable_dev TO autrement_capable_user;
ALTER DATABASE autrement_capable_dev OWNER TO autrement_capable_user;

# Exit PostgreSQL
\q
```

#### Test Database Connection
```bash
# Test connection with created user
psql -h localhost -U autrement_capable_user -d autrement_capable_dev
# Enter password when prompted: dev_password_123
```

### Database Environment Variables
```bash
# Backend/.env (create this file)
POSTGRES_SERVER=localhost
POSTGRES_USER=autrement_capable_user
POSTGRES_PASSWORD=dev_password_123
POSTGRES_DB=autrement_capable_dev
POSTGRES_PORT=5432
```

## Backend Setup

### Python Environment Setup
```bash
cd Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Install Dependencies
```bash
# Install all backend dependencies
pip install -r requirements.txt

# For development, also install dev dependencies
pip install pytest pytest-asyncio httpx pytest-order pytest-dependency debugpy
```

### Environment Configuration
```bash
# Create environment file
cp .env.example .env  # If example exists, otherwise create manually

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

#### Complete Backend .env Configuration
```bash
# Backend/.env
# Server Configuration
HOST=0.0.0.0
PORT=5000
DEBUG=True
MODE=DEV
VERSION=0.1.0alpha

# Database Configuration
POSTGRES_SERVER=localhost
POSTGRES_USER=autrement_capable_user
POSTGRES_PASSWORD=dev_password_123
POSTGRES_DB=autrement_capable_dev
POSTGRES_PORT=5432

# Security Configuration
SERVER_SECRET=your_super_secret_development_key_change_in_production
AES_KEY=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=

# WebAuthn Configuration
RP_ID=localhost
ORIGIN=http://localhost

# Email Configuration (Optional for development)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# AI Configuration (Optional)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Development Database URLs
DATABASE_URL=postgresql+asyncpg://autrement_capable_user:dev_password_123@localhost:5432/autrement_capable_dev

# Debug Configuration
DEBUG_PORT=5678
```

### Initialize Database Schema
```bash
# Run database initialization
python -c "
import asyncio
from app.db.postgress.engine import postgress

async def init_db():
    await postgress.create_all()
    print('Database tables created successfully')

asyncio.run(init_db())
"
```

### Start Backend Development Server
```bash
# Start with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

# Alternative: Start with debug mode
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000 --log-level debug
```

#### Verify Backend is Running
```bash
# Test API health endpoint
curl http://localhost:5000/health

# Check API documentation
# Open http://localhost:5000/docs in your browser
```

## Frontend Setup

### Node.js Environment Setup
```bash
cd website

# Verify Node.js version
node --version  # Should be 18.x or higher

# Install package manager (if not already installed)
npm install -g yarn  # Optional: use yarn instead of npm
```

### Install Frontend Dependencies
```bash
# Using npm
npm install

# Or using yarn
yarn install

# Verify installation
npm list --depth=0
```

### Frontend Environment Configuration
```bash
# Create environment file
# website/.env.local (create this file)
VUE_APP_SERVER_URL=http://localhost:5000
VUE_APP_ENVIRONMENT=development
VUE_APP_DEBUG=true
```

### Start Frontend Development Server
```bash
# Using npm
npm run serve

# Using yarn
yarn serve

# For specific port (if 8080 is occupied)
npm run serve -- --port 3000
```

#### Verify Frontend is Running
- **URL**: http://localhost:8080 (or the port shown in terminal)
- **Hot Reload**: Changes should reflect automatically
- **Vue DevTools**: Install browser extension for better debugging

## Development Tools Setup

### IDE Configuration

#### VS Code (Recommended)
```bash
# Install recommended extensions
code --install-extension octref.vetur
code --install-extension ms-python.python
code --install-extension ms-vscode.vscode-json
code --install-extension bradlc.vscode-tailwindcss
code --install-extension ms-vscode.vscode-eslint
```

#### VS Code Settings (workspace)
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./Backend/venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "eslint.workingDirectories": ["website"],
  "prettier.configPath": "./website/.prettierrc",
  "files.associations": {
    "*.vue": "vue"
  }
}
```

### Browser Developer Tools

#### Required Browser Extensions
- **Vue.js DevTools**: For Vue component debugging
- **axe DevTools**: For accessibility testing
- **WAVE**: Web accessibility evaluation tool

#### Browser Setup
```bash
# Chrome extensions (install from Chrome Web Store)
# - Vue.js devtools
# - axe DevTools
# - WAVE Evaluation Tool

# Firefox extensions (install from Firefox Add-ons)
# - Vue.js devtools
# - axe DevTools
```

## Running Tests

### Backend Tests
```bash
cd Backend

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run with debug output
pytest -s tests/test_specific_function.py
```

### Frontend Tests
```bash
cd website

# Run unit tests
npm run test:unit

# Run tests with coverage
npm run test:unit -- --coverage

# Run tests in watch mode
npm run test:unit -- --watch

# Run linting
npm run lint

# Fix linting issues automatically
npm run lint -- --fix
```

## Common Development Tasks

### Starting All Services
```bash
# Terminal 1: Database (if using Docker)
cd Backend
docker-compose up -d db

# Terminal 2: Backend
cd Backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

# Terminal 3: Frontend
cd website
npm run serve
```

### Stopping All Services
```bash
# Stop frontend: Ctrl+C in terminal 3
# Stop backend: Ctrl+C in terminal 2
# Stop database: 
cd Backend
docker-compose down
```

### Database Management

#### Reset Database
```bash
cd Backend

# Stop all services first
docker-compose down

# Remove database volume
docker-compose down -v

# Restart services
docker-compose up -d

# Reinitialize database
python -c "
import asyncio
from app.db.postgress.engine import postgress

async def init_db():
    await postgress.create_all()
    print('Database reset and recreated')

asyncio.run(init_db())
"
```

#### View Database Contents
```bash
# Connect to database
docker-compose exec db psql -U postgres -d autrement_capable_dev

# List tables
\dt

# View table structure
\d users

# Query data
SELECT * FROM users LIMIT 5;

# Exit
\q
```

### Log Monitoring

#### Backend Logs
```bash
# Real-time backend logs
tail -f Backend/logs/app.log  # If logging to file

# Or monitor console output from uvicorn terminal
```

#### Frontend Logs
- **Browser Console**: F12 → Console tab
- **Network Tab**: Monitor API requests
- **Vue DevTools**: Component state and events

## Troubleshooting

### Common Issues and Solutions

#### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

#### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps  # For Docker setup
brew services list | grep postgresql  # macOS
sudo systemctl status postgresql  # Linux

# Test connection manually
psql -h localhost -U autrement_capable_user -d autrement_capable_dev
```

#### Python Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Node.js Dependencies Issues
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### Frontend Build Issues
```bash
# Check Node.js version
node --version  # Must be 18.x+

# Clear Vue CLI cache
rm -rf node_modules/.cache

# Restart dev server
npm run serve
```

### Performance Optimization

#### Backend Performance
```bash
# Run with performance profiling
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000 --access-log
```

#### Frontend Performance
```bash
# Analyze bundle size
npm run build
npm install -g webpack-bundle-analyzer
npx webpack-bundle-analyzer dist/static/js/*.js
```

### Debug Mode Setup

#### Backend Debugging
```bash
# Start backend in debug mode
python -m debugpy --listen 5678 --wait-for-client -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

#### Frontend Debugging
- **Vue DevTools**: Install browser extension
- **Browser DevTools**: F12 for inspector
- **VS Code Debugging**: Use "Debugger for Chrome" extension

## Next Steps

After completing the setup:

1. **Verify Everything Works**: Visit http://localhost:8080 and try to register
2. **Run Tests**: Make sure all tests pass
3. **Explore the Code**: Start with the main components
4. **Pick Your First Task**: Look for "good first issue" labels
5. **Set Up Development Workflow**: Configure git hooks and IDE settings

### Useful Commands Reference
```bash
# Quick start all services
make dev  # If Makefile exists

# Backend only
cd Backend && docker-compose up -d && source venv/bin/activate && python -m uvicorn app.main:app --reload

# Frontend only
cd website && npm run serve

# Run tests
cd Backend && pytest
cd website && npm run test:unit

# Check code quality
cd Backend && pylint app/
cd website && npm run lint
```

---

*This setup provides a complete local development environment for contributing to Autrement Capable. If you encounter issues not covered here, please check the troubleshooting section or ask for help.*