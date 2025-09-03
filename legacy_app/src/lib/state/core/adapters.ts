/**
 * State Management Adapters
 *
 * This module provides adapters between different state management approaches,
 * allowing for gradual migration from the old registry-based system to the new
 * container-based system.
 */

import { writable, derived, get, type Writable, type Readable } from 'svelte/store';
import { stateRegistry } from './registry';
import { createEffect } from './container';

// Check if we're running in a Svelte 5 environment with runes support
const hasRunes = typeof globalThis.$state !== 'undefined';

/**
 * Converts a state container to a Svelte store
 * This allows new container-based state to be used with existing store-based components
 *
 * @param container A state container created with createContainer
 * @returns A Svelte store with the same API as the container
 */
export function containerToStore<T extends object, A extends Record<string, Function>>(
	container: { state: T } & A & { reset: () => void }
): Writable<T> & A & { reset: () => void } {
	// If the container already has a subscribe method, it's already store-compatible
	if ('subscribe' in container) {
		return container as any;
	}

	// Create a writable store with the current state
	const store = writable<T>(container.state);

	// Set up an effect to update the store when the container state changes
	if (hasRunes) {
		createEffect(() => {
			store.set(container.state);
		});
	}

	// Create a proxy that forwards method calls to the container
	const proxy = {
		subscribe: store.subscribe,
		set: (value: T) => {
			Object.assign(container.state, value);
			store.set(value);
		},
		update: (updater: (value: T) => T) => {
			const newValue = updater(container.state);
			Object.assign(container.state, newValue);
			store.set(newValue);
		},
		reset: container.reset
	};

	// Add all action methods from the container
	for (const [key, value] of Object.entries(container)) {
		if (typeof value === 'function' && key !== 'reset' && !key.startsWith('_')) {
			(proxy as any)[key] = value;
		}
	}

	return proxy as Writable<T> & A & { reset: () => void };
}

/**
 * Registers a container with the state registry
 * This allows new container-based state to be used with the existing registry system
 *
 * @param id The ID to register the container under
 * @param container A state container created with createContainer
 * @param options Registration options
 * @returns The container
 */
export function registerContainer<T extends object, A extends Record<string, Function>>(
	id: string,
	container: { state: T } & A & { reset: () => void },
	options: { persist?: boolean; description?: string } = {}
): { state: T } & A & { reset: () => void } {
	// Convert the container to a store
	const store = containerToStore(container);

	// Register the store with the registry
	stateRegistry.registerStore(id, store, {
		persist: options.persist,
		description: options.description
	});

	return container;
}

/**
 * Creates a derived container from another container
 *
 * @param container The source container
 * @param deriveFn A function that derives a new state from the source state
 * @returns A new container with the derived state
 */
export function deriveContainer<T extends object, U extends object>(
	container: { state: T },
	deriveFn: (state: T) => U
): { state: U } {
	if (hasRunes) {
		// Import the runes version dynamically to avoid loading it in non-runes environments
		const { deriveContainerWithRunes } = require('./adapters.svelte');
		return deriveContainerWithRunes(container, deriveFn);
	} else {
		// Create a derived store
		const derivedStore = derived(
			// If the container has a subscribe method, use it directly
			'subscribe' in container ? (container as unknown as Readable<T>) : writable(container.state),
			(state) => deriveFn(state)
		);

		// Return an object with a state getter that reads from the derived store
		return {
			get state() {
				return get(derivedStore);
			},
			// Add subscribe for compatibility
			subscribe: derivedStore.subscribe
		} as { state: U };
	}
}
