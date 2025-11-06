/**
 * Navigation Domain Types
 *
 * Core types for the navigation system.
 */

/**
 * Tab within a module
 * Represents a navigation tab within a specific module (e.g., "Construct" tab in Create module)
 */
export interface Section {
  id: string;
  label: string;
  icon: string;
  description?: string;
  color?: string;
  gradient?: string; // Optional gradient for colorful icons
  disabled?: boolean; // For conditional tab accessibility
}


// Module-based navigation types
export type ModuleId = "create" | "explore" | "learn" | "collect" | "animate" | "library" | "write" | "word_card" | "admin";

/**
 * Module Definition
 * Represents a top-level module with its sections
 */
export interface ModuleDefinition {
  id: ModuleId;
  label: string;
  icon: string;
  description?: string;
  isMain: boolean;
  sections: Section[]; // Sections within this module
}

export interface ModuleSelectorState {
  isOpen: boolean;
  showDiscoveryHint: boolean;
}
