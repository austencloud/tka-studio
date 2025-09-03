import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Define the UI state interface
interface UIState {
	isBrowserPanelOpen: boolean;
	browserPanelWidth: number;
	scrollPosition: {
		beatGrid: number;
		cueScroll: number;
	};
	gridSettings: {
		cellSize: number;
	};
	preferences: {
		confirmDeletions: boolean;
	};
}

// Create the initial state
const initialState: UIState = {
	isBrowserPanelOpen: true,
	browserPanelWidth: 300, // Default browser panel width in pixels
	scrollPosition: {
		beatGrid: 0,
		cueScroll: 0
	},
	gridSettings: {
		cellSize: 80 // Default cell size in pixels
	},
	preferences: {
		confirmDeletions: true // Default to showing confirmation dialogs
	}
};

// Create the writable store
function createUIStore() {
	// Load saved state from localStorage if available
	let savedState = initialState;

	if (browser) {
		try {
			const saved = localStorage.getItem('write_tab_ui_state');
			if (saved) {
				savedState = { ...initialState, ...JSON.parse(saved) };
			}
		} catch (error) {
			console.error('Failed to load UI state:', error);
		}
	}

	const { subscribe, set, update } = writable<UIState>(savedState);

	// Save state to localStorage when it changes
	if (browser) {
		subscribe((state) => {
			try {
				localStorage.setItem('write_tab_ui_state', JSON.stringify(state));
			} catch (error) {
				console.error('Failed to save UI state:', error);
			}
		});
	}

	return {
		subscribe,

		/**
		 * Toggle the browser panel open/closed state
		 */
		toggleBrowserPanel: () => {
			update((state) => ({
				...state,
				isBrowserPanelOpen: !state.isBrowserPanelOpen
			}));
		},

		/**
		 * Set the browser panel open/closed state
		 */
		setBrowserPanelOpen: (isOpen: boolean) => {
			update((state) => ({
				...state,
				isBrowserPanelOpen: isOpen
			}));
		},

		/**
		 * Update the scroll position for the beat grid
		 */
		updateBeatGridScroll: (position: number) => {
			update((state) => ({
				...state,
				scrollPosition: {
					...state.scrollPosition,
					beatGrid: position
				}
			}));
		},

		/**
		 * Update the scroll position for the cue scroll
		 */
		updateCueScrollPosition: (position: number) => {
			update((state) => ({
				...state,
				scrollPosition: {
					...state.scrollPosition,
					cueScroll: position
				}
			}));
		},

		/**
		 * Sync the scroll positions between beat grid and cue scroll
		 */
		syncScrollPositions: (position: number) => {
			update((state) => ({
				...state,
				scrollPosition: {
					beatGrid: position,
					cueScroll: position
				}
			}));
		},

		/**
		 * Update the grid cell size
		 */
		updateCellSize: (size: number) => {
			update((state) => ({
				...state,
				gridSettings: {
					...state.gridSettings,
					cellSize: size
				}
			}));
		},

		/**
		 * Zoom in by increasing the cell size
		 */
		zoomIn: () => {
			update((state) => {
				const newSize = Math.min(state.gridSettings.cellSize + 20, 200); // Max size 200px
				return {
					...state,
					gridSettings: {
						...state.gridSettings,
						cellSize: newSize
					}
				};
			});
		},

		/**
		 * Zoom out by decreasing the cell size
		 */
		zoomOut: () => {
			update((state) => {
				const newSize = Math.max(state.gridSettings.cellSize - 20, 40); // Min size 40px
				return {
					...state,
					gridSettings: {
						...state.gridSettings,
						cellSize: newSize
					}
				};
			});
		},

		/**
		 * Update the browser panel width
		 */
		updateBrowserPanelWidth: (width: number) => {
			// Constrain width between 200px and 1200px
			const constrainedWidth = Math.max(200, Math.min(1200, width));
			update((state) => ({
				...state,
				browserPanelWidth: constrainedWidth
			}));
		},

		/**
		 * Toggle whether to show confirmation dialogs for deletions
		 */
		toggleConfirmDeletions: (value?: boolean) => {
			update((state) => ({
				...state,
				preferences: {
					...state.preferences,
					confirmDeletions: value !== undefined ? value : !state.preferences.confirmDeletions
				}
			}));
		},

		/**
		 * Reset the UI state to defaults
		 */
		reset: () => {
			set(initialState);
		}
	};
}

// Create and export the store
export const uiStore = createUIStore();
