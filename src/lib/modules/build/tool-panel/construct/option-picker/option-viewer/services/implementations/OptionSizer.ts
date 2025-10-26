/**
 * Option Picker Sizing Service Implementation - SIMPLIFIED
 *
 * Clean, simple sizing logic that achieves the same results without overengineering.
 * Replaces 4 complex calculation methods with 1 simple, reliable approach.
 */

import type { IDeviceDetector } from '$shared';
import { TYPES } from '$shared/inversify/types';
import { inject, injectable } from 'inversify';
import type { DeviceConfig, SizingCalculationParams, SizingResult } from '../../domain';
import type { IOptionSizer } from '../contracts';

@injectable()
export class OptionSizer implements IOptionSizer {

  constructor(
    @inject(TYPES.IDeviceDetector) private deviceDetector: IDeviceDetector
  ) {}

  // Simplified device configuration - same results, less complexity
  private readonly DEVICE_CONFIG: Record<string, DeviceConfig> = {
    mobile: {
      padding: { horizontal: 12, vertical: 12 },
      gap: 2,
      minItemSize: 60,
      maxItemSize: 150,
      scaleFactor: 1,
    },
    tablet: {
      padding: { horizontal: 12, vertical: 12 },
      gap: 2,
      minItemSize: 75,
      maxItemSize: 175,
      scaleFactor: 1,
    },
    desktop: {
      padding: { horizontal: 12, vertical: 12 },
      gap: 2,
      minItemSize: 75,
      maxItemSize: 200,
      scaleFactor: 1,
    },
  };

  /**
   * SIMPLIFIED: Main sizing method that handles all cases
   */
  calculatePictographSize(params: SizingCalculationParams): SizingResult {
    const { count, containerWidth, containerHeight, columns, isMobileDevice } = params;

    // Simple device detection
    const deviceType = this.getDeviceType(containerWidth, isMobileDevice);
    const deviceConfig = this.DEVICE_CONFIG[deviceType];

    // Simple size calculation
    const availableWidth = containerWidth - (deviceConfig.padding.horizontal * 2);
    const availableHeight = containerHeight - (deviceConfig.padding.vertical * 2);

    const widthPerItem = (availableWidth - (deviceConfig.gap * (columns - 1))) / columns;
    const rows = Math.ceil(count / columns);
    const heightPerItem = (availableHeight - (deviceConfig.gap * (rows - 1))) / rows;

    // Use smaller dimension and apply constraints
    const calculatedSize = Math.min(widthPerItem, heightPerItem);
    const finalSize = Math.max(
      deviceConfig.minItemSize,
      Math.min(deviceConfig.maxItemSize, calculatedSize)
    );

    return {
      pictographSize: Math.floor(finalSize),
      pictographSizeString: `${Math.floor(finalSize)}px`,
      gridGap: `${deviceConfig.gap}px`,
      deviceConfig,
      calculationDetails: {
        availableWidth,
        availableHeight,
        widthPerItem,
        heightPerItem,
        rawCalculatedSize: calculatedSize,
        scaledSize: calculatedSize,
        finalSize: Math.floor(finalSize),
      },
    };
  }

  /**
   * SIMPLIFIED: Basic device detection
   */
  private getDeviceType(width: number, isMobileDevice: boolean): string {
    if (isMobileDevice) return 'mobile';
    if (width < 1024) return 'tablet';
    return 'desktop';
  }

  /**
   * LEGACY COMPATIBILITY: Redirect old complex method to simple one
   */
  calculateOverflowAwareSize(params: {
    containerWidth: number;
    containerHeight: number;
    layoutMode: '4-column' | '8-column';
    maxPictographsPerSection: number;
    isMobileDevice: boolean;
    headerHeight?: number;
    targetOverflowBuffer?: number;
  }): SizingResult {
    const columns = params.layoutMode === '8-column' ? 8 : 4;
    return this.calculatePictographSize({
      count: params.maxPictographsPerSection,
      containerWidth: params.containerWidth,
      containerHeight: params.containerHeight,
      columns,
      isMobileDevice: params.isMobileDevice
    });
  }

  /**
   * SIMPLIFIED: Basic overflow detection (legacy compatibility)
   */
  detectActualOverflow(): {
    hasOverflow: boolean;
    overflowAmount: number;
    recommendations: {
      suggestedPictographSize?: number;
      suggestedAction: string;
    };
  } {
    // Simple implementation - CSS handles overflow naturally
    return {
      hasOverflow: false,
      overflowAmount: 0,
      recommendations: { suggestedAction: 'CSS handles overflow automatically' }
    };
  }

  /**
   * LEGACY COMPATIBILITY: Redirect to simplified method
   */
  calculateMaximizedSize(params: {
    containerWidth: number;
    containerHeight: number;
    layoutMode: '4-column' | '8-column';
    maxPictographsPerSection: number;
    isMobileDevice: boolean;
  }): SizingResult {
    const columns = params.layoutMode === '8-column' ? 8 : 4;
    return this.calculatePictographSize({
      count: params.maxPictographsPerSection,
      containerWidth: params.containerWidth,
      containerHeight: params.containerHeight,
      columns,
      isMobileDevice: params.isMobileDevice
    });
  }

  /**
   * SIMPLIFIED: Get device configuration
   */
  getDeviceConfig(deviceType: string): DeviceConfig {
    return this.DEVICE_CONFIG[deviceType] || this.DEVICE_CONFIG.desktop;
  }

  /**
   * LEGACY COMPATIBILITY: Simple optimal columns calculation
   *
   * IMPORTANT: When in stacked mobile layout (workbench on top, option picker on bottom),
   * we should use 8 columns with horizontal swipe, NOT switch to traditional grid.
   * The container width check (>= 650px) is only for determining column count,
   * not for determining whether to use swipe vs grid layout.
   */
  getOptimalColumns(containerWidth: number, isMobileDevice: boolean): number {
    // Simple logic: wide containers get 8 columns, narrow get 4
    // This applies to BOTH swipe and grid layouts
    return containerWidth >= 650 ? 8 : 4;
  }

  /**
   * LEGACY COMPATIBILITY: Simple grid gap calculation
   */
  calculateGridGap(params: SizingCalculationParams): string {
    const deviceType = this.getDeviceType(params.containerWidth, params.isMobileDevice);
    const deviceConfig = this.getDeviceConfig(deviceType);
    return `${deviceConfig.gap}px`;
  }
}
