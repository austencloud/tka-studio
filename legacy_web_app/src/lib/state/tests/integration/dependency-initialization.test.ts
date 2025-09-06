/**
 * Tests for dependency-aware initialization
 */
import { describe, it, expect } from 'vitest';
import { get } from 'svelte/store';
import { stateRegistry } from '../../core/registry';
import { createStore } from '../../core/store';
import { setupIntegrationTests } from './setup';

describe('Dependency-Aware Initialization', () => {
  setupIntegrationTests();

  it('initializes state containers in the correct order based on dependencies', () => {
    const initOrder: string[] = [];

    // Create stores with dependencies
    const baseStore = createStore<{ isInitialized: boolean }, { initialize: () => void }>(
      'baseStore',
      { isInitialized: false },
      (set) => ({
        initialize: () => {
          initOrder.push('baseStore');
          set({ isInitialized: true });
        }
      })
    );

    const dependentStore1 = createStore<{ isInitialized: boolean }, { initialize: () => void }>(
      'dependentStore1',
      { isInitialized: false },
      (set) => ({
        initialize: () => {
          // Should only initialize after baseStore
          if (get(baseStore).isInitialized) {
            initOrder.push('dependentStore1');
            set({ isInitialized: true });
          }
        }
      })
    );

    const dependentStore2 = createStore<{ isInitialized: boolean }, { initialize: () => void }>(
      'dependentStore2',
      { isInitialized: false },
      (set) => ({
        initialize: () => {
          // Should only initialize after dependentStore1
          if (get(dependentStore1).isInitialized) {
            initOrder.push('dependentStore2');
            set({ isInitialized: true });
          }
        }
      })
    );

    // Register dependencies
    stateRegistry.addDependency('dependentStore1', 'baseStore');
    stateRegistry.addDependency('dependentStore2', 'dependentStore1');

    // Get initialization order
    const orderFromRegistry = stateRegistry.getInitializationOrder();

    // Verify order includes all stores
    expect(orderFromRegistry).toContain('baseStore');
    expect(orderFromRegistry).toContain('dependentStore1');
    expect(orderFromRegistry).toContain('dependentStore2');

    // Verify order is correct
    const baseIndex = orderFromRegistry.indexOf('baseStore');
    const dep1Index = orderFromRegistry.indexOf('dependentStore1');
    const dep2Index = orderFromRegistry.indexOf('dependentStore2');

    expect(baseIndex).toBeLessThan(dep1Index);
    expect(dep1Index).toBeLessThan(dep2Index);

    // Simulate initialization in registry order
    orderFromRegistry.forEach((id) => {
      // Call each store's initialize method
      switch (id) {
        case 'baseStore':
          baseStore.initialize();
          break;
        case 'dependentStore1':
          dependentStore1.initialize();
          break;
        case 'dependentStore2':
          dependentStore2.initialize();
          break;
      }
    });

    // Verify all stores were initialized
    expect(get(baseStore).isInitialized).toBe(true);
    expect(get(dependentStore1).isInitialized).toBe(true);
    expect(get(dependentStore2).isInitialized).toBe(true);

    // Verify initialization order was correct
    expect(initOrder).toEqual(['baseStore', 'dependentStore1', 'dependentStore2']);
  });
});
