/**
 * Modern State Management
 *
 * This module exports all the utilities for the modern state management approach.
 * It serves as the main entry point for the new state management system.
 */

// Export container utilities
export * from './container';

// Export machine utilities
export * from './modernMachine';

// Export adapter utilities
export * from './adapters';

// Export testing utilities
export * from './modernTesting';

// Re-export types from the registry for compatibility
export { type StateContainer, type StateContainerType } from './registry/types';

/**
 * Creates a simple state object with a getter
 *
 * This is a utility for creating simple state objects with a getter
 * that can be used in components.
 *
 * @param initialState The initial state
 * @returns An object with a state getter
 */
export function createState<T>(initialState: T): { state: T } {
	// Check if we're running in a Svelte 5 environment with runes support
	const hasRunes = typeof globalThis.$state !== 'undefined';

	if (hasRunes) {
		// Import the runes version dynamically to avoid loading it in non-runes environments
		const { createStateWithRunes } = require('./modern.svelte');
		return createStateWithRunes(initialState);
	} else {
		// For Svelte 4, just return the initial state
		return {
			state: initialState
		};
	}
}

/**
 * Creates a simple derived state object with a getter
 *
 * This is a utility for creating simple derived state objects with a getter
 * that can be used in components.
 *
 * @param fn A function that computes the derived value
 * @returns An object with a state getter
 */
export function createDerivedState<T>(fn: () => T): { state: T } {
	// Check if we're running in a Svelte 5 environment with runes support
	const hasRunes = typeof globalThis.$state !== 'undefined';

	if (hasRunes) {
		// Import the runes version dynamically to avoid loading it in non-runes environments
		const { createDerivedStateWithRunes } = require('./modern.svelte');
		return createDerivedStateWithRunes(fn);
	} else {
		// For Svelte 4, just compute the value once
		return {
			state: fn()
		};
	}
}
