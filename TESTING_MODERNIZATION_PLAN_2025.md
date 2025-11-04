# 🚀 TKA Studio Testing Framework - 2025 Rocket Ship Transformation Plan

**Date:** January 2025
**Project:** The Kinetic Alphabet Studio
**Current State:** "Dinky Car"
**Target State:** "Rocket Ship"

---

## 📊 Executive Summary

This document outlines a comprehensive plan to transform TKA Studio's testing framework from its current state into a modern, scalable, high-performance testing system aligned with 2025 best practices.

### Current State Analysis

**Strengths:**
- ✅ Modern foundation: Vitest 3.2.4 + Playwright 1.54.2
- ✅ Good test organization structure
- ✅ SvelteKit integration working
- ✅ E2E flow tests covering critical paths

**Weaknesses:**
- ⚠️ **Inverted test pyramid:** Heavy on E2E (~80 tests), light on unit tests (~21 tests)
- ⚠️ **Brittle E2E tests:** Using fragile selectors and explicit timeouts
- ⚠️ **Missing layers:** No component testing, no visual regression testing
- ⚠️ **No test coverage tracking:** Unknown code coverage metrics
- ⚠️ **Manual mocking:** Repetitive setup in every test file
- ⚠️ **Slow feedback loop:** Heavy E2E tests slow down development
- ⚠️ **No CI optimization:** Tests run sequentially without parallelization

### Success Metrics

- 🎯 **Coverage:** Achieve 80%+ code coverage
- 🎯 **Speed:** Reduce full test suite time from ~5-10 min to <2 min
- 🎯 **Reliability:** Reduce flaky test rate to <1%
- 🎯 **Developer Experience:** Test feedback in <30 seconds for unit/component tests
- 🎯 **CI/CD:** Parallel execution with test sharding
- 🎯 **Quality Gates:** Automated visual regression detection

---

## 🏗️ Architecture: The Proper Test Pyramid

```
        /\         ← E2E Tests (Critical User Journeys)
       /  \          10-15 tests | Playwright | ~5-10 min
      /    \
     /------\      ← Component Tests (UI Components)
    /        \       50-100 tests | Vitest Browser Mode | ~30-60 sec
   /----------\
  /            \   ← Integration Tests (Business Logic)
 /--------------\    30-50 tests | Vitest + MSW | ~10-20 sec
/________________\
                   ← Unit Tests (Pure Functions)
                     100-200 tests | Vitest | <5 sec
```

---

## 🎯 Phase 1: Foundation & Infrastructure (Week 1-2)

### 1.1 Vitest Browser Mode for Component Testing

**Why:** Svelte 5 runes require a real browser environment. jsdom can't handle the new reactivity system properly.

**Implementation:**

```typescript
// tests/config/vitest.config.ts
import { defineConfig } from 'vitest/config'
import { sveltekit } from '@sveltejs/kit/vite'
import { playwright } from '@vitest/browser-playwright'

export default defineConfig({
  plugins: [sveltekit()],

  test: {
    // Unit tests (jsdom for non-Svelte code)
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup/vitest-setup.ts'],

    // Browser mode for component tests
    browser: {
      enabled: true,
      provider: playwright({
        launchOptions: {
          slowMo: 0,
        },
      }),
      instances: [
        { browser: 'chromium' },
      ],
    },

    // Test organization
    include: [
      'tests/unit/**/*.{test,spec}.{js,ts}',
      'tests/integration/**/*.{test,spec}.{js,ts}',
      'tests/components/**/*.{test,spec}.{js,ts}', // NEW
    ],
    exclude: [
      'node_modules/**/*',
      'tests/e2e/**/*',
      'archive/**/*', // Exclude legacy code
    ],

    // Performance optimization
    pool: 'forks',
    poolOptions: {
      forks: {
        singleFork: true,
      },
    },
    isolate: true,

    // Coverage configuration
    coverage: {
      provider: 'v8',
      enabled: true,
      reporter: ['text', 'json', 'html', 'json-summary'],
      reportOnFailure: true,
      include: [
        'src/**/*.{ts,svelte}',
      ],
      exclude: [
        '**/node_modules/**',
        '**/tests/**',
        '**/*.config.*',
        '**/types/**',
        '**/*.d.ts',
        'archive/**',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
        autoUpdate: true, // Auto-improve thresholds
      },
    },
  },

  resolve: {
    conditions: ['browser'],
  },
})
```

