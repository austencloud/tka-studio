/**
 * Navigation Domain Types
 *
 * Core types for the navigation system including dropdown functionality.
 */

export interface ModeOption {
  id: string;
  label: string;
  icon: string;
  description?: string;
  color?: string;
  gradient?: string; // Optional gradient for colorful icons
  disabled?: boolean; // For conditional tab accessibility
}

export interface TabWithModes {
  id: string;
  label: string;
  icon: string;
  isMain?: boolean;
  modes?: ModeOption[];
  currentMode?: string;
}

export interface DropdownState {
  isOpen: boolean;
  tabId: string | null;
  showDiscoveryHint: boolean;
}

export interface OnboardingState {
  hasSeenBuildModes: boolean;
  hasSeenLearnModes: boolean;
  showTooltips: boolean;
}

// New types for module-based navigation
export type ModuleId = "build" | "explore" | "learn" | "write" | "word_card";

export interface ModuleDefinition {
  id: ModuleId;
  label: string;
  icon: string;
  description?: string;
  isMain: boolean;
  subModes: ModeOption[];
}

export interface ModuleSelectorState {
  isOpen: boolean;
  showDiscoveryHint: boolean;
}

export interface NavigationMode {
  module: ModuleId;
  subMode: string;
}
