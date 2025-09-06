/**
 * Svelte 5 Runes Utilities
 *
 * This module provides utilities for working with Svelte 5 runes,
 * particularly for state management and persistence.
 *
 * This file re-exports the runes-based functions from the .svelte.ts file
 * to ensure they're only used in the correct context.
 */

export {
	createPersistentState,
	createPersistentObjectState,
	createSharedContext
} from './runes.svelte';
