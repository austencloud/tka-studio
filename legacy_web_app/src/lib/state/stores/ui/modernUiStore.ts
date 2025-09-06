/**
 * Modern UI Store
 *
 * This module provides a modern implementation of the UI store using
 * the new container-based approach.
 */

import { createContainer } from '$lib/state/core/modern';

// Define the UI state interface
export interface UiState {
	activeTab: number;
	sidebarOpen: boolean;
	modalOpen: boolean;
	modalContent: string | null;
	theme: 'light' | 'dark' | 'system';
	isMobile: boolean;
	isLoading: boolean;
}

// Create the initial state
const initialState: UiState = {
	activeTab: 0,
	sidebarOpen: false,
	modalOpen: false,
	modalContent: null,
	theme: 'system',
	isMobile: false,
	isLoading: false
};

/**
 * Creates the UI store
 *
 * @returns The UI store container
 */
function createUiStore() {
	// Create the container with state and actions
	const container = createContainer(initialState, (state, _update) => ({
		// Tab actions
		setActiveTab: (tab: number) => {
			state.activeTab = tab;
		},

		// Sidebar actions
		openSidebar: () => {
			state.sidebarOpen = true;
		},
		closeSidebar: () => {
			state.sidebarOpen = false;
		},
		toggleSidebar: () => {
			state.sidebarOpen = !state.sidebarOpen;
		},

		// Modal actions
		openModal: (content: string) => {
			state.modalOpen = true;
			state.modalContent = content;
		},
		closeModal: () => {
			state.modalOpen = false;
			state.modalContent = null;
		},

		// Theme actions
		setTheme: (theme: 'light' | 'dark' | 'system') => {
			state.theme = theme;
		},

		// Device actions
		setMobile: (isMobile: boolean) => {
			state.isMobile = isMobile;
		},

		// Loading actions
		setLoading: (isLoading: boolean) => {
			state.isLoading = isLoading;
		}
	}));

	// Return the container without derived values
	return container;
}

// Create and export the UI store
export const uiStore = createUiStore();

// Create a custom wrapper for the registry
// We need to use a different approach since the registerContainer function
// has strict type requirements that our store doesn't meet
import { stateRegistry } from '$lib/state/core/registry';
import { writable } from 'svelte/store';

// Create a writable store from the UI store state
const uiWritableStore = writable(uiStore.state);

// Update the writable store when the UI store state changes
// This is a simple polling approach since we don't have proper reactivity
const updateInterval = setInterval(() => {
	uiWritableStore.set(uiStore.state);
}, 100);

// Clean up on page unload
if (typeof window !== 'undefined') {
	window.addEventListener('beforeunload', () => {
		clearInterval(updateInterval);
	});
}

// Register with the registry directly
export const uiStoreCompat = stateRegistry.registerStore('ui', uiWritableStore, {
	persist: true,
	description: 'UI state store'
});
