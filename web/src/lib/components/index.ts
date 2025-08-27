/**
 * TKA Components - Main component barrel export
 *
 * Organized component exports following modern architectural patterns:
 * - core: Universal domain components (pictographs, etc.)
 * - ui: Reusable UI primitives and atoms
 * - features: Feature-specific component hierarchies
 * - layout: App-level structural components
 */

// Top-level app components
export { default as ErrorScreen } from "./ErrorScreen.svelte";
export { default as LoadingScreen } from "./LoadingScreen.svelte";
export { default as SettingsDialog } from "./SettingsDialog.svelte";

// Organized component categories
export * from "./core";
export * from "./ui";
export * from "./features";
export * from "./layout";
