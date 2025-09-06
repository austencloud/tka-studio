import {
	isSequenceFullScreen,
	openSequenceFullScreen,
	closeSequenceFullScreen
} from '$lib/stores/sequence/sequenceOverlayStore';
import { onDestroy } from 'svelte';

/**
 * Interface for the full screen manager return value
 */
export interface FullScreenManagerResult {
	isFullScreen: boolean;
	openFullScreen: () => void;
	closeFullScreen: () => void;
}

/**
 * Manages the full screen state for the sequence widget
 * @returns Object with full screen state and functions
 */
export function useFullScreenManager(): FullScreenManagerResult {
	// Create a variable to hold the current state
	let isFullScreen = false;

	// Subscribe to the store to keep the value updated
	const unsubscribe = isSequenceFullScreen.subscribe((value) => {
		isFullScreen = value;
	});

	// Clean up subscription on component destroy
	onDestroy(() => {
		unsubscribe();
	});

	// Define the functions to open and close fullscreen
	function openFullScreen() {
		console.log('Opening sequence overlay from manager');
		openSequenceFullScreen();
	}

	function closeFullScreen() {
		console.log('Closing sequence overlay from manager');
		closeSequenceFullScreen();
	}

	// Return the manager object
	return {
		get isFullScreen() {
			return isFullScreen;
		},
		openFullScreen,
		closeFullScreen
	};
}
