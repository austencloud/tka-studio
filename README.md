# TKA - The Kinetic Alphabet

A comprehensive application for creating, editing, and learning kinetic sequences.

## Project Structure

This is a monorepo containing two main applications:

### 🌐 Web Application (`/web`)

- **Technology:** SvelteKit + TypeScript
- **Purpose:** Browser-based sequence editor and viewer
- **Deployment:** Netlify (see [DEPLOYMENT.md](DEPLOYMENT.md))
- **Features:**
  - Interactive sequence creation
  - Real-time preview
  - Export/import functionality
  - Responsive design

### 🖥️ Desktop Application (`/desktop`)

- **Technology:** Python (with GUI framework)
- **Purpose:** Full-featured desktop application
- **Distribution:** Standalone executables
- **Features:**
  - Advanced editing capabilities
  - Local file management
  - Performance optimizations
  - Platform-specific integrations

## Quick Start

### Web Development

```bash
cd web/
npm install
npm run dev
```

### Desktop Development

```bash
cd desktop/
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt  # If available
python main.py  # Adjust to your entry point
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Web App (Netlify)

The web application is configured for automatic deployment to Netlify:

- **Production:** Deploys automatically from `main` branch
- **Preview:** Deploys on pull requests
- **Configuration:** Root-level `netlify.toml`

### Desktop App

Build standalone executables for distribution:

```bash
cd desktop/
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## Documentation

- [Deployment Guide](DEPLOYMENT.md)
- [Web Architecture](web/ARCHITECTURE.md)
- [Testing Guide](web/TESTING_GUIDE.md)
- [Manual Testing Checklist](web/MANUAL_TESTING_CHECKLIST.md)

## Development Workflow

1. **Feature Development:** Create feature branches from `main`
2. **Testing:** Run tests locally and in CI
3. **Review:** Submit pull requests for code review
4. **Deployment:** Merge to `main` triggers automatic deployment (web) or manual release (desktop)

## Contributing

1. Clone the repository
2. Choose your development environment (web or desktop)
3. Follow the quick start instructions above
4. Make your changes and test thoroughly
5. Submit a pull request

## License

[Add your license information here]
