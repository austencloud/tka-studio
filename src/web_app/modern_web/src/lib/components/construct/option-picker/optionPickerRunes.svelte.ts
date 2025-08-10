/**
 * Sophisticated Option Picker State using ONLY Svelte 5 Runes
 *
 * Complete port of the legacy system with advanced features using pure runes:
 * - 		if (sequence && sequence.length > 			// For empty sequence, try to get start position from localStorage
			const startPositionData = localStorage.getItem('start_position');
			if (startPositionData) {
				const startPosition = JSON.parse(startPositionData);
				const endPosition = typeof startPosition.endPos === 'string' ? startPosition.endPos : null;
				if (endPosition) {
					console.log(`🎯 Runes loading options for start position: ${endPosition}`);

					const optionDataService = new OptionDataService();
					await optionDataService.initialize();

					nextOptions = await optionDataService.getNextOptionsFromEndPosition(
						endPosition,
						GridMode.DIAMOND,
						{}
					);astBeat = sequence[sequence.length - 1];
			const endPosition = typeof lastBeat?.end_position === 'string' ? lastBeat.end_position :
				typeof lastBeat?.metadata?.endPosition === 'string' ? lastBeat.metadata.endPosition : null;

			if (endPosition && typeof endPosition === 'string') {
				console.log(`🎯 Runes loading options for end position: ${endPosition}`);

				// Create OptionDataService instance
				const optionDataService = new OptionDataService();
				await optionDataService.initialize();

				nextOptions = await optionDataService.getNextOptionsFromEndPosition(
					endPosition,
					GridMode.DIAMOND,
					{} // No filters
				);ate management
 * - Sophisticated filtering and grouping
 * - Real option data service integration
 * - Performance optimizations
 * - Complex reactive state derivations
 */

import { GridMode } from '$lib/domain/enums';
import type { PictographData } from '$lib/domain/PictographData';
import { OptionDataService } from '$services/implementations/OptionDataService';
import type { ReversalFilter, SortMethod } from './config';
import { determineGroupKey, getSortedGroupKeys, getSorter } from './services/OptionsService';

// ===== Types =====
export type LastSelectedTabState = Partial<Record<SortMethod, string | null>>;

interface UIState {
	sortMethod: SortMethod;
	isLoading: boolean;
	error: string | null;
	lastSelectedTab: LastSelectedTabState;
}

// ===== Helper Functions =====
function getStoredState(): UIState {
	if (typeof window === 'undefined')
		return {
			sortMethod: 'type',
			isLoading: false,
			error: null,
			lastSelectedTab: {},
		};

	try {
		const stored = localStorage.getItem('optionPickerUIState');

		if (!stored)
			return {
				sortMethod: 'type',
				isLoading: false,
				error: null,
				lastSelectedTab: { type: 'all' },
			};

		const parsed = JSON.parse(stored);

		return {
			sortMethod: parsed.sortMethod || 'type',
			isLoading: false,
			error: null,
			lastSelectedTab: parsed.lastSelectedTab || { type: 'all' },
		};
	} catch (e) {
		console.error('Error reading from localStorage:', e);
		return {
			sortMethod: 'type',
			isLoading: false,
			error: null,
			lastSelectedTab: { type: 'all' },
		};
	}
}

function saveStateToLocalStorage(state: UIState) {
	if (typeof window === 'undefined') return;

	try {
		const saveData = {
			sortMethod: state.sortMethod,
			lastSelectedTab: state.lastSelectedTab,
		};
		localStorage.setItem('optionPickerUIState', JSON.stringify(saveData));
	} catch (e) {
		console.error('Error writing to localStorage:', e);
	}
}

/**
 * Create sophisticated option picker state using ONLY Svelte 5 runes
 */
