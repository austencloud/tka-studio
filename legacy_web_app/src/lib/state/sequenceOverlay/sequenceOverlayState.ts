// src/lib/state/sequenceOverlay/sequenceOverlayState.ts
import { writable } from 'svelte/store';

/**
 * Interface for the sequence overlay state
 */
export interface SequenceOverlayState {
	isOpen: boolean;
}

/**
 * Centralized state for the sequence overlay using Svelte stores
 * This state is maintained across hot module reloads
 */
export const sequenceOverlayStore = writable<SequenceOverlayState>({
	isOpen: false
});

// Create a singleton object that can be used in non-Svelte contextsLet me shut it off of I'm going to shut a little metal You're an absolute wonderful Significant oK significant love Simply you're looking simply from your human from your together don't love you forever I love you forever I love you forever we're always What's the joke with a little cat I love you I love you it's true it's true I love you Yeah
// and will be properly reactive in Svelte components
export const sequenceOverlayState = {
	get isOpen() {
		let value = false;
		const unsubscribe = sequenceOverlayStore.subscribe((state) => {
			value = state.isOpen;
		});
		unsubscribe();
		return value;
	},
	set isOpen(value: boolean) {
		sequenceOverlayStore.update((state) => ({
			...state,
			isOpen: value
		}));
	}
};

/**
 * Opens the sequence overlay
 */
export function openSequenceOverlay() {
	console.log('Opening sequence overlay');
	sequenceOverlayStore.update((state) => ({
		...state,
		isOpen: true
	}));
}

/**
 * Closes the sequence overlay
 */
export function closeSequenceOverlay() {
	console.log('Closing sequence overlay');
	sequenceOverlayStore.update((state) => ({
		...state,
		isOpen: false
	}));
}

/**
 * Toggles the sequence overlay
 */
export function toggleSequenceOverlay() {
	sequenceOverlayStore.update((state) => {
		console.log('Toggling sequence overlay, current value:', state.isOpen);
		return {
			...state,
			isOpen: !state.isOpen
		};
	});
}
