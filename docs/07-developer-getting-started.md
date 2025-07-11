# Developer Getting Started Guide

## Welcome to Autrement Capable Development

This guide will help you get started contributing to the Autrement Capable platform. Whether you're a new team member or an external contributor, this document provides everything you need to begin coding effectively.

## Project Understanding

### Core Mission
Before diving into code, understand that Autrement Capable serves neurodivergent youth. Every decision should consider:
- **Accessibility**: Is this usable by people with different abilities?
- **Inclusivity**: Does this welcome all users?
- **Simplicity**: Is this as simple as possible while still being effective?
- **Privacy**: Does this protect user data and privacy?

### Development Philosophy
- **Accessibility First**: WCAG 2.1 AA compliance is mandatory
- **Progressive Enhancement**: Core functionality works without JavaScript
- **Privacy by Design**: Minimal data collection, maximum user control
- **Performance Matters**: Fast load times improve accessibility
- **Documentation Driven**: Code should be self-documenting

## Development Environment Setup

### 1. Prerequisites Installation

#### Required Tools
```bash
# Node.js and Package Managers
node --version    # Required: 18.x or higher
npm --version     # Required: 9.x or higher
yarn --version    # Required: 1.22.x or higher

# Python and Environment
python --version  # Required: 3.11 or higher
pip --version     # Required: 23.x or higher

# Database
psql --version    # Required: PostgreSQL 15 or higher

# Containerization
docker --version  # Required: 20.x or higher
docker-compose --version  # Required: 2.x or higher

# Version Control
git --version     # Required: 2.x or higher
```

#### Installation Commands
```bash
# macOS using Homebrew
brew install node python@3.11 postgresql docker git
brew install --cask docker

# Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm python3.11 python3-pip postgresql-15 docker.io docker-compose git

# Windows using Chocolatey
choco install nodejs python postgresql docker-desktop git
```

### 2. Repository Setup

#### Clone and Initial Setup
```bash
# Clone the repository
git clone https://github.com/Autrement-capable/AutrementCapable.git
cd AutrementCapable

# Create your feature branch
git checkout -b feature/your-feature-name

# Set up git hooks (if available)
chmod +x contribution-check.sh
```

#### Environment Configuration
```bash
# Backend environment setup
cd Backend
cp .env.example .env  # Create if doesn't exist
# Edit .env with your local configuration

# Frontend environment setup
cd ../website
cp .env.example .env  # Create if doesn't exist
# Edit .env with your local configuration
```

### 3. Database Setup

#### Local PostgreSQL Setup
```bash
# Start PostgreSQL service
# macOS
brew services start postgresql

# Ubuntu/Debian
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create development database
createdb autrement_capable_dev
createuser autrement_capable_user --pwprompt

# Grant permissions
psql -c "GRANT ALL PRIVILEGES ON DATABASE autrement_capable_dev TO autrement_capable_user;"
```

#### Docker Database Setup (Alternative)
```bash
cd Backend
docker-compose up -d db  # Start only the database
```

### 4. Backend Setup

```bash
cd Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python -m alembic upgrade head  # If migrations exist

# Start development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

#### Backend Environment Variables
```bash
# Backend/.env
HOST=0.0.0.0
PORT=5000
DEBUG=True
MODE=DEV

# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=autrement_capable_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=autrement_capable_dev
POSTGRES_PORT=5432

# Security
SERVER_SECRET=your_development_secret_key
AES_KEY=your_32_character_key_here

# WebAuthn
RP_ID=localhost
ORIGIN=http://localhost

# AI (Optional for development)
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Frontend Setup

```bash
cd website

# Install dependencies
yarn install
# or
npm install

# Start development server
yarn serve
# or
npm run serve
```

#### Frontend Environment Variables
```bash
# website/.env
VUE_APP_SERVER_URL=http://localhost:5000
VUE_APP_ENVIRONMENT=development
```

## Code Organization

