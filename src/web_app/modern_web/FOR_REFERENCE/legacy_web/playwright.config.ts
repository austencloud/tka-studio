import { defineConfig, devices } from "@playwright/test";

/**
 * Playwright configuration for The Kinetic Constructor
 *
 * This configuration is designed to work alongside the existing Vitest setup
 * and focuses on end-to-end testing of the application's visual components
 * and user flows.
 */
export default defineConfig({
  // Test directory structure
  testDir: "./e2e",

  // File pattern for test files
  testMatch: "**/*.spec.ts",

  // Maximum time one test can run for (increased to 60 seconds for more stability)
  timeout: 60 * 1000,

  // Run tests in files in parallel
  fullyParallel: true,

  // Slow down test execution to improve stability
  expect: {
    timeout: 10000, // Increase timeout for expect assertions
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.05, // Allow 5% difference in screenshots
    },
  },

  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,

  // Retry on CI only
  retries: process.env.CI ? 2 : 0,

  // Opt out of parallel tests on CI
  workers: process.env.CI ? 1 : undefined,

  // Reporter to use
  reporter: [["html", { open: "never" }], ["list"]],

  // Shared settings for all projects
  use: {
    // Base URL to use in actions like `await page.goto('/')`
    baseURL: "http://localhost:5175",

    // Collect trace when retrying the failed test
    trace: "on-first-retry",

    // Take screenshot on test failure
    screenshot: "only-on-failure",

    // Record video for visual tests
    video: "on-first-retry",

    // Improve stability with longer timeouts
    navigationTimeout: 30000,
    actionTimeout: 15000,

    // Viewport size
    viewport: { width: 1280, height: 800 },

    // Improve stability by slowing down actions
    launchOptions: {
      slowMo: 100, // Slow down each action by 100ms
    },
  },

  // Configure projects for different browsers
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
    // Mobile viewports
    {
      name: "mobile-chrome",
      use: { ...devices["Pixel 5"] },
    },
    {
      name: "mobile-safari",
      use: { ...devices["iPhone 12"] },
    },
    // Visual testing project
    {
      name: "visual-tests",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 1280, height: 720 },
      },
      testMatch: "**/*.visual.spec.ts",
    },
  ],

  // Local development server setup
  webServer: {
    command: "npm run dev",
    port: 5175,
    reuseExistingServer: !process.env.CI,
    stdout: "pipe",
    stderr: "pipe",
  },
});