export function createOptionPickerRunes() {
	// ===== Core State Using Runes =====
	let sequenceData = $state<PictographData[]>([]);
	let optionsData = $state<PictographData[]>([]);
	let selectedPictograph = $state<PictographData | null>(null);

	// ===== UI State Using Runes =====
	const storedState = getStoredState();
	let uiState = $state<UIState>({
		sortMethod: storedState.sortMethod,
		isLoading: storedState.isLoading,
		error: storedState.error,
		lastSelectedTab: storedState.lastSelectedTab,
	});

	// ===== Derived State Using Runes =====

	// Filtered and sorted options
	const filteredOptions = $derived(() => {
		const options = [...optionsData];
		options.sort(getSorter(uiState.sortMethod, sequenceData));
		return options;
	});

	// Grouped options based on sort method
	const groupedOptions = $derived(() => {
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

	// Category keys available
	const categoryKeys = $derived(() => Object.keys(groupedOptions));

	// ===== State Persistence Effect =====
	$effect(() => {
		// Save state changes to localStorage
		saveStateToLocalStorage(uiState);
	});

	// ===== Actions =====
	async function loadOptions(sequence: PictographData[]) {
		console.log('🚀 Runes loadOptions called with sequence:', {
			sequenceLength: sequence?.length || 0,
			isEmpty: !sequence || sequence.length === 0,
		});

		// For empty sequence, load from start position
		if (!sequence || sequence.length === 0) {
			console.log('🎯 Empty sequence - loading from start position...');
			// Don't return early - continue to load from start position
		}

		sequenceData = sequence;

		// **NEW: Check for preloaded options first to avoid loading state**
		try {
			// First check for specific preloaded options (from individual clicks)
			const preloadedData = localStorage.getItem('preloaded_options');
			if (preloadedData) {
				console.log('✨ Using individually preloaded options for seamless transition');
				const preloadedOptions = JSON.parse(preloadedData);
				console.log(
					`🔧 Runes setting optionsData with ${preloadedOptions?.length || 0} preloaded options`
				);
				optionsData = preloadedOptions || [];
				uiState.isLoading = false;
				uiState.error = null;

				// Clear preloaded data so it's only used once
				localStorage.removeItem('preloaded_options');

				// Set default tab if needed
				if (
					!uiState.lastSelectedTab[uiState.sortMethod] ||
					uiState.lastSelectedTab[uiState.sortMethod] === null
				) {
					console.log('No tab selected yet, defaulting to "all"');
					setLastSelectedTabForSort(uiState.sortMethod, 'all');
				}

				return; // Skip the loading process
			}

			// Check for bulk preloaded options (from component load)
			const allPreloadedData = localStorage.getItem('all_preloaded_options');
			if (allPreloadedData) {
				const allPreloadedOptions = JSON.parse(allPreloadedData);

				// Determine the current end position we need options for
				let targetEndPosition: string | null = null;

				if (sequence && sequence.length > 0) {
					const lastBeat = sequence[sequence.length - 1];
					const endPos = lastBeat?.end_position || lastBeat?.metadata?.endPosition;
					targetEndPosition = typeof endPos === 'string' ? endPos : null;
				} else {
					// For empty sequence, get from start position
					const startPositionData = localStorage.getItem('start_position');
					if (startPositionData) {
						const startPosition = JSON.parse(startPositionData);
						targetEndPosition = startPosition.endPos || null;
					}
				}

				// If we have preloaded options for this end position, use them
				if (targetEndPosition && allPreloadedOptions[targetEndPosition]) {
					console.log(
						`✨ Using bulk preloaded options for end position: ${targetEndPosition}`
					);
					const optionsForPosition = allPreloadedOptions[targetEndPosition];
					console.log(
						`🔧 Runes setting optionsData with ${optionsForPosition?.length || 0} bulk preloaded options`
					);
					optionsData = optionsForPosition || [];
					uiState.isLoading = false;
					uiState.error = null;

					// Set default tab if needed
					if (
						!uiState.lastSelectedTab[uiState.sortMethod] ||
						uiState.lastSelectedTab[uiState.sortMethod] === null
					) {
						console.log('No tab selected yet, defaulting to "all"');
						setLastSelectedTabForSort(uiState.sortMethod, 'all');
					}

					return; // Skip the loading process
				}
			}
		} catch (error) {
			console.warn(
				'Failed to load preloaded options, falling back to normal loading:',
				error
			);
		}

		// Normal loading process (only if no preloaded options)
		// Note: Set loading state here to avoid brief flash when preloaded data exists
		uiState.isLoading = true;
		uiState.error = null;

		try {
			// Extract end position from sequence for the real OptionDataService
			let nextOptions: PictographData[] = [];

			if (sequence && sequence.length > 0) {
				const lastBeat = sequence[sequence.length - 1];
				const endPosition = lastBeat?.end_position || lastBeat?.metadata?.endPosition;

				if (endPosition && typeof endPosition === 'string') {
					console.log(`🎯 Runes loading options for end position: ${endPosition}`);

					// Create OptionDataService instance
					const optionDataService = new OptionDataService();
					await optionDataService.initialize();

					nextOptions = await optionDataService.getNextOptionsFromEndPosition(
						endPosition,
						GridMode.DIAMOND,
						{} // No filters
					);
				} else {
					console.warn('No end position found in sequence');
				}
			} else {
				// For empty sequence, try to get start position from localStorage
				const startPositionData = localStorage.getItem('start_position');
				if (startPositionData) {
					const startPosition = JSON.parse(startPositionData);
					const endPosition =
						typeof startPosition.endPos === 'string' ? startPosition.endPos : null;
					if (endPosition) {
						console.log(`🎯 Runes loading options for start position: ${endPosition}`);

						const optionDataService = new OptionDataService();
						await optionDataService.initialize();

						nextOptions = await optionDataService.getNextOptionsFromEndPosition(
							endPosition,
							GridMode.DIAMOND,
							{}
						);
					}
				}
			}

			// If we got no options, log a warning but don't treat it as an error
			if (!nextOptions || nextOptions.length === 0) {
				console.warn('No options available for the current sequence');
			}

			console.log(`🔧 Runes setting optionsData with ${nextOptions?.length || 0} options`);
			optionsData = nextOptions || [];
			console.log(`🔧 Runes optionsData set, current length: ${optionsData.length}`);
			uiState.isLoading = false;

			// Only set default tab if we don't have a selected tab yet
			if (
				!uiState.lastSelectedTab[uiState.sortMethod] ||
				uiState.lastSelectedTab[uiState.sortMethod] === null
			) {
				console.log('No tab selected yet, defaulting to "all"');
				setLastSelectedTabForSort(uiState.sortMethod, 'all');

				if (typeof document !== 'undefined') {
					const viewChangeEvent = new CustomEvent('viewchange', {
						detail: { mode: 'all' },
						bubbles: true,
					});
					document.dispatchEvent(viewChangeEvent);
				}
			}
		} catch (error) {
			console.error('Error loading options:', error);
			uiState.isLoading = false;
			uiState.error =
				error instanceof Error ? error.message : 'Unknown error loading options';
			optionsData = [];
		}
	}

	function setSortMethod(method: SortMethod) {
		uiState.sortMethod = method;
	}

	function setReversalFilter(filter: ReversalFilter) {
		// Note: ReversalFilter would need to be added to UIState if needed
		console.log('Setting reversal filter:', filter);
	}

	function setLastSelectedTabForSort(sortMethod: SortMethod, tabKey: string | null) {
		// Avoid unnecessary updates if the value hasn't changed
		if (uiState.lastSelectedTab[sortMethod] === tabKey) {
			return;
		}

		uiState.lastSelectedTab = {
			...uiState.lastSelectedTab,
			[sortMethod]: tabKey,
		};
	}

	async function selectOption(option: PictographData) {
		// Update selected pictograph
		selectedPictograph = option;

		// Dispatch custom events
		if (typeof document !== 'undefined') {
			const beatAddedEvent = new CustomEvent('beat-added', {
				detail: { beat: option },
				bubbles: true,
			});
			document.dispatchEvent(beatAddedEvent);

			const optionSelectedEvent = new CustomEvent('option-selected', {
				detail: { option },
				bubbles: true,
			});
			document.dispatchEvent(optionSelectedEvent);
		}
	}

	function reset() {
		optionsData = [];
		sequenceData = [];

		// Preserve user preferences
		const currentSortMethod = uiState.sortMethod || 'type';
		uiState = {
			sortMethod: currentSortMethod,
			isLoading: false,
			error: null,
			lastSelectedTab: uiState.lastSelectedTab || {},
		};

		// Ensure 'all' is set as the default tab for the current sort method
		setLastSelectedTabForSort(currentSortMethod, 'all');
		selectedPictograph = null;
	}

	function setLoading(loading: boolean) {
		uiState.isLoading = loading;
	}

	function setError(error: string | null) {
		uiState.error = error;
	}

	// ===== Return Reactive Interface =====
	return {
		// ✅ FIXED: Use getters that access the state directly for reactivity
		get optionsData() {
			return optionsData;
		},
		get sequenceData() {
			return sequenceData;
		},
		get selectedPictograph() {
			return selectedPictograph;
		},
		get filteredOptions() {
			return filteredOptions();
		},
		get groupedOptions() {
			return groupedOptions();
		},
		get categoryKeys() {
			return categoryKeys();
		},

		// ✅ Keep getters for backward compatibility, but prefer direct access above
		get sequence() {
			return sequenceData;
		},
		get allOptions() {
			return optionsData;
		},
		get isLoading() {
			return uiState.isLoading;
		},
		get error() {
			return uiState.error;
		},
		get sortMethod() {
			return uiState.sortMethod;
		},
		get lastSelectedTab() {
			return uiState.lastSelectedTab;
		},

		// Actions
		loadOptions,
		setSortMethod,
		setReversalFilter,
		setLastSelectedTabForSort,
		selectOption,
		reset,
		setLoading,
		setError,

		// Direct state setters (for advanced use)
		setSequence: (seq: PictographData[]) => {
			sequenceData = seq;
		},
		setOptions: (opts: PictographData[]) => {
			console.log('🔧 setOptions called with:', {
				optionsCount: opts?.length,
				firstOption: opts?.[0]?.letter,
				currentOptionsDataLength: optionsData?.length,
			});
			optionsData = opts;
			console.log('🔧 setOptions completed, new optionsData length:', optionsData?.length);
		},
		setSelectedPictograph: (opt: PictographData | null) => {
			selectedPictograph = opt;
		},
	};
}
/**
 * Type for the option picker runes instance
 */
export type OptionPickerRunes = ReturnType<typeof createOptionPickerRunes>;