**Installation:**
```bash
npm install -D @vitest/browser-playwright
npx playwright install chromium
```

### 1.2 MSW (Mock Service Worker) for API Mocking

**Why:** Reusable, realistic API mocking at the network level. Works across unit, integration, and E2E tests.

**Installation:**
```bash
npm install -D msw
```

**Setup:**

```typescript
// tests/mocks/handlers.ts
import { http, HttpResponse } from 'msw'

export const handlers = [
  // Firebase Firestore mocks
  http.get('https://firestore.googleapis.com/v1/*', () => {
    return HttpResponse.json({
      documents: [],
    })
  }),

  // Firebase Auth mocks
  http.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword', () => {
    return HttpResponse.json({
      idToken: 'mock-token',
      email: 'test@example.com',
      refreshToken: 'mock-refresh',
      expiresIn: '3600',
    })
  }),
]

// tests/mocks/server.ts
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

export const server = setupServer(...handlers)

// tests/setup/vitest-setup.ts
import { server } from '../mocks/server'

beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

### 1.3 Test Factories with TypeScript

**Why:** Generate realistic test data quickly without repetitive boilerplate.

**Installation:**
```bash
npm install -D @faker-js/faker
```

**Implementation:**

```typescript
// tests/factories/sequence.factory.ts
import { faker } from '@faker-js/faker'
import type { SequenceData } from '$shared/foundation/domain/models/SequenceData'
import type { BeatData } from '$create/workbench/domain/models/BeatData'

export const createMockBeat = (overrides?: Partial<BeatData>): BeatData => ({
  beat_number: faker.number.int({ min: 0, max: 32 }),
  letter: faker.helpers.arrayElement(['A', 'B', 'C', 'D']),
  start_location: 'n',
  end_location: 's',
  timing: 1,
  direction: 'cw',
  rotation: 0,
  blue_attributes: { start_ori: 'in', end_ori: 'out' },
  red_attributes: { start_ori: 'out', end_ori: 'in' },
  ...overrides,
})

export const createMockSequence = (overrides?: Partial<SequenceData>): SequenceData => ({
  id: faker.string.uuid(),
  name: faker.lorem.words(3),
  beats: Array.from({ length: 8 }, (_, i) => createMockBeat({ beat_number: i })),
  prop_type: 'staff',
  grid_mode: 'diamond',
  created_at: faker.date.recent(),
  updated_at: faker.date.recent(),
  ...overrides,
})

// Usage in tests:
import { createMockSequence } from '@tests/factories/sequence.factory'

test('should handle sequence with specific prop type', () => {
  const sequence = createMockSequence({ prop_type: 'fan' })
  // Test with realistic data
})
```

---

## 🎯 Phase 2: Component Testing Layer (Week 2-3)

### 2.1 Create Component Test Suite

**Target:** 50-100 component tests covering all UI components

**Example Component Test:**

```typescript
// tests/components/BeatCell.component.test.ts
import { expect, test } from 'vitest'
import { render, screen } from '@testing-library/svelte'
import { userEvent } from '@testing-library/user-event'
import BeatCell from '$lib/modules/create/workspace-panel/sequence-display/components/BeatCell.svelte'
import { createMockBeat } from '@tests/factories/sequence.factory'

test('should render beat number', async () => {
  const beat = createMockBeat({ beat_number: 5 })

  render(BeatCell, { props: { beat } })

  expect(screen.getByText('5')).toBeInTheDocument()
})

test('should emit select event when clicked', async () => {
  const beat = createMockBeat()
  const user = userEvent.setup()

  const { component } = render(BeatCell, { props: { beat } })

  const selectPromise = new Promise(resolve => {
    component.$on('select', (e) => resolve(e.detail))
  })

  await user.click(screen.getByRole('button'))

  const selectedBeat = await selectPromise
  expect(selectedBeat).toEqual(beat)
})

