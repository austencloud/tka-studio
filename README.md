# TKA Studio

**TKA Studio** - Browser-based movement notation software for creating visual "pictographs" showing dance and flow art sequences.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open browser to http://localhost:5173/
```

## What is TKA Studio?

TKA Studio is digital "sheet music" for dancers and flow artists, built on The Kinetic Alphabet notation system. It creates visual diagrams showing movement sequences with:

- **Props** (staff, triad, etc.) - Physical objects being manipulated
- **Grid positions** (where props are located)
- **Arrows** (direction of movement)
- **Timing** (beat-by-beat sequences)
- **Orientations** (how props are rotated)

Think of it as musical notation, but for physical movement instead of sound.

## Technology Stack

- **Framework**: SvelteKit 2.0 with Svelte 5
- **Language**: TypeScript 5.0
- **State Management**: Svelte 5 runes ($state, $derived, $effect)
- **Dependency Injection**: InversifyJS 7.9
- **Build Tool**: Vite 6.0
- **Deployment**: Netlify

## Project Structure

```
web/
├── src/
│   ├── lib/
│   │   ├── modules/          # Feature modules
│   │   │   ├── about/        # Landing page
│   │   │   ├── animator/     # Animation engine
│   │   │   ├── browse/       # Browse sequences
│   │   │   ├── build/        # Sequence construction
│   │   │   ├── learn/        # Learning tools
│   │   │   └── word-card/    # Word card generation
│   │   └── shared/           # Cross-module infrastructure
│   │       ├── application/  # App coordination
│   │       ├── inversify/    # DI container
│   │       ├── pictograph/   # Core rendering engine
│   │       └── utils/        # Helper functions
│   └── routes/               # SvelteKit pages
├── static/                   # Static assets
├── tests/                    # Test files
└── docs/                     # Documentation
```

## Development

### Available Scripts

```bash
# Development
npm run dev              # Start dev server
npm run dev:clean        # Start with clean cache (use after deleting files)

# Building
npm run build            # Build for production
npm run preview          # Preview production build

# Quality Checks
npm run check            # Type checking
npm run check:watch      # Type checking in watch mode
npm run lint             # Lint code
npm run lint:fix         # Fix linting issues
npm run format           # Format code with Prettier

# Testing
npm run test             # Run unit tests
npm run test:e2e         # Run E2E tests
npm run test:e2e:ui      # Run E2E tests with UI

# Validation
npm run validate         # Run all checks (lint + type + test)
```

### Development Guide

**📖 See [DEVELOPMENT.md](./DEVELOPMENT.md) for:**

- Hot Module Reload (HMR) best practices
- Common issues and solutions
- Architecture guidelines
- Debugging tips
- Testing strategies
- Git workflow

**⚠️ Important:** Always use `npm run dev:clean` after deleting or renaming files to avoid HMR cache issues.

## Architecture

### Module-First Organization

Each feature is a self-contained module with:

```
module-name/
├── components/          # UI Components (Svelte)
├── domain/              # Data models & types
│   ├── constants/       # Module constants
│   ├── enums/          # Enumerations
│   ├── models/         # Data models
│   └── types/          # Type definitions
├── services/           # Business logic layer
│   ├── contracts/      # Service interfaces
│   └── implementations/ # Service classes
├── state/              # Reactive state management
└── index.ts            # Module barrel exports
```

### Key Principles

- **Pure Services** - Zero UI concerns, completely testable
- **Svelte 5 Runes** - All reactive state uses $state, $derived, $effect
- **InversifyJS** - Professional dependency injection
- **Interface-Driven** - All services implement contracts
- **Module Boundaries** - Modules communicate via shared infrastructure only

## Contributing

### Before Making Changes

1. Read [DEVELOPMENT.md](./DEVELOPMENT.md)
2. Check existing patterns with codebase search
3. Follow the module architecture
4. Write tests for new features
5. Run `npm run validate` before committing

### Code Style

- Use TypeScript for all code
- Follow existing naming conventions
- Use Svelte 5 runes (not stores)
- Keep components focused on presentation
- Put business logic in services

## Deployment

The application is deployed to Netlify automatically on push to main branch.

```bash
# Build for production
npm run build

# Preview production build locally
npm run preview
```

## Resources

- **Svelte 5 Docs**: https://svelte.dev/docs/svelte/overview
- **SvelteKit Docs**: https://kit.svelte.dev/docs
- **Vite Docs**: https://vitejs.dev/guide/
- **InversifyJS Docs**: https://inversify.io/

## License

Copyright © 2025 Austen Cloud (tkaflowarts@gmail.com)

## Contact

- **Email**: tkaflowarts@gmail.com
- **Developer**: Austen Cloud

---

**For detailed development information, see [DEVELOPMENT.md](./DEVELOPMENT.md)**
