/**
 * Layout Configuration
 *
 * Domain configuration for responsive layouts, breakpoints, and device settings
 */

import type {
  BreakpointConfig,
  AspectRatioConfig,
  DeviceConfig,
  DeviceType,
  ResponsiveLayoutTemplates,
  LayoutCategory,
  FoldableDeviceSpec,
} from "./types";

// ============================================================================
// BREAKPOINTS
// ============================================================================

export const BREAKPOINTS: BreakpointConfig = {
  smallMobile: 375,
  mobile: 480,
  tablet: 768,
  laptop: 1024,
  desktop: 1280,
  largeDesktop: 1600,
};

// ============================================================================
// ASPECT RATIO THRESHOLDS
// ============================================================================

export const ASPECT_RATIO: AspectRatioConfig = {
  tall: 0.8,
  square: 1.3,
  wide: 2.0,
};

// ============================================================================
// DEVICE CONFIGURATION
// ============================================================================

export const DEVICE_CONFIG: Record<DeviceType, DeviceConfig> = {
  smallMobile: {
    padding: { horizontal: 12, vertical: 12 },
    gap: 2,
    minItemSize: 80,
    maxItemSize: 150,
    scaleFactor: 1,
  },
  mobile: {
    padding: { horizontal: 12, vertical: 12 },
    gap: 2,
    minItemSize: 80,
    maxItemSize: 175,
    scaleFactor: 1,
  },
  tablet: {
    padding: { horizontal: 12, vertical: 12 },
    gap: 2,
    minItemSize: 80,
    maxItemSize: 175,
    scaleFactor: 1,
  },
  desktop: {
    padding: { horizontal: 12, vertical: 12 },
    gap: 2,
    minItemSize: 90,
    maxItemSize: 180,
    scaleFactor: 1,
  },
  largeDesktop: {
    padding: { horizontal: 12, vertical: 12 },
    gap: 2,
    minItemSize: 100,
    maxItemSize: 200,
    scaleFactor: 1,
  },
};

// ============================================================================
// LAYOUT TEMPLATES
// ============================================================================

export const LAYOUT_TEMPLATES: ResponsiveLayoutTemplates = {
  singleItem: {
    cols: 1,
    class: "single-item-grid",
  },
  twoItems: {
    horizontal: { cols: 2, class: "two-item-grid horizontal-layout" },
    vertical: { cols: 1, class: "two-item-grid vertical-layout" },
  },
  fewItems: {
    portraitDevice: { cols: 4, class: "few-items-grid" },
    landscapeDevice: { cols: 4, class: "few-items-grid" },
  },
  mediumItems: {
    portraitDevice: { cols: 4, class: "medium-items-grid" },
    landscapeDevice: { cols: 4, class: "medium-items-grid" },
  },
  manyItems: {
    portraitDevice: { cols: 4, class: "many-items-grid" },
    landscapeDevice: { cols: 4, class: "many-items-grid" },
  },
};

// ============================================================================
// GAP ADJUSTMENTS
// ============================================================================

export const GAP_ADJUSTMENTS: Record<LayoutCategory, number> = {
  singleItem: 0,
  twoItems: 3,
  fewItems: 3,
  mediumItems: 3,
  manyItems: 3,
};

// ============================================================================
// FOLDABLE DEVICE SPECIFICATIONS
// ============================================================================

export const FOLDABLE_DEVICE_SPECS: Record<string, FoldableDeviceSpec> = {
  zfold3: {
    models: ["SM-F926"],
    foldedDimensions: {
      width: { min: 350, max: 400 },
      height: { min: 800, max: 900 },
    },
    unfoldedDimensions: {
      width: { min: 700, max: 800 },
      height: { min: 800, max: 900 },
    },
  },
  zfold4: {
    models: ["SM-F936"],
    foldedDimensions: {
      width: { min: 350, max: 400 },
      height: { min: 800, max: 900 },
    },
    unfoldedDimensions: {
      width: { min: 700, max: 800 },
      height: { min: 800, max: 900 },
    },
  },
  zfold5: {
    models: ["SM-F946"],
    foldedDimensions: {
      width: { min: 350, max: 400 },
      height: { min: 800, max: 900 },
    },
    unfoldedDimensions: {
      width: { min: 700, max: 820 },
      height: { min: 800, max: 920 },
    },
  },
  zfold6: {
    models: ["SM-F956"],
    foldedDimensions: {
      width: { min: 350, max: 400 },
      height: { min: 800, max: 900 },
    },
    unfoldedDimensions: {
      width: { min: 700, max: 820 },
      height: { min: 800, max: 920 },
    },
  },
};
