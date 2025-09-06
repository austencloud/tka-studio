// src/lib/stores/browseTab/browseTabStore.ts
import { writable, derived, get } from 'svelte/store';
import { browser } from '$app/environment';
import type { Writable, Readable } from 'svelte/store';

// Define types for the browse tab
export type FilterType =
	| 'all'
	| 'favorites'
	| 'tag'
	| 'difficulty'
	| 'startingPosition'
	| 'startingLetter'
	| 'containsLetters'
	| 'length'
	| 'gridMode';

export type SortType = 'alphabetical' | 'difficulty' | 'dateAdded' | 'length';

export type SortDirection = 'asc' | 'desc';

export interface FilterCriteria {
	type: FilterType;
	value?: string | number | string[];
}

export interface SortCriteria {
	field: SortType;
	direction: SortDirection;
}

export interface SequenceVariation {
	id: string;
	thumbnailPath: string;
	metadata: {
		level?: number;
		author?: string;
		dateAdded?: string;
		gridMode?: string;
		startingPosition?: string;
		isFavorite?: boolean;
		length?: number;
		tags?: string[];
		[key: string]: any;
	};
}

export interface SequenceData {
	id: string;
	word: string;
	variations: SequenceVariation[];
	metadata: {
		level?: number;
		author?: string;
		dateAdded?: string;
		gridMode?: string;
		startingPosition?: string;
		length?: number;
		tags?: string[];
		[key: string]: any;
	};
}

export interface BrowseTabState {
	allSequences: SequenceData[];
	currentFilter: FilterCriteria;
	currentSort: SortCriteria;
	selectedSequenceId: string | null;
	selectedVariationIndex: number;
	isLoading: boolean;
	error: string | null;
}

