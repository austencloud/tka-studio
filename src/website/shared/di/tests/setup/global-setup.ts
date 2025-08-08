/**
 * 🧪 GLOBAL TEST SETUP
 *
 * Global configuration and setup for TKA DI tests,
 * ensuring consistent test environment and utilities.
 */

import { beforeAll, afterAll, beforeEach, afterEach } from 'vitest';

// Global test configuration
declare global {
  var __TKA_DI_TEST_MODE__: boolean;
  var __TKA_DI_DEBUG__: boolean;
  var gc: (() => void) | undefined;
}

// Set global test flags
globalThis.__TKA_DI_TEST_MODE__ = true;
globalThis.__TKA_DI_DEBUG__ = true;

// Performance monitoring
interface PerformanceMemory {
  usedJSHeapSize: number;
  totalJSHeapSize: number;
  jsHeapSizeLimit: number;
}

declare global {
  interface Performance {
    memory?: PerformanceMemory;
  }
}

// Test utilities
export class TestUtils {
  static async waitForNextTick(): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, 0));
  }

  static async waitFor(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  static generateRandomId(): string {
    return `test_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  static measurePerformance<T>(fn: () => T): { result: T; duration: number } {
    const start = performance.now();
    const result = fn();
    const duration = performance.now() - start;
    return { result, duration };
  }

  static async measureAsyncPerformance<T>(fn: () => Promise<T>): Promise<{ result: T; duration: number }> {
    const start = performance.now();
    const result = await fn();
    const duration = performance.now() - start;
    return { result, duration };
  }

  static getMemoryUsage(): number {
    if (typeof performance !== 'undefined' && performance.memory) {
      return performance.memory.usedJSHeapSize;
    }
    return 0;
  }

  static forceGarbageCollection(): void {
    if (typeof globalThis.gc === 'function') {
      globalThis.gc();
    }
  }
}

// Global test state
let testStartTime: number;
let testMemoryStart: number;

// Global setup
beforeAll(() => {
  console.log('🧪 Starting TKA DI Test Suite');
  console.log('📊 Test Environment:', {
    nodeVersion: typeof process !== 'undefined' ? process.version : 'N/A',
    platform: typeof process !== 'undefined' ? process.platform : 'browser',
    testMode: globalThis.__TKA_DI_TEST_MODE__,
    debugMode: globalThis.__TKA_DI_DEBUG__
  });

  testStartTime = performance.now();
  testMemoryStart = TestUtils.getMemoryUsage();
});

// Global cleanup
afterAll(() => {
  const testDuration = performance.now() - testStartTime;
  const memoryEnd = TestUtils.getMemoryUsage();
  const memoryDelta = memoryEnd - testMemoryStart;

  console.log('✅ TKA DI Test Suite Completed');
  console.log('📊 Test Summary:', {
    duration: `${testDuration.toFixed(2)}ms`,
    memoryDelta: `${(memoryDelta / 1024 / 1024).toFixed(2)}MB`,
    finalMemory: `${(memoryEnd / 1024 / 1024).toFixed(2)}MB`
  });

  // Force garbage collection at the end
  TestUtils.forceGarbageCollection();
});

// Per-test setup
beforeEach(() => {
  // Reset any global state if needed
  TestUtils.forceGarbageCollection();
});

// Per-test cleanup
afterEach(() => {
  // Cleanup after each test
  TestUtils.forceGarbageCollection();
});

// Error handling
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
});

// Export utilities for use in tests
export { TestUtils };

// Mock console methods for testing if needed
export const mockConsole = {
  log: vi.fn(),
  warn: vi.fn(),
  error: vi.fn(),
  debug: vi.fn(),
  info: vi.fn()
};

// Test data factories
export class TestDataFactory {
  static createMockService(name: string = 'MockService') {
    return class MockService {
      readonly name = name;
      readonly id = TestUtils.generateRandomId();
      readonly createdAt = new Date();

      getValue(): string {
        return `${this.name}-${this.id}`;
      }

      dispose(): void {
        // Mock disposal
      }
    };
  }

  static createMockServiceInterface(name: string) {
    return {
      name,
      symbol: Symbol(name),
      type: this.createMockService(name),
      metadata: {
        description: `Mock service interface for ${name}`,
        version: '1.0.0',
        tags: ['test', 'mock']
      }
    };
  }

  static createMockContainer() {
    const services = new Map();

    return {
      register: (name: string, service: any) => services.set(name, service),
      resolve: (name: string) => services.get(name),
      isRegistered: (name: string) => services.has(name),
      clear: () => services.clear(),
      size: () => services.size
    };
  }
}

// Performance benchmarking utilities
export class BenchmarkUtils {
  static async benchmark(
    name: string,
    fn: () => void | Promise<void>,
    iterations: number = 1000
  ): Promise<{
    name: string;
    iterations: number;
    totalTime: number;
    averageTime: number;
    minTime: number;
    maxTime: number;
  }> {
    const times: number[] = [];

    for (let i = 0; i < iterations; i++) {
      const start = performance.now();
      await fn();
      const end = performance.now();
      times.push(end - start);
    }

    const totalTime = times.reduce((sum, time) => sum + time, 0);
    const averageTime = totalTime / iterations;
    const minTime = Math.min(...times);
    const maxTime = Math.max(...times);

    const result = {
      name,
      iterations,
      totalTime,
      averageTime,
      minTime,
      maxTime
    };

    console.log(`📊 Benchmark: ${name}`, {
      iterations,
      average: `${averageTime.toFixed(4)}ms`,
      min: `${minTime.toFixed(4)}ms`,
      max: `${maxTime.toFixed(4)}ms`,
      total: `${totalTime.toFixed(2)}ms`
    });

    return result;
  }

  static comparePerformance(
    baseline: { averageTime: number },
    current: { averageTime: number }
  ): {
    improvement: number;
    degradation: number;
    percentChange: number;
  } {
    const improvement = baseline.averageTime - current.averageTime;
    const degradation = current.averageTime - baseline.averageTime;
    const percentChange = ((current.averageTime - baseline.averageTime) / baseline.averageTime) * 100;

    return {
      improvement: Math.max(0, improvement),
      degradation: Math.max(0, degradation),
      percentChange
    };
  }
}

// Test assertion helpers
export class TestAssertions {
  static assertPerformance(actualTime: number, expectedMaxTime: number, operation: string): void {
    if (actualTime > expectedMaxTime) {
      throw new Error(
        `Performance assertion failed: ${operation} took ${actualTime.toFixed(4)}ms, ` +
        `expected less than ${expectedMaxTime}ms`
      );
    }
  }

  static assertMemoryUsage(actualMemory: number, expectedMaxMemory: number, operation: string): void {
    if (actualMemory > expectedMaxMemory) {
      throw new Error(
        `Memory assertion failed: ${operation} used ${(actualMemory / 1024 / 1024).toFixed(2)}MB, ` +
        `expected less than ${(expectedMaxMemory / 1024 / 1024).toFixed(2)}MB`
      );
    }
  }

  static assertNoMemoryLeak(beforeMemory: number, afterMemory: number, tolerance: number = 1024 * 1024): void {
    const memoryGrowth = afterMemory - beforeMemory;
    if (memoryGrowth > tolerance) {
      throw new Error(
        `Memory leak detected: ${(memoryGrowth / 1024 / 1024).toFixed(2)}MB growth, ` +
        `tolerance: ${(tolerance / 1024 / 1024).toFixed(2)}MB`
      );
    }
  }
}

console.log('🔧 Global test setup completed');
