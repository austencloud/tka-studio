/**
 * TKA Glyph Module
 *
 * Handles all TKA glyph-related functionality including letter rendering,
 * turn indicators, and glyph utilities.
 */

// Components
export { default as TKAGlyph } from "./components/TKAGlyph.svelte";

// Services
export * from "./services/contracts";
export * from "./services/implementations";

// Domain
export * from "./domain";

// State
export * from "./state";

// Utils - but exclude Dimensions type to avoid conflict with background module
export type { Position, TurnPositions } from "./utils/turn-position-calculator";
export { calculateTurnPositions } from "./utils/turn-position-calculator";
