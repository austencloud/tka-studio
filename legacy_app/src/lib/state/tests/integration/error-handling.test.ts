/**
 * Tests for error propagation and recovery
 */
import { describe, it, expect, vi } from 'vitest';
import { get } from 'svelte/store';
import { stateRegistry } from '../../core/registry';
import { createStore, createPersistentStore } from '../../core/store';
import { setupIntegrationTests } from './setup';

describe('Error Propagation and Recovery', () => {
  setupIntegrationTests();

  it('handles errors in one store without breaking others', () => {
    // Create a store that will throw an error
    const erroringStore = createStore<
      { count: number },
      { increment: () => void; triggerError: () => void }
    >('erroringStore', { count: 0 }, (set, update) => ({
      increment: () => update((state) => ({ count: state.count + 1 })),
      triggerError: () => {
        throw new Error('Test error');
      }
    }));

    // Create a dependent store
    const dependentStore = createStore<
      { sourceCount: number },
      { updateFromSource: (count: number) => void }
    >('dependentStore', { sourceCount: 0 }, (set) => ({
      updateFromSource: (count: number) => set({ sourceCount: count })
    }));

    // Set up synchronization
    const unsubscribe = erroringStore.subscribe((state) => {
      // This should continue to work even after errors
      dependentStore.updateFromSource(state.count);
    });

    // Normal operation
    erroringStore.increment();
    expect(get(dependentStore).sourceCount).toBe(1);

    // Trigger error but catch it
    expect(() => erroringStore.triggerError()).toThrow();

    // Store should still function after error
    erroringStore.increment();
    expect(get(erroringStore).count).toBe(2);
    expect(get(dependentStore).sourceCount).toBe(2);

    // Clean up
    unsubscribe();
  });

  it('recovers from persistence errors without data loss', () => {
    // Mock localStorage to simulate errors
    let shouldThrow = false;
    const mockSetItem = vi.fn((key, value) => {
      if (shouldThrow) {
        throw new DOMException('Quota exceeded', 'QuotaExceededError');
      }
    });

    vi.stubGlobal('localStorage', {
      getItem: vi.fn(),
      setItem: mockSetItem,
      removeItem: vi.fn(),
      clear: vi.fn()
    });

    interface PersistentData {
      important: string;
      nonEssential: string;
    }

    // Create a persistent store
    const persistentStore = createPersistentStore<PersistentData>(
      'persistentTestStore',
      {
        important: 'critical data',
        nonEssential: 'extra data'
      },
      {
        // Prioritize important fields
        persistFields: ['important']
      }
    );

    // Update the store normally
    persistentStore.update((state) => ({
      ...state,
      important: 'updated critical data',
      nonEssential: 'updated extra data'
    }));

    // Run timers to trigger debounced persistence
    vi.runAllTimers();

    // Verify persistence happened
    expect(mockSetItem).toHaveBeenCalled();

    // Now simulate quota exceeded error
    shouldThrow = true;

    // The next update should handle the error gracefully
    persistentStore.update((state) => ({
      ...state,
      important: 'newer critical data'
    }));

    // Run timers
    vi.runAllTimers();

    // Store should still have the updated data in memory even if persistence failed
    expect(get(persistentStore)).toEqual({
      important: 'newer critical data',
      nonEssential: 'updated extra data'
    });
  });
});
