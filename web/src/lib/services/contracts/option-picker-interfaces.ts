/**
 * Option Picker Service Interfaces
 *
 * Interfaces for option picker layout calculations, device detection,
 * and responsive grid configuration specific to the option picker component.
 */
// ============================================================================
// LAYOUT CALCULATION INTERFACES
// ============================================================================
import type {
  OptionPickerLayoutCalculationParams,
  OptionPickerLayoutCalculationResult,
  PictographData,
} from "$domain";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

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
