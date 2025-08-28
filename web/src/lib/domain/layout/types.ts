/**
 * Layout Domain Types
 *
 * Core types for layout calculations, device detection, and responsive design
 */

// ============================================================================
// DEVICE AND VIEWPORT TYPES
// ============================================================================

export type DeviceType =
  | "smallMobile"
  | "mobile"
  | "tablet"
  | "desktop"
  | "largeDesktop";

export type ContainerAspect = "tall" | "square" | "wide";

export type LayoutCategory =
  | "singleItem"
  | "twoItems"
  | "fewItems"
  | "mediumItems"
  | "manyItems";

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
