/**
 * Pictograph Store Selectors
 *
 * This file contains selectors for the pictograph store.
 * Selectors are functions that extract specific pieces of state from the store.
 */

import { derived } from 'svelte/store';
import { pictographStore } from './pictograph.store.js';
import { createSelector } from '../state/core.js';

// Basic selectors
export const selectPictographData = createSelector(
  derived(pictographStore, $store => $store.data),
  { id: 'pictograph.data', description: 'Current pictograph data' }
);

export const selectPictographStatus = createSelector(
  derived(pictographStore, $store => $store.status),
  { id: 'pictograph.status', description: 'Current pictograph loading status' }
);

export const selectPictographError = createSelector(
  derived(pictographStore, $store => $store.error),
  { id: 'pictograph.error', description: 'Current pictograph error' }
);

export const selectPictographLoadProgress = createSelector(
  derived(pictographStore, $store => $store.loadProgress),
  { id: 'pictograph.loadProgress', description: 'Current pictograph load progress' }
);

export const selectPictographComponents = createSelector(
  derived(pictographStore, $store => $store.components),
  { id: 'pictograph.components', description: 'Pictograph component loading status' }
);

export const selectPictographStateHistory = createSelector(
  derived(pictographStore, $store => $store.stateHistory),
  { id: 'pictograph.stateHistory', description: 'Pictograph state transition history' }
);

// Derived selectors
export const selectIsLoading = createSelector(
  derived(
    pictographStore,
    $store => ['initializing', 'grid_loading', 'props_loading', 'arrows_loading'].includes($store.status)
  ),
  { id: 'pictograph.isLoading', description: 'Whether the pictograph is loading' }
);

export const selectIsComplete = createSelector(
  derived(pictographStore, $store => $store.status === 'complete'),
  { id: 'pictograph.isComplete', description: 'Whether the pictograph is completely loaded' }
);

export const selectHasError = createSelector(
  derived(pictographStore, $store => $store.status === 'error'),
  { id: 'pictograph.hasError', description: 'Whether the pictograph has an error' }
);

export const selectRedPropData = createSelector(
  derived(pictographStore, $store => $store.data?.redPropData || null),
  { id: 'pictograph.redPropData', description: 'Red prop data' }
);

export const selectBluePropData = createSelector(
  derived(pictographStore, $store => $store.data?.bluePropData || null),
  { id: 'pictograph.bluePropData', description: 'Blue prop data' }
);

export const selectRedArrowData = createSelector(
  derived(pictographStore, $store => $store.data?.redArrowData || null),
  { id: 'pictograph.redArrowData', description: 'Red arrow data' }
);

export const selectBlueArrowData = createSelector(
  derived(pictographStore, $store => $store.data?.blueArrowData || null),
  { id: 'pictograph.blueArrowData', description: 'Blue arrow data' }
);

export const selectGridMode = createSelector(
  derived(pictographStore, $store => $store.data?.gridMode || 'diamond'),
  { id: 'pictograph.gridMode', description: 'Grid mode' }
);
