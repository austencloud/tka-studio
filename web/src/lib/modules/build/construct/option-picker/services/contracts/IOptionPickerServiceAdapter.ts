/**
 * Option Picker Service Adapter Interface
 *
 * Provides a clean, component-friendly interface to option picker services.
 * Acts as a facade that combines layout and data services.
 */

import type { PictographData } from "$shared";
import type { OptionPickerLayoutCalculationParams, OptionPickerLayoutCalculationResult } from "../../domain/models";
import type { IOptionPickerDataService } from "./IOptionPickerDataService";
import type { IOptionPickerLayoutService } from "./IOptionPickerLayoutService";

export interface OptionPickerServices {
  layout: IOptionPickerLayoutService;
  data: IOptionPickerDataService;
}

export interface IOptionPickerServiceAdapter {
  // ============================================================================
  // ERROR HANDLING
  // ============================================================================

  /**
   * Get the last error that occurred
   */
  getLastError(): string | null;

  /**
   * Clear any stored errors
   */
  clearErrors(): void;

  /**
   * Retry the last failed operation
   */
  retryLastOperation(): Promise<void>;

  // ============================================================================
  // LAYOUT OPERATIONS
  // ============================================================================

  /**
   * Calculate complete layout for option picker
   */
  calculateLayout(
    params: OptionPickerLayoutCalculationParams
  ): OptionPickerLayoutCalculationResult;

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
  };

  /**
   * Calculate optimal option size
   */
  calculateOptimalOptionSize(
    count: number,
    containerWidth: number,
    containerHeight: number,
    targetColumns?: number
  ): number;

  /**
   * Check if mobile layout should be used
   */
  shouldUseMobileLayout(
    containerWidth: number,
    isMobileUserAgent?: boolean
  ): boolean;

  /**
   * Clear layout cache
   */
  clearLayoutCache(): void;

  // ============================================================================
  // DATA OPERATIONS
  // ============================================================================

  /**
   * Load options based on sequence
   */
  loadOptionsFromSequence(
    sequence: PictographData[]
  ): Promise<PictographData[]>;

  /**
   * Select an option
   */
  selectOption(option: PictographData): Promise<void>;

  /**
   * Get current options
   */
  getCurrentOptions(): PictographData[];

  /**
   * Clear current options
   */
  clearOptions(): void;

  /**
   * Check if options are loaded
   */
  hasOptions(): boolean;

  /**
   * Get loading state
   */
  isLoading(): boolean;

  /**
   * Get error state
   */
  getError(): string | null;

  /**
   * Get filtered and sorted options
   */
  getFilteredOptions(
    options: PictographData[],
    sortMethod: string,
    reversalFilter: string
  ): PictographData[];

  // ============================================================================
  // COMBINED OPERATIONS
  // ============================================================================

  /**
   * Complete option picker initialization
   * Combines data loading and layout calculation
   */
  initializeOptionPicker(
    sequence: PictographData[],
    containerWidth: number,
    containerHeight: number
  ): Promise<{
    options: PictographData[];
    layout: OptionPickerLayoutCalculationResult;
  }>;

  // ============================================================================
  // DIRECT SERVICE ACCESS (for advanced use cases)
  // ============================================================================

  /**
   * Get direct access to services for advanced operations
   */
  getServices(): OptionPickerServices;
}
