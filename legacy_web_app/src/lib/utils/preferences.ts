/**
 * User Preferences Utility
 *
 * This module provides functions for saving and loading user preferences
 * directly to/from localStorage.
 */

import { browser } from '$app/environment';
import type { BackgroundType } from '$lib/components/Backgrounds/types/types';

// Storage keys
export const KEYS = {
	BACKGROUND: 'user_pref_background',
	ACTIVE_TAB: 'user_pref_active_tab'
};

/**
 * Save the background preference to localStorage
 */
export function saveBackgroundPreference(background: BackgroundType): void {
	if (!browser) return;

	try {
		localStorage.setItem(KEYS.BACKGROUND, background);
	} catch (error) {
		console.error('Error saving background preference:', error);
	}
}

/**
 * Load the background preference from localStorage
 */
export function loadBackgroundPreference(): BackgroundType {
	if (!browser) return 'snowfall';

	try {
		const savedBackground = localStorage.getItem(KEYS.BACKGROUND);

		if (savedBackground) {
			const validBackgrounds: BackgroundType[] = ['snowfall', 'nightSky'];
			if (validBackgrounds.includes(savedBackground as BackgroundType)) {
				return savedBackground as BackgroundType;
			}
		}
	} catch (error) {
		console.error('Error loading background preference:', error);
	}

	return 'snowfall'; // Default
}

/**
 * Save the active tab preference to localStorage
 */
export function saveActiveTabPreference(tabIndex: number): void {
	if (!browser) return;

	try {
		localStorage.setItem(KEYS.ACTIVE_TAB, tabIndex.toString());
	} catch (error) {
		console.error('Error saving active tab preference:', error);
	}
}

/**
 * Load the active tab preference from localStorage
 */
export function loadActiveTabPreference(): number {
	if (!browser) return 0;

	try {
		const savedTab = localStorage.getItem(KEYS.ACTIVE_TAB);

		if (savedTab !== null) {
			const tabIndex = parseInt(savedTab, 10);
			if (!isNaN(tabIndex) && tabIndex >= 0 && tabIndex <= 4) {
				return tabIndex;
			}
		}
	} catch (error) {
		console.error('Error loading active tab preference:', error);
	}

	return 0; // Default to first tab
}
