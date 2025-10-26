/**
 * Option Picker Sizing Service Interface
 *
 * Provides centralized sizing calculations for consistent pictograph sizing
 * across all sections and groups in the option picker.
 */

import type { DeviceConfig, SizingCalculationParams, SizingResult } from "../../domain";


export interface IOptionSizer {
  /**
   * Calculate consistent pictograph size for all sections
   * This is the main method that ensures all pictographs are the same size
   */
  calculatePictographSize(params: SizingCalculationParams): SizingResult;

  /**
   * Calculate maximized pictograph size based on layout constraints
   * This method maximizes space usage for the given layout mode
   */
  calculateMaximizedSize(params: {
    containerWidth: number;
    containerHeight: number;
    layoutMode: '4-column' | '8-column';
    maxPictographsPerSection: number;
    isMobileDevice: boolean;
  }): SizingResult;

  /**
   * Calculate size that prevents overflow by iteratively testing sizes
   * This method ensures content fits within available space
   */
  calculateOverflowAwareSize(params: {
    containerWidth: number;
    containerHeight: number;
    layoutMode: '4-column' | '8-column';
    maxPictographsPerSection: number;
    isMobileDevice: boolean;
    headerHeight?: number;
    targetOverflowBuffer?: number;
  }): SizingResult;

  /**
   * Real-time overflow detection for actual DOM elements
   */
  detectActualOverflow(): {
    hasOverflow: boolean;
    overflowAmount: number;
    recommendations: {
      suggestedPictographSize?: number;
      suggestedAction: string;
    };
  };

  /**
   * Get device configuration for a specific device type
   */
  getDeviceConfig(deviceType: string): DeviceConfig;

  /**
   * Calculate grid gap based on device and container
   */
  calculateGridGap(params: SizingCalculationParams): string;

  /**
   * Get the optimal number of columns for the given parameters
   */
  getOptimalColumns(containerWidth: number, isMobileDevice: boolean): number;
}
