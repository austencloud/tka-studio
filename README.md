# TKA Monorepo

## The Kinetic Constructor - Desktop and Web Applications

[![CI/CD](https://github.com/austencloud/the-kinetic-constructor/actions/workflows/ci.yml/badge.svg)](https://github.com/austencloud/the-kinetic-constructor/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org)

A professional monorepo containing desktop (PyQt) and web (SvelteKit) applications for kinetic sequence construction and animation.

## 🏗️ Architecture

```
TKA Monorepo
├── 🖥️  Desktop App (PyQt + FastAPI)
├── 🌐 Web App (SvelteKit + TypeScript)
├── 🎨 Landing Page (SvelteKit)
├── 🎬 Animator Tool (SvelteKit)
└── 📦 Shared Packages (Types, Constants, Utils)
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** - [Download](https://python.org)
- **Node.js 18+** - [Download](https://nodejs.org)
- **Git** - [Download](https://git-scm.com)

### Setup

```bash
# Clone the repository
git clone https://github.com/austencloud/the-kinetic-constructor.git
cd the-kinetic-constructor

# Set up development environment
python scripts/setup.py
```

### Development

```bash
# Start desktop application
python scripts/dev.py desktop

# Start web application
python scripts/dev.py web

# Start API server only
python scripts/dev.py api

# Start full-stack (API + Web)
python scripts/dev.py fullstack

# Run all tests
python scripts/dev.py test

# Build all applications
python scripts/dev.py build

# Clean build artifacts
python scripts/clean.py
```

## 📦 Applications

### Desktop Application (`apps/desktop/`)

PyQt6-based desktop application with modern architecture:

- **Modern**: Clean architecture with DI, services, events
- **Legacy**: Existing codebase (maintenance mode)
- **API**: FastAPI server for web integration

**Key Features:**

- Kinetic sequence construction
- Real-time animation preview
- Export/import functionality
- Advanced editing tools

### Web Application (`apps/web/`)

SvelteKit web application providing browser-based access:

- Real-time synchronization with desktop
- Responsive design
- Progressive Web App features
- Cross-platform compatibility

### Landing Page (`apps/landing/`)

Marketing website built with SvelteKit:

- Product showcase
- Documentation
- Download links
- Community resources

### Animator Tool (`apps/animator/`)

Specialized tool for pictograph animation:

- Frame-by-frame animation
- Export to various formats
- Timeline editing
- Effect libraries

## 🔧 Development

### Workspace Structure

```
F:\CODE\TKA\
├── .vscode/                    # VSCode configuration
├── .github/                    # CI/CD workflows
├── apps/                       # Applications
│   ├── desktop/               # PyQt desktop app
│   ├── web/                   # SvelteKit web app
│   ├── landing/               # Marketing site
│   └── animator/              # Animation tool
├── packages/                   # Shared packages
│   ├── shared-types/          # TypeScript/Python types
│   ├── constants/             # Shared constants
│   ├── utils/                 # Utility functions
│   └── assets/                # Shared assets
├── data/                      # Shared data files
├── docs/                      # Documentation
├── scripts/                   # Development scripts
├── tests/                     # Integration tests
├── package.json               # Workspace configuration
└── pyproject.toml            # Python configuration
```

### Commands

```bash
# Development
npm run dev:desktop     # Start desktop app
npm run dev:web         # Start web app
npm run dev:fullstack   # Start API + web
npm run dev:landing     # Start landing page
npm run dev:animator    # Start animator

# Testing
npm run test:all        # Run all tests
npm run test:desktop    # Python tests
npm run test:web        # Web tests

# Building
npm run build:all       # Build everything
npm run build:web       # Build web app
npm run build:landing   # Build landing page
npm run build:animator  # Build animator

# Maintenance
npm run lint:all        # Lint all code
npm run clean           # Clean artifacts
npm run setup           # Setup environment
```

### VSCode Integration

- Install recommended extensions
- Use `Ctrl+Shift+P` → "Tasks: Run Task" for quick actions
- Configured for Python and TypeScript debugging
- Integrated testing and linting

## 🧪 Testing

```bash
# Desktop tests
cd apps/desktop && python -m pytest modern/tests/

# Web tests
cd apps/web && npm test

# Integration tests
python scripts/test_integration.py

# All tests
python scripts/dev.py test
```

## 🏗️ Building

```bash
# Build web applications
npm run build:web
npm run build:landing
npm run build:animator

# Build desktop application
cd apps/desktop && python scripts/build.py

# Build everything
python scripts/dev.py build
```

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Desktop Development](docs/desktop.md)
- [Web Development](docs/web.md)
- [Contributing Guide](docs/contributing.md)
- [Architecture Overview](docs/architecture.md)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Development Workflow

1. Run `python scripts/setup.py` to set up environment
2. Use `python scripts/dev.py fullstack` for development
3. Write tests for new features
4. Run `python scripts/dev.py test` before committing
5. Follow code style guidelines

## 🔄 CI/CD

Automated workflows handle:

- **Testing**: Python and JavaScript tests
- **Building**: All applications
- **Security**: Vulnerability scanning
- **Dependencies**: Automated updates via Dependabot
- **Deployment**: Automated releases

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- PyQt6 for desktop framework
- SvelteKit for web framework
- FastAPI for backend API
- All contributors and community members

---

**Made with ❤️ by the TKA Team**
