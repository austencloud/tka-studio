/**
 * Option Picker Service Adapter
 *
 * Provides a clean, component-friendly interface to option picker services.
 * Acts as a facade that combines layout and data services.
 */


import type { PictographData } from "$shared";
import { TYPES } from "$shared";
import { inject, injectable } from "inversify";
import type { OptionPickerLayoutCalculationParams, OptionPickerLayoutCalculationResult } from "../../domain/models";
import type { IOptionPickerDataService, IOptionPickerLayoutService, IOptionPickerServiceAdapter, OptionPickerServices } from "../contracts";

@injectable()
export class OptionPickerServiceAdapter implements IOptionPickerServiceAdapter {
  private lastError: string | null = null;
  private lastOperation: { type: string; params: unknown } | null = null;

  constructor(
    @inject(TYPES.IOptionPickerLayoutService)
    private layoutService: IOptionPickerLayoutService,
    @inject(TYPES.IOptionPickerDataService)
    private dataService: IOptionPickerDataService
  ) {}

  // ============================================================================
  // ERROR HANDLING METHODS
  // ============================================================================

  getLastError(): string | null {
    return this.lastError;
  }

  clearErrors(): void {
    this.lastError = null;
    this.lastOperation = null;
  }

  async retryLastOperation(): Promise<void> {
    if (!this.lastOperation) {
      throw new Error("No operation to retry");
    }

    // Retry logic would depend on the operation type
    console.log("Retrying operation:", this.lastOperation.type);
    // Implementation would call the appropriate method based on lastOperation.type
  }

  getCurrentOptions(): PictographData[] {
    // These methods are state-related and should be handled by the state layer
    // The adapter focuses on coordinating services, not managing state
    return [];
  }

  clearOptions(): void {
    // State management is handled by the state layer
    console.log("Clear options called - handled by state layer");
  }

  hasOptions(): boolean {
    // State management is handled by the state layer
    return false;
  }

  isLoading(): boolean {
    // State management is handled by the state layer
    return false;
  }

  getError(): string | null {
    // State management is handled by the state layer
    return null;
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
