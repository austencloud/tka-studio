// Core Pictograph Module - Foundational rendering and data structures
// This module provides the core pictograph functionality used throughout the application

// Export components
export { default as PictographSVG } from './components/PictographSVG.svelte';
export { default as Grid } from './components/Grid.svelte';
export { default as Arrow } from './components/Arrow.svelte';
export { default as Prop } from './components/Prop.svelte';
export { default as TKAGlyph } from './components/TKAGlyph.svelte';
export { default as PictographWrapper } from './components/PictographWrapper.svelte';
export { default as PictographError } from './components/PictographError.svelte';
export { default as PictographLoading } from './components/PictographLoading.svelte';
export { default as StyledBorderOverlay } from './components/StyledBorderOverlay.svelte';

// Export types
export type { PictographData } from './types/PictographData.js';
export type { MotionData } from './types/MotionData.js';
export type { TKAPosition } from './types/TKAPosition.js';

// Export utilities
export * from './utils/index.js';

// Export data
export { circleCoordinates } from './components/circleCoordinates.js';
export type { GridData } from './components/GridData.js';
