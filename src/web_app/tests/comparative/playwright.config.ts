import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright Configuration for Start Position Picker Comparative Tests
 * 
 * Optimized configuration for running comparative tests between legacy and modern
 * web applications with appropriate timeouts, parallelization, and reporting.
 */

export default defineConfig({
  // Test directory
  testDir: '.',
  
  // Test file patterns
  testMatch: ['**/*.test.ts'],
  
  // Global test timeout
  timeout: 120000, // 2 minutes per test (allows for dual app navigation)
  
  // Expect timeout for assertions
  expect: {
    timeout: 10000 // 10 seconds for assertions
  },
  
  // Test execution settings
  fullyParallel: false, // Sequential execution to avoid resource conflicts
  forbidOnly: !!process.env.CI, // Fail if test.only is committed
  retries: process.env.CI ? 2 : 1, // Retry failed tests in CI
  workers: process.env.CI ? 1 : 2, // Limited workers to manage browser contexts
  
  // Reporter configuration
  reporter: [
    ['html', { 
      outputFolder: './test-results/html-report',
      open: process.env.CI ? 'never' : 'on-failure'
    }],
    ['json', { 
      outputFile: './test-results/results.json' 
    }],
    ['junit', { 
      outputFile: './test-results/junit.xml' 
    }],
    ['list'], // Console output
    ...(process.env.CI ? [] : [['line']]) // Detailed line output for local development
  ],
  
  // Global test setup
  globalSetup: './setup/global-setup.ts',
  globalTeardown: './setup/global-teardown.ts',
  
  // Output directory for test artifacts
  outputDir: './test-results/artifacts',
  
  // Use configuration
  use: {
    // Base URL (will be overridden per test)
    baseURL: 'http://localhost:5173',
    
    // Browser settings
    headless: process.env.CI ? true : false,
    viewport: { width: 1280, height: 720 },
    
    // Action timeouts
    actionTimeout: 15000, // 15 seconds for actions
    navigationTimeout: 30000, // 30 seconds for navigation
    
    // Screenshots and videos
    screenshot: {
      mode: 'only-on-failure',
      fullPage: true
    },
    video: {
      mode: 'retain-on-failure',
      size: { width: 1280, height: 720 }
    },
    
    // Trace collection
    trace: {
      mode: 'retain-on-failure',
      screenshots: true,
      snapshots: true,
      sources: true
    },
    
    // Context options
    ignoreHTTPSErrors: true,
    
    // Locale and timezone
    locale: 'en-US',
    timezoneId: 'America/New_York'
  },

  // Project configurations for different browsers and scenarios
  projects: [
    {
      name: 'comparative-chromium',
      use: { 
        ...devices['Desktop Chrome'],
        // Increased context timeout for dual app testing
        contextOptions: {
          // Allow multiple contexts for legacy/modern app comparison
          // Each test will create separate contexts
        }
      },
      testMatch: ['start-position-picker-comparison.test.ts']
    },
    
    {
      name: 'comparative-firefox',
      use: { 
        ...devices['Desktop Firefox']
      },
      testMatch: ['start-position-picker-comparison.test.ts']
    },
    
    {
      name: 'comparative-webkit',
      use: { 
        ...devices['Desktop Safari']
      },
      testMatch: ['start-position-picker-comparison.test.ts']
    },
    
    // Mobile testing (optional)
    {
      name: 'comparative-mobile-chrome',
      use: { 
        ...devices['Pixel 5']
      },
      testMatch: ['start-position-picker-comparison.test.ts'],
      // Only run mobile tests if explicitly requested
      testIgnore: process.env.MOBILE_TESTS ? [] : ['**/*']
    }
  ],

  // Web server configuration
  webServer: [
    {
      command: 'npm run dev',
      cwd: '../../legacy_web',
      port: 5173,
      timeout: 60000,
      reuseExistingServer: !process.env.CI,
      stdout: 'pipe',
      stderr: 'pipe',
      env: {
        NODE_ENV: 'test'
      }
    },
    {
      command: 'npm run dev',
      cwd: '../../modern_web',
      port: 5177,
      timeout: 60000,
      reuseExistingServer: !process.env.CI,
      stdout: 'pipe',
      stderr: 'pipe',
      env: {
        NODE_ENV: 'test'
      }
    }
  ],

  // Test metadata
  metadata: {
    testType: 'comparative',
    purpose: 'Start Position Picker Validation',
    applications: ['legacy_web', 'modern_web'],
    gridModes: ['diamond', 'box'],
    positions: [
      'alpha1_alpha1', 'beta5_beta5', 'gamma11_gamma11', // Diamond
      'alpha2_alpha2', 'beta4_beta4', 'gamma12_gamma12'  // Box
    ]
  }
});

// Environment-specific overrides
if (process.env.TEST_ENV === 'ci') {
  // CI-specific optimizations
  module.exports.use.headless = true;
  module.exports.use.screenshot = { mode: 'off' };
  module.exports.use.video = { mode: 'off' };
  module.exports.use.trace = { mode: 'off' };
  module.exports.workers = 1;
  module.exports.retries = 3;
}

if (process.env.TEST_ENV === 'production') {
  // Production validation settings
  module.exports.timeout = 180000; // 3 minutes for production
  module.exports.use.actionTimeout = 20000;
  module.exports.use.navigationTimeout = 45000;
  module.exports.retries = 0; // No retries in production validation
}

if (process.env.TEST_ENV === 'development') {
  // Development settings for debugging
  module.exports.use.headless = false;
  module.exports.use.screenshot = { mode: 'on' };
  module.exports.use.video = { mode: 'on' };
  module.exports.use.trace = { mode: 'on' };
  module.exports.workers = 1; // Sequential for easier debugging
}
