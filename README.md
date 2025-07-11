# Autrement Capable

An inclusive, gamified self-discovery platform designed specifically for neurodivergent youth, particularly those with Autism Spectrum Disorder (ASD). The platform helps users build confidence, understand their strengths, and prepare for their professional future through accessible, engaging mini-games and AI-powered personalization.

## 🎯 Purpose

Autrement Capable addresses the unique challenges faced by neurodivergent youth in understanding their strengths and preparing for the workforce. Through a series of accessible mini-games, AI-powered avatar creation, and personalized profile building, users can:

- Discover their professional interests and strengths
- Build confidence through positive reinforcement
- Develop self-awareness in a safe, gamified environment
- Prepare for future career opportunities

## ✨ Key Features

### 🎮 Six Self-Discovery Mini-Games
- **Passion Explorer**: Rate job videos to identify career interests
- **Ideal Work Environment**: Customize a 3D workspace to define preferences
- **Typing Ability**: Assess motor skills through progressive typing challenges
- **Logical Thinking**: Solve visual sequences to test logical reasoning
- **Skill Self-Assessment**: Identify existing skills and areas for development
- **Emotional Intelligence**: Navigate workplace scenarios to assess soft skills

### 🤖 AI-Powered Features
- **Custom Avatar Generation**: AI-created avatars with emotional expressions
- **Personalized Profiles**: Dynamic profiles that evolve based on game interactions
- **Intelligent Recommendations**: Tailored suggestions based on user data

### 🔐 Accessibility & Security
- **Passwordless Authentication**: Secure Passkey/WebAuthn implementation
- **Accessibility Widget**: Real-time adaptations for text size, contrast, audio
- **Inclusive Design**: Co-designed with autism specialists and neurodivergent youth

### 🏆 Progression System
- **Visual Badge System**: Track progress through meaningful achievements
- **Evolving Central Badge**: Dynamic representation of user growth
- **Minimalist Dashboard**: Clear, accessible interface design

## 🛠️ Technology Stack

- **Frontend**: Vue.js 3, TailwindCSS, Three.js, TresJS
- **Backend**: FastAPI, PostgreSQL, AsyncPG
- **AI**: OpenAI API integration
- **Authentication**: WebAuthn/Passkeys
- **Deployment**: Docker, Docker Compose, GitHub Actions
- **Development**: ESLint, Prettier, pytest

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](./docs/) directory:

- **[📖 Full Documentation Index](./docs/README.md)**
- **[🏗️ Technical Architecture](./docs/04-technical-architecture.md)**
- **[👨‍💻 Developer Getting Started](./docs/07-developer-getting-started.md)**
- **[💻 Local Development Setup](./docs/08-local-development.md)**
- **[🚀 Deployment Guide](./docs/10-deployment.md)**

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and yarn/npm
- Python 3.11+
- PostgreSQL 15+
- Docker and Docker Compose

### Local Development
```bash
# Clone the repository
git clone https://github.com/Autrement-capable/AutrementCapable.git
cd AutrementCapable

# Backend setup
cd Backend
pip install -r requirements.txt
docker-compose up -d  # Start PostgreSQL
# Configure environment variables
python -m uvicorn app.main:app --reload

# Frontend setup (in new terminal)
cd ../website
yarn install
yarn serve
```

For detailed setup instructions, see [Local Development Setup](./docs/08-local-development.md).

## 🤝 Contributing

We welcome contributions! Please see our:
- [Developer Onboarding Guide](./docs/07-developer-getting-started.md)
- [Architecture Documentation](./docs/04-technical-architecture.md)
- [Beta Test Plan](./BTP.md) for current development focus

## 🔒 Security & Privacy

This platform prioritizes user privacy and security:
- No personal data is shared with third parties
- Passwordless authentication reduces security risks
- All user data is encrypted and stored securely
- GDPR-compliant data handling practices

## 📞 Support

For questions or support, please refer to our documentation or contact the development team.

---

*Empowering neurodivergent youth through accessible technology and inclusive design.*