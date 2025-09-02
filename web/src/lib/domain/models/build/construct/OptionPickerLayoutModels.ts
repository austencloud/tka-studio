/**
 * Layout Domain Types
 *
 * Core types for layout calculations, device detection, and responsive design
 */

// ============================================================================
// DEVICE AND VIEWPORT TYPES
// ============================================================================

import type {
  ContainerAspect,
  DeviceType,
  LayoutCategory,
} from "$domain";

// ============================================================================
// CONFIGURATION TYPES
// ============================================================================

export interface DeviceConfig {
  padding: {
    horizontal: number;
    vertical: number;
  };
  gap: number;
  minItemSize: number;
  maxItemSize: number;
  scaleFactor: number;
}

export interface LayoutTemplate {
  cols: number;
  class: string;
}

export interface TwoItemsLayoutTemplate {
  horizontal: LayoutTemplate;
  vertical: LayoutTemplate;
}

export interface ResponsiveLayoutTemplates {
  singleItem: LayoutTemplate;
  twoItems: TwoItemsLayoutTemplate;
  fewItems: {
    portraitDevice: LayoutTemplate;
    landscapeDevice: LayoutTemplate;
  };
  mediumItems: {
    portraitDevice: LayoutTemplate;
    landscapeDevice: LayoutTemplate;
  };
  manyItems: {
    portraitDevice: LayoutTemplate;
    landscapeDevice: LayoutTemplate;
  };
}

// ============================================================================
// BREAKPOINT CONFIGURATION
// ============================================================================

export interface BreakpointConfig {
  smallMobile: number;
  mobile: number;
  tablet: number;
  laptop: number;
  desktop: number;
  largeDesktop: number;
}

export interface AspectRatioConfig {
  tall: number;
  square: number;
  wide: number;
}

// ============================================================================
// FOLDABLE DEVICE TYPES
// ============================================================================

export interface FoldableDeviceSpec {
  models: string[];
  foldedDimensions: {
    width: { min: number; max: number };
    height: { min: number; max: number };
  };
  unfoldedDimensions: {
    width: { min: number; max: number };
    height: { min: number; max: number };
  };
}

export interface FoldableDetectionResult {
  isFoldable: boolean;
  isUnfolded: boolean;
  detectedDevice: string | null;
  confidence: number;
  aspectRatio: number;
  debugInfo?: {
    userAgent: string;
    dimensions: { width: number; height: number };
    matchedSpecs?: string[];
  };
}

// ============================================================================
// OPTION PICKER LAYOUT CALCULATION TYPES
// ============================================================================

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
  layoutCategory: LayoutCategory;
  canFitHorizontally: boolean;
  optimalSize: number;
  debugInfo?: {
    userAgent: string;
    dimensions: { width: number; height: number };
    matchedSpecs?: string[];
  };
}

export interface ResponsiveLayoutConfig {
  gridColumns: string;
  optionSize: string;
  gridGap: string;
  gridClass: string;
  aspectClass: string;
  scaleFactor: number;
}

// Re-export types for convenience
export type { ContainerAspect, DeviceType, LayoutCategory };