test('should show selected state', async () => {
  const beat = createMockBeat()

  const { rerender } = render(BeatCell, {
    props: { beat, selected: false }
  })

  expect(screen.getByRole('button')).not.toHaveClass('selected')

  await rerender({ beat, selected: true })

  expect(screen.getByRole('button')).toHaveClass('selected')
})
```

### 2.2 Test Organization

```
tests/
├── components/           # NEW: Component tests
│   ├── create/
│   │   ├── BeatCell.component.test.ts
│   │   ├── OptionCard.component.test.ts
│   │   └── HandpathBuilder.component.test.ts
│   ├── shared/
│   │   ├── ConfirmDialog.component.test.ts
│   │   └── ThemeToggle.component.test.ts
│   └── explore/
│       └── SearchExplorePanel.component.test.ts
├── unit/                 # Existing unit tests
├── integration/          # Business logic tests
├── e2e/                  # Existing E2E tests
├── factories/            # NEW: Test data factories
├── mocks/                # NEW: MSW handlers
└── setup/                # Test setup files
```

---

## 🎯 Phase 3: E2E Test Hardening (Week 3-4)

### 3.1 Replace Brittle Selectors

**Before (Dinky Car):**
```typescript
await page.locator('.nav-tab-container').filter({ hasText: 'Build' }).click()
await page.waitForTimeout(500) // ❌ Flaky!
```

**After (Rocket Ship):**
```typescript
await page.getByRole('tab', { name: 'Build' }).click()
await page.waitForLoadState('networkidle') // ✅ Reliable!
```

### 3.2 Page Object Model Pattern

**Create reusable page objects:**

```typescript
// tests/e2e/pages/ConstructPage.ts
import { expect, type Page, type Locator } from '@playwright/test'

export class ConstructPage {
  readonly page: Page
  readonly startPositionPicker: Locator
  readonly optionViewer: Locator
  readonly animateButton: Locator
  readonly constructButton: Locator
  readonly clearButton: Locator

  constructor(page: Page) {
    this.page = page
    this.startPositionPicker = page.getByRole('region', { name: 'Start Position' })
    this.optionViewer = page.getByRole('region', { name: 'Options' })
    this.animateButton = page.getByRole('button', { name: 'Animate' })
    this.constructButton = page.getByRole('button', { name: 'Construct' })
    this.clearButton = page.getByRole('button', { name: /clear/i })
  }

  async goto() {
    await this.page.goto('/')
    await this.page.getByRole('tab', { name: 'Build' }).click()
  }

  async selectStartPosition(index: number = 0) {
    const positions = this.startPositionPicker.getByRole('button')
    await positions.nth(index).click()
    await expect(this.optionViewer).toBeVisible()
  }

  async addBeats(count: number) {
    for (let i = 0; i < count; i++) {
      const optionCard = this.optionViewer.getByRole('button').first()
      await optionCard.click()
      // Wait for beat to be added to sequence
      await this.page.waitForFunction(() => {
        return document.querySelectorAll('[data-testid="beat-cell"]').length > i
      })
    }
  }

  async clearSequence() {
    await this.clearButton.click()
    await expect(this.startPositionPicker).toBeVisible()
  }
}

// Usage in test:
import { ConstructPage } from './pages/ConstructPage'

test('Complete Construct Flow', async ({ page }) => {
  const constructPage = new ConstructPage(page)

  await constructPage.goto()
  await constructPage.selectStartPosition()
  await constructPage.addBeats(4)
  await constructPage.animateButton.click()

  await expect(page.getByRole('region', { name: 'Animation' })).toBeVisible()
})
```

### 3.3 Update Playwright Config

```typescript
// tests/config/playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',

  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 4,

  reporter: process.env.CI
    ? [['html'], ['json', { outputFile: 'test-results/results.json' }]]
    : 'list',

  use: {
    baseURL: 'http://localhost:5173',

    // Enable tracing for debugging
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',

    // Accessibility-first testing
    // Automatically wait for elements to be actionable
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
})
```

---

## 🎯 Phase 4: Visual Regression Testing (Week 4)

### 4.1 Setup Visual Testing

```typescript
// tests/e2e/visual/homepage.visual.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Homepage Visual Regression', () => {
  test('should match baseline - desktop', async ({ page }) => {
    await page.goto('/')

    // Wait for animations to complete
    await page.waitForLoadState('networkidle')

    // Take full-page screenshot
    await expect(page).toHaveScreenshot('homepage-desktop.png', {
      fullPage: true,
      threshold: 0.2, // 0.2 = 20% tolerance for anti-aliasing
    })
  })

  test('should match baseline - mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await page.waitForLoadState('networkidle')

    await expect(page).toHaveScreenshot('homepage-mobile.png', {
      fullPage: true,
      threshold: 0.2,
    })
  })

  test('should match BeatCell component', async ({ page }) => {
    await page.goto('/')
    await page.getByRole('tab', { name: 'Build' }).click()

    // Wait for specific component
    const beatCell = page.locator('[data-testid="beat-cell"]').first()
    await beatCell.waitFor()

    // Screenshot specific element
    await expect(beatCell).toHaveScreenshot('beat-cell.png', {
      threshold: 0.1,
    })
  })
})
```

### 4.2 Visual Testing Best Practices

1. **Use consistent environments:** Run visual tests in Docker containers in CI
2. **Set appropriate thresholds:** 0.1-0.2 (10-20%) for anti-aliasing tolerance
3. **Test critical UI components:** Focus on frequently changing areas
4. **Review diffs carefully:** Always validate baseline images before committing

---

## 🎯 Phase 5: CI/CD Optimization (Week 5)

### 5.1 GitHub Actions Workflow with Test Sharding

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  # Fast feedback: Unit & Component tests
  unit-component-tests:
    name: Unit & Component Tests
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/coverage-final.json

      - name: Check coverage thresholds
        run: npm run test:coverage-check

  # E2E tests with sharding
  e2e-tests:
    name: E2E Tests (Shard ${{ matrix.shard }})
    runs-on: ubuntu-latest
    timeout-minutes: 20

    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]
        shardTotal: [4]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps chromium

      - name: Run E2E tests
        run: npm run test:e2e -- --shard=${{ matrix.shard }}/${{ matrix.shardTotal }}

      - name: Upload test results
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-traces-shard-${{ matrix.shard }}
          path: test-results/
          retention-days: 7

  # Visual regression tests
  visual-tests:
    name: Visual Regression Tests
    runs-on: ubuntu-latest
    timeout-minutes: 15
    container:
      image: mcr.microsoft.com/playwright:v1.54.2-jammy

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run visual tests
        run: npm run test:visual

      - name: Upload visual diffs
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: visual-diffs
          path: test-results/
          retention-days: 30
```

