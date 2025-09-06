/**
 * Settings Store
 *
 * This store manages application settings.
 */

import { createStore } from '$lib/state/core';
import type { BackgroundType } from '$lib/components/Backgrounds/types/types';
import type { GridMode } from '$lib/components/objects/Grid/types';

// Define the store state interface
export interface SettingsStoreState {
	// Display settings
	theme: 'light' | 'dark' | 'system';
	background: BackgroundType;
	backgroundQuality: 'high' | 'medium' | 'low' | 'minimal';

	// Grid settings
	defaultGridMode: GridMode;
	showGridDebug: boolean;

	// Performance settings
	enableAnimations: boolean;
	enableTransitions: boolean;

	// User preferences
	autoSave: boolean;
	showTutorials: boolean;

	// Accessibility
	highContrast: boolean;
	reducedMotion: boolean;

	// Mobile experience
	hapticFeedback: boolean;

	// Last updated timestamp
	lastUpdated: number;
}

// Initial state
const initialState: SettingsStoreState = {
	theme: 'system',
	background: 'snowfall',
	backgroundQuality: 'medium',

	defaultGridMode: 'diamond',
	showGridDebug: false,

	enableAnimations: true,
	enableTransitions: true,

	autoSave: true,
	showTutorials: true,

	highContrast: false,
	reducedMotion: false,

	// Enable haptic feedback by default on mobile devices
	hapticFeedback: true,

	lastUpdated: Date.now()
};

// Create the store
export const settingsStore = createStore<
	SettingsStoreState,
	{
		setTheme: (theme: SettingsStoreState['theme']) => void;
		setBackground: (background: BackgroundType) => void;
		setBackgroundQuality: (quality: SettingsStoreState['backgroundQuality']) => void;
		setDefaultGridMode: (mode: GridMode) => void;
		setShowGridDebug: (show: boolean) => void;
		setEnableAnimations: (enable: boolean) => void;
		setEnableTransitions: (enable: boolean) => void;
		setAutoSave: (enable: boolean) => void;
		setShowTutorials: (show: boolean) => void;
		setHighContrast: (enable: boolean) => void;
		setReducedMotion: (enable: boolean) => void;
		setHapticFeedback: (enable: boolean) => void;
		updateSettings: (settings: Partial<SettingsStoreState>) => void;
	}
>(
	'settings',
	initialState,
	(set, update) => {
		return {
			setTheme: (theme) => {
				update((state) => ({
					...state,
					theme,
					lastUpdated: Date.now()
				}));
			},

			setBackground: (background) => {
				update((state) => ({
					...state,
					background,
					lastUpdated: Date.now()
				}));
			},

			setBackgroundQuality: (quality) => {
				update((state) => ({
					...state,
					backgroundQuality: quality,
					lastUpdated: Date.now()
				}));
			},

			setDefaultGridMode: (mode) => {
				update((state) => ({
					...state,
					defaultGridMode: mode,
					lastUpdated: Date.now()
				}));
			},

			setShowGridDebug: (show) => {
				update((state) => ({
					...state,
					showGridDebug: show,
					lastUpdated: Date.now()
				}));
			},

			setEnableAnimations: (enable) => {
				update((state) => ({
					...state,
					enableAnimations: enable,
					lastUpdated: Date.now()
				}));
			},

			setEnableTransitions: (enable) => {
				update((state) => ({
					...state,
					enableTransitions: enable,
					lastUpdated: Date.now()
				}));
			},

			setAutoSave: (enable) => {
				update((state) => ({
					...state,
					autoSave: enable,
					lastUpdated: Date.now()
				}));
			},

			setShowTutorials: (show) => {
				update((state) => ({
					...state,
					showTutorials: show,
					lastUpdated: Date.now()
				}));
			},

			setHighContrast: (enable) => {
				update((state) => ({
					...state,
					highContrast: enable,
					lastUpdated: Date.now()
				}));
			},

			setReducedMotion: (enable) => {
				update((state) => ({
					...state,
					reducedMotion: enable,
					lastUpdated: Date.now()
				}));
			},

			setHapticFeedback: (enable) => {
				update((state) => ({
					...state,
					hapticFeedback: enable,
					lastUpdated: Date.now()
				}));
			},

			updateSettings: (settings) => {
				update((state) => ({
					...state,
					...settings,
					lastUpdated: Date.now()
				}));
			}
		};
	},
	{
		persist: true,
		description: 'Manages application settings'
	}
);
