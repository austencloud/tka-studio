import { createStore } from '../core/store';

/**
 * Interface for UI state
 */
export interface UIState {
	isLoading: boolean;
	activeTabIndex: number;
	isSettingsOpen: boolean;
	isFullScreen: boolean;
	windowWidth: number;
	windowHeight: number;
	isMobile: boolean;
	isTablet: boolean;
	isDesktop: boolean;
	theme: 'light' | 'dark' | 'system';
	sidebarOpen: boolean;
}

/**
 * Initial UI state
 */
const initialState: UIState = {
	isLoading: true,
	activeTabIndex: 0,
	isSettingsOpen: false,
	isFullScreen: false,
	windowWidth: typeof window !== 'undefined' ? window.innerWidth : 1024,
	windowHeight: typeof window !== 'undefined' ? window.innerHeight : 768,
	isMobile: typeof window !== 'undefined' ? window.innerWidth < 768 : false,
	isTablet:
		typeof window !== 'undefined' ? window.innerWidth >= 768 && window.innerWidth < 1024 : false,
	isDesktop: typeof window !== 'undefined' ? window.innerWidth >= 1024 : true,
	theme: 'system',
	sidebarOpen: true
};

/**
 * Create the UI store
 */
export const uiStore = createStore<
	UIState,
	{
		updateWindowDimensions: (width: number, height: number) => void;
		setActiveTab: (index: number) => void;
		toggleSettings: () => void;
		setSettingsOpen: (isOpen: boolean) => void;
		toggleFullScreen: () => void;
		setFullScreen: (isFullScreen: boolean) => void;
		setTheme: (theme: 'light' | 'dark' | 'system') => void;
		toggleSidebar: () => void;
		setSidebarOpen: (isOpen: boolean) => void;
	}
>('ui', initialState, (_set, update) => ({
	/**
	 * Update window dimensions and responsive breakpoints
	 */
	updateWindowDimensions: (width: number, height: number) => {
		update((state) => ({
			...state,
			windowWidth: width,
			windowHeight: height,
			isMobile: width < 768,
			isTablet: width >= 768 && width < 1024,
			isDesktop: width >= 1024
		}));
	},

	/**
	 * Set the active tab
	 */
	setActiveTab: (index: number) => {
		update((state) => ({ ...state, activeTabIndex: index }));
	},

	/**
	 * Toggle settings dialog
	 */
	toggleSettings: () => {
		update((state) => ({ ...state, isSettingsOpen: !state.isSettingsOpen }));
	},

	/**
	 * Set settings dialog state
	 */
	setSettingsOpen: (isOpen: boolean) => {
		update((state) => ({ ...state, isSettingsOpen: isOpen }));
	},

	/**
	 * Toggle fullscreen mode
	 */
	toggleFullScreen: () => {
		update((state) => ({ ...state, isFullScreen: !state.isFullScreen }));
	},

	/**
	 * Set fullscreen mode
	 */
	setFullScreen: (isFullScreen: boolean) => {
		update((state) => ({ ...state, isFullScreen }));
	},

	/**
	 * Set theme
	 */
	setTheme: (theme: 'light' | 'dark' | 'system') => {
		update((state) => ({ ...state, theme }));

		// Apply theme to document
		if (typeof document !== 'undefined') {
			if (theme === 'system') {
				const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
				document.documentElement.classList.toggle('dark', prefersDark);
			} else {
				document.documentElement.classList.toggle('dark', theme === 'dark');
			}
		}
	},

	/**
	 * Toggle sidebar
	 */
	toggleSidebar: () => {
		update((state) => ({ ...state, sidebarOpen: !state.sidebarOpen }));
	},

	/**
	 * Set sidebar state
	 */
	setSidebarOpen: (isOpen: boolean) => {
		update((state) => ({ ...state, sidebarOpen: isOpen }));
	}
}));

/**
 * Setup window resize listener
 */
if (typeof window !== 'undefined') {
	window.addEventListener('resize', () => {
		uiStore.updateWindowDimensions(window.innerWidth, window.innerHeight);
	});

	// Setup theme listener
	const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
	mediaQuery.addEventListener('change', () => {
		// Get the current state using the subscribe method
		let currentState: UIState | undefined;
		const unsubscribe = uiStore.subscribe((state) => {
			currentState = state;
		});
		unsubscribe();

		if (currentState && currentState.theme === 'system') {
			document.documentElement.classList.toggle('dark', mediaQuery.matches);
		}
	});
}
