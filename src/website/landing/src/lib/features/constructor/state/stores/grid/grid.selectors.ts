/**
 * Grid Store Selectors
 *
 * This file contains selectors for the grid store.
 * Selectors are functions that extract specific pieces of state from the store.
 */

import { derived } from 'svelte/store';
import { gridStore } from './grid.store.js';
import { createSelector } from '../state/core.js';

// Basic selectors
export const selectGridData = createSelector(
  derived(gridStore, $store => $store.data),
  { id: 'grid.data', description: 'Current grid data' }
);

export const selectGridMode = createSelector(
  derived(gridStore, $store => $store.mode),
  { id: 'grid.mode', description: 'Current grid mode' }
);

export const selectGridStatus = createSelector(
  derived(gridStore, $store => $store.status),
  { id: 'grid.status', description: 'Current grid loading status' }
);

export const selectGridError = createSelector(
  derived(gridStore, $store => $store.error),
  { id: 'grid.error', description: 'Current grid error' }
);

export const selectGridDebugMode = createSelector(
  derived(gridStore, $store => $store.debugMode),
  { id: 'grid.debugMode', description: 'Whether grid debug mode is enabled' }
);

// Derived selectors
export const selectIsGridLoading = createSelector(
  derived(gridStore, $store => $store.status === 'loading'),
  { id: 'grid.isLoading', description: 'Whether the grid is loading' }
);

export const selectIsGridLoaded = createSelector(
  derived(gridStore, $store => $store.status === 'loaded'),
  { id: 'grid.isLoaded', description: 'Whether the grid is loaded' }
);

export const selectHasGridError = createSelector(
  derived(gridStore, $store => $store.status === 'error'),
  { id: 'grid.hasError', description: 'Whether the grid has an error' }
);

export const selectGridCenterPoint = createSelector(
  derived(gridStore, $store => $store.data?.centerPoint || null),
  { id: 'grid.centerPoint', description: 'The center point of the grid' }
);

export const selectGridHandPoints = createSelector(
  derived(gridStore, $store => $store.data?.handPoints || null),
  { id: 'grid.handPoints', description: 'Hand points of the grid' }
);

export const selectGridLayer2Points = createSelector(
  derived(gridStore, $store => $store.data?.layer2Points || null),
  { id: 'grid.layer2Points', description: 'Layer 2 points of the grid' }
);

export const selectGridOuterPoints = createSelector(
  derived(gridStore, $store => $store.data?.outerPoints || null),
  { id: 'grid.outerPoints', description: 'Outer points of the grid' }
);
