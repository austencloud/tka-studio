/**
 * Tests for state synchronization between different state containers
 */
import { describe, it, expect } from 'vitest';
import { get } from 'svelte/store';
import { createMachine, assign } from 'xstate';
import { stateRegistry } from '../../core/registry';
import { createStore } from '../../core/store';
import { setupIntegrationTests } from './setup';

describe('State Synchronization', () => {
  setupIntegrationTests();

  it('synchronizes related stores through derived selectors', () => {
    // Create two related stores
    const sourceStore = createStore<{ count: number }, { increment: () => void }>(
      'sourceStore',
      { count: 0 },
      (set, update) => ({
        increment: () => update((state) => ({ count: state.count + 1 }))
      })
    );

    const derivedStore = createStore<
      { doubledCount: number },
      { setDoubledCount: (value: number) => void }
    >('derivedStore', { doubledCount: 0 }, (set) => ({
      setDoubledCount: (value: number) => set({ doubledCount: value })
    }));

    // Set up synchronization
    const unsubscribe = sourceStore.subscribe((state) => {
      derivedStore.setDoubledCount(state.count * 2);
    });

    // Trigger an update in the source store
    sourceStore.increment();

    // Check that the derived store was updated
    expect(get(derivedStore).doubledCount).toBe(2);

    // Update again
    sourceStore.increment();

    // Check synchronization
    expect(get(derivedStore).doubledCount).toBe(4);

    // Clean up
    unsubscribe();
  });

  it('synchronizes machine state with multiple dependent stores', async () => {
    interface AppContext {
      data: Record<string, any> | null;
      error: string | null;
      isLoading: boolean;
    }

    interface LoadedEvent {
      type: 'LOADED';
      data: Record<string, any>;
    }

    interface ErrorEvent {
      type: 'ERROR';
      message: string;
    }

    interface UpdateEvent {
      type: 'UPDATE';
      updates: Record<string, any>;
    }

    type AppEvent =
      | LoadedEvent
      | ErrorEvent
      | UpdateEvent
      | { type: 'RELOAD' }
      | { type: 'RETRY' };

    // Create a machine that tracks application state
    const appStateMachine = createMachine({
      id: 'appState',
      initial: 'loading',
      context: {
        data: null,
        error: null,
        isLoading: true
      },
      types: {} as {
        context: AppContext;
        events: AppEvent;
      },
      states: {
        loading: {
          on: {
            LOADED: {
              target: 'ready',
              actions: assign({
                data: ({ event }) => event.data,
                isLoading: false
              })
            },
            ERROR: {
              target: 'error',
              actions: assign({
                error: ({ event }) => event.message,
                isLoading: false
              })
            }
          }
        },
        ready: {
          on: {
            UPDATE: {
              actions: assign({
                data: ({ event, context }) => ({ ...context.data, ...event.updates })
              })
            },
            RELOAD: {
              target: 'loading',
              actions: assign({ isLoading: true })
            }
          }
        },
        error: {
          on: {
            RETRY: {
              target: 'loading',
              actions: assign({
                error: null,
                isLoading: true
              })
            }
          }
        }
      }
    });

    // Register the machine
    const appActor = stateRegistry.registerMachine('appState', appStateMachine);

    // Create dependent stores
    const loadingStore = createStore<
      { isLoading: boolean },
      { setLoading: (isLoading: boolean) => void }
    >('loadingStore', { isLoading: true }, (set) => ({
      setLoading: (isLoading: boolean) => set({ isLoading })
    }));

    const dataStore = createStore<
      { currentData: Record<string, any> | null },
      { setData: (data: Record<string, any>) => void }
    >('dataStore', { currentData: null }, (set) => ({
      setData: (data: Record<string, any>) => set({ currentData: data })
    }));

    const errorStore = createStore<
      { currentError: string | null },
      { setError: (error: string | null) => void }
    >('errorStore', { currentError: null }, (set) => ({
      setError: (error: string | null) => set({ currentError: error })
    }));

    // Set up synchronization
    const subscription = appActor.subscribe((state) => {
      loadingStore.setLoading(state.context.isLoading);

      if (state.context.data) {
        dataStore.setData(state.context.data);
      }

      if (state.context.error) {
        errorStore.setError(state.context.error);
      } else {
        errorStore.setError(null);
      }
    });

    // Simulate loading completion
    appActor.send({
      type: 'LOADED',
      data: { id: 123, name: 'Test Item' }
    });

    // Check store synchronization
    expect(get(loadingStore).isLoading).toBe(false);
    expect(get(dataStore).currentData).toEqual({ id: 123, name: 'Test Item' });
    expect(get(errorStore).currentError).toBeNull();

    // Simulate an error
    appActor.send({
      type: 'RELOAD'
    });

    appActor.send({
      type: 'ERROR',
      message: 'Failed to load data'
    });

    // Check error state synchronization
    expect(get(loadingStore).isLoading).toBe(false);
    expect(get(errorStore).currentError).toBe('Failed to load data');

    // Clean up
    subscription.unsubscribe();
  });
});
