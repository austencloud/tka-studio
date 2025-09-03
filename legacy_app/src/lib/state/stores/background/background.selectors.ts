/**
 * Background Store Selectors
 *
 * This file contains selectors for the background store.
 * Selectors are functions that extract specific pieces of state from the store.
 */

import { derived } from 'svelte/store';
import { backgroundStore } from './background.store';
import { createSelector } from '$lib/state/core';

// Basic selectors
export const selectCurrentBackground = createSelector(
  derived(backgroundStore, $store => $store.currentBackground),
  { id: 'background.current', description: 'Current background type' }
);

export const selectIsBackgroundReady = createSelector(
  derived(backgroundStore, $store => $store.isReady),
  { id: 'background.isReady', description: 'Whether the background is ready' }
);

export const selectIsBackgroundVisible = createSelector(
  derived(backgroundStore, $store => $store.isVisible),
  { id: 'background.isVisible', description: 'Whether the background is visible' }
);

export const selectBackgroundQuality = createSelector(
  derived(backgroundStore, $store => $store.quality),
  { id: 'background.quality', description: 'Current background quality level' }
);

export const selectBackgroundPerformanceMetrics = createSelector(
  derived(backgroundStore, $store => $store.performanceMetrics),
  { id: 'background.performanceMetrics', description: 'Background performance metrics' }
);

export const selectAvailableBackgrounds = createSelector(
  derived(backgroundStore, $store => $store.availableBackgrounds),
  { id: 'background.available', description: 'Available background types' }
);

export const selectBackgroundError = createSelector(
  derived(backgroundStore, $store => $store.error),
  { id: 'background.error', description: 'Background error' }
);

// Derived selectors
export const selectHasBackgroundError = createSelector(
  derived(backgroundStore, $store => $store.error !== null),
  { id: 'background.hasError', description: 'Whether there is a background error' }
);

export const selectBackgroundFps = createSelector(
  derived(backgroundStore, $store => $store.performanceMetrics?.fps || 0),
  { id: 'background.fps', description: 'Background frames per second' }
);

export const selectBackgroundWarnings = createSelector(
  derived(backgroundStore, $store => $store.performanceMetrics?.warnings || []),
  { id: 'background.warnings', description: 'Background performance warnings' }
);
