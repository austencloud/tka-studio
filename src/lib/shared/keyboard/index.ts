/**
 * Keyboard Shortcuts Module
 *
 * Main export file for the keyboard shortcuts system.
 * Provides domain models, services, state management, and components.
 *
 * Domain: Keyboard Shortcuts
 */

// Domain layer
export * from "./domain";

// Service layer
export * from "./services";

// State layer
export * from "./state";

// Re-export key types for convenience
export type {
  KeyModifier,
  ShortcutContext,
  ShortcutScope,
  ShortcutDefinition,
  ShortcutRegistrationOptions,
  CommandPaletteItem,
  ShortcutSettings,
} from "./domain";
