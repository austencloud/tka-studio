import { writable } from 'svelte/store';

interface WorkbenchState {
	toolsPanelOpen: boolean;
	activeTab: 'generate' | 'construct';
}

const initialState: WorkbenchState = {
	toolsPanelOpen: false,
	activeTab: 'generate'
};

export const workbenchStore = writable<WorkbenchState>(initialState);
