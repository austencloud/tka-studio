import {
	sequenceOverlayState,
	openSequenceOverlay,
	closeSequenceOverlay
} from '$lib/state/sequenceOverlay/sequenceOverlayState';

/**
 * Interface for the sequence overlay manager return value
 */
export interface SequenceOverlayManagerResult {
	isOpen: boolean;
	openOverlay: () => void;
	closeOverlay: () => void;
}

/**
 * Manages the overlay state for the sequence widget using Svelte 5 runes
 * @returns Object with overlay state and functions
 */
export function useSequenceOverlayManager(): SequenceOverlayManagerResult {
	// Define the functions to open and close overlay
	function openOverlay() {
		console.log('Opening sequence overlay from manager');
		openSequenceOverlay();
	}

	function closeOverlay() {
		console.log('Closing sequence overlay from manager');
		closeSequenceOverlay();
	}

	// Return the manager object
	return {
		get isOpen() {
			return sequenceOverlayState.isOpen;
		},
		openOverlay,
		closeOverlay
	};
}