// Create the main store
const createBrowseTabStore = () => {
	// Default state
	const defaultState: BrowseTabState = {
		allSequences: [],
		currentFilter: { type: 'all' },
		currentSort: { field: 'alphabetical', direction: 'asc' },
		selectedSequenceId: null,
		selectedVariationIndex: 0,
		isLoading: false,
		error: null
	};

	// Create the writable store
	const { subscribe, set, update } = writable<BrowseTabState>(defaultState);

	// Load state from localStorage if available
	const loadStateFromStorage = () => {
		if (!browser) return;

		try {
			const savedState = localStorage.getItem('browseTabState');
			if (savedState) {
				const parsedState = JSON.parse(savedState);
				// Only restore filter and sort preferences, not the sequence data
				update((state) => ({
					...state,
					currentFilter: parsedState.currentFilter || state.currentFilter,
					currentSort: parsedState.currentSort || state.currentSort
				}));
			}
		} catch (error) {
			console.error('Error loading browse tab state from localStorage:', error);
		}
	};

	// Save state to localStorage
	const saveStateToStorage = (state: BrowseTabState) => {
		if (!browser) return;

		try {
			// Only save filter and sort preferences, not the sequence data
			const stateToSave = {
				currentFilter: state.currentFilter,
				currentSort: state.currentSort
			};
			localStorage.setItem('browseTabState', JSON.stringify(stateToSave));
		} catch (error) {
			console.error('Error saving browse tab state to localStorage:', error);
		}
	};

	// Initialize the store
	if (browser) {
		loadStateFromStorage();
	}

	// Return the store with custom methods
	return {
		subscribe,

		// Load state from localStorage
		loadState: () => {
			loadStateFromStorage();
		},

		// Save state to localStorage
		saveState: () => {
			const state = get({ subscribe });
			saveStateToStorage(state);
		},

		// Load initial sequence data
		loadInitialData: async () => {
			update((state) => ({ ...state, isLoading: true, error: null }));

			try {
				const { fetchSequences } = await import('$lib/services/sequenceService');
				const sequences = await fetchSequences();

				update((state) => {
					const newState = {
						...state,
						allSequences: sequences,
						isLoading: false
					};
					saveStateToStorage(newState);
					return newState;
				});
			} catch (error) {
				update((state) => ({
					...state,
					isLoading: false,
					error: error instanceof Error ? error.message : 'Failed to load sequences'
				}));
			}
		},

		// Apply a filter
		applyFilter: (filterCriteria: FilterCriteria) => {
			update((state) => {
				const newState = {
					...state,
					currentFilter: filterCriteria,
					// Reset selection when filter changes
					selectedSequenceId: null,
					selectedVariationIndex: 0
				};
				saveStateToStorage(newState);
				return newState;
			});
		},

		// Apply a sort
		applySort: (sortCriteria: SortCriteria) => {
			update((state) => {
				const newState = {
					...state,
					currentSort: sortCriteria
				};
				saveStateToStorage(newState);
				return newState;
			});
		},

		// Select a sequence
		selectSequence: (sequenceId: string) => {
			update((state) => {
				// Find the sequence
				const sequence = state.allSequences.find((seq) => seq.id === sequenceId);

				// If sequence not found, don't update
				if (!sequence) return state;

				return {
					...state,
					selectedSequenceId: sequenceId,
					selectedVariationIndex: 0 // Reset to first variation
				};
			});
		},

		// Select a variation
		selectVariation: (index: number) => {
			update((state) => {
				// Find the sequence
				const sequence = state.allSequences.find((seq) => seq.id === state.selectedSequenceId);

				// If sequence not found or index out of bounds, don't update
				if (!sequence || index < 0 || index >= sequence.variations.length) return state;

				return {
					...state,
					selectedVariationIndex: index
				};
			});
		},

		// Toggle favorite status
		toggleFavorite: async (sequenceId: string, variationId: string) => {
			// Get current state
			const state = get({ subscribe });

			// Find the sequence and variation
			const sequence = state.allSequences.find((seq) => seq.id === sequenceId);
			if (!sequence) return;

			const variationIndex = sequence.variations.findIndex((v) => v.id === variationId);
			if (variationIndex === -1) return;

			// Get current favorite status
			const isFavorite = sequence.variations[variationIndex].metadata.isFavorite || false;

			// Update optimistically
			update((state) => {
				const newSequences = [...state.allSequences];
				const sequenceIndex = newSequences.findIndex((seq) => seq.id === sequenceId);

				if (sequenceIndex !== -1) {
					newSequences[sequenceIndex] = {
						...newSequences[sequenceIndex],
						variations: [...newSequences[sequenceIndex].variations]
					};

					newSequences[sequenceIndex].variations[variationIndex] = {
						...newSequences[sequenceIndex].variations[variationIndex],
						metadata: {
							...newSequences[sequenceIndex].variations[variationIndex].metadata,
							isFavorite: !isFavorite
						}
					};
				}

				return { ...state, allSequences: newSequences };
			});

			// Call API
			try {
				const { updateFavoriteStatus } = await import('$lib/services/sequenceService');
				await updateFavoriteStatus(sequenceId, variationId, !isFavorite);
			} catch (error) {
				// Revert on error
				update((state) => {
					const newSequences = [...state.allSequences];
					const sequenceIndex = newSequences.findIndex((seq) => seq.id === sequenceId);

					if (sequenceIndex !== -1) {
						newSequences[sequenceIndex] = {
							...newSequences[sequenceIndex],
							variations: [...newSequences[sequenceIndex].variations]
						};

						newSequences[sequenceIndex].variations[variationIndex] = {
							...newSequences[sequenceIndex].variations[variationIndex],
							metadata: {
								...newSequences[sequenceIndex].variations[variationIndex].metadata,
								isFavorite: isFavorite
							}
						};
					}

					return {
						...state,
						allSequences: newSequences,
						error: error instanceof Error ? error.message : 'Failed to update favorite status'
					};
				});
			}
		},

		// Delete a variation
		deleteVariation: async (sequenceId: string, variationId: string) => {
			// Get current state
			const state = get({ subscribe });

			// Find the sequence
			const sequence = state.allSequences.find((seq) => seq.id === sequenceId);
			if (!sequence) return;

			// Store original sequences for potential rollback
			const originalSequences = state.allSequences;

			// Update optimistically
			update((state) => {
				const newSequences = [...state.allSequences];
				const sequenceIndex = newSequences.findIndex((seq) => seq.id === sequenceId);

				if (sequenceIndex !== -1) {
					// Filter out the deleted variation
					const newVariations = newSequences[sequenceIndex].variations.filter(
						(v) => v.id !== variationId
					);

					// If this was the last variation, remove the entire sequence
					if (newVariations.length === 0) {
						newSequences.splice(sequenceIndex, 1);

						return {
							...state,
							allSequences: newSequences,
							selectedSequenceId: null,
							selectedVariationIndex: 0
						};
					} else {
						// Otherwise, update the sequence with the remaining variations
						newSequences[sequenceIndex] = {
							...newSequences[sequenceIndex],
							variations: newVariations
						};

						// Adjust selected variation index if needed
						let newVariationIndex = state.selectedVariationIndex;
						if (newVariationIndex >= newVariations.length) {
							newVariationIndex = newVariations.length - 1;
						}

						return {
							...state,
							allSequences: newSequences,
							selectedVariationIndex: newVariationIndex
						};
					}
				}

				return state;
			});

			// Call API
			try {
				const { deleteVariationApi } = await import('$lib/services/sequenceService');
				await deleteVariationApi(sequenceId, variationId);
			} catch (error) {
				// Revert on error
				update((state) => ({
					...state,
					allSequences: originalSequences,
					error: error instanceof Error ? error.message : 'Failed to delete variation'
				}));
			}
		},

		// Delete an entire sequence
		deleteSequence: async (sequenceId: string) => {
			// Get current state
			const state = get({ subscribe });

			// Store original sequences for potential rollback
			const originalSequences = state.allSequences;

			// Update optimistically
			update((state) => {
				const newSequences = state.allSequences.filter((seq) => seq.id !== sequenceId);

				return {
					...state,
					allSequences: newSequences,
					selectedSequenceId: null,
					selectedVariationIndex: 0
				};
			});

			// Call API
			try {
				const { deleteSequenceApi } = await import('$lib/services/sequenceService');
				await deleteSequenceApi(sequenceId);
			} catch (error) {
				// Revert on error
				update((state) => ({
					...state,
					allSequences: originalSequences,
					error: error instanceof Error ? error.message : 'Failed to delete sequence'
				}));
			}
		},

		// Reset any error
		clearError: () => {
			update((state) => ({ ...state, error: null }));
		}
	};
};

