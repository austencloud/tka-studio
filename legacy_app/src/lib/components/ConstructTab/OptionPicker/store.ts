// src/lib/components/OptionPicker/store.ts
import { writable, derived } from 'svelte/store';
import type { PictographData } from '$lib/types/PictographData';
import { selectedPictograph } from '$lib/stores/sequence/selectedPictographStore';
import type { SortMethod, ReversalFilter } from './config';
import {
	getNextOptions,
	determineReversalCategory,
	determineGroupKey,
	getSortedGroupKeys,
	getSorter
} from './services/OptionsService';
import { get } from 'svelte/store';
import { browser } from '$app/environment';
// Import the sequenceActions and sequenceSelectors from the state machine
import { sequenceActions, sequenceSelectors } from '$lib/state/machines/sequenceMachine';

// ===== Core State =====
export const sequenceStore = writable<PictographData[]>([]);
export const optionsStore = writable<PictographData[]>([]);

// ===== UI State =====
export type LastSelectedTabState = Partial<Record<SortMethod, string | null>>;

// Define the helper function to get stored state from localStorage
function getStoredState() {
	if (!browser) return { sortMethod: 'type', lastSelectedTab: {} };

	try {
		const stored = localStorage.getItem('optionPickerUIState');

		if (!stored) return { sortMethod: 'type', lastSelectedTab: { type: 'all' } };

		const parsed = JSON.parse(stored);

		// Ensure we have a valid structure
		return {
			sortMethod: parsed.sortMethod || 'type',
			lastSelectedTab: parsed.lastSelectedTab || { type: 'all' }
		};
	} catch (e) {
		console.error('Error reading from localStorage:', e);
		return { sortMethod: 'type', lastSelectedTab: { type: 'all' } };
	}
}

// Get the stored state
const storedState = getStoredState();

// Initialize uiState with the stored values
export const uiState = writable({
	sortMethod: storedState.sortMethod as SortMethod,
	isLoading: false,
	error: null as string | null,
	lastSelectedTab: storedState.lastSelectedTab as LastSelectedTabState
});

// Set up the localStorage subscription to persist state changes
if (browser) {
	uiState.subscribe((state) => {
		try {
			// Save the complete state
			const saveData = {
				sortMethod: state.sortMethod,
				lastSelectedTab: state.lastSelectedTab
			};
			localStorage.setItem('optionPickerUIState', JSON.stringify(saveData));
		} catch (e) {
			console.error('Error writing to localStorage:', e);
		}
	});
}