### 5.2 Performance Optimization

**Expected Results:**
- Unit tests: <5 seconds
- Component tests: 30-60 seconds
- E2E tests (single shard): ~2-3 minutes
- Full suite (parallel): <5 minutes

**Key Optimizations:**
1. **Test sharding:** Split E2E tests across 4 parallel jobs
2. **Browser caching:** Reuse Playwright browser installations
3. **Dependency caching:** Cache node_modules
4. **Fail-fast strategy:** Stop on first critical failure
5. **Selective test runs:** Only run affected tests on PRs

---

## 🎯 Phase 6: Developer Experience (Week 6)

### 6.1 Custom Vitest Matchers

```typescript
// tests/matchers/custom-matchers.ts
import { expect } from 'vitest'
import type { BeatData } from '$create/workbench/domain/models/BeatData'

interface CustomMatchers<R = unknown> {
  toBeValidBeat: () => R
  toHaveSequenceLength: (length: number) => R
}

declare module 'vitest' {
  interface Assertion<T = any> extends CustomMatchers<T> {}
  interface AsymmetricMatchersContaining extends CustomMatchers {}
}

expect.extend({
  toBeValidBeat(received: BeatData) {
    const pass =
      typeof received.beat_number === 'number' &&
      received.beat_number >= 0 &&
      typeof received.letter === 'string' &&
      received.letter.length === 1

    return {
      pass,
      message: () =>
        pass
          ? `Expected beat to be invalid`
          : `Expected beat to be valid, but got: ${JSON.stringify(received)}`,
    }
  },

  toHaveSequenceLength(received: any, expected: number) {
    const actualLength = received.beats?.length ?? 0
    const pass = actualLength === expected

    return {
      pass,
      message: () =>
        `Expected sequence to have ${expected} beats, but got ${actualLength}`,
      actual: actualLength,
      expected,
    }
  },
})

// Usage:
import { createMockBeat, createMockSequence } from '@tests/factories'
import '@tests/matchers/custom-matchers'

test('should create valid beat', () => {
  const beat = createMockBeat()
  expect(beat).toBeValidBeat()
})

test('should have correct sequence length', () => {
  const sequence = createMockSequence()
  expect(sequence).toHaveSequenceLength(8)
})
```

### 6.2 Test Scripts in package.json

```json
{
  "scripts": {
    "test": "vitest",
    "test:unit": "vitest run tests/unit",
    "test:component": "vitest run tests/components",
    "test:integration": "vitest run tests/integration",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage",
    "test:coverage-check": "vitest run --coverage --coverage.thresholds.autoUpdate=false",

    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:headed": "playwright test --headed",
    "test:visual": "playwright test tests/e2e/visual",
    "test:visual:update": "playwright test tests/e2e/visual --update-snapshots",

    "test:watch": "vitest",
    "test:ci": "vitest run && playwright test",
    "test:all": "npm run test:coverage && npm run test:e2e"
  }
}
```

