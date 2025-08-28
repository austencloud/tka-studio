/**
 * Option Picker Service Interfaces
 *
 * Interfaces for option picker layout calculations, device detection,
 * and responsive grid configuration specific to the option picker component.
 */

import type { DeviceType, ContainerAspect } from "$lib/domain/layout/types";
import type { PictographData } from "$lib/domain/PictographData";

// ============================================================================
// LAYOUT CALCULATION INTERFACES
// ============================================================================

export interface OptionPickerLayoutDimensions {
  width: number;
  height: number;
}

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
  isMobile: boolean;
  isTablet: boolean;
  isPortrait: boolean;
}

// ============================================================================
// SERVICE INTERFACES
// ============================================================================

/**
 * Service for calculating responsive layouts specifically for option picker grids
 */
export interface IOptionPickerLayoutService {
  /**
   * Calculate optimal layout configuration for option picker grid
   */
  calculateLayout(
    params: OptionPickerLayoutCalculationParams
  ): OptionPickerLayoutCalculationResult;

  /**
   * Get simple layout metrics (optionsPerRow and optionSize only)
   */
  getSimpleLayout(
    count: number,
    containerWidth: number,
    containerHeight: number
  ): {
    optionsPerRow: number;
    optionSize: number;
  };

  /**
   * Calculate optimal option size for given parameters
   */
  calculateOptimalOptionSize(
    count: number,
    containerWidth: number,
    containerHeight: number,
    targetColumns?: number
  ): number;

  /**
   * Get grid gap for given parameters
   */
  calculateGridGap(
    count: number,
    containerWidth: number,
    containerHeight: number
  ): string;

  /**
   * Determine if mobile layout should be used
   */
  shouldUseMobileLayout(
    containerWidth: number,
    isMobileUserAgent?: boolean
  ): boolean;

  /**
   * Clear any internal caches
   */
  clearCache(): void;
}

/**
 * Service for managing option picker data and business logic
 */
export interface IOptionPickerDataService {
  /**
   * Load available options based on current sequence
   */
  loadOptionsFromSequence(
    sequence: PictographData[]
  ): Promise<PictographData[]>;

  /**
   * Select an option and handle any side effects
   */
  selectOption(option: PictographData): Promise<void>;

  /**
   * Get filtered and sorted options based on current criteria
   */
  getFilteredOptions(
    options: PictographData[],
    sortMethod: string,
    reversalFilter: string
  ): PictographData[];

  /**
   * Calculate end position from motion data
   */
  getEndPosition(pictographData: PictographData): string | null;
}
