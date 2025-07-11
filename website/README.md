# Autrement Capable - Frontend

This is the Vue.js frontend application for the Autrement Capable platform - an inclusive, gamified self-discovery platform for neurodivergent youth.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Backend API running (see [Backend setup](../Backend/README.md))

### Installation
```bash
# Install dependencies
yarn install
# or
npm install
```

### Development
```bash
# Start development server with hot-reload
yarn serve
# or
npm run serve

# Access the application at http://localhost:8080
```

### Production
```bash
# Build for production
yarn build
# or
npm run build

# The built files will be in the `dist/` directory
```

## 🛠️ Development

### Code Quality
```bash
# Lint and fix files
yarn lint
# or
npm run lint

# Run linting without auto-fix
yarn lint --no-fix
```

### Testing
```bash
# Run unit tests
yarn test:unit
# or
npm run test:unit

# Run tests with coverage
yarn test:unit --coverage
```

## 📁 Project Structure

```
src/
├── components/          # Reusable Vue components
│   ├── common/         # Shared UI components
│   ├── accessibility/ # Accessibility-specific components
│   ├── games/         # Game-related components
│   └── ui/            # Base UI elements
├── views/              # Page components
│   ├── auth/          # Authentication pages
│   ├── games/         # Game interfaces
│   ├── profile/       # User profile pages
│   └── dashboard/     # Main dashboard
├── router/             # Vue Router configuration
├── services/           # API service layer
├── utils/              # Utility functions
├── assets/             # Static assets
└── data/              # Static data files
```

## 🎯 Key Features

- **Vue 3 Composition API**: Modern reactive framework
- **TailwindCSS**: Utility-first CSS framework
- **Three.js Integration**: 3D graphics for environment game
- **WebAuthn Support**: Passwordless authentication
- **Accessibility First**: WCAG 2.1 AA compliant components
- **Progressive Web App**: Offline capabilities and app-like experience

## 🔧 Configuration

### Environment Variables
```bash
# .env.local (create this file)
VUE_APP_SERVER_URL=http://localhost:5000
VUE_APP_ENVIRONMENT=development
VUE_APP_DEBUG=true
```

### Customization
- **Vue CLI Configuration**: See `vue.config.js`
- **TailwindCSS Configuration**: See `tailwind.config.js`
- **ESLint Configuration**: See `.eslintrc.js`
- **Babel Configuration**: See `babel.config.js`

## 🌐 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 📚 Documentation

- **[Complete Documentation](../docs/README.md)**: Comprehensive project documentation
- **[Developer Guide](../docs/07-developer-getting-started.md)**: How to start contributing
- **[Local Development](../docs/08-local-development.md)**: Complete development setup
- **[Technical Architecture](../docs/04-technical-architecture.md)**: System architecture overview

## 🤝 Contributing

1. **Setup**: Follow the [local development guide](../docs/08-local-development.md)
2. **Standards**: Read the [developer guide](../docs/07-developer-getting-started.md)
3. **Accessibility**: Ensure all changes maintain WCAG 2.1 AA compliance
4. **Testing**: Write tests for new components and features

## 🔍 Troubleshooting

### Common Issues

#### Node.js Version
```bash
# Check Node.js version
node --version  # Should be 18.x or higher

# Use Node Version Manager to switch versions
nvm use 18
```

#### Dependencies
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### Development Server
```bash
# If port 8080 is in use
yarn serve --port 3000

# Clear Vue CLI cache
rm -rf node_modules/.cache
```

## 📞 Support

- **Documentation**: Check the [comprehensive docs](../docs/README.md)
- **Issues**: Report issues in the GitHub repository
- **Development**: Join the team discussions for development questions

---

*Building an inclusive future for neurodivergent youth through accessible technology.*
