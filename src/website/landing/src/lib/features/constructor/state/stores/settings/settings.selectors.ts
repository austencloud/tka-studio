/**
 * Settings Store Selectors
 *
 * This file contains selectors for the settings store.
 * Selectors are functions that extract specific pieces of state from the store.
 */

import { derived } from 'svelte/store';
import { settingsStore } from './settings.store.js';
import { createSelector } from '../state/core.js';

// Display settings selectors
export const selectTheme = createSelector(
  derived(settingsStore, $store => $store.theme),
  { id: 'settings.theme', description: 'Current theme setting' }
);

export const selectBackground = createSelector(
  derived(settingsStore, $store => $store.background),
  { id: 'settings.background', description: 'Current background setting' }
);

export const selectBackgroundQuality = createSelector(
  derived(settingsStore, $store => $store.backgroundQuality),
  { id: 'settings.backgroundQuality', description: 'Current background quality setting' }
);

// Grid settings selectors
export const selectDefaultGridMode = createSelector(
  derived(settingsStore, $store => $store.defaultGridMode),
  { id: 'settings.defaultGridMode', description: 'Default grid mode setting' }
);

export const selectShowGridDebug = createSelector(
  derived(settingsStore, $store => $store.showGridDebug),
  { id: 'settings.showGridDebug', description: 'Show grid debug setting' }
);

// Performance settings selectors
export const selectEnableAnimations = createSelector(
  derived(settingsStore, $store => $store.enableAnimations),
  { id: 'settings.enableAnimations', description: 'Enable animations setting' }
);

export const selectEnableTransitions = createSelector(
  derived(settingsStore, $store => $store.enableTransitions),
  { id: 'settings.enableTransitions', description: 'Enable transitions setting' }
);

// User preferences selectors
export const selectAutoSave = createSelector(
  derived(settingsStore, $store => $store.autoSave),
  { id: 'settings.autoSave', description: 'Auto save setting' }
);

export const selectShowTutorials = createSelector(
  derived(settingsStore, $store => $store.showTutorials),
  { id: 'settings.showTutorials', description: 'Show tutorials setting' }
);

// Accessibility selectors
export const selectHighContrast = createSelector(
  derived(settingsStore, $store => $store.highContrast),
  { id: 'settings.highContrast', description: 'High contrast setting' }
);

export const selectReducedMotion = createSelector(
  derived(settingsStore, $store => $store.reducedMotion),
  { id: 'settings.reducedMotion', description: 'Reduced motion setting' }
);

// Derived selectors
export const selectEffectiveTheme = createSelector(
  derived(settingsStore, $store => {
    if ($store.theme === 'system') {
      // Check system preference
      if (typeof window !== 'undefined') {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }
      return 'light'; // Default to light if not in browser
    }
    return $store.theme;
  }),
  { id: 'settings.effectiveTheme', description: 'Effective theme after resolving system preference' }
);

export const selectLastUpdated = createSelector(
  derived(settingsStore, $store => $store.lastUpdated),
  { id: 'settings.lastUpdated', description: 'Timestamp of last settings update' }
);
