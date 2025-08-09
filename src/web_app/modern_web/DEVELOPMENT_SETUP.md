# Development Environment Setup Guide

This guide covers the complete development environment configuration for the TKA V2 Modern Web Application.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run in separate terminal for development
npm run dev:open  # Opens browser automatically
```

## 📋 Available Scripts

### Development

- `npm run dev` - Start development server on localhost:5174
- `npm run dev:open` - Start development server and open browser
- `npm run dev:bash` - Start development server using Git Bash

### Building

- `npm run build` - Build for production
- `npm run build:analyze` - Build with bundle analysis
- `npm run preview` - Preview production build
- `npm run preview:open` - Preview production build and open browser

### Code Quality

- `npm run lint` - Run ESLint on all files
- `npm run lint:fix` - Run ESLint and fix auto-fixable issues
- `npm run lint:check` - Run ESLint with zero warnings tolerance
- `npm run format` - Format all files with Prettier
- `npm run format:check` - Check if files are properly formatted
- `npm run type-check` - Run TypeScript type checking

### Testing

- `npm run test` - Run unit tests with Vitest
- `npm run test:watch` - Run tests in watch mode
- `npm run test:ui` - Run tests with UI interface
- `npm run test:coverage` - Run tests with coverage report
- `npm run test:e2e` - Run end-to-end tests with Playwright
- `npm run test:e2e:ui` - Run E2E tests with UI
- `npm run test:e2e:debug` - Run E2E tests in debug mode

### Validation & Maintenance

- `npm run validate` - Run all checks (format, lint, type-check, coverage)
- `npm run clean` - Clean build artifacts and cache
- `npm run clean:deps` - Clean and reinstall dependencies

## 🛠️ Configuration Files

### Core Configuration

- **package.json** - Project dependencies and scripts
- **tsconfig.json** - TypeScript configuration with strict settings
- **vite.config.ts** - Vite build tool configuration
- **svelte.config.js** - Svelte framework configuration

### Code Quality

- **eslint.config.js** - ESLint linting rules for TypeScript and Svelte
- **.prettierrc** - Prettier code formatting rules
- **.editorconfig** - Editor configuration for consistent coding styles

### Styling

- **tailwind.config.js** - Tailwind CSS configuration with custom theme
- **postcss.config.js** - PostCSS configuration with Tailwind and Autoprefixer

### Testing

- **vitest.config.ts** - Vitest unit testing configuration
- **playwright.config.ts** - Playwright E2E testing configuration
- **vitest-setup.ts** - Test environment setup

### Development Environment

- **.env.example** - Environment variables template
- **.env.local** - Local development environment variables
- **.gitignore** - Git ignore patterns
- **.gitattributes** - Git file handling rules

### VSCode Integration

- **.vscode/settings.json** - VSCode workspace settings
- **.vscode/extensions.json** - Recommended VSCode extensions

## 🎯 Development Workflow

### 1. Initial Setup

```bash
# Clone and navigate to project
cd src/web_app/modern_web

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local
```

### 2. Daily Development

```bash
# Start development server
npm run dev

# In separate terminal, run tests in watch mode
npm run test:watch

# Before committing, validate code
npm run validate
```

### 3. Code Quality Checks

```bash
# Format code
npm run format

# Fix linting issues
npm run lint:fix

# Check types
npm run type-check

# Run all validations
npm run validate
```

## 🔧 Tool Configuration

### ESLint

- TypeScript support with strict rules
- Svelte component linting
- Prettier integration
- Custom rules for unused variables and imports

### Prettier

- Tab indentation (4 spaces)
- Single quotes
- Trailing commas
- 100 character line width
- Svelte plugin integration

### TypeScript

- Strict mode enabled
- Path mapping for imports (`$lib`, `@/*`)
- Comprehensive type checking
- Svelte 5 runes support

### Tailwind CSS

- Custom color palette
- Extended spacing and typography
- Custom animations and transitions
- Dark mode support
- Responsive design utilities

## 🧪 Testing Strategy

### Unit Tests (Vitest)

- Component testing with Svelte Testing Library
- Service and utility function testing
- Mock support for external dependencies
- Coverage reporting

### E2E Tests (Playwright)

- Cross-browser testing (Chrome, Firefox, Safari)
- Visual regression testing
- User interaction testing
- Automated screenshot comparison

### Integration Tests

- API endpoint testing
- Database integration testing
- Service integration testing

## 🚨 Common Issues & Solutions

### Node.js Version

- Ensure Node.js 18+ is installed
- Use `nvm` to manage Node.js versions if needed

### Port Conflicts

- Development server runs on port 5174
- Change port in `vite.config.ts` if needed

### TypeScript Errors

- Run `npm run type-check` to see all type errors
- Many existing files have type issues that need gradual fixing

### Linting Errors

- Run `npm run lint:fix` to auto-fix many issues
- Some errors require manual intervention

### Environment Variables

- Copy `.env.example` to `.env.local`
- Restart development server after changing environment variables

## 📚 Additional Resources

- [Svelte 5 Documentation](https://svelte.dev/docs/svelte/overview)
- [SvelteKit Documentation](https://kit.svelte.dev/docs)
- [Vite Documentation](https://vitejs.dev/guide/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Vitest Documentation](https://vitest.dev/guide/)
- [Playwright Documentation](https://playwright.dev/docs/intro)

## 🎉 Success Indicators

Your environment is properly configured when:

- ✅ `npm run dev` starts without errors
- ✅ `npm run build` completes successfully
- ✅ `npm run test` runs without failures
- ✅ `npm run lint` shows manageable number of issues
- ✅ `npm run format:check` passes or shows expected formatting issues
- ✅ TypeScript compilation works in your editor
- ✅ Hot reload works when editing files
- ✅ Browser opens to localhost:5174 and shows the application
