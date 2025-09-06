// src/lib/components/SequenceWorkbench/ButtonPanel/stores/panelStore.ts
import { writable, derived } from 'svelte/store';
import type { PanelState, LayoutOrientation } from '../types';
import { browser } from '$app/environment'; // Import browser check

// Initial panel state
const initialState: PanelState = {
	layout: 'horizontal' // Default layout
};

// Create the panel state store
const createPanelStore = () => {
	const { subscribe, update, set } = writable<PanelState>(initialState);

	return {
		subscribe,

		// Update layout orientation
		setLayout: (layout: LayoutOrientation) => {
			update((state) => ({ ...state, layout }));
		},

		// Reset store to initial state
		reset: () => set(initialState)
	};
};

// Export the panel store instance
export const panelStore = createPanelStore();

// Number of buttons to account for in sizing (update this if buttons count changes)
const TYPICAL_BUTTON_COUNT = 7;
const BUTTON_GAP = 12; // Gap between buttons (matches CSS in ButtonsContainer)
const BUTTON_PADDING = 8 * 2; // Padding on both sides (matches CSS in ButtonsContainer)

// Helper function (extracted from original component)
function calculateButtonSize(width: number, height: number, isPortrait: boolean): number {
	// Check for browser environment for window access if needed, though here width/height are passed in
	const isMobile = browser ? window.innerWidth <= 768 : width <= 768; // Example of browser check if needed

	// Calculate available space for buttons
	let maxSize: number;

	if (isPortrait || isMobile) {
		// For horizontal layout (portrait or mobile), divide the width
		const availableWidth = width - BUTTON_PADDING;
		// Account for button count and gaps between buttons
		maxSize = (availableWidth - BUTTON_GAP * (TYPICAL_BUTTON_COUNT - 1)) / TYPICAL_BUTTON_COUNT;
	} else {
		// For vertical layout (landscape desktop), use height with more breathing room
		const availableHeight = height - BUTTON_PADDING;
		maxSize = (availableHeight - BUTTON_GAP * (TYPICAL_BUTTON_COUNT - 1)) / TYPICAL_BUTTON_COUNT;
	}

	// Enforce min/max boundaries for aesthetics and usability
	return Math.max(28, Math.min(55, maxSize));
}

// Derived store that provides the calculation *function*
// It depends on the panelStore only to potentially trigger recalculation if needed,
// but the calculation itself uses arguments passed to the returned function.
export const buttonSizeStore = derived<
	[typeof panelStore], // Depends on panelStore only to ensure reactivity if layout influenced size
	(width: number, height: number, isPortrait: boolean) => number
>([panelStore], ([$panelState]) => {
	// The derived store's value *is* the calculation function
	return (width: number, height: number, isPortrait: boolean): number => {
		// Call the helper function with the provided arguments
		return calculateButtonSize(width, height, isPortrait);
	};
});