### 6.3 VS Code Test Extension Configuration

```json
// .vscode/settings.json
{
  "vitest.enable": true,
  "vitest.commandLine": "npm run test",
  "playwright.reuseBrowser": true,
  "playwright.showTrace": true
}
```

---

## 🎯 Phase 7: Accessibility Testing (Week 6)

### 7.1 Setup axe-core Integration

```bash
npm install -D @axe-core/playwright
```

```typescript
// tests/e2e/accessibility/a11y.spec.ts
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test.describe('Accessibility Tests', () => {
  test('should not have accessibility violations on homepage', async ({ page }) => {
    await page.goto('/')

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    expect(results.violations).toEqual([])
  })

  test('should have accessible navigation', async ({ page }) => {
    await page.goto('/')

    // Verify keyboard navigation
    await page.keyboard.press('Tab')
    const firstFocusable = page.locator(':focus')
    await expect(firstFocusable).toBeVisible()

    // Verify ARIA labels
    await expect(page.getByRole('navigation')).toBeVisible()
    await expect(page.getByRole('main')).toBeVisible()
  })

  test('should have accessible form controls', async ({ page }) => {
    await page.goto('/settings')

    const results = await new AxeBuilder({ page })
      .include('[role="dialog"]')
      .analyze()

    expect(results.violations).toEqual([])
  })
})
```

---

## 📚 Testing Best Practices Handbook

### Unit Test Best Practices

1. **Test pure functions first:** They're easiest to test and most valuable
2. **Use AAA pattern:** Arrange, Act, Assert
3. **One assertion per test:** Keep tests focused
4. **Descriptive test names:** `should [expected behavior] when [condition]`
5. **Avoid implementation details:** Test behavior, not internals

### Component Test Best Practices

1. **Test user interactions:** Click, type, navigate
2. **Test visual states:** Loading, error, success
3. **Test props and events:** Input validation and output events
4. **Use data-testid sparingly:** Prefer accessibility selectors
5. **Mock external dependencies:** Use MSW for API calls

### E2E Test Best Practices

1. **Test critical user journeys:** Focus on business value
2. **Use Page Object Model:** Reusable, maintainable test code
3. **Avoid explicit waits:** Use Playwright's auto-waiting
4. **Test across browsers:** Desktop Chrome, Firefox, Safari + Mobile
5. **Enable tracing:** Always capture traces on failure

### General Testing Principles

1. **Fast feedback loop:** Unit tests <5s, component tests <60s
2. **Deterministic tests:** Same input = same output
3. **Independent tests:** No shared state between tests
4. **Readable tests:** Tests are documentation
5. **Maintainable tests:** Follow DRY principle with factories and helpers

---

## 🚀 Implementation Timeline

### Week 1-2: Foundation
- [ ] Configure Vitest browser mode
- [ ] Set up MSW for API mocking
- [ ] Create test factories
- [ ] Configure test coverage with thresholds
- [ ] Update test scripts

### Week 2-3: Component Testing
- [ ] Write 50+ component tests
- [ ] Test all critical UI components
- [ ] Set up component test organization
- [ ] Achieve 80% coverage on components

### Week 3-4: E2E Hardening
- [ ] Refactor E2E tests with accessibility selectors
- [ ] Create Page Object Models
- [ ] Remove all waitForTimeout() calls
- [ ] Add trace capture on failure

### Week 4: Visual Regression
- [ ] Set up visual testing
- [ ] Create baseline screenshots
- [ ] Add visual tests for critical pages
- [ ] Configure visual diff thresholds

### Week 5: CI/CD Optimization
- [ ] Set up GitHub Actions workflow
- [ ] Configure test sharding
- [ ] Add coverage reporting
- [ ] Optimize parallel execution

### Week 6: DX & Accessibility
- [ ] Create custom matchers
- [ ] Add VS Code test integration
- [ ] Set up axe-core testing
- [ ] Document testing patterns

---

## 📊 Success Metrics & KPIs

### Before (Dinky Car)
- ⚠️ Unit tests: ~21
- ⚠️ Component tests: 0
- ⚠️ E2E tests: ~80
- ⚠️ Code coverage: Unknown
- ⚠️ Test execution time: ~5-10 minutes
- ⚠️ Flaky test rate: Unknown (but likely high due to timeouts)
- ⚠️ CI feedback time: Sequential, slow

