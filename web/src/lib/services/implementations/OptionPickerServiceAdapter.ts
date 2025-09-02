/**
 * Option Picker Service Adapter
 *
 * Provides a clean, component-friendly interface to option picker services.
 * Acts as a facade that combines layout and data services.
 */

import type {
  IOptionPickerDataService,
  IOptionPickerLayoutService,
} from "$contracts";
import type {
  OptionPickerLayoutCalculationParams,
  OptionPickerLayoutCalculationResult,
  PictographData,
} from "$domain";
import { resolve, TYPES } from "$lib/services/inversify/container";

export interface OptionPickerServices {
  layout: IOptionPickerLayoutService;
  data: IOptionPickerDataService;
}

export class OptionPickerServiceAdapter {
  private layoutService: IOptionPickerLayoutService;
  private dataService: IOptionPickerDataService;

  constructor() {
    this.layoutService = resolve(
      TYPES.IOptionPickerLayoutService
    ) as IOptionPickerLayoutService;
    this.dataService = resolve(
      TYPES.IOptionPickerDataService
    ) as IOptionPickerDataService;
  }

  // ============================================================================
  // LAYOUT OPERATIONS
  // ============================================================================

  /**
   * Calculate complete layout for option picker
   */
  calculateLayout(
    params: OptionPickerLayoutCalculationParams
  ): OptionPickerLayoutCalculationResult {
    return this.layoutService.calculateLayout(params);
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
    return this.layoutService.getSimpleLayout(
      count,
      containerWidth,
      containerHeight
    );
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
    return this.layoutService.calculateOptimalOptionSize(
      count,
      containerWidth,
      containerHeight,
      targetColumns
    );
  }

  /**
   * Check if mobile layout should be used
   */
  shouldUseMobileLayout(
    containerWidth: number,
    isMobileUserAgent?: boolean
  ): boolean {
    return this.layoutService.shouldUseMobileLayout(
      containerWidth,
      isMobileUserAgent
    );
  }

  /**
   * Clear layout cache
   */
  clearLayoutCache(): void {
    this.layoutService.clearCache();
  }

  // ============================================================================
  // DATA OPERATIONS
  // ============================================================================

  /**
   * Load options based on sequence
   */
  async loadOptionsFromSequence(
    sequence: PictographData[]
  ): Promise<PictographData[]> {
    return this.dataService.loadOptionsFromSequence(sequence);
  }

  /**
   * Select an option
   */
  async selectOption(option: PictographData): Promise<void> {
    return this.dataService.selectOption(option);
  }

  /**
   * Get filtered and sorted options
   */
  getFilteredOptions(
    options: PictographData[],
    sortMethod: string,
    reversalFilter: string
  ): PictographData[] {
    return this.dataService.getFilteredOptions(
      options,
      sortMethod,
      reversalFilter
    );
  }

  /**
   * Get end position from pictograph data
   */
  getEndPosition(pictographData: PictographData): string | null {
    return this.dataService.getEndPosition(pictographData);
  }

  // ============================================================================
  // COMBINED OPERATIONS
  // ============================================================================

  /**
   * Complete option picker initialization
   * Combines data loading and layout calculation
   */
  async initializeOptionPicker(
    sequence: PictographData[],
    containerWidth: number,
    containerHeight: number
  ): Promise<{
    options: PictographData[];
    layout: OptionPickerLayoutCalculationResult;
  }> {
    // Load options
    const options = await this.loadOptionsFromSequence(sequence);

    // Calculate layout
    const layout = this.calculateLayout({
      count: options.length,
      containerWidth,
      containerHeight,
    });

    return { options, layout };
  }

  // ============================================================================
  // DIRECT SERVICE ACCESS (for advanced use cases)
  // ============================================================================

  /**
   * Get direct access to services for advanced operations
   */
  getServices(): OptionPickerServices {
    return {
      layout: this.layoutService,
      data: this.dataService,
    };
  }
}
