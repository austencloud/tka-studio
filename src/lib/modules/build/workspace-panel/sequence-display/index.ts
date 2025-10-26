// Barrel exports for sequence-display module

export * from "./components";
export * from "./state";

// NOTE: Domain and utils both export GridLayout interface
// Do not use wildcard export to avoid conflicts
// Import GridLayout explicitly from the specific file you need:
// - from "./domain" for beat grid display layout
// - from "./utils" for grid calculation layout

// Export specific utilities (avoid GridLayout conflict)
export { calculateBeatPosition, calculateGridLayout, type GridSizingConfig } from "./utils";
