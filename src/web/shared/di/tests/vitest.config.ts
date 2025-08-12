/**
 * 🧪 VITEST CONFIGURATION FOR TKA DI TESTS
 * 
 * Comprehensive test configuration for the TKA Enterprise DI system,
 * optimized for performance, coverage, and reliability.
 */

import { defineConfig } from 'vitest/config';
import { resolve } from 'path';

export default defineConfig({
  test: {
    // Test Environment
    environment: 'jsdom', // For browser-like environment
    globals: true, // Enable global test functions
    
    // Test Discovery
    include: [
      '**/*.test.ts',
      '**/*.spec.ts'
    ],
    exclude: [
      '**/node_modules/**',
      '**/dist/**',
      '**/build/**'
    ],

    // Test Execution
    testTimeout: 10000, // 10 seconds for complex DI tests
    hookTimeout: 5000,  // 5 seconds for setup/teardown
    teardownTimeout: 5000,
    
    // Parallel Execution
    threads: true,
    maxThreads: 4,
    minThreads: 1,
    
    // Coverage Configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      reportsDirectory: './coverage',
      
      // Coverage Thresholds (Enterprise Standards)
      thresholds: {
        global: {
          branches: 90,
          functions: 95,
          lines: 95,
          statements: 95
        }
      },
      
      // Include/Exclude Patterns
      include: [
        'src/web/shared/di/**/*.ts'
      ],
      exclude: [
        '**/*.test.ts',
        '**/*.spec.ts',
        '**/tests/**',
        '**/examples/**',
        '**/node_modules/**'
      ]
    },

    // Reporting
    reporter: [
      'verbose',
      'json',
      'html'
    ],
    outputFile: {
      json: './test-results/results.json',
      html: './test-results/report.html'
    },

    // Performance Monitoring
    benchmark: {
      include: ['**/*.bench.ts'],
      exclude: ['**/node_modules/**']
    },

    // Mock Configuration
    clearMocks: true,
    restoreMocks: true,
    mockReset: true,

    // Setup Files
    setupFiles: [
      './tests/setup/global-setup.ts'
    ],

    // Watch Mode
    watch: false, // Disable for CI
    
    // Retry Configuration
    retry: 2, // Retry flaky tests
    
    // Isolation
    isolate: true, // Run each test file in isolation
    
    // Pool Options
    pool: 'threads',
    poolOptions: {
      threads: {
        singleThread: false,
        isolate: true
      }
    }
  },

  // Resolve Configuration
  resolve: {
    alias: {
      '@tka/di': resolve(__dirname, '../index.ts'),
      '@tka/di/core': resolve(__dirname, '../core'),
      '@tka/di/testing': resolve(__dirname, '../testing'),
      '@tka/di/examples': resolve(__dirname, '../examples')
    }
  },

  // Build Configuration for Tests
  esbuild: {
    target: 'es2020'
  },

  // Define Global Constants
  define: {
    __TEST_ENV__: true,
    __DI_DEBUG__: true
  }
});
