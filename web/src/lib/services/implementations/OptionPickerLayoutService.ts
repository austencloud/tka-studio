/**
 * Option Picker Layout Service Implementation
 *
 * Handles layout calculations, responsive grid configuration,
 * and device-specific optimizations for the option picker component.
 */
import { getContainerAspect, getDeviceConfig, getDeviceType } from "$domain";
import type {
  DeviceType,
  OptionPickerLayoutCalculationParams,
  OptionPickerLayoutCalculationResult,
} from "$domain";
import { injectable } from "inversify";
import type { IOptionPickerLayoutService } from "$contracts";

@injectable()
export class OptionPickerLayoutService implements IOptionPickerLayoutService {
  private static lastCalculationKey: string = "";
  private static lastCalculationResult: OptionPickerLayoutCalculationResult | null =
    null;

  // ============================================================================
  // TYPE CONVERSION HELPERS
  // ============================================================================

  // Type conversion functions are no longer needed since we're using the same types

  /**
   * Calculate sophisticated responsive layout for option picker
   */
  calculateLayout(
    params: OptionPickerLayoutCalculationParams
  ): OptionPickerLayoutCalculationResult {
    const {
      count,
      containerWidth,
      containerHeight,
      windowWidth = containerWidth,
      windowHeight = containerHeight,
      isMobileUserAgent = false,
    } = params;

    // Create cache key for this calculation
    const cacheKey = `${count}:${containerWidth}:${containerHeight}:${windowWidth}:${windowHeight}:${isMobileUserAgent}`;

    // Return cached result if parameters haven't changed
    if (
      OptionPickerLayoutService.lastCalculationKey === cacheKey &&
      OptionPickerLayoutService.lastCalculationResult
    ) {
      return OptionPickerLayoutService.lastCalculationResult;
    }

    // Get device and layout information
    const deviceType = getDeviceType(containerWidth, isMobileUserAgent);
    const containerAspect = getContainerAspect(containerWidth, containerHeight);

    const isMobile = deviceType === "smallMobile" || deviceType === "mobile";
    const isTablet = deviceType === "tablet";
    const isPortrait = containerAspect === "tall";

    // Calculate grid configuration
    const gridConfig = this.calculateGridConfiguration(
      count,
      containerWidth,
      containerHeight,
      deviceType,
      isPortrait,
      isMobile
    );

    const result: OptionPickerLayoutCalculationResult = {
      optionsPerRow: gridConfig.columns,
      optionSize: gridConfig.itemSize,
      gridGap: gridConfig.gap,
      gridColumns: `repeat(${gridConfig.columns}, 1fr)`,
      gridClass: gridConfig.gridClass,
      aspectClass: gridConfig.aspectClass,
      scaleFactor: gridConfig.scaleFactor,
      deviceType,
      containerAspect,
      isMobile,
      isTablet,
      isPortrait,
    };

    // Cache the result
    OptionPickerLayoutService.lastCalculationKey = cacheKey;
    OptionPickerLayoutService.lastCalculationResult = result;

    return result;
  }

  /**
   * Get simple layout metrics
   */
  getSimpleLayout(
    count: number,
    containerWidth: number,
    containerHeight: number
  ): {
    optionsPerRow: number;
    optionSize: number;
  } {
    const result = this.calculateLayout({
      count,
      containerWidth,
      containerHeight,
    });

    return {
      optionsPerRow: result.optionsPerRow,
      optionSize: result.optionSize,
    };
  }

  /**
   * Calculate optimal option size
   */
  calculateOptimalOptionSize(
    count: number,
    containerWidth: number,
    containerHeight: number,
    targetColumns?: number
  ): number {
    if (targetColumns) {
      // Direct calculation for specific column count
      const padding = 24; // Total horizontal padding
      const gapSize = 8; // Estimated gap size
      const totalGap = (targetColumns - 1) * gapSize;
      const availableWidth = containerWidth - padding - totalGap;
      return Math.floor(availableWidth / targetColumns);
    }

    const result = this.calculateLayout({
      count,
      containerWidth,
      containerHeight,
    });

    return result.optionSize;
  }

