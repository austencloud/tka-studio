/**
 * Option Picker Container with Svelte 5 Runes
 *
 * This module provides an implementation of the option picker state using
 * the container-based approach with Svelte 5 runes.
 */

import { createContainer, createDerived } from '$lib/state/core/container';
import { createPersistentObjectState } from '$lib/state/core/runes.svelte';
import type { PictographData } from '$lib/types/PictographData';
import type { SortMethod, ReversalFilter } from '$lib/components/ConstructTab/OptionPicker/config';
import {
	getNextOptions,
	determineGroupKey,
	getSortedGroupKeys,
	getSorter
} from '$lib/components/ConstructTab/OptionPicker/services/OptionsService';
import { sequenceActions, sequenceSelectors } from '$lib/state/machines/sequenceMachine';
import { browser } from '$app/environment';
import type { LastSelectedTabState, OptionPickerState } from './types';
import hapticFeedbackService from '$lib/services/HapticFeedbackService';

// Initial state for the option picker container
const initialState: OptionPickerState = {
	sequence: [],
	options: [],
	selectedPictograph: null,
	sortMethod: 'type',
	isLoading: false,
	error: null,
	lastSelectedTab: { type: 'all' },
	selectedTab: 'all'
};

/**
 * Creates an option picker container with the given initial state
 */
function createOptionPickerContainer() {
	// Create persistent UI state
	const persistentUIState = createPersistentObjectState('optionPickerUIState', {
		sortMethod: initialState.sortMethod,
		lastSelectedTab: initialState.lastSelectedTab
	});

	return createContainer<
		OptionPickerState,
		{
			loadOptions: (sequence: PictographData[]) => void;
			setSortMethod: (method: SortMethod) => void;
			setReversalFilter: (filter: ReversalFilter) => void;
			setLastSelectedTabForSort: (sortMethod: SortMethod, tabKey: string | null) => void;
			selectOption: (option: PictographData) => void;
			setSelectedTab: (tab: string | null) => void;
			reset: () => void;
		}
	>(
		// Initialize with both initial state and persisted UI state
		{
			...initialState,
			sortMethod: persistentUIState.sortMethod,
			lastSelectedTab: persistentUIState.lastSelectedTab
		},
		(state, update) => {
			// Helper function to persist UI state changes
			const persistUIState = () => {
				persistentUIState.sortMethod = state.sortMethod;
				persistentUIState.lastSelectedTab = state.lastSelectedTab;
			};

			return {
				loadOptions: (sequence: PictographData[]) => {
					// Don't try to load options if sequence is empty
					if (!sequence || sequence.length === 0) {
						console.warn('Attempted to load options with empty sequence');
						update((state) => {
							state.options = [];
							state.isLoading = false;
							state.error = null;
						});
						return;
					}

					update((state) => {
						state.sequence = sequence;
						state.isLoading = true;
						state.error = null;
					});

					try {
						const nextOptions = getNextOptions(sequence);

						// If we got no options, log a warning but don't treat it as an error
						if (!nextOptions || nextOptions.length === 0) {
							console.warn('No options available for the current sequence');
						}

						update((state) => {
							state.options = nextOptions || [];
							state.isLoading = false;
						});
					} catch (error) {
						console.error('Error loading options:', error);
						update((state) => {
							state.isLoading = false;
							state.error =
								error instanceof Error ? error.message : 'Unknown error loading options';
							state.options = [];
						});
					}
				},

				setSortMethod: (method: SortMethod) => {
					update((state) => {
						state.sortMethod = method;
					});
					persistUIState();
				},

				setReversalFilter: (filter: ReversalFilter) => {
					update((state) => {
						state.reversalFilter = filter;
					});
					persistUIState();
				},

				setLastSelectedTabForSort: (sortMethod: SortMethod, tabKey: string | null) => {
					// Avoid unnecessary updates if the value hasn't changed
					if (state.lastSelectedTab[sortMethod] === tabKey) {
						return;
					}

					update((state) => {
						state.lastSelectedTab = {
							...state.lastSelectedTab,
							[sortMethod]: tabKey
						};
					});
					persistUIState();
				},

				setSelectedTab: (tab: string | null) => {
					update((state) => {
						state.selectedTab = tab;
					});
				},

				selectOption: (option: PictographData) => {
					// First, update the selected pictograph
					update((state) => {
						state.selectedPictograph = option;
					});

					// Provide haptic feedback for selection
					if (browser) {
						hapticFeedbackService.trigger('selection');
					}

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
					if (browser) {
						const beatAddedEvent = new CustomEvent('beat-added', {
							detail: { beat: beatData },
							bubbles: true
						});
						document.dispatchEvent(beatAddedEvent);
					}
				},

				reset: () => {
					update((state) => {
						state.options = [];
						state.sequence = [];
						state.selectedPictograph = null;
						state.isLoading = false;
						state.error = null;
					});
				}
			};
		}
	);
}

// Create the option picker container instance
export const optionPickerContainer = createOptionPickerContainer();

// Create derived values
export const filteredOptions = createDerived(() => {
	const options = [...optionPickerContainer.state.options];
	options.sort(
		getSorter(optionPickerContainer.state.sortMethod, optionPickerContainer.state.sequence)
	);
	return options;
});

export const groupedOptions = createDerived(() => {
	const groups: Record<string, PictographData[]> = {};
	const options = filteredOptions.value;

	options.forEach((option: PictographData) => {
		const groupKey = determineGroupKey(
			option,
			optionPickerContainer.state.sortMethod,
			optionPickerContainer.state.sequence
		);
		if (!groups[groupKey]) groups[groupKey] = [];
		groups[groupKey].push(option);
	});

	const sortedKeys = getSortedGroupKeys(
		Object.keys(groups),
		optionPickerContainer.state.sortMethod
	);
	const sortedGroups: Record<string, PictographData[]> = {};

	sortedKeys.forEach((key) => {
		if (groups[key]) {
			sortedGroups[key] = groups[key];
		}
	});

	return sortedGroups;
});

export const optionsToDisplay = createDerived(() => {
	const selectedTab = optionPickerContainer.state.selectedTab;

	// When 'all' is selected, show all filtered options regardless of grouping
	if (selectedTab === 'all') {
		return filteredOptions.value;
	}

	// Otherwise, show the options for the selected category tab
	return (selectedTab && groupedOptions.value[selectedTab]) || [];
});

export const categoryKeys = createDerived(() => {
	return Object.keys(groupedOptions.value);
});
