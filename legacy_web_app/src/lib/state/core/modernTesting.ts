/**
 * Testing utilities for modern state management
 *
 * This module provides utilities for testing state containers and machines
 * in a way that's compatible with both the old and new state management approaches.
 */

import { get, type Readable } from 'svelte/store';
import type { AnyActorRef } from 'xstate';

/**
 * Gets the current state from a container or store
 *
 * @param containerOrStore A state container or Svelte store
 * @returns The current state
 */
export function getState<T>(containerOrStore: { state: T } | Readable<T>): T {
  // If it's a container with a state property
  if ('state' in containerOrStore) {
    return containerOrStore.state;
  }

  // If it's a store with a subscribe method
  if ('subscribe' in containerOrStore) {
    return get(containerOrStore as Readable<T>);
  }

  throw new Error('Invalid container or store');
}

/**
 * Creates a mock container for testing
 *
 * @param initialState The initial state
 * @returns A mock container with the state and a setState method
 */
export function createMockContainer<T extends object>(initialState: T) {
  let state = { ...initialState };

  return {
    get state() { return state; },
    setState: (newState: Partial<T>) => {
      state = { ...state, ...newState };
    },
    reset: () => {
      state = { ...initialState };
    }
  };
}

/**
 * Creates a mock machine container for testing
 *
 * @param initialState The initial machine state
 * @returns A mock machine container
 */
export function createMockMachineContainer<
  TContext extends object,
  TState extends string = string
>(
  initialState: {
    value: TState;
    context: TContext;
    status?: string;
  }
) {
  const state = {
    value: initialState.value,
    context: { ...initialState.context },
    status: initialState.status || 'active'
  };

  const events: { type: string; payload?: any }[] = [];

  return {
    get state() { return state; },
    send: (event: { type: string; [key: string]: any }) => {
      events.push(event);
      return state;
    },
    transition: (newState: TState, contextUpdates: Partial<TContext> = {}) => {
      state.value = newState;
      state.context = { ...state.context, ...contextUpdates };
    },
    getEvents: () => [...events],
    clearEvents: () => {
      events.length = 0;
    },
    reset: () => {
      state.value = initialState.value;
      state.context = { ...initialState.context };
      state.status = initialState.status || 'active';
      events.length = 0;
    }
  };
}

/**
 * Waits for a condition to be true
 *
 * @param condition A function that returns a boolean
 * @param timeout Maximum time to wait in milliseconds
 * @returns A promise that resolves when the condition is true
 */
export async function waitFor(
  condition: () => boolean,
  timeout = 1000,
  interval = 50
): Promise<void> {
  const startTime = Date.now();

  while (!condition()) {
    if (Date.now() - startTime > timeout) {
      throw new Error(`Timeout waiting for condition after ${timeout}ms`);
    }

    await new Promise(resolve => setTimeout(resolve, interval));
  }
}

/**
 * Waits for a specific state value in a machine container
 *
 * @param container A machine container
 * @param stateValue The state value to wait for
 * @param timeout Maximum time to wait in milliseconds
 * @returns A promise that resolves when the machine is in the specified state
 */
export async function waitForState<T extends string>(
  container: { state: { value: any } } | AnyActorRef,
  stateValue: T,
  timeout = 1000
): Promise<void> {
  const getStateValue = () => {
    if ('getSnapshot' in container) {
      return container.getSnapshot().value;
    }
    return container.state.value;
  };

  return waitFor(() => getStateValue() === stateValue, timeout);
}

/**
 * Creates a test harness for a container
 *
 * @param container A state container
 * @returns A test harness with utilities for testing the container
 */
export function createContainerTestHarness<T extends object, A extends Record<string, Function>>(
  container: { state: T } & A
) {
  const stateHistory: T[] = [{ ...container.state }];

  // Track state changes
  const unsubscribe = 'subscribe' in container
    ? (container as any).subscribe((state: T) => {
        stateHistory.push({ ...state });
      })
    : setInterval(() => {
        const currentState = { ...container.state };
        const lastState = stateHistory[stateHistory.length - 1];

        // Only add to history if state has changed
        if (JSON.stringify(currentState) !== JSON.stringify(lastState)) {
          stateHistory.push(currentState);
        }
      }, 50);

  return {
    getState: () => container.state,
    getHistory: () => [...stateHistory],
    getLastState: () => stateHistory[stateHistory.length - 1],
    cleanup: () => {
      if (typeof unsubscribe === 'function') {
        unsubscribe();
      } else {
        clearInterval(unsubscribe);
      }
    }
  };
}
