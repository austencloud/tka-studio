/**
 * State Management Testing Utilities
 *
 * Provides utilities for testing state management components.
 */

import { get, type Readable } from 'svelte/store';
import { stateRegistry } from './registry';
import type { AnyActorRef } from 'xstate';

/**
 * Reset all state containers in the registry
 *
 * This is useful for resetting the application state between tests.
 */
export function resetAllState(): void {
	// Clear the registry
	stateRegistry.clear();
}

/**
 * Get the current value of a store
 *
 * @param store The store to get the value from
 * @returns The current value of the store
 */
export function getStoreValue<T>(store: Readable<T>): T {
	return get(store);
}

/**
 * Wait for a store to match a predicate
 *
 * @param store The store to watch
 * @param predicate A function that returns true when the desired state is reached
 * @param timeout Maximum time to wait in milliseconds
 * @returns A promise that resolves when the predicate returns true
 */
export function waitForStore<T>(
	store: Readable<T>,
	predicate: (value: T) => boolean,
	timeout = 5000
): Promise<T> {
	return new Promise((resolve, reject) => {
		// Check if the store already matches the predicate
		const initialValue = get(store);
		if (predicate(initialValue)) {
			resolve(initialValue);
			return;
		}

		let unsubscribe: () => void;

		// Set up a timeout
		const timeoutId = setTimeout(() => {
			if (unsubscribe) {
				unsubscribe();
			}
			reject(new Error(`Timed out waiting for store to match predicate after ${timeout}ms`));
		}, timeout);

		// Subscribe to the store
		unsubscribe = store.subscribe((value) => {
			if (predicate(value)) {
				clearTimeout(timeoutId);
				unsubscribe();
				resolve(value);
			}
		});
	});
}

/**
 * Wait for a machine to reach a specific state
 *
 * @param actor The actor reference to watch
 * @param stateValue The state value to wait for
 * @param timeout Maximum time to wait in milliseconds
 * @returns A promise that resolves when the machine reaches the specified state
 */
export function waitForState(actor: AnyActorRef, stateValue: string, timeout = 5000): Promise<any> {
	return new Promise((resolve, reject) => {
		// Check if the machine is already in the desired state
		const snapshot = actor.getSnapshot();
		if (snapshot.matches(stateValue)) {
			resolve(snapshot);
			return;
		}

		let subscription: any = null;

		// Set up a timeout
		const timeoutId = setTimeout(() => {
			if (subscription) {
				subscription.unsubscribe();
			}
			reject(
				new Error(`Timed out waiting for machine to reach state "${stateValue}" after ${timeout}ms`)
			);
		}, timeout);

		// Subscribe to the machine
		subscription = actor.subscribe((snapshot) => {
			if (snapshot.matches(stateValue)) {
				clearTimeout(timeoutId);
				if (subscription) {
					subscription.unsubscribe();
				}
				resolve(snapshot);
			}
		});
	});
}

/**
 * Create a mock store for testing
 *
 * @param initialValue The initial value of the store
 * @returns A mock store with additional testing utilities
 */
export function createMockStore<T>(initialValue: T) {
	let value = initialValue;
	const subscribers: Array<(value: T) => void> = [];

	// Create the store
	const store = {
		subscribe: (run: (value: T) => void) => {
			subscribers.push(run);
			run(value);

			return () => {
				const index = subscribers.indexOf(run);
				if (index !== -1) {
					subscribers.splice(index, 1);
				}
			};
		},

		// Testing utilities
		set: (newValue: T) => {
			value = newValue;
			subscribers.forEach((run) => run(value));
		},

		update: (updater: (value: T) => T) => {
			value = updater(value);
			subscribers.forEach((run) => run(value));
		},

		getValue: () => value
	};

	return store;
}
