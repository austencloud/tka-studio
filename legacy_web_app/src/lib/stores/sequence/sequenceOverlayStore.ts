// src/lib/stores/sequence/sequenceOverlayStore.ts
import { writable } from 'svelte/store';

// Create a store to track the overlay state of the sequence
export const isSequenceFullScreen = writable<boolean>(false);

// Helper functions to manipulate the store
export function openSequenceFullScreen() {
	console.log('Setting sequence overlay to open');
	isSequenceFullScreen.set(true);
}

export function closeSequenceFullScreen() {
	console.log('Setting sequence overlay to closed');
	isSequenceFullScreen.set(false);
}

export function toggleSequenceFullScreen() {
	isSequenceFullScreen.update((value) => {
		console.log('Toggling sequence overlay, current value:', value);
		return !value;
	});
}