// Create the store instance
export const browseTabStore = createBrowseTabStore();

// Create derived stores for filtered and grouped sequences
export const filteredSequences: Readable<SequenceData[]> = derived(
	browseTabStore,
	($browseTabStore) => {
		const { allSequences, currentFilter } = $browseTabStore;

		// Apply filtering
		return allSequences.filter((sequence) => {
			switch (currentFilter.type) {
				case 'all':
					return true;

				case 'favorites':
					// Check if any variation is a favorite
					return sequence.variations.some((v) => v.metadata.isFavorite);

				case 'tag':
					// Check if sequence has the specified tag
					return sequence.metadata.tags?.includes(currentFilter.value as string) || false;

				case 'difficulty':
					// Check if sequence difficulty matches
					return sequence.metadata.level === currentFilter.value;

				case 'startingPosition':
					// Check if starting position matches
					return sequence.metadata.startingPosition === currentFilter.value;

				case 'startingLetter':
					// Check if word starts with the specified letter
					return sequence.word
						.toLowerCase()
						.startsWith((currentFilter.value as string).toLowerCase());

				case 'containsLetters':
					// Check if word contains all specified letters
					const letters = currentFilter.value as string[];
					return letters.every((letter) =>
						sequence.word.toLowerCase().includes(letter.toLowerCase())
					);

				case 'length':
					// Check if sequence length matches
					return sequence.metadata.length === currentFilter.value;

				case 'gridMode':
					// Check if grid mode matches
					return sequence.metadata.gridMode === currentFilter.value;

				default:
					return true;
			}
		});
	}
);

