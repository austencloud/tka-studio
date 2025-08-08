/**
 * Pictograph Selectors
 *
 * This file contains selectors for the pictograph container.
 * These selectors replace the deprecated pictograph.selectors.ts.
 */

import { createDerived } from '../state/core/container.js';
import { pictographContainer } from './pictographContainer.js';

// Basic selectors
export const pictographData = createDerived(() =>
  pictographContainer.state.data
);

export const pictographStatus = createDerived(() =>
  pictographContainer.state.status
);

export const pictographError = createDerived(() =>
  pictographContainer.state.error
);

export const pictographLoadProgress = createDerived(() =>
  pictographContainer.state.loadProgress
);

export const pictographComponents = createDerived(() =>
  pictographContainer.state.components
);

export const pictographStateHistory = createDerived(() =>
  pictographContainer.state.stateHistory
);

// Derived selectors
export const isLoading = createDerived(() =>
  ['initializing', 'grid_loading', 'props_loading', 'arrows_loading'].includes(pictographContainer.state.status)
);

export const isComplete = createDerived(() =>
  pictographContainer.state.status === 'complete'
);

export const hasError = createDerived(() =>
  pictographContainer.state.status === 'error'
);

export const redPropData = createDerived(() =>
  pictographContainer.state.data?.redPropData || null
);

export const bluePropData = createDerived(() =>
  pictographContainer.state.data?.bluePropData || null
);

export const redArrowData = createDerived(() =>
  pictographContainer.state.data?.redArrowData || null
);

export const blueArrowData = createDerived(() =>
  pictographContainer.state.data?.blueArrowData || null
);

export const gridMode = createDerived(() =>
  pictographContainer.state.data?.gridMode || 'diamond'
);
