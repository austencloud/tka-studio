/**
 * Common setup for integration tests
 */
import { beforeEach, afterEach, vi } from 'vitest';
import { resetAllState } from '../../core/testing';

export function setupIntegrationTests() {
  beforeEach(() => {
    vi.resetAllMocks();
    vi.useFakeTimers();
    // Mock localStorage
    vi.stubGlobal('localStorage', {
      getItem: vi.fn(),
      setItem: vi.fn(),
      removeItem: vi.fn(),
      clear: vi.fn()
    });

    // Reset all state before each test
    resetAllState();
  });

  afterEach(() => {
    // Clean up after each test
    vi.useRealTimers();
    vi.restoreAllMocks();
  });
}
