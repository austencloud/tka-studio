/**
 * Svelte 5 Runes Integration
 *
 * This module provides utilities for integrating our store-based state management
 * with Svelte 5 runes. This file has a .svelte.ts extension to enable runes support.
 */

import type { Readable } from 'svelte/store';

/**
 * Creates a reactive state variable from a Svelte store
 *
 * @param store A Svelte store
 * @returns A reactive state variable that updates when the store changes
 */
export function useStore<T>(store: Readable<T>): T {
	// Create a mutable reactive state variable
	let state = $state<T | undefined>(undefined);

	// Initialize with first value
	let initialized = false;

	// Set up an effect to update the state when the store changes
	$effect(() => {
		const unsubscribe = store.subscribe((value) => {
			state = value;
			initialized = true;
		});

		return unsubscribe;
	});

	// Create a variable to store the state
	const stateValue = $derived(state as T);

	// Return a proxy that throws if accessed before initialization
	return new Proxy(Object.create(null), {
		get: (_target, prop) => {
			if (!initialized) {
				throw new Error('Store not initialized yet');
			}
			return stateValue[prop as keyof T];
		}
	}) as T;
}

/**
 * Creates a reactive state variable from a container
 *
 * @param container A state container
 * @returns A reactive state variable that updates when the container changes
 */
export function useContainer<T extends object>(container: {
	state: T;
	subscribe: Readable<T>['subscribe'];
}): T {
	// Create a mutable reactive state variable with initial value from container
	let state = $state<T>({ ...container.state });

	// Set up an effect to update the state when the container changes
	$effect(() => {
		const unsubscribe = container.subscribe((value) => {
			// Update all properties of the state object
			Object.assign(state, value);
		});

		return unsubscribe;
	});

	return state;
}

/**
 * Creates a derived value from a reactive state variable
 *
 * @param fn A function that computes the derived value
 * @returns A derived value that updates when dependencies change
 */
export function useDerived<T>(fn: () => T): T {
	const value = $derived(fn());
	return value;
}

/**
 * Creates an effect that runs when dependencies change
 *
 * @param fn A function that performs side effects
 * @returns A cleanup function
 */
export function useEffect(fn: () => void | (() => void)): void {
	$effect(() => {
		return fn();
	});
}

/**
 * Creates a reactive state variable from an XState machine container
 *
 * @param container A machine container
 * @returns A reactive state object with machine state and helper methods
 */
export function useMachine<T extends object, E extends { type: string }>(container: {
	state: T;
	subscribe: Readable<T>['subscribe'];
	send: (event: E) => void;
	can: (eventType: string) => boolean;
	matches: (stateValue: string) => boolean;
	hasTag: (tag: string) => boolean;
}) {
	// Create a mutable reactive state variable with initial value from container
	let state = $state<T>({ ...container.state });

	// Set up an effect to update the state when the container changes
	$effect(() => {
		const unsubscribe = container.subscribe((value) => {
			// Update all properties of the state object
			Object.assign(state, value);
		});

		return unsubscribe;
	});

	// Create helper methods that use the reactive state
	const can = (eventType: string) => container.can(eventType);
	const matches = (stateValue: string) => container.matches(stateValue);
	const hasTag = (tag: string) => container.hasTag(tag);
	const send = (event: E) => container.send(event);

	return {
		state,
		can,
		matches,
		hasTag,
		send
	};
}