// ===== Actions =====
export const actions = {
	loadOptions: (sequence: PictographData[]) => {
		// Don't try to load options if sequence is empty
		if (!sequence || sequence.length === 0) {
			console.warn('Attempted to load options with empty sequence');
			optionsStore.set([]);
			uiState.update((state) => ({ ...state, isLoading: false, error: null }));
			return;
		}

		sequenceStore.set(sequence);
		uiState.update((state) => ({ ...state, isLoading: true, error: null }));

		try {
			const nextOptions = getNextOptions(sequence);

			// If we got no options, log a warning but don't treat it as an error
			if (!nextOptions || nextOptions.length === 0) {
				console.warn('No options available for the current sequence');
			}

			optionsStore.set(nextOptions || []);

			// Get the current UI state
			const currentState = get(uiState);
			const currentSortMethod = currentState.sortMethod;

			// Instead of always resetting to 'all', retain the current tab selection
			uiState.update((state) => ({
				...state,
				isLoading: false
				// No longer forcing the tab to 'all' - we'll keep the user's selection
			}));

			// Only dispatch a viewchange event if we don't have a selected tab yet
			if (
				typeof document !== 'undefined' &&
				(!currentState.lastSelectedTab[currentSortMethod] ||
					currentState.lastSelectedTab[currentSortMethod] === null)
			) {
				console.log('No tab selected yet, defaulting to "all"');
				// Only in this case, set the default tab to 'all'
				actions.setLastSelectedTabForSort(currentSortMethod, 'all');

				const viewChangeEvent = new CustomEvent('viewchange', {
					detail: { mode: 'all' },
					bubbles: true
				});
				document.dispatchEvent(viewChangeEvent);
			}
		} catch (error) {
			console.error('Error loading options:', error);
			uiState.update((state) => ({
				...state,
				isLoading: false,
				error: error instanceof Error ? error.message : 'Unknown error loading options'
			}));
			optionsStore.set([]);
		}
	},

	setSortMethod: (method: SortMethod) => {
		// Only update the sortMethod here. The component will reactively
		// update the selectedTab based on the new method and stored preferences.
		uiState.update((state) => ({ ...state, sortMethod: method }));
	},

	setReversalFilter: (filter: ReversalFilter) => {
		uiState.update((state) => ({ ...state, reversalFilter: filter }));
	},

	// ADDED: Action to store the last selected tab for a given sort method
	setLastSelectedTabForSort: (sortMethod: SortMethod, tabKey: string | null) => {
		uiState.update((state) => {
			// Avoid unnecessary updates if the value hasn't changed
			if (state.lastSelectedTab[sortMethod] === tabKey) {
				return state;
			}
			return {
				...state,
				lastSelectedTab: {
					...state.lastSelectedTab,
					[sortMethod]: tabKey
				}
			};
		});
	},

	selectOption: (option: PictographData) => {
		// First, update the selected pictograph store
		selectedPictograph.set(option);

		// Now add the selected option to the beat sequence using the state machine
		// Convert PictographData to StoreBeatData format
		const beatData = {
			id: crypto.randomUUID(),
			number: sequenceSelectors.beatCount() + 1, // Get the current beat count and add 1
			redPropData: option.redPropData,
			bluePropData: option.bluePropData,
			redMotionData: option.redMotionData,
			blueMotionData: option.blueMotionData,
			metadata: {
				letter: option.letter,
				startPos: option.startPos,
				endPos: option.endPos
			}
		};

		// Add the beat using the state machine
		sequenceActions.addBeat(beatData);

		// Dispatch a custom event to notify components that a beat was added
		if (typeof document !== 'undefined') {
			const beatAddedEvent = new CustomEvent('beat-added', {
				detail: { beat: beatData },
				bubbles: true
			});
			document.dispatchEvent(beatAddedEvent);
		}
	},

	// Reset the option picker state while preserving user preferences
	reset: () => {
		optionsStore.set([]);
		sequenceStore.set([]);

		// Get current state to preserve user preferences
		const currentState = get(uiState);

		// Preserve the sort method and tab preferences
		uiState.set({
			sortMethod: currentState.sortMethod || 'type',
			isLoading: false,
			error: null,
			lastSelectedTab: currentState.lastSelectedTab || {}
		});

		// Ensure 'all' is set as the default tab for the current sort method
		// This prevents "No options for X" messages when there are no options
		const sortMethod = currentState.sortMethod || 'type';
		actions.setLastSelectedTabForSort(sortMethod, 'all');

		selectedPictograph.set(null);
	}
};

// ===== Derived Stores =====

// Filtered options - applies filtering and sorting based on uiState
export const filteredOptionsStore = derived(
	[optionsStore, sequenceStore, uiState],
	([$options, $sequence, $ui]) => {
		let options = [...$options];

		options.sort(getSorter($ui.sortMethod, $sequence));
		return options;
	}
);

// Grouped options - groups the filtered/sorted options based on the current sortMethod
export const groupedOptionsStore = derived(
	[filteredOptionsStore, sequenceStore, uiState],
	([$filteredOptions, $sequence, $ui]) => {
		const groups: Record<string, PictographData[]> = {};
		$filteredOptions.forEach((option) => {
			const groupKey = determineGroupKey(option, $ui.sortMethod, $sequence);
			if (!groups[groupKey]) groups[groupKey] = [];
			groups[groupKey].push(option);
		});
		const sortedKeys = getSortedGroupKeys(Object.keys(groups), $ui.sortMethod);
		const sortedGroups: Record<string, PictographData[]> = {};
		sortedKeys.forEach((key) => {
			if (groups[key]) {
				sortedGroups[key] = groups[key];
			}
		});
		return sortedGroups;
	}
);

// Convenience export (optional)
export const optionPickerStore = {
	subscribe: derived([optionsStore, sequenceStore, uiState], ([$options, $sequence, $ui]) => ({
		allOptions: $options,
		currentSequence: $sequence,
		sortMethod: $ui.sortMethod,
		isLoading: $ui.isLoading,
		error: $ui.error
		// components interact via actions or specific selectors if needed.
	})).subscribe,
	...actions
};