export const sortedSequences: Readable<SequenceData[]> = derived(
	[filteredSequences, browseTabStore],
	([$filteredSequences, $browseTabStore]) => {
		const { currentSort } = $browseTabStore;

		// Create a copy to avoid mutating the original
		const sequences = [...$filteredSequences];

		// Apply sorting
		return sequences.sort((a, b) => {
			const direction = currentSort.direction === 'asc' ? 1 : -1;

			switch (currentSort.field) {
				case 'alphabetical':
					return direction * a.word.localeCompare(b.word);

				case 'difficulty':
					const levelA = a.metadata.level || 0;
					const levelB = b.metadata.level || 0;
					return direction * (levelA - levelB);

				case 'dateAdded':
					const dateA = a.metadata.dateAdded ? new Date(a.metadata.dateAdded).getTime() : 0;
					const dateB = b.metadata.dateAdded ? new Date(b.metadata.dateAdded).getTime() : 0;
					return direction * (dateA - dateB);

				case 'length':
					const lengthA = a.metadata.length || 0;
					const lengthB = b.metadata.length || 0;
					return direction * (lengthA - lengthB);

				default:
					return 0;
			}
		});
	}
);

export const groupedSequences: Readable<{ section: string; sequences: SequenceData[] }[]> = derived(
	[sortedSequences, browseTabStore],
	([$sortedSequences, $browseTabStore]) => {
		const { currentSort } = $browseTabStore;

		// Group sequences based on sort field
		const groups: Record<string, SequenceData[]> = {};

		$sortedSequences.forEach((sequence) => {
			let sectionKey: string;

			switch (currentSort.field) {
				case 'alphabetical':
					// Group by first letter
					sectionKey = sequence.word.charAt(0).toUpperCase();
					break;

				case 'difficulty':
					// Group by difficulty level
					sectionKey = `Level ${sequence.metadata.level || 'Unknown'}`;
					break;

				case 'dateAdded':
					// Group by month/year
					if (sequence.metadata.dateAdded) {
						const date = new Date(sequence.metadata.dateAdded);
						sectionKey = `${date.toLocaleString('default', { month: 'long' })} ${date.getFullYear()}`;
					} else {
						sectionKey = 'Unknown Date';
					}
					break;

				case 'length':
					// Group by length
					sectionKey = `${sequence.metadata.length || 'Unknown'} Beats`;
					break;

				default:
					sectionKey = 'All';
			}

			// Initialize group if it doesn't exist
			if (!groups[sectionKey]) {
				groups[sectionKey] = [];
			}

			// Add sequence to group
			groups[sectionKey].push(sequence);
		});

		// Convert groups object to array
		return Object.entries(groups).map(([section, sequences]) => ({
			section,
			sequences
		}));
	}
);

export const selectedSequenceData: Readable<{
	sequence: SequenceData | null;
	variation: SequenceVariation | null;
}> = derived(browseTabStore, ($browseTabStore) => {
	const { allSequences, selectedSequenceId, selectedVariationIndex } = $browseTabStore;

	// Find selected sequence
	const sequence = allSequences.find((seq) => seq.id === selectedSequenceId) || null;

	// Find selected variation
	const variation =
		sequence && selectedVariationIndex >= 0 && selectedVariationIndex < sequence.variations.length
			? sequence.variations[selectedVariationIndex]
			: null;

	return { sequence, variation };
});
