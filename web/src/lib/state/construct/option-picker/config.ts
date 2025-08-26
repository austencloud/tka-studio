/**
 * Configuration types and constants for option picker state management
 */

// Device types
export type DeviceType = "mobile" | "tablet" | "desktop";

// Container aspects
export type ContainerAspect = "square" | "landscape" | "portrait";

// Import the actual enum
import { OptionPickerSortMethod } from "$lib/domain";

// Sort methods - use the actual enum
export type SortMethod = OptionPickerSortMethod;

// Breakpoints for responsive design
export const BREAKPOINTS = {
  mobile: 768,
  tablet: 1024,
  desktop: 1200,
} as const;

// Responsive layout configuration
export interface ResponsiveLayoutConfig {
  columns: number;
  itemSize: number;
  gap: number;
  padding: number;
  gridColumns?: string;
  optionSize?: string;
  gridGap?: string;
  gridClass?: string;
}

// Default responsive layouts
export const DEFAULT_LAYOUTS: Record<DeviceType, ResponsiveLayoutConfig> = {
  mobile: {
    columns: 2,
    itemSize: 120,
    gap: 8,
    padding: 16,
  },
  tablet: {
    columns: 3,
    itemSize: 140,
    gap: 12,
    padding: 20,
  },
  desktop: {
    columns: 4,
    itemSize: 160,
    gap: 16,
    padding: 24,
  },
};

// Animation durations
export const ANIMATION_DURATIONS = {
  fast: 150,
  normal: 300,
  slow: 500,
} as const;

// Scroll behavior configuration
export interface ScrollBehaviorConfig {
  smoothScrolling: boolean;
  scrollThreshold: number;
  debounceMs: number;
}

export const DEFAULT_SCROLL_CONFIG: ScrollBehaviorConfig = {
  smoothScrolling: true,
  scrollThreshold: 50,
  debounceMs: 100,
};

// Utility functions
export function getContainerAspect(
  width: number,
  height: number
): ContainerAspect {
  const ratio = width / height;

  if (ratio > 1.2) return "landscape";
  if (ratio < 0.8) return "portrait";
  return "square";
}
