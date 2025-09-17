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
