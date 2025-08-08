// Backgrounds Feature - Background animation system
// This module provides background animation functionality

// Export background components
export { default as BackgroundCanvas } from './Backgrounds/BackgroundCanvas.svelte';
export { default as BackgroundController } from './Backgrounds/BackgroundController.svelte';
export { default as BackgroundProvider } from './Backgrounds/BackgroundProvider.svelte';
export { default as BackgroundSettings } from './Backgrounds/BackgroundSettings.svelte';
export { default as SimpleNightSkyCanvas } from './Backgrounds/SimpleNightSkyCanvas.svelte';

// Export background core functionality
export * from './Backgrounds/core/index.js';

// Export background types
export * from './Backgrounds/types/index.js';
