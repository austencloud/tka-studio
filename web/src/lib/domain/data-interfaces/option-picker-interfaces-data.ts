/**
 * Option Picker Service Interfaces
 *
 * Interfaces for option picker layout calculations, device detection,
 * and responsive grid configuration specific to the option picker component.
 */
// ============================================================================
// LAYOUT CALCULATION INTERFACES
// ============================================================================
import type {
  ContainerAspect,
  DeviceType,
} from "$domain/build/option-picker/layout/types";

// ============================================================================
// DATA CONTRACTS (Domain Models)
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
  isMobile: boolean;
  isTablet: boolean;
  isPortrait: boolean;
}