### After (Rocket Ship)
- ✅ Unit tests: 100-200
- ✅ Component tests: 50-100
- ✅ E2E tests: 10-15 (focused on critical flows)
- ✅ Code coverage: 80%+
- ✅ Test execution time: <2 minutes (parallel)
- ✅ Flaky test rate: <1%
- ✅ CI feedback time: <5 minutes with sharding

### Developer Experience Improvements
- ⚡ Unit test feedback: <5 seconds
- ⚡ Component test feedback: <60 seconds
- 🎯 Test reliability: >99%
- 🔍 Debugging tools: Trace viewer, UI mode
- 📊 Coverage reports: Real-time visibility
- ♿ Accessibility: Automated WCAG compliance checks

---

## 🛠️ Tools & Dependencies

### Required Installations

```bash
# Testing frameworks (already installed)
# @playwright/test: ^1.54.2
# vitest: ^3.2.4

# New dependencies
npm install -D @vitest/browser-playwright
npm install -D @faker-js/faker
npm install -D @axe-core/playwright
npm install -D msw
npm install -D @testing-library/svelte
npm install -D @testing-library/user-event

# Browser installation
npx playwright install chromium firefox webkit
```

### VS Code Extensions (Recommended)

- Vitest (ZixuanChen.vitest-explorer)
- Playwright Test for VSCode (ms-playwright.playwright)
- Test Explorer UI (hbenl.vscode-test-explorer)

---

## 🎓 Learning Resources

### Official Documentation
- [Vitest 3 Guide](https://vitest.dev/guide/)
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [MSW Documentation](https://mswjs.io/docs/)
- [Testing Library](https://testing-library.com/docs/svelte-testing-library/intro)

### 2025 Best Practices
- [Vitest Browser Mode Guide](https://vitest.dev/guide/browser/)
- [Playwright Component Testing](https://playwright.dev/docs/test-components)
- [Visual Regression Testing](https://playwright.dev/docs/test-snapshots)
- [Accessibility Testing Guide](https://playwright.dev/docs/accessibility-testing)

---

## 🚧 Potential Challenges & Solutions

### Challenge 1: Svelte 5 Runes Compatibility
**Problem:** jsdom doesn't support Svelte 5's new reactivity system
**Solution:** Use Vitest browser mode with Playwright provider

### Challenge 2: Firebase Mocking
**Problem:** Complex Firebase API interactions
**Solution:** Use MSW to mock Firestore and Auth at the network level

### Challenge 3: Test Migration Effort
**Problem:** Rewriting 80+ E2E tests takes time
**Solution:** Incremental migration - focus on most flaky tests first

### Challenge 4: CI Performance
**Problem:** Full test suite takes too long
**Solution:** Implement test sharding and parallel execution

### Challenge 5: Learning Curve
**Problem:** Team needs to learn new patterns
**Solution:** Pair programming, documentation, and gradual rollout

---

## ✅ Definition of Done

A test is considered "rocket ship quality" when it:

1. ✅ **Runs fast:** Unit <100ms, Component <1s, E2E <30s
2. ✅ **Is reliable:** Passes 100 times in a row
3. ✅ **Is maintainable:** Uses page objects, factories, and helpers
4. ✅ **Is readable:** Clear test name and structure
5. ✅ **Is independent:** No shared state or order dependencies
6. ✅ **Is valuable:** Tests user-facing behavior
7. ✅ **Is accessible:** Uses getByRole and accessibility selectors

---

## 🎉 Expected Outcomes

After implementing this plan, the TKA Studio testing framework will be:

1. **Fast:** Developer feedback in seconds, not minutes
2. **Reliable:** Flaky tests eliminated through proper waiting and selectors
3. **Comprehensive:** 80%+ code coverage across all layers
4. **Maintainable:** Reusable factories, page objects, and helpers
5. **CI-Optimized:** Parallel execution with test sharding
6. **Accessible:** Automated WCAG compliance testing
7. **Visual:** Screenshot comparison for UI regressions
8. **Developer-Friendly:** Great DX with Vitest UI and Playwright trace viewer

**The testing framework will go from a "dinky car" to a "rocket ship" 🚀**

---

**Document Version:** 1.0
**Last Updated:** January 2025
**Maintained By:** TKA Studio Team