### Frontend Structure
```
website/src/
├── components/
│   ├── common/              # Reusable UI components
│   │   ├── Button.vue       # Accessible button component
│   │   └── Modal.vue        # Accessible modal component
│   ├── accessibility/       # Accessibility-specific components
│   │   └── AccessibilityWidget.vue
│   ├── games/              # Game-specific components
│   │   ├── GameContainer.vue
│   │   └── ScoreDisplay.vue
│   └── ui/                 # Base UI elements
├── views/                  # Page components
│   ├── auth/               # Authentication pages
│   ├── games/              # Game interfaces
│   ├── profile/            # User profile pages
│   └── dashboard/          # Main dashboard
├── router/                 # Vue Router configuration
├── services/               # API service layer
│   ├── AuthService.js      # Authentication logic
│   ├── GameService.js      # Game data management
│   └── PictureService.js   # Avatar/image handling
├── utils/                  # Utility functions
└── assets/                 # Static assets
```

### Backend Structure
```
Backend/app/
├── api/                    # API endpoints
│   ├── auth/               # Authentication endpoints
│   │   ├── __init__.py
│   │   ├── login.py        # Login/logout endpoints
│   │   └── register.py     # Registration endpoints
│   ├── data/               # Game data endpoints
│   │   ├── games.py        # Game data CRUD
│   │   └── profile.py      # User profile endpoints
│   └── dev/                # Development-only endpoints
├── core/                   # Core application code
│   ├── application.py      # FastAPI app setup
│   ├── config.py           # Configuration management
│   ├── security/           # Security middleware
│   └── cors/               # CORS configuration
├── db/                     # Database layer
│   ├── models/             # SQLAlchemy models
│   ├── repositories/       # Data access layer
│   └── postgress/          # PostgreSQL specific code
├── services/               # Business logic
│   ├── auth/               # Authentication services
│   ├── scheduler/          # Background tasks
│   └── content/            # Content management
└── utils/                  # Utility functions
```

## Development Workflow

### 1. Feature Development Process

#### Planning Phase
1. **Read Requirements**: Understand the feature from user perspective
2. **Check Accessibility**: Consider WCAG guidelines and neurodivergent needs
3. **Design API**: Plan backend endpoints and data structures
4. **Component Planning**: Identify reusable components needed

#### Implementation Phase
```bash
# 1. Create feature branch
git checkout -b feature/add-new-game

# 2. Backend development
cd Backend
# Write tests first (TDD approach)
pytest tests/test_new_game.py -v

# Write implementation
# Run tests frequently
pytest tests/ -v

# 3. Frontend development
cd ../website
# Implement components
# Test accessibility
# Run linting
npm run lint

# 4. Integration testing
# Test full flow
# Verify accessibility
# Check performance
```

#### Review Phase
```bash
# 1. Self-review
git diff main...feature/add-new-game

# 2. Run full test suite
cd Backend && pytest
cd ../website && npm run test

# 3. Check code quality
cd Backend && pylint app/
cd ../website && npm run lint

# 4. Accessibility testing
# Use screen reader
# Check keyboard navigation
# Verify color contrast
```

### 2. Testing Strategy

#### Backend Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run tests with debugging
pytest -s tests/test_games.py::test_scenario_game
```

#### Frontend Testing
```bash
# Run unit tests
npm run test:unit

# Run with coverage
npm run test:unit -- --coverage

# Run specific test
npm run test:unit -- tests/unit/components/Button.spec.js

# Lint code
npm run lint

# Fix linting issues
npm run lint -- --fix
```

#### Accessibility Testing
```bash
# Install accessibility testing tools
npm install -g @axe-core/cli

# Run accessibility tests
axe http://localhost:8080

# Manual testing checklist:
# - Tab navigation works
# - Screen reader compatibility
# - High contrast mode
# - Keyboard-only navigation
# - Color blindness simulation
```

### 3. Code Style Guidelines

#### Frontend Code Style
```javascript
// Vue Component Example
<template>
  <div class="game-container" role="main" :aria-label="gameTitle">
    <button 
      @click="startGame"
      :disabled="isLoading"
      :aria-label="`Start ${gameTitle} game`"
      class="btn btn-primary"
    >
      {{ isLoading ? 'Loading...' : 'Start Game' }}
    </button>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'GameContainer',
  props: {
    gameTitle: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const isLoading = ref(false)
    
    const startGame = async () => {
      isLoading.value = true
      try {
        // Game logic here
      } catch (error) {
        console.error('Game start failed:', error)
        // Handle error appropriately
      } finally {
        isLoading.value = false
      }
    }
    
    return {
      isLoading,
      startGame
    }
  }
}
</script>
```

#### Backend Code Style
```python
# FastAPI Endpoint Example
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..db.postgress.engine import get_session
from ..db.postgress.repositories.games_data import get_scenario_game_data
from ..core.security.decorators import require_auth
from ..models.game_models import ScenarioGameResponse

