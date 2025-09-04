/**
 * Option Picker Data Service Implementation
 *
 * Handles data management, service integration, and business logic
 * for the option picker component.
 */

import type { IGridPositionDeriver, IMotionQueryHandler, IOptionPickerDataService } from "$services";
import type { PictographData } from "$shared/domain";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";

@injectable()
export class OptionPickerDataService implements IOptionPickerDataService {
  constructor(
    @inject(TYPES.IPositionMapper) private positionMapper: IGridPositionDeriver,
    @inject(TYPES.IMotionQueryHandler)
    private MotionQueryHandler: IMotionQueryHandler
  ) {}

  /**
   * Load available options based on current sequence
   */
  async loadOptionsFromSequence(
    sequence: PictographData[]
  ): Promise<PictographData[]> {
    if (!sequence || sequence.length === 0) {
      return [];
    }

    const lastBeat = sequence[sequence.length - 1];
    const endPosition = this.getEndPosition(lastBeat);

    if (!endPosition || typeof endPosition !== "string") {
      return [];
    }

    try {
      // Get next options from motion query service
      const nextOptions =
        await this.MotionQueryHandler.getNextOptionsForSequence(sequence);

      return nextOptions || [];
    } catch (error) {
      console.error("Failed to load options from sequence:", error);
      return [];
    }
  }

  /**
   * Select an option and handle any side effects
   */
  async selectOption(option: PictographData): Promise<void> {
    // This could include validation, state updates, analytics, etc.
    // For now, it's a simple pass-through
    console.log("Option selected:", option);

    // Future enhancements could include:
    // - Validation of the selected option
    // - Analytics tracking
    // - State persistence
    // - Side effects like clearing filters
  }

  /**
   * Get filtered and sorted options based on current criteria
   */
  getFilteredOptions(
    options: PictographData[],
    sortMethod: string,
    reversalFilter: string
  ): PictographData[] {
    let filteredOptions = [...options];

    // Apply reversal filter
    if (reversalFilter && reversalFilter !== "all") {
      filteredOptions = this.applyReversalFilter(
        filteredOptions,
        reversalFilter
      );
    }

    // Apply sorting
    if (sortMethod && sortMethod !== "none") {
      filteredOptions = this.applySorting(filteredOptions, sortMethod);
    }

    return filteredOptions;
  }

  /**
   * Calculate end position from motion data
   */
  getEndPosition(pictographData: PictographData): string | null {
    if (pictographData.motions?.blue && pictographData.motions?.red) {
      const position = this.positionMapper.getPositionFromLocations(
        pictographData.motions.blue.endLocation,
        pictographData.motions.red.endLocation
      );
      return position?.toString() || null;
    }
    return null;
  }

  // ============================================================================
  // PRIVATE HELPER METHODS
  // ============================================================================

  /**
   * Apply reversal filter to options
   */
  private applyReversalFilter(
    options: PictographData[],
    filter: string
  ): PictographData[] {
    // Implementation depends on your reversal filter logic
    // This is a placeholder implementation
    switch (filter) {
      case "reversals":
        return options.filter((option) => this.isReversal(option));
      case "no-reversals":
        return options.filter((option) => !this.isReversal(option));
      default:
        return options;
    }
  }

  /**
   * Apply sorting to options
   */
  private applySorting(
    options: PictographData[],
    sortMethod: string
  ): PictographData[] {
    const sorted = [...options];

    switch (sortMethod) {
      case "alphabetical":
        return sorted.sort((a, b) => {
          const aName = this.getPictographDisplayName(a);
          const bName = this.getPictographDisplayName(b);
          return aName.localeCompare(bName);
        });

      case "complexity":
        return sorted.sort((a, b) => {
          const aComplexity = this.calculateComplexity(a);
          const bComplexity = this.calculateComplexity(b);
          return aComplexity - bComplexity;
        });

      case "frequency":
        return sorted.sort((a, b) => {
          const aFreq = this.getUsageFrequency(a);
          const bFreq = this.getUsageFrequency(b);
          return bFreq - aFreq; // Higher frequency first
        });

      default:
        return sorted;
    }
  }

  /**
   * Check if a pictograph is a reversal
   */
  private isReversal(option: PictographData): boolean {
    // Placeholder implementation - replace with actual reversal detection logic
    return option.letter?.toLowerCase().includes("rev") || false;
  }

  /**
   * Get display name for pictograph
   */
  private getPictographDisplayName(option: PictographData): string {
    return option.letter?.toString() || "Unknown";
  }

  /**
   * Calculate complexity score for pictograph
   */
  private calculateComplexity(option: PictographData): number {
    // Placeholder implementation - replace with actual complexity calculation
    let complexity = 0;

    // Base complexity from motion count
    if (option.motions) {
      complexity += Object.keys(option.motions).length;
    }

    // Future: Add complexity for arrows, props when they exist in the domain model

    return complexity;
  }

  /**
   * Get usage frequency for pictograph
   */
  private getUsageFrequency(_option: PictographData): number {
    // Placeholder implementation - replace with actual frequency data
    // Could be based on historical usage, user preferences, etc.
    return Math.random(); // Random for now
  }
}
