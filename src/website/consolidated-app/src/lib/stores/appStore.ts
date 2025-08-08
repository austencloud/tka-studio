import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface AppState {
	isLoading: boolean;
	currentBackground: string;
	isFullscreen: boolean;
	error: string | null;
}

const initialState: AppState = {
	isLoading: false,
	currentBackground: 'deepOcean',
	isFullscreen: false,
	error: null
};

function createAppStore() {
	const { subscribe, set, update } = writable<AppState>(initialState);

	return {
		subscribe,
		setLoading: (loading: boolean) =>
			update(state => ({ ...state, isLoading: loading })),

		setBackground: (background: string) => {
			update(state => ({ ...state, currentBackground: background }));
			if (browser) {
				localStorage.setItem('tka-background', background);
			}
		},

		setFullscreen: (fullscreen: boolean) =>
			update(state => ({ ...state, isFullscreen: fullscreen })),

		setError: (error: string | null) =>
			update(state => ({ ...state, error })),

		reset: () => set(initialState)
	};
}

export const appStore = createAppStore();