router = APIRouter(prefix="/games", tags=["games"])

@router.get("/scenario/{user_id}", response_model=ScenarioGameResponse)
@require_auth()
async def get_user_scenario_data(
    user_id: int,
    session: AsyncSession = Depends(get_session)
) -> ScenarioGameResponse:
    """
    Get scenario game data for a user.
    
    Args:
        user_id: The ID of the user
        session: Database session
        
    Returns:
        ScenarioGameResponse: User's scenario game data
        
    Raises:
        HTTPException: If user not found or access denied
    """
    try:
        game_data = await get_scenario_game_data(session, user_id)
        if not game_data:
            raise HTTPException(status_code=404, detail="Game data not found")
        
        return ScenarioGameResponse.from_orm(game_data)
    except Exception as e:
        logger.error(f"Error retrieving scenario data for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### 4. Common Development Tasks

#### Adding a New Game
```bash
# 1. Backend: Create game model
# Backend/app/db/postgress/models/test_model.py
class NewGameData(Base):
    __tablename__ = "new_game_data"
    
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    completion = mapped_column(Float, nullable=False, default=0.0)
    game_specific_data = mapped_column(JSON, nullable=False, default={})

# 2. Backend: Create repository functions
# Backend/app/db/postgress/repositories/games_data.py
async def get_new_game_data(session: AsyncSession, user_id: int):
    # Implementation here

# 3. Backend: Create API endpoints
# Backend/app/api/data/games.py
@router.get("/new-game/{user_id}")
async def get_new_game_data(user_id: int):
    # Implementation here

# 4. Frontend: Create game component
# website/src/views/skillGames/NewGame.vue
<template>
  <!-- Game interface here -->
</template>

# 5. Frontend: Add to router
# website/src/router/index.js
{
  path: '/games/new-game',
  component: () => import('@/views/skillGames/NewGame.vue')
}
```

#### Adding a New API Endpoint
```python
# 1. Define Pydantic models
class GameRequest(BaseModel):
    game_type: str
    data: dict

class GameResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

# 2. Implement endpoint
@router.post("/games/submit", response_model=GameResponse)
@require_auth()
async def submit_game_data(
    request: GameRequest,
    current_user = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    # Implementation here
    pass

# 3. Add to main router
from .api.data.games import router as games_router
app.include_router(games_router)
```

## Debugging and Troubleshooting

### Common Issues and Solutions

#### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U autrement_capable_user -d autrement_capable_dev

# Reset database
dropdb autrement_capable_dev
createdb autrement_capable_dev
```

#### Frontend Build Issues
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for conflicting dependencies
npm audit
npm audit fix
```

#### Backend Import Issues
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall in development mode
pip install -e .
```

### Development Tools

#### VS Code Extensions (Recommended)
- **Vetur**: Vue.js support
- **Python**: Python language support
- **SQLAlchemy**: Database schema support
- **axe Accessibility Linter**: Accessibility checking
- **Prettier**: Code formatting
- **ESLint**: JavaScript linting

#### Browser Extensions
- **axe DevTools**: Accessibility testing
- **Vue.js DevTools**: Vue debugging
- **WAVE**: Web accessibility evaluation

## Next Steps

### After Setup
1. **Explore the codebase**: Read through existing components and services
2. **Run the test suite**: Make sure everything works on your machine
3. **Pick a small task**: Start with documentation or minor bug fixes
4. **Ask questions**: Join team discussions and ask for help when needed

### Learning Resources
- [Vue.js 3 Documentation](https://vuejs.org/guide/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

### Contributing Guidelines
- Follow the code style guide
- Write tests for new features
- Update documentation for changes
- Consider accessibility in all implementations
- Test with screen readers when possible

---

*Welcome to the team! Remember, every contribution helps create a more inclusive future for neurodivergent youth.*