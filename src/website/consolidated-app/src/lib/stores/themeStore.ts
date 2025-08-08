import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export type Theme = 'dark' | 'light' | 'auto';

interface ThemeState {
	theme: Theme;
	systemTheme: 'dark' | 'light';
	effectiveTheme: 'dark' | 'light';
}

const initialState: ThemeState = {
	theme: 'auto',
	systemTheme: 'dark',
	effectiveTheme: 'dark'
};

function createThemeStore() {
	const { subscribe, set, update } = writable<ThemeState>(initialState);

	// Initialize theme from localStorage or system preference
	if (browser) {
		const savedTheme = localStorage.getItem('tka-theme') as Theme | null;
		const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

		const theme = savedTheme || 'auto';
		const effectiveTheme = theme === 'auto' ? systemTheme : theme;

		set({
			theme,
			systemTheme,
			effectiveTheme
		});

		// Listen for system theme changes
		const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
		mediaQuery.addEventListener('change', (e) => {
			update(state => ({
				...state,
				systemTheme: e.matches ? 'dark' : 'light',
				effectiveTheme: state.theme === 'auto' ? (e.matches ? 'dark' : 'light') : state.effectiveTheme
			}));
		});
	}

	return {
		subscribe,

		setTheme: (theme: Theme) => {
			update(state => {
				const effectiveTheme = theme === 'auto' ? state.systemTheme : theme;
				const newState = { ...state, theme, effectiveTheme };

				if (browser) {
					localStorage.setItem('tka-theme', theme);
					document.documentElement.setAttribute('data-theme', effectiveTheme);
				}

				return newState;
			});
		},

		toggleTheme: () => {
			update(state => {
				const newTheme: Theme = state.theme === 'dark' ? 'light' :
								  	   state.theme === 'light' ? 'auto' : 'dark';
				const effectiveTheme = newTheme === 'auto' ? state.systemTheme : newTheme;

				if (browser) {
					localStorage.setItem('tka-theme', newTheme);
					document.documentElement.setAttribute('data-theme', effectiveTheme);
				}

				return { ...state, theme: newTheme, effectiveTheme };
			});
		}
	};
}

export const themeStore = createThemeStore();