  /**
   * Calculate grid gap
   */
  calculateGridGap(
    count: number,
    containerWidth: number,
    containerHeight: number
  ): string {
    const result = this.calculateLayout({
      count,
      containerWidth,
      containerHeight,
    });

    return result.gridGap;
  }

  /**
   * Determine if mobile layout should be used
   */
  shouldUseMobileLayout(
    containerWidth: number,
    isMobileUserAgent?: boolean
  ): boolean {
    const result = this.calculateLayout({
      count: 1, // Minimal count for device detection
      containerWidth,
      containerHeight: 400, // Default height for detection
      isMobileUserAgent,
    });

    return result.isMobile;
  }

  /**
   * Clear layout calculation cache
   */
  clearCache(): void {
    OptionPickerLayoutService.lastCalculationKey = "";
    OptionPickerLayoutService.lastCalculationResult = null;
  }

  // ============================================================================
  // PRIVATE HELPER METHODS
  // ============================================================================

  /**
   * Calculate grid configuration based on parameters
   */
  private calculateGridConfiguration(
    count: number,
    containerWidth: number,
    containerHeight: number,
    deviceType: DeviceType,
    isPortrait: boolean,
    isMobile: boolean
  ): {
    columns: number;
    itemSize: number;
    gap: string;
    gridClass: string;
    aspectClass: string;
    scaleFactor: number;
  } {
    const deviceConfig = getDeviceConfig(deviceType);
    const columns = this.calculateOptimalColumns(
      count,
      containerWidth,
      isMobile,
      isPortrait
    );

    // Calculate item size based on available space
    const totalPadding = deviceConfig.padding.horizontal * 2;
    const gapSize = deviceConfig.gap;
    const totalGaps = (columns - 1) * gapSize;
    const availableWidth = containerWidth - totalPadding - totalGaps;

    let itemSize = Math.floor(availableWidth / columns);

    // Apply device constraints
    itemSize = Math.max(
      deviceConfig.minItemSize,
      Math.min(itemSize, deviceConfig.maxItemSize)
    );

    // Generate CSS classes
    const gridClass = this.generateGridClass(count, columns, deviceType);
    const aspectClass = this.generateAspectClass(
      containerWidth,
      containerHeight
    );

    return {
      columns,
      itemSize,
      gap: `${gapSize}px`,
      gridClass,
      aspectClass,
      scaleFactor: deviceConfig.scaleFactor,
    };
  }

  /**
   * Calculate optimal number of columns
   */
  private calculateOptimalColumns(
    count: number,
    containerWidth: number,
    isMobile: boolean,
    isPortrait: boolean
  ): number {
    // Handle special cases
    if (count === 1) return 1;
    if (count === 2) return isPortrait ? 1 : 2;

    // Base columns on device and container width
    let baseColumns: number;

    if (isMobile) {
      baseColumns = isPortrait ? 3 : 4;
    } else if (containerWidth < 600) {
      baseColumns = 3;
    } else if (containerWidth < 900) {
      baseColumns = 4;
    } else if (containerWidth < 1200) {
      baseColumns = 5;
    } else {
      baseColumns = 6;
    }

    // Adjust based on count
    if (count <= 4) {
      return Math.min(count, baseColumns);
    } else if (count <= 8) {
      return Math.min(4, baseColumns);
    } else {
      return baseColumns;
    }
  }

  /**
   * Generate appropriate grid CSS class
   */
  private generateGridClass(
    count: number,
    columns: number,
    deviceType: DeviceType
  ): string {
    const base = "option-picker-grid";
    const deviceClass = `${base}-${deviceType}`;
    const countClass =
      count === 1
        ? "single"
        : count === 2
          ? "double"
          : count <= 8
            ? "few"
            : "many";
    const columnClass = `cols-${columns}`;

    return `${base} ${deviceClass} ${base}-${countClass} ${base}-${columnClass}`;
  }

  /**
   * Generate aspect ratio CSS class
   */
  private generateAspectClass(width: number, height: number): string {
    const aspect = getContainerAspect(width, height);
    return `aspect-${aspect}`;
  }
}
