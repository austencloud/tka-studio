// src/lib/components/OptionPicker/runesStore.svelte.ts
import type { PictographData } from '$lib/types/PictographData';
import type { SortMethod, ReversalFilter } from './config';
import {
	getNextOptions,
	determineReversalCategory,
	determineGroupKey,
	getSortedGroupKeys,
	getSorter
} from './services/OptionsService';
import { browser } from '$app/environment';
// Import the sequenceActions and sequenceSelectors from the state machine
import { sequenceActions, sequenceSelectors } from '$lib/state/machines/sequenceMachine';
import { createPersistentObjectState } from '$lib/state/core/runes.svelte';

// ===== Core State =====
// Using Svelte 5 runes for state management
export let sequenceData = $state<PictographData[]>([]);
export let optionsData = $state<PictographData[]>([]);
export let selectedPictographData = $state<PictographData | null>(null);

// ===== UI State =====
export type LastSelectedTabState = Partial<Record<SortMethod, string | null>>;

// Create persistent UI state using runes
export const uiState = createPersistentObjectState('optionPickerUIState', {
	sortMethod: 'type' as SortMethod,
	isLoading: false,
	error: null as string | null,
	lastSelectedTab: { type: 'all' } as LastSelectedTabState,
	reversalFilter: 'all' as ReversalFilter
});

// ===== Derived State =====
// Filtered options - applies filtering and sorting based on uiState
export const filteredOptions = $derived(() => {
	let options = [...optionsData];
	options.sort(getSorter(uiState.sortMethod, sequenceData));
	return options;
});

// Grouped options - groups the filtered/sorted options based on the current sortMethod
export const groupedOptions = $derived(() => {
	const groups: Record<string, PictographData[]> = {};
	const options = filteredOptions();
	options.forEach((option) => {
		const groupKey = determineGroupKey(option, uiState.sortMethod, sequenceData);
		if (!groups[groupKey]) groups[groupKey] = [];
		groups[groupKey].push(option);
	});
	const sortedKeys = getSortedGroupKeys(Object.keys(groups), uiState.sortMethod);
	const sortedGroups: Record<string, PictographData[]> = {};
	sortedKeys.forEach((key) => {
		if (groups[key]) {
			sortedGroups[key] = groups[key];
		}
	});
	return sortedGroups;
});

// ===== Actions =====
export const actions = {
	loadOptions: (sequence: PictographData[]) => {
		// Don't try to load options if sequence is empty
		if (!sequence || sequence.length === 0) {
			console.warn('Attempted to load options with empty sequence');
			optionsData = [];
			uiState.isLoading = false;
			uiState.error = null;
			return;
		}

		sequenceData = sequence;
		uiState.isLoading = true;
		uiState.error = null;

		try {
			const nextOptions = getNextOptions(sequence);

			// If we got no options, log a warning but don't treat it as an error
			if (!nextOptions || nextOptions.length === 0) {
				console.warn('No options available for the current sequence');
			}

			optionsData = nextOptions || [];

			// Always ensure we're showing 'all' options when loading new options
			// This ensures users see options immediately after selecting a start position
			const currentSortMethod = uiState.sortMethod;

			// Update UI state
			uiState.isLoading = false;
			// Always set the last selected tab to 'all' for the current sort method
			uiState.lastSelectedTab = {
				...uiState.lastSelectedTab,
				[currentSortMethod]: 'all'
			};

			// Dispatch a viewchange event to ensure the UI updates
			if (typeof document !== 'undefined') {
				const viewChangeEvent = new CustomEvent('viewchange', {
					detail: { mode: 'all' },
					bubbles: true
				});
				document.dispatchEvent(viewChangeEvent);
			}
		} catch (error) {
			console.error('Error loading options:', error);
			uiState.isLoading = false;
			uiState.error = error instanceof Error ? error.message : 'Unknown error loading options';
			optionsData = [];
		}
	},

	setSortMethod: (method: SortMethod) => {
		// Only update the sortMethod here. The component will reactively
		// update the selectedTab based on the new method and stored preferences.
		uiState.sortMethod = method;
	},

	setReversalFilter: (filter: ReversalFilter) => {
		uiState.reversalFilter = filter;
	},

	// Action to store the last selected tab for a given sort method
	setLastSelectedTabForSort: (sortMethod: SortMethod, tabKey: string | null) => {
		// Avoid unnecessary updates if the value hasn't changed
		if (uiState.lastSelectedTab[sortMethod] === tabKey) {
			return;
		}

		uiState.lastSelectedTab = {
			...uiState.lastSelectedTab,
			[sortMethod]: tabKey
		};
	},

	selectOption: (option: PictographData) => {
		// First, update the selected pictograph
		selectedPictographData = option;

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
		optionsData = [];
		sequenceData = [];

		// Preserve the sort method and tab preferences
		const currentSortMethod = uiState.sortMethod;
		uiState.isLoading = false;
		uiState.error = null;

		// Ensure 'all' is set as the default tab for the current sort method
		// This prevents "No options for X" messages when there are no options
		actions.setLastSelectedTabForSort(currentSortMethod, 'all');

		selectedPictographData = null;
	}
};
