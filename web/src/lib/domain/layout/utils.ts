/**
 * Layout Domain Utils
 *
 * Pure domain logic for layout calculations and device type determination
 */

import { ASPECT_RATIO, BREAKPOINTS, DEVICE_CONFIG } from "./config";
import type {
  ContainerAspect,
  DeviceType,
  LayoutCategory,
  DeviceConfig,
} from "./types";

// ============================================================================
// CONTAINER ASPECT RATIO
// ============================================================================

/**
 * Determines container aspect ratio based on dimensions
 */
export function getContainerAspect(
  width: number,
  height: number
): ContainerAspect {
  if (!width || !height) return "square";
  const ratio = width / height;
  if (ratio < ASPECT_RATIO.tall) return "tall";
  if (ratio > ASPECT_RATIO.square) return "wide";
  return "square";
}

// ============================================================================
// DEVICE TYPE DETECTION
// ============================================================================

/**
 * Determines the device type based on container width and mobile status
 */
export function getDeviceType(
  width: number,
  _isMobileUserAgent: boolean
): DeviceType {
  if (width < BREAKPOINTS.mobile) {
    return width < BREAKPOINTS.smallMobile ? "smallMobile" : "mobile";
  }
  if (width < BREAKPOINTS.tablet) return "mobile";
  if (width < BREAKPOINTS.laptop) return "tablet";
  if (width < BREAKPOINTS.desktop) return "desktop";
  return "largeDesktop";
}

/**
 * Gets a simplified device category
 */
export function getSimplifiedDeviceCategory(
  width: number
): "mobile" | "tablet" | "desktop" {
  if (width < BREAKPOINTS.tablet) return "mobile";
  if (width < BREAKPOINTS.laptop) return "tablet";
  return "desktop";
}

// ============================================================================
// LAYOUT CATEGORIES
// ============================================================================

/**
 * Gets the layout category based on item count
 */
export function getLayoutCategory(count: number): LayoutCategory {
  if (count === 1) return "singleItem";
  if (count === 2) return "twoItems";
  if (count <= 8) return "fewItems";
  if (count <= 16) return "mediumItems";
  return "manyItems";
}

// ============================================================================
// DEVICE CONFIGURATION
// ============================================================================

/**
 * Gets the device config for a specific device type
 */
export function getDeviceConfig(deviceType: DeviceType): DeviceConfig {
  return DEVICE_CONFIG[deviceType] || DEVICE_CONFIG.desktop;
}

// ============================================================================
// VALIDATION HELPERS
// ============================================================================

/**
 * Validates if dimensions are reasonable for layout calculations
 */
export function validateDimensions(width: number, height: number): boolean {
  return width > 0 && height > 0 && width < 10000 && height < 10000;
}

/**
 * Sanitizes dimensions to prevent invalid calculations
 */
export function sanitizeDimensions(
  width: number,
  height: number
): {
  width: number;
  height: number;
} {
  return {
    width: Math.max(1, Math.min(width, 9999)),
    height: Math.max(1, Math.min(height, 9999)),
  };
}
