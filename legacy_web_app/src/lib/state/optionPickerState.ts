/**
 * Option Picker State Management
 *
 * This module provides state management for the OptionPicker component
 * using Svelte stores instead of runes.
 */

import { browser } from '$app/environment';
import { writable, derived, get } from 'svelte/store';
import type { PictographData } from '$lib/types/PictographData';
import type { SortMethod, ReversalFilter } from '$lib/components/ConstructTab/OptionPicker/config';
import {
	getNextOptions,
	determineGroupKey,
	getSortedGroupKeys,
	getSorter
} from '$lib/components/ConstructTab/OptionPicker/services/OptionsService';
import { sequenceActions, sequenceSelectors } from '$lib/state/machines/sequenceMachine';

// ===== Type Definitions =====
export type LastSelectedTabState = Partial<Record<SortMethod, string | null>>;

// ===== Load Initial State =====
function loadUIState() {
	if (!browser) {
		return {
			sortMethod: 'type' as SortMethod,
			isLoading: false,
			error: null as string | null,
			lastSelectedTab: { type: 'all' } as LastSelectedTabState
		};
	}

	try {
		const stored = localStorage.getItem('optionPickerUIState');
		if (!stored) {
			return {
				sortMethod: 'type' as SortMethod,
				isLoading: false,
				error: null as string | null,
				lastSelectedTab: { type: 'all' } as LastSelectedTabState
			};
		}

		const parsed = JSON.parse(stored);
		return {
			sortMethod: (parsed.sortMethod || 'type') as SortMethod,
			isLoading: false,
			error: null as string | null,
			lastSelectedTab: parsed.lastSelectedTab || ({ type: 'all' } as LastSelectedTabState)
		};
	} catch (e) {
		console.error('Error reading from localStorage:', e);
		return {
			sortMethod: 'type' as SortMethod,
			isLoading: false,
			error: null as string | null,
			lastSelectedTab: { type: 'all' } as LastSelectedTabState
		};
	}
}

// ===== Core State Stores =====
const initialState = loadUIState();

// Create the core state stores
const sequenceStore = writable<PictographData[]>([]);
const optionsStore = writable<PictographData[]>([]);
const selectedPictographStore = writable<PictographData | null>(null);
const sortMethodStore = writable<SortMethod>(initialState.sortMethod);
const isLoadingStore = writable<boolean>(initialState.isLoading);
const errorStore = writable<string | null>(initialState.error);
const lastSelectedTabStore = writable<LastSelectedTabState>(initialState.lastSelectedTab);

// ===== Derived Stores =====
// Filtered options - applies filtering and sorting based on UI state
export const filteredOptions = derived(
	[optionsStore, sortMethodStore, sequenceStore],
	([$options, $sortMethod, $sequence]) => {
		let filteredOpts = [...$options];
		filteredOpts.sort(getSorter($sortMethod, $sequence));
		return filteredOpts;
	}
);

// Grouped options - groups the filtered/sorted options based on the current sortMethod
export const groupedOptions = derived(
	[filteredOptions, sortMethodStore, sequenceStore],
	([$filteredOptions, $sortMethod, $sequence]) => {
		const groups: Record<string, PictographData[]> = {};
		$filteredOptions.forEach((option) => {
			const groupKey = determineGroupKey(option, $sortMethod, $sequence);
			if (!groups[groupKey]) groups[groupKey] = [];
			groups[groupKey].push(option);
		});

		const sortedKeys = getSortedGroupKeys(Object.keys(groups), $sortMethod);
		const sortedGroups: Record<string, PictographData[]> = {};
		sortedKeys.forEach((key) => {
			if (groups[key]) {
				sortedGroups[key] = groups[key];
			}
		});

		return sortedGroups;
	}
);

