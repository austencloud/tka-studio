import { writable, derived } from 'svelte/store';
import type { Act, Sequence, Beat } from '../models/Act';
import { createEmptyAct } from '../models/Act';
import { browser } from '$app/environment';

// Constants
const STORAGE_KEY = 'current_act';
const DEFAULT_ROWS = 24;
const DEFAULT_COLUMNS = 8;

// Define history entry for undo/redo
interface HistoryEntry {
	act: Act;
	description: string;
	timestamp: number;
}

// Define the store state interface
interface ActStoreState {
	act: Act;
	isLoading: boolean;
	error: string | null;
	isDirty: boolean;
	history: HistoryEntry[];
	historyIndex: number;
	maxHistorySize: number;
}

// Create the initial state
const initialState: ActStoreState = {
	act: createEmptyAct(DEFAULT_ROWS, DEFAULT_COLUMNS),
	isLoading: false,
	error: null,
	isDirty: false,
	history: [],
	historyIndex: -1,
	maxHistorySize: 20 // Store up to 20 history entries
};

// Create the writable store
function createActStore() {
	const { subscribe, set, update } = writable<ActStoreState>(initialState);

	// Helper function to add a history entry
	function addHistoryEntry(state: ActStoreState, description: string): ActStoreState {
		// Create a deep copy of the current act
		const actCopy = JSON.parse(JSON.stringify(state.act)) as Act;

		// Create a new history entry
		const newEntry: HistoryEntry = {
			act: actCopy,
			description,
			timestamp: Date.now()
		};

		// Create a new history array, removing any entries after the current index
		const newHistory = state.history.slice(0, state.historyIndex + 1);

		// Add the new entry
		newHistory.push(newEntry);

		// Trim history if it exceeds the maximum size
		if (newHistory.length > state.maxHistorySize) {
			newHistory.shift(); // Remove the oldest entry
		}

		// Return the updated state
		return {
			...state,
			history: newHistory,
			historyIndex: newHistory.length - 1
		};
	}

	return {
		subscribe,

		/**
		 * Undo the last action
		 * @returns The description of the undone action, or null if nothing to undo
		 */
		undo: () => {
			let undoneActionDescription: string | null = null;

			update((state) => {
				// Check if we can undo
				if (state.historyIndex <= 0) {
					return state; // Nothing to undo
				}

				// Get the previous history entry
				const previousIndex = state.historyIndex - 1;
				const previousEntry = state.history[previousIndex];

				// Store the description of the action being undone
				undoneActionDescription = state.history[state.historyIndex].description;

				// Return the updated state
				return {
					...state,
					act: JSON.parse(JSON.stringify(previousEntry.act)),
					historyIndex: previousIndex,
					isDirty: true
				};
			});

			return undoneActionDescription;
		},

		/**
		 * Redo the last undone action
		 * @returns The description of the redone action, or null if nothing to redo
		 */
		redo: () => {
			let redoneActionDescription: string | null = null;

			update((state) => {
				// Check if we can redo
				if (state.historyIndex >= state.history.length - 1) {
					return state; // Nothing to redo
				}

				// Get the next history entry
				const nextIndex = state.historyIndex + 1;
				const nextEntry = state.history[nextIndex];

				// Store the description of the action being redone
				redoneActionDescription = nextEntry.description;

				// Return the updated state
				return {
					...state,
					act: JSON.parse(JSON.stringify(nextEntry.act)),
					historyIndex: nextIndex,
					isDirty: true
				};
			});

			return redoneActionDescription;
		},

		/**
		 * Check if undo is available
		 */
		canUndo: () => {
			let result = false;
			update((state) => {
				result = state.historyIndex > 0;
				return state;
			});
			return result;
		},

		/**
		 * Check if redo is available
		 */
		canRedo: () => {
			let result = false;
			update((state) => {
				result = state.historyIndex < state.history.length - 1;
				return state;
			});
			return result;
		},

		/**
		 * Initialize the act store by loading from localStorage or creating a new empty act
		 */
		initialize: () => {
			if (!browser) return;

			update((state) => ({ ...state, isLoading: true }));

			try {
				const savedAct = localStorage.getItem(STORAGE_KEY);

				if (savedAct) {
					const parsedAct = JSON.parse(savedAct) as Act;
					update((state) => ({
						...state,
						act: parsedAct,
						isLoading: false,
						isDirty: false
					}));
				} else {
					update((state) => ({
						...state,
						act: createEmptyAct(DEFAULT_ROWS, DEFAULT_COLUMNS),
						isLoading: false,
						isDirty: false
					}));
				}
			} catch (error) {
				console.error('Failed to load act:', error);
				update((state) => ({
					...state,
					error: 'Failed to load act data',
					isLoading: false,
					act: createEmptyAct(DEFAULT_ROWS, DEFAULT_COLUMNS)
				}));
			}
		},

		/**
		 * Save the current act to localStorage
		 */
		save: () => {
			if (!browser) return;

			update((state) => {
				try {
					localStorage.setItem(STORAGE_KEY, JSON.stringify(state.act));
					return { ...state, isDirty: false };
				} catch (error) {
					console.error('Failed to save act:', error);
					return { ...state, error: 'Failed to save act data' };
				}
			});
		},

		/**
		 * Update the act title
		 */
		updateTitle: (title: string) => {
			update((state) => {
				const updatedAct = { ...state.act, title };
				return { ...state, act: updatedAct, isDirty: true };
			});
		},

		/**
		 * Update a beat at the specified row and column
		 */
		updateBeat: (row: number, col: number, beat: Partial<Beat>) => {
			update((state) => {
				const sequences = [...state.act.sequences];

				// Ensure the row exists
				if (row >= sequences.length) {
					for (let i = sequences.length; i <= row; i++) {
						sequences.push({
							sequence_start_marker: i === 0,
							cue: '',
							timestamp: '',
							beats: Array(DEFAULT_COLUMNS)
								.fill(null)
								.map(() => ({
									step_label: '',
									is_filled: false
								}))
						});
					}
				}

				// Update the beat
				const updatedBeats = [...sequences[row].beats];
				updatedBeats[col] = { ...updatedBeats[col], ...beat };

				sequences[row] = {
					...sequences[row],
					beats: updatedBeats
				};

				return {
					...state,
					act: {
						...state.act,
						sequences
					},
					isDirty: true
				};
			});
		},

		/**
		 * Update a cue and timestamp for a row
		 */
		updateCueAndTimestamp: (row: number, cue: string, timestamp: string) => {
			update((state) => {
				const sequences = [...state.act.sequences];

				// Ensure the row exists
				if (row >= sequences.length) return state;

				sequences[row] = {
					...sequences[row],
					cue,
					timestamp
				};

				return {
					...state,
					act: {
						...state.act,
						sequences
					},
					isDirty: true
				};
			});
		},

		/**
		 * Populate a sequence from dropped data
		 */
		populateFromDrop: (sequenceData: any, startRow: number = 0, startCol: number = 0) => {
			update((state) => {
				// Clone the current sequences
				const sequences = [...state.act.sequences];

				// Find the first empty beat position starting from the given row and column
				let currentRow = startRow;
				let currentCol = startCol;

				// If we have pictograph data, populate beats
				if (sequenceData && sequenceData.beats) {
					for (const beatData of sequenceData.beats) {
						// Skip if we've reached the end of the grid
						if (currentRow >= sequences.length) break;

						// Update the beat
						const updatedBeats = [...sequences[currentRow].beats];
						updatedBeats[currentCol] = {
							...updatedBeats[currentCol],
							pictograph_data: beatData.pictograph_data || beatData,
							step_label: beatData.step_label || '',
							is_filled: true
						};

						sequences[currentRow] = {
							...sequences[currentRow],
							beats: updatedBeats
						};

						// Move to the next position
						currentCol++;
						if (currentCol >= DEFAULT_COLUMNS) {
							currentCol = 0;
							currentRow++;
						}
					}
				}

				return {
					...state,
					act: {
						...state.act,
						sequences
					},
					isDirty: true
				};
			});
		},

		/**
		 * Erase a single beat at the specified row and column
		 */
		eraseBeat: (row: number, col: number) => {
			update((state) => {
				// Save the current state to history before making changes
				const stateWithHistory = addHistoryEntry(state, `Erased beat ${row * 8 + col + 1}`);

				const sequences = [...stateWithHistory.act.sequences];

				// Ensure the row exists
				if (row >= sequences.length) return stateWithHistory;

				// Update the beat to be empty
				const updatedBeats = [...sequences[row].beats];
				updatedBeats[col] = {
					step_label: '',
					is_filled: false,
					pictograph_data: null
				};

				sequences[row] = {
					...sequences[row],
					beats: updatedBeats
				};

				return {
					...stateWithHistory,
					act: {
						...stateWithHistory.act,
						sequences
					},
					isDirty: true
				};
			});
		},

		/**
		 * Erase an entire sequence (row)
		 */
		eraseSequence: (row: number) => {
			update((state) => {
				// Save the current state to history before making changes
				const stateWithHistory = addHistoryEntry(state, `Erased sequence ${row + 1}`);

				const sequences = [...stateWithHistory.act.sequences];

				// Ensure the row exists
				if (row >= sequences.length) return stateWithHistory;

				// Create empty beats for the row
				const emptyBeats = Array(DEFAULT_COLUMNS)
					.fill(null)
					.map(() => ({
						step_label: '',
						is_filled: false,
						pictograph_data: null
					}));

				// Keep the cue and timestamp, just clear the beats
				sequences[row] = {
					...sequences[row],
					beats: emptyBeats
				};

				return {
					...stateWithHistory,
					act: {
						...stateWithHistory.act,
						sequences
					},
					isDirty: true
				};
			});
		},

		/**
		 * Erase the entire act (clear all sequences but keep the structure)
		 */
		eraseAct: () => {
			update((state) => {
				// Save the current state to history before making changes
				const stateWithHistory = addHistoryEntry(state, `Erased entire act`);

				// Create empty sequences with the same structure
				const emptySequences = Array(DEFAULT_ROWS)
					.fill(null)
					.map((_, index) => ({
						sequence_start_marker: index === 0,
						cue: '',
						timestamp: '',
						beats: Array(DEFAULT_COLUMNS)
							.fill(null)
							.map(() => ({
								step_label: '',
								is_filled: false,
								pictograph_data: null
							}))
					}));

				return {
					...stateWithHistory,
					act: {
						...stateWithHistory.act,
						sequences: emptySequences
					},
					isDirty: true
				};
			});
		},

		/**
		 * Reset the act to an empty state (including title and metadata)
		 */
		reset: () => {
			update((state) => ({
				...state,
				act: createEmptyAct(DEFAULT_ROWS, DEFAULT_COLUMNS),
				isDirty: true
			}));
		}
	};
}

// Create and export the store
export const actStore = createActStore();

// Create derived stores for convenience
export const actTitle = derived(actStore, ($store) => $store.act.title);
export const actSequences = derived(actStore, ($store) => $store.act.sequences);
export const isDirty = derived(actStore, ($store) => $store.isDirty);
export const isLoading = derived(actStore, ($store) => $store.isLoading);
export const error = derived(actStore, ($store) => $store.error);

// Auto-save when the act changes (debounced)
if (browser) {
	let saveTimeout: ReturnType<typeof setTimeout> | null = null;

	actStore.subscribe(($store) => {
		if ($store.isDirty) {
			if (saveTimeout) clearTimeout(saveTimeout);

			saveTimeout = setTimeout(() => {
				actStore.save();
				saveTimeout = null;
			}, 500);
		}
	});
}
