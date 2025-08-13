/**
 * OptionPickerLayoutManager - Sophisticated layout calculations using the advanced layout system
 *
 * Replaces the simple layout calculations with the full sophisticated system
 * from the legacy implementation, including device detection, responsive layouts,
 * and performance optimizations.
 */

import {
  getContainerAspect,
  type ContainerAspect,
  type DeviceType,
  type ResponsiveLayoutConfig,
} from "./config";
import {
  detectFoldableDevice,
  type FoldableDetectionResult,
} from "./utils/deviceDetection";
import {
  getEnhancedDeviceType,
  getResponsiveLayout,
} from "./utils/layoutUtils";

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
  foldableInfo: FoldableDetectionResult;
  layoutConfig: ResponsiveLayoutConfig;
}

export class OptionPickerLayoutManager {
  private static lastCalculationKey: string = "";
  private static lastCalculationResult: LayoutCalculationResult | null = null;

  /**
   * Calculate sophisticated responsive layout using the advanced layout system
   */
  static calculateLayout(
    params: LayoutCalculationParams,
  ): LayoutCalculationResult {
    const {
      count,
      containerWidth,
      containerHeight,
      windowWidth = containerWidth,
      windowHeight = containerHeight,
      isMobileUserAgent = false,
    } = params;

    // Create a cache key for this calculation
    const cacheKey = `${count}:${containerWidth}:${containerHeight}:${windowWidth}:${windowHeight}:${isMobileUserAgent}`;

    // Return cached result if the parameters haven't changed
    if (this.lastCalculationKey === cacheKey && this.lastCalculationResult) {
      return this.lastCalculationResult;
    }

    // Detect foldable device
    const foldableInfo = detectFoldableDevice();

    // Get enhanced device information
    const enhancedDeviceInfo = getEnhancedDeviceType(
      containerWidth,
      isMobileUserAgent,
    );
    const deviceType = enhancedDeviceInfo.deviceType;
    const isMobile = deviceType === "smallMobile" || deviceType === "mobile";
    const isTablet = deviceType === "tablet";
    const isPortrait = containerHeight > containerWidth;
    const containerAspect = getContainerAspect(containerWidth, containerHeight);

    // Get the sophisticated responsive layout configuration
    const layoutConfig = getResponsiveLayout(
      count,
      containerHeight,
      containerWidth,
      isMobile,
      isPortrait,
      foldableInfo,
    );

    // Extract grid columns count from the CSS grid template
    const columnsMatch = layoutConfig.gridColumns.match(/repeat\((\d+),/);
    const optionsPerRow =
      columnsMatch && columnsMatch[1] ? parseInt(columnsMatch[1], 10) : 4;

    // Parse option size (remove 'px' suffix)
    const optionSizeMatch = layoutConfig.optionSize.match(/(\d+)px/);
    const optionSize =
      optionSizeMatch && optionSizeMatch[1]
        ? parseInt(optionSizeMatch[1], 10)
        : 100;

    const result: LayoutCalculationResult = {
      optionsPerRow,
      optionSize,
      gridGap: layoutConfig.gridGap,
      gridColumns: layoutConfig.gridColumns,
      gridClass: layoutConfig.gridClass,
      aspectClass: layoutConfig.aspectClass,
      scaleFactor: layoutConfig.scaleFactor,
      deviceType,
      containerAspect,
      isMobile,
      isTablet,
      isPortrait,
      foldableInfo,
      layoutConfig,
    };

    // Cache the result
    this.lastCalculationKey = cacheKey;
    this.lastCalculationResult = result;

    return result;
  }

  /**
   * Legacy compatibility method - simplified interface
   */
  static calculateSimpleLayout(containerWidth: number): {
    optionsPerRow: number;
    optionSize: number;
  } {
    const result = this.calculateLayout({
      count: 10, // Default count for legacy compatibility
      containerWidth,
      containerHeight: 600, // Default height
    });

    return {
      optionsPerRow: result.optionsPerRow,
      optionSize: result.optionSize,
    };
  }

  /**
   * Get responsive layout configuration for a specific count and container dimensions
   */
  static getResponsiveConfig(
    count: number,
    containerWidth: number,
    containerHeight: number,
  ): ResponsiveLayoutConfig {
    const result = this.calculateLayout({
      count,
      containerWidth,
      containerHeight,
    });

    return result.layoutConfig;
  }

  /**
   * Determine if the current layout should use mobile optimizations
   */
  static shouldUseMobileLayout(
    containerWidth: number,
    _isMobileUserAgent?: boolean,
  ): boolean {
    const result = this.calculateLayout({
      count: 1, // Minimal count for device detection
      containerWidth,
      containerHeight: 400, // Default height for detection
    });

    return result.isMobile;
  }

  /**
   * Get device information for the current container dimensions
   */
  static getDeviceInfo(containerWidth: number, _isMobileUserAgent?: boolean) {
    const result = this.calculateLayout({
      count: 1,
      containerWidth,
      containerHeight: 400,
    });

    return {
      deviceType: result.deviceType,
      isMobile: result.isMobile,
      isTablet: result.isTablet,
      foldableInfo: result.foldableInfo,
    };
  }

  /**
   * Calculate optimal option size for given parameters
   */
  static calculateOptimalOptionSize(
    count: number,
    containerWidth: number,
    containerHeight: number,
    targetColumns?: number,
  ): number {
    if (targetColumns) {
      // If specific column count is requested, calculate directly
      const padding = 24; // Total horizontal padding
      const gapSize = 8; // Estimated gap size
      const totalGap = (targetColumns - 1) * gapSize;
      const availableWidth = containerWidth - padding - totalGap;
      return Math.floor(availableWidth / targetColumns);
    }

    // Use the sophisticated layout system
    const result = this.calculateLayout({
      count,
      containerWidth,
      containerHeight,
    });

    return result.optionSize;
  }

  /**
   * Get grid gap for given parameters
   */
  static calculateGridGap(
    count: number,
    containerWidth: number,
    containerHeight: number,
  ): string {
    const result = this.calculateLayout({
      count,
      containerWidth,
      containerHeight,
    });

    return result.gridGap;
  }

  /**
   * Clear the layout calculation cache
   */
  static clearCache() {
    this.lastCalculationKey = "";
    this.lastCalculationResult = null;
  }
}
