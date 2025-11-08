/**
 * Unified Animation System
 *
 * Export all animation utilities and presets.
 */

// Core presets and utilities
export * from "./presets";

// Animation utility classes
export * from "./animations.svelte";

// Re-export Svelte 5 motion classes for convenience
export { Spring, Tween } from "svelte/motion";
