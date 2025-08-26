/**
 * Layout utilities for option picker responsive design
 */

import type {
  DeviceType,
  ResponsiveLayoutConfig,
  ContainerAspect,
} from "../config";
import { DEFAULT_LAYOUTS } from "../config";
import type { FoldableDetectionResult } from "./deviceDetection";

export interface DeviceInfo {
  type: DeviceType;
  width: number;
  height: number;
  isFoldable: boolean;
}

export interface LayoutMetrics {
  itemSize: number;
  columns: number;
  rows: number;
  gap: number;
  padding: number;
}

export interface ScrollBehaviorConfig {
  smoothScrolling: boolean;
  scrollThreshold: number;
  debounceMs: number;
}

export interface EnhancedDeviceType {
  base: DeviceType;
  deviceType: DeviceType; // Add for compatibility
  isFoldable: boolean;
  orientation: "portrait" | "landscape";
}

/**
 * Get enhanced device type with additional context
 */
export function getEnhancedDeviceType(
  baseType: DeviceType,
  foldableResult: FoldableDetectionResult,
  isLandscape: boolean
): EnhancedDeviceType {
  return {
    base: baseType,
    deviceType: baseType, // Add for compatibility
    isFoldable: foldableResult.isFoldable,
    orientation: isLandscape ? "landscape" : "portrait",
  };
}

/**
 * Get responsive layout configuration for device
 */
export function getResponsiveLayout(
  deviceType: DeviceType,
  containerWidth: number,
  containerHeight: number
): ResponsiveLayoutConfig {
  const baseLayout = DEFAULT_LAYOUTS[deviceType];

  // Adjust layout based on container dimensions
  const aspectRatio = containerWidth / containerHeight;
  let adjustedColumns = baseLayout.columns;

  if (aspectRatio > 2) {
    // Very wide container - add more columns
    adjustedColumns = Math.min(baseLayout.columns + 1, 6);
  } else if (aspectRatio < 0.8) {
    // Tall container - reduce columns
    adjustedColumns = Math.max(baseLayout.columns - 1, 1);
  }

  return {
    ...baseLayout,
    columns: adjustedColumns,
  };
}

/**
 * Calculate container aspect ratio
 */
export function getContainerAspect(
  width: number,
  height: number
): ContainerAspect {
  const ratio = width / height;

  if (ratio > 1.2) return "landscape";
  if (ratio < 0.8) return "portrait";
  return "square";
}

/**
 * Calculate optimal item size based on container and columns
 */
export function calculateOptimalItemSize(
  containerWidth: number,
  columns: number,
  gap: number,
  padding: number
): number {
  const availableWidth = containerWidth - padding * 2 - gap * (columns - 1);
  return Math.floor(availableWidth / columns);
}

/**
 * Calculate grid dimensions
 */
export interface GridDimensions {
  itemWidth: number;
  itemHeight: number;
  totalWidth: number;
  totalHeight: number;
  rows: number;
}

export function calculateGridDimensions(
  itemCount: number,
  layout: ResponsiveLayoutConfig,
  containerWidth: number
): GridDimensions {
  const { columns, gap, padding } = layout;
  const rows = Math.ceil(itemCount / columns);

  const itemWidth = calculateOptimalItemSize(
    containerWidth,
    columns,
    gap,
    padding
  );
  const itemHeight = itemWidth; // Square items

  const totalWidth = containerWidth;
  const totalHeight = rows * itemHeight + (rows - 1) * gap + padding * 2;

  return {
    itemWidth,
    itemHeight,
    totalWidth,
    totalHeight,
    rows,
  };
}
