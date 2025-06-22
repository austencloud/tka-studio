# End-to-End Testing with Playwright

This directory contains end-to-end tests for The Kinetic Constructor using Playwright. These tests complement the existing Vitest unit tests by verifying the application's functionality from a user's perspective.

## Directory Structure

- `/e2e/components/` - Tests for individual components
- `/e2e/flows/` - Tests for user flows across multiple components
- `/e2e/visual/` - Visual tests for SVG rendering
- `/e2e/performance/` - Performance tests
- `/e2e/fixtures/` - Page object models and test fixtures
- `/e2e/utils/` - Utility functions and helpers

## Running Tests

```bash
# Run all E2E tests
npm run test:e2e

# Run tests with UI mode
npm run test:e2e:ui

# Run tests in debug mode
npm run test:e2e:debug

# Run only visual tests
npm run test:e2e:visual

# View the HTML report
npm run test:e2e:report
```

## Test Architecture

### Page Objects

We use the Page Object Model pattern to encapsulate selectors and actions for different parts of the application. This makes tests more maintainable and readable.

Page objects are located in the `/e2e/fixtures/` directory:

- `AppPage` - Main application navigation and layout
- `PictographPage` - Pictograph component interactions
- `GenerateTabPage` - Generate tab functionality
- `WriteTabPage` - Write tab functionality

### Visual Testing

Visual tests verify the rendering of SVG components:

1. Grid rendering in different modes
2. Prop rendering with different properties
3. Arrow visualization
4. Animation states

### Performance Testing

Performance tests measure:

1. SVG rendering time
2. Animation smoothness
3. State transition timing
4. Scroll performance with multiple pictographs

## Best Practices

1. **Use data-test attributes**: Add `data-test="component-name"` to components for stable selectors
2. **Test real user flows**: Focus on testing complete user journeys
3. **Visual testing**: Use snapshots sparingly and focus on critical visual elements
4. **State management**: Test XState transitions and state persistence
5. **Performance**: Set reasonable thresholds based on user experience requirements

## CI Integration

Tests run automatically on GitHub Actions for:

- Pull requests to main/master
- Pushes to main/master
- Manual triggers

The workflow is defined in `.github/workflows/playwright.yml`.
