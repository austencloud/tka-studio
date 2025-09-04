# TKA Web App - Test Suite

## 🎯 Overview

This directory contains all tests for the TKA Web Application, organized in a clean, maintainable structure that separates different types of tests by purpose and scope.

## 📁 Directory Structure

```
tests/
├── unit/                    # Fast, isolated unit tests
│   ├── components/          # Component unit tests
│   ├── services/           # Service unit tests
│   └── domain/             # Domain logic tests
├── integration/            # Integration tests
│   └── services/           # Service integration tests
├── debug/                  # Debug and development tests
│   ├── positioning/        # Positioning debug tests
│   └── circular-dependency/ # Circular dependency debugging
├── e2e/                    # End-to-end tests (Playwright)
├── setup/                  # Test configuration and setup
└── README.md               # This file
```

## 🚀 Running Tests

### All Tests

```bash
npm run test                # Run all Vitest tests (unit + integration + debug)
```

### By Category

```bash
npm run test:unit          # Run only unit tests
npm run test:integration   # Run only integration tests
npm run test:debug         # Run only debug tests
```

### End-to-End Tests

```bash
npm run test:seo           # Run SEO integration tests
npm run test:seo:headed    # Run SEO tests with browser UI
npm run test:seo:debug     # Run SEO tests in debug mode
```

## 📋 Test Categories

### Unit Tests (`tests/unit/`)

- **Purpose**: Fast, isolated tests for individual components and services
- **Scope**: Single component or service in isolation
- **Speed**: < 1 second per test
- **Dependencies**: Mocked or stubbed

### Integration Tests (`tests/integration/`)

- **Purpose**: Test interactions between multiple components/services
- **Scope**: Multiple components working together
- **Speed**: < 5 seconds per test
- **Dependencies**: Real services, mocked external APIs

### Debug Tests (`tests/debug/`)

- **Purpose**: Development and debugging tests
- **Scope**: Specific debugging scenarios and edge cases
- **Speed**: Variable
- **Dependencies**: Real or mocked as needed

### E2E Tests (`tests/e2e/`)

- **Purpose**: Full user workflow testing
- **Scope**: Complete user journeys
- **Speed**: 10+ seconds per test
- **Dependencies**: Real browser, real services

## 🔧 Config

### Vitest Config

- **Config File**: `vitest.config.ts`
- **Setup File**: `tests/setup/vitest-setup.ts`
- **Environment**: jsdom
- **Aliases**: `$lib` and `$app` for imports

### Playwright Config

- **Config File**: `playwright.config.ts`
- **Test Directory**: `tests/e2e/`
- **Browsers**: Chrome, Firefox, Safari

## 📝 Writing Tests

### Import Patterns

Use the configured aliases for clean imports:

```typescript
// ✅ Good - Use aliases
import { MyService } from "$lib/services/MyService";
import { MyComponent } from "$components/MyComponent.svelte";

// ❌ Avoid - Relative paths
import { MyService } from "../../../src/lib/services/MyService";
```

### Test File Naming

- Unit tests: `ComponentName.test.ts`
- Integration tests: `feature-integration.test.ts`
- Debug tests: `debug-scenario.test.ts`
- E2E tests: `workflow-name.spec.ts`

## 🧹 Maintenance

This test structure was reorganized from a scattered approach to improve:

- **Discoverability**: Easy to find relevant tests
- **Maintainability**: Clear separation of concerns
- **Performance**: Faster test execution with proper categorization
- **CI/CD**: Better pipeline organization

## 🔍 Migration Notes

Tests were moved from these locations:

- `src/tests/` → `tests/unit/`, `tests/integration/`, `tests/debug/`
- Component `__tests__/` directories → `tests/unit/components/`
- Service `__tests__/` directories → `tests/unit/services/`
- Root-level test files → Appropriate category directories
- `src/lib/test/setup.ts` → `tests/setup/vitest-setup.ts`

All import paths have been updated to use `$lib` and `$app` aliases for consistency.
