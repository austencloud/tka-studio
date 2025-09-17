/**
 * Mode Switcher Domain Types
 * 
 * Core types for the mode switcher component system.
 */

export interface ModeOption {
  id: string;
  label: string;
  icon: string;
  description?: string;
}

export interface ModeSwitcherProps {
  contextLabel?: string;
  currentMode: string;
  modes: ModeOption[];
  onModeChange: (mode: string) => void;
  showBreadcrumb?: boolean;
}
