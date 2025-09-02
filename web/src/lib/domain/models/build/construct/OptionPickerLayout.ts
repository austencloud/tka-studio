/**
 * Option Picker Layout Domain Types
 *
 * Types for option picker layout calculations, grid configuration,
 * and responsive layout management specific to the construct tab.
 */

// ============================================================================
// OPTION PICKER LAYOUT TYPES
// ============================================================================

export interface OptionPickerLayoutDimensions {
  width: number;
  height: number;
}

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
