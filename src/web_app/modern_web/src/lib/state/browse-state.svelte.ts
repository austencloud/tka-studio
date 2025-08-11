/**
 * Browse State - Runes Implementation
 *
 * Reactive state management for browse functionality using Svelte 5 runes.
 * Wraps browse services for UI reactivity while keeping business logic in services.
 */

import {
	NavigationMode,
	SortMethod as SortMethodEnum,
	createDefaultDisplayState,
	createDefaultLoadingState,
} from '$lib/domain/browse';
import type {
	BrowseDisplayState,
	BrowseLoadingState,
	BrowseSequenceMetadata,
	FilterType,
	FilterValue,
	IBrowseService,
	ISequenceIndexService,
	IThumbnailService,
	SortMethod,
} from '$lib/services/interfaces';

export function createBrowseState(
	browseService: IBrowseService,
	thumbnailService: IThumbnailService,
	sequenceIndexService: ISequenceIndexService
) {
	// ✅ PURE RUNES: Reactive state for UI
	let allSequences = $state<BrowseSequenceMetadata[]>([]);
	let filteredSequences = $state<BrowseSequenceMetadata[]>([]);
	let displayedSequences = $state<BrowseSequenceMetadata[]>([]);
	let selectedSequence = $state<BrowseSequenceMetadata | null>(null);

	// Navigation and filtering state
	let currentFilter = $state<{ type: FilterType; value: FilterValue } | null>(null);
	let currentSort = $state<SortMethod>(SortMethodEnum.ALPHABETICAL);
	let navigationMode = $state<NavigationMode>(NavigationMode.FILTER_SELECTION);

	// UI state
	const loadingState = $state<BrowseLoadingState>(createDefaultLoadingState());
	let displayState = $state<BrowseDisplayState>(createDefaultDisplayState());
	let searchQuery = $state<string>('');

	// ✅ DERIVED RUNES: Computed values
	const isLoading = $derived(loadingState.isLoading);
	const hasSequences = $derived(displayedSequences.length > 0);
	const hasError = $derived(loadingState.error !== null);
	const sequenceCount = $derived(displayedSequences.length);
	const sortedSections = $derived(() => {
		if (displayedSequences.length === 0) return {};
		// This will be computed by grouping sequences
		return groupSequencesBySection(displayedSequences, currentSort);
	});

	// ✅ RUNES METHODS: UI state management that delegates to services
	async function loadAllSequences() {
		try {
			loadingState.isLoading = true;
			loadingState.currentOperation = 'Loading sequences...';
			loadingState.error = null;

			// Delegate to service for business logic
			const sequences = await browseService.loadSequenceMetadata();

			// Update reactive state
			allSequences = sequences;
			filteredSequences = sequences;
			displayedSequences = sequences;

			loadingState.isLoading = false;
			loadingState.loadedCount = sequences.length;
			loadingState.totalCount = sequences.length;
		} catch (error) {
			loadingState.isLoading = false;
			loadingState.error =
				error instanceof Error ? error.message : 'Failed to load sequences';
		}
	}

	async function applyFilter(filterType: FilterType, filterValue: FilterValue) {
		try {
			console.log('🎯 browse-state.applyFilter() called with:', filterType, filterValue);
			loadingState.isLoading = true;
			loadingState.currentOperation = 'Applying filter...';

			// Update current filter state
			currentFilter = { type: filterType, value: filterValue };
			console.log('📝 Updated currentFilter:', currentFilter);

			console.log('📊 allSequences available:', allSequences.length, 'items');

			// Delegate filtering to service
			const filtered = await browseService.applyFilter(allSequences, filterType, filterValue);
			console.log('🔍 Filtered sequences received:', filtered.length, 'items');

			// Apply current sort
			const sorted = await browseService.sortSequences(filtered, currentSort);
			console.log('📈 Sorted sequences:', sorted.length, 'items');

			// Update reactive state
			filteredSequences = filtered;
			displayedSequences = sorted;
			navigationMode = NavigationMode.SEQUENCE_BROWSER;

			loadingState.isLoading = false;
		} catch (error) {
			loadingState.isLoading = false;
			loadingState.error = error instanceof Error ? error.message : 'Failed to apply filter';
		}
	}

	async function updateSort(sortMethod: SortMethod) {
		try {
			currentSort = sortMethod;

			// Delegate sorting to service
			const sorted = await browseService.sortSequences(filteredSequences, sortMethod);

			// Update reactive state
			displayedSequences = sorted;
		} catch (error) {
			loadingState.error =
				error instanceof Error ? error.message : 'Failed to sort sequences';
		}
	}

	async function searchSequences(query: string) {
		try {
			searchQuery = query;

			if (!query.trim()) {
				// Reset to filtered sequences if no search query
				displayedSequences = filteredSequences;
				return;
			}

			loadingState.isLoading = true;
			loadingState.currentOperation = 'Searching...';

			// Delegate search to service
			const searchResults = await sequenceIndexService.searchSequences(query);

			// Filter search results by current filter if one is applied
			let results = searchResults;
			if (currentFilter) {
				results = await browseService.applyFilter(
					searchResults,
					currentFilter.type,
					currentFilter.value
				);
			}

			// Apply current sort
			const sorted = await browseService.sortSequences(results, currentSort);

			displayedSequences = sorted;
			loadingState.isLoading = false;
		} catch (error) {
			loadingState.isLoading = false;
			loadingState.error = error instanceof Error ? error.message : 'Search failed';
		}
	}

	function selectSequence(sequence: BrowseSequenceMetadata) {
		selectedSequence = sequence;
	}

	function clearSelection() {
		selectedSequence = null;
	}

	function backToFilters() {
		navigationMode = NavigationMode.FILTER_SELECTION;
		currentFilter = null;
		searchQuery = '';
		displayedSequences = allSequences;
	}

	async function preloadThumbnails(sequences: BrowseSequenceMetadata[]) {
		try {
			const thumbnailsToPreload = sequences
				.slice(0, 20) // Preload first 20 thumbnails
				.flatMap((seq) =>
					seq.thumbnails.map((thumb) => ({
						sequenceId: seq.id,
						thumbnailPath: thumb,
					}))
				);

			await thumbnailService.preloadThumbnails(thumbnailsToPreload);
		} catch (error) {
			console.warn('Failed to preload thumbnails:', error);
		}
	}

	function getThumbnailUrl(sequenceId: string, thumbnailPath: string): string {
		return thumbnailService.getThumbnailUrl(sequenceId, thumbnailPath);
	}

	function updateDisplaySettings(settings: Partial<BrowseDisplayState>) {
		displayState = { ...displayState, ...settings };
	}

	function clearError() {
		loadingState.error = null;
	}

	// ✅ RUNES EFFECT: Auto-preload thumbnails when sequences change
	$effect(() => {
		if (displayedSequences.length > 0) {
			preloadThumbnails(displayedSequences);
		}
	});

	// Helper function for derived sections
	function groupSequencesBySection(
		sequences: BrowseSequenceMetadata[],
		sortMethod: SortMethod
	): Record<string, BrowseSequenceMetadata[]> {
		const sections: Record<string, BrowseSequenceMetadata[]> = {};

		for (const sequence of sequences) {
			const sectionKey = getSectionKey(sequence, sortMethod);
			if (!sections[sectionKey]) {
				sections[sectionKey] = [];
			}
			sections[sectionKey].push(sequence);
		}

		return sections;
	}

	function getSectionKey(sequence: BrowseSequenceMetadata, sortMethod: SortMethod): string {
		switch (sortMethod) {
			case SortMethodEnum.ALPHABETICAL:
				return sequence.word[0]?.toUpperCase() || '#';
			case SortMethodEnum.DIFFICULTY_LEVEL:
				return sequence.difficultyLevel || 'Unknown';
			case SortMethodEnum.AUTHOR:
				return sequence.author || 'Unknown';
			case SortMethodEnum.SEQUENCE_LENGTH:
				const length = sequence.sequenceLength || 0;
				if (length <= 4) return '3-4 beats';
				if (length <= 6) return '5-6 beats';
				if (length <= 8) return '7-8 beats';
				return '9+ beats';
			default:
				return 'All';
		}
	}

	return {
		// ✅ REACTIVE STATE GETTERS
		get allSequences() {
			return allSequences;
		},
		get displayedSequences() {
			return displayedSequences;
		},
		get selectedSequence() {
			return selectedSequence;
		},
		get currentFilter() {
			return currentFilter;
		},
		get currentSort() {
			return currentSort;
		},
		get navigationMode() {
			return navigationMode;
		},
		get searchQuery() {
			return searchQuery;
		},

		// ✅ DERIVED STATE GETTERS
		get isLoading() {
			return isLoading;
		},
		get hasSequences() {
			return hasSequences;
		},
		get hasError() {
			return hasError;
		},
		get sequenceCount() {
			return sequenceCount;
		},
		get sortedSections() {
			return sortedSections;
		},
		get loadingState() {
			return loadingState;
		},
		get displayState() {
			return displayState;
		},

		// ✅ ACTION METHODS
		loadAllSequences,
		applyFilter,
		updateSort,
		searchSequences,
		selectSequence,
		clearSelection,
		backToFilters,
		getThumbnailUrl,
		updateDisplaySettings,
		clearError,
	};
}

export type BrowseState = ReturnType<typeof createBrowseState>;