// ===== Persistence =====
// Save UI state to localStorage when it changes
if (browser) {
	const unsubscribe = derived(
		[sortMethodStore, lastSelectedTabStore],
		([$sortMethod, $lastSelectedTab]) => ({
			sortMethod: $sortMethod,
			lastSelectedTab: $lastSelectedTab
		})
	).subscribe(($state) => {
		try {
			localStorage.setItem('optionPickerUIState', JSON.stringify($state));
		} catch (e) {
			console.error('Error writing to localStorage:', e);
		}
	});
}

// ===== Actions =====
export const actions = {
	loadOptions: (newSequence: PictographData[]) => {
		console.log('loadOptions called with sequence:', newSequence.length);

		// Don't try to load options if sequence is empty
		if (!newSequence || newSequence.length === 0) {
			console.warn('Attempted to load options with empty sequence');
			optionsStore.set([]);
			isLoadingStore.set(false);
			errorStore.set(null);
			return;
		}

		// Set loading state first
		isLoadingStore.set(true);
		errorStore.set(null);

		// Then update the sequence
		sequenceStore.set(newSequence);

		try {
			// Get next options based on the sequence
			const nextOptions = getNextOptions(newSequence);
			console.log('Next options calculated:', nextOptions?.length || 0);

			// If we got no options, log a warning but don't treat it as an error
			if (!nextOptions || nextOptions.length === 0) {
				console.warn('No options available for the current sequence');
			}

			// Update the options store
			optionsStore.set(nextOptions || []);

			// Always ensure we're showing 'all' options when loading new options
			// This ensures users see options immediately after selecting a start position
			const currentSortMethod = get(sortMethodStore);

			// Update UI state - set loading to false AFTER options are set
			setTimeout(() => {
				isLoadingStore.set(false);
				console.log('Loading state set to false');

				// Always set the last selected tab to 'all' for the current sort method
				lastSelectedTabStore.update((tabs) => ({
					...tabs,
					[currentSortMethod]: 'all'
				}));

				// Dispatch a viewchange event to ensure the UI updates
				if (typeof document !== 'undefined') {
					const viewChangeEvent = new CustomEvent('viewchange', {
						detail: { mode: 'all' },
						bubbles: true
					});
					document.dispatchEvent(viewChangeEvent);
				}
			}, 100); // Small delay to ensure options are processed
		} catch (err) {
			console.error('Error loading options:', err);
			isLoadingStore.set(false);
			errorStore.set(err instanceof Error ? err.message : 'Unknown error loading options');
			optionsStore.set([]);
		}
	},

	setSortMethod: (method: SortMethod) => {
		sortMethodStore.set(method);
	},

	setReversalFilter: (filter: ReversalFilter) => {
		// Store the filter in state if needed
	},

	setLastSelectedTabForSort: (method: SortMethod, tabKey: string | null) => {
		// Avoid unnecessary updates if the value hasn't changed
		const currentLastSelectedTab = get(lastSelectedTabStore);
		if (currentLastSelectedTab[method] === tabKey) {
			return;
		}

		lastSelectedTabStore.update((tabs) => ({
			...tabs,
			[method]: tabKey
		}));
	},

	selectOption: (option: PictographData) => {
		// Update the selected pictograph
		selectedPictographStore.set(option);

		// Now add the selected option to the beat sequence using the state machine
		const beatData = {
			id: crypto.randomUUID(),
			number: sequenceSelectors.beatCount() + 1,
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

	reset: () => {
		optionsStore.set([]);
		sequenceStore.set([]);
		isLoadingStore.set(false);
		errorStore.set(null);

		// Ensure 'all' is set as the default tab for the current sort method
		const currentSortMethod = get(sortMethodStore);
		actions.setLastSelectedTabForSort(currentSortMethod, 'all');
		selectedPictographStore.set(null);
	}
};

// ===== Exports =====
// Export the stores directly to maintain the same API
export const sequence = sequenceStore;
export const options = optionsStore;
export const selectedPictograph = selectedPictographStore;
export const sortMethod = sortMethodStore;
export const isLoading = isLoadingStore;
export const error = errorStore;
export const lastSelectedTab = lastSelectedTabStore;
