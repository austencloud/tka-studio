// src/lib/stores/sequence/selectionStore.ts
import { writable, derived, type Readable } from 'svelte/store';
import type { PictographData } from '$lib/types/PictographData';
import { beatsStore } from './beatsStore';
import type { BeatData } from '$lib/components/SequenceWorkbench/BeatFrame/BeatData';
import { browser } from '$app/environment';

// Storage key for the start position
const START_POSITION_STORAGE_KEY = 'selected_start_position';

// Create a custom store for selectedStartPos with localStorage persistence
function createSelectedStartPosStore() {
	// Try to load the initial value from localStorage
	let initialValue: PictographData | null = null;

	if (browser) {
		try {
			const savedValue = localStorage.getItem(START_POSITION_STORAGE_KEY);
			if (savedValue) {
				initialValue = JSON.parse(savedValue);

			}
		} catch (error) {
			console.error('Error loading start position from localStorage:', error);
		}
	}

	const { subscribe, set: originalSet, update } = writable<PictographData | null>(initialValue);

	// Override the set method to also save to localStorage
	function set(value: PictographData | null) {
		if (browser) {
			try {
				if (value) {
					localStorage.setItem(START_POSITION_STORAGE_KEY, JSON.stringify(value));
					if (import.meta.env.DEV) {
					}
				} else {
					localStorage.removeItem(START_POSITION_STORAGE_KEY);
				}
			} catch (error) {
				console.error('Error saving start position to localStorage:', error);
			}
		}

		originalSet(value);
	}

	return {
		subscribe,
		set,
		update: (updater: (value: PictographData | null) => PictographData | null) => {
			update((current) => {
				const newValue = updater(current);

				// Save the new value to localStorage
				if (browser) {
					try {
						if (newValue) {
							localStorage.setItem(START_POSITION_STORAGE_KEY, JSON.stringify(newValue));

						} else {
							localStorage.removeItem(START_POSITION_STORAGE_KEY);

						}
					} catch (error) {
						console.error('Error saving start position to localStorage:', error);
					}
				}

				return newValue;
			});
		}
	};
}

// Primary selection stores
export const selectedBeatIndexStore = writable<number | null>(null);
export const selectedStartPosStore = createSelectedStartPosStore();

// Derived store for the selected beat data
export const selectedBeat: Readable<BeatData | null> = derived(
	[beatsStore, selectedBeatIndexStore],
	([$beats, $selectedIndex]) => {
		if ($selectedIndex === null || $selectedIndex < 0 || $selectedIndex >= $beats.length) {
			return null;
		}
		return $beats[$selectedIndex];
	}
);

// Derived store for whether we're in "selecting start position" mode
export const isSelectingStartPos = derived(
	[selectedBeatIndexStore, selectedStartPosStore],
	([$selectedBeatIndex, $selectedStartPos]) => {
		return $selectedBeatIndex === null && $selectedStartPos !== null;
	}
);

// Derived store for whether we're in "selecting beat" mode
export const isSelectingBeat = derived(
	selectedBeatIndexStore,
	($selectedBeatIndex) => $selectedBeatIndex !== null
);

// Derived store for whether any selection is active
export const hasSelection = derived(
	[selectedBeatIndexStore, selectedStartPosStore],
	([$selectedBeatIndex, $selectedStartPos]) =>
		$selectedBeatIndex !== null || $selectedStartPos !== null
);

/**
 * Selection actions encapsulate all the ways to manipulate selection state
 * These are pure functions that update the selection stores in a controlled way
 */
export const selectionActions = {
	/**
	 * Select a beat by its index
	 * This will clear any start position selection
	 */
	selectBeat: (index: number | null) => {
		selectedBeatIndexStore.set(index);

		// If selecting a beat, clear start position selection
		if (index !== null) {
			selectedStartPosStore.set(null);
		}
	},

	/**
	 * Select a start position
	 * This will clear any beat selection
	 */
	selectStartPos: (data: PictographData | null) => {
		selectedStartPosStore.set(data);

		// If selecting a start position, clear beat selection
		if (data !== null) {
			selectedBeatIndexStore.set(null);
		}
	},

	/**
	 * Clear all selections
	 */
	clearAllSelections: () => {
		selectedBeatIndexStore.set(null);
		selectedStartPosStore.set(null);
	},

	/**
	 * Toggle beat selection
	 * If the beat is already selected, unselect it
	 * If a different beat is selected, select the new one
	 */
	toggleBeatSelection: (index: number) => {
		selectedBeatIndexStore.update((currentIndex) => (currentIndex === index ? null : index));

		// Clear start position selection when toggling beat selection
		selectedStartPosStore.set(null);
	}
};

// Export the selected start position store for backward compatibility
// This allows gradual migration without breaking existing code
export const selectedStartPos = selectedStartPosStore;
