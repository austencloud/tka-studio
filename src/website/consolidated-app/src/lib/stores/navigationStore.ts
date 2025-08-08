import { writable } from 'svelte/store';

interface NavigationState {
	currentRoute: string;
	isNavigating: boolean;
	history: string[];
}

const initialState: NavigationState = {
	currentRoute: '/',
	isNavigating: false,
	history: ['/']
};

function createNavigationStore() {
	const { subscribe, set, update } = writable<NavigationState>(initialState);

	return {
		subscribe,

		navigate: (route: string) => {
			update(state => ({
				...state,
				currentRoute: route,
				isNavigating: true,
				history: [...state.history, route]
			}));
		},

		setNavigating: (navigating: boolean) =>
			update(state => ({ ...state, isNavigating: navigating })),

		goBack: () => {
			update(state => {
				if (state.history.length > 1) {
					const newHistory = state.history.slice(0, -1);
					const previousRoute = newHistory[newHistory.length - 1];
					return {
						...state,
						currentRoute: previousRoute,
						history: newHistory
					};
				}
				return state;
			});
		},

		reset: () => set(initialState)
	};
}

export const navigationStore = createNavigationStore();
