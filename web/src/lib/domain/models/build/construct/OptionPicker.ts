/**
 * Option Picker Domain Types
 *
 * Types for option picker layout, configuration, and responsive behavior.
 */

// Import authoritative types from layout domain
import type { ContainerAspect, DeviceType } from "$domain";

export interface LayoutDimensions {
  width: number;
  height: number;
}

export interface GridConfiguration {
  columns: number;
  gap: string;
  itemSize: number;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
}

export interface ResponsiveLayoutConfig {
  gridColumns: string;
  optionSize: string;
  gridGap: string;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
}

export interface LayoutCalculationParams {
  count: number;
  containerWidth: number;
  containerHeight: number;
  windowWidth?: number;
  windowHeight?: number;
  isMobileUserAgent?: boolean;
}

export interface LayoutCalculationResult {
  optionsPerRow: number;
  optionSize: number;
  gridGap: string;
  gridColumns: string;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
  deviceType: DeviceType;
  containerAspect: ContainerAspect;
  isMobile: boolean;
  isTablet: boolean;
  isPortrait: boolean;
  layoutConfig: ResponsiveLayoutConfig;
}

// Keep the option-picker specific interface separate for clarity
export interface OptionPickerGridConfiguration {
  columns: number;
  gap: string;
  itemSize: number;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
}

export interface OptionPickerLayoutCalculationParams {
  count: number;
  containerWidth: number;
  containerHeight: number;
  windowWidth?: number;
  windowHeight?: number;
  isMobileUserAgent?: boolean;
}

export interface OptionPickerLayoutCalculationResult {
  optionsPerRow: number;
  optionSize: number;
  gridGap: string;
  gridColumns: string;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
  deviceType: DeviceType;
  containerAspect: ContainerAspect;
  // Computed properties for backward compatibility
  isMobile: boolean;
  isTablet: boolean;
  isPortrait: boolean;
}
