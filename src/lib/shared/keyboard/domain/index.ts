/**
 * Keyboard Shortcuts Domain Layer
 *
 * Exports all domain models and types for the keyboard shortcut system.
 */

// Types
export type * from "./types/keyboard-types";

// Models
export { Shortcut } from "./models/Shortcut";
export { NormalizedKeyboardEvent } from "./models/KeyboardEvent";
