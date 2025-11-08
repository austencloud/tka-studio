/**
 * Option Picker Sizing Service Interface
 *
 * Provides centralized sizing calculations for consistent pictograph sizing
 * across all sections and groups in the option picker.
 */

import type {
  DeviceConfig,
  SizingCalculationParams,
  SizingResult,
} from "../../domain";

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
    layoutMode: "4-column" | "8-column";
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
    layoutMode: "4-column" | "8-column";
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
   * Subscribe to overflow changes with automatic polling
   *
   * Monitors overflow every 2 seconds and calls callback when status changes.
   * Returns unsubscribe function for cleanup.
   *
   * @param callback Called when overflow status changes
   * @returns Unsubscribe function to stop monitoring
   */
  subscribeToOverflowChanges(
    callback: (hasOverflow: boolean, overflowAmount: number) => void
  ): () => void;

  /**
   * Determine if floating button should be used instead of full header
   *
   * Shows floating button when BOTH conditions are true:
   * 1. Pictographs are too small (< 80px threshold)
   * 2. Height is the constraining factor (removing header will help)
   *
   * Extracted from OptionViewer.svelte (lines 402-457)
   *
   * @param params Layout parameters
   * @returns true if should use floating button, false for full header
   */
  shouldUseFloatingButton(params: {
    containerWidth: number;
    containerHeight: number;
    pictographSize: number;
    columns: number;
    maxPictographsPerSection: number;
  }): boolean;

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
