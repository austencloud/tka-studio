/**
 * Tests for communication between machines and stores
 */
import { describe, it, expect } from 'vitest';
import { get } from 'svelte/store';
import { createMachine, assign } from 'xstate';
import { stateRegistry } from '../../core/registry';
import { createStore } from '../../core/store';
import { setupIntegrationTests } from './setup';

describe('Machine-to-Store Communication', () => {
  setupIntegrationTests();

  it('updates stores when machines dispatch events', async () => {
    // Create a test store that will be updated by the machine
    const testStore = createStore('testStore', { value: 0 }, (set) => ({
      setValue: (value: number) => set({ value })
    }));

    // Create a test machine that will update the store
    const testMachine = createMachine(
      {
        id: 'testMachine',
        initial: 'idle',
        context: { value: 0 },
        states: {
          idle: {
            on: { INCREMENT: { actions: 'incrementValue' } }
          }
        }
      },
      {
        actions: {
          incrementValue: assign({
            value: ({ context }) => context.value + 1
          })
        }
      }
    );

    // Register the machine with the registry
    const actor = stateRegistry.registerMachine('testMachine', testMachine);

    // Set up an effect to sync the machine state with the store
    const subscription = actor.subscribe((state) => {
      testStore.setValue(state.context.value);
    });

    // Trigger an event on the machine
    actor.send({ type: 'INCREMENT' });

    // Check that the store was updated
    expect(get(testStore).value).toBe(1);

    // Send another event
    actor.send({ type: 'INCREMENT' });

    // Check that the store was updated again
    expect(get(testStore).value).toBe(2);

    // Clean up
    subscription.unsubscribe();
  });

  it('updates machines when stores change', async () => {
    // Create a test store
    const testStore = createStore<
      { command: string | null },
      { setCommand: (command: string) => void }
    >('controlStore', { command: null }, (set) => ({
      setCommand: (command: string) => set({ command })
    }));

    // Create a test machine that will react to store changes
    const testMachine = createMachine({
      id: 'reactingMachine',
      initial: 'idle',
      context: { lastCommand: null as string | null },
      types: {} as {
        context: { lastCommand: string | null };
        events: { type: 'STORE_UPDATED'; command: string };
      },
      states: {
        idle: {
          on: {
            STORE_UPDATED: {
              actions: assign({
                lastCommand: ({ event }) => event.command
              })
            }
          }
        }
      }
    });

    // Register the machine with the registry
    const actor = stateRegistry.registerMachine('reactingMachine', testMachine);

    // Set up an effect to send store updates to the machine
    const unsubscribe = testStore.subscribe((state) => {
      if (state.command) {
        actor.send({ type: 'STORE_UPDATED', command: state.command });
      }
    });

    // Update the store
    testStore.setCommand('test-command');

    // Check that the machine received the update
    expect(actor.getSnapshot().context.lastCommand).toBe('test-command');

    // Clean up
    unsubscribe();
  });
});
