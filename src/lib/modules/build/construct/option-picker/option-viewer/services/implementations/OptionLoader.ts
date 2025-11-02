/**
 * Option Loader Service Implementation
 *
 * Handles loading of available pictograph options based on sequence context.
 * Extracted from OptionPickerService for better separation of concerns.
 */

import type { GridMode, IMotionQueryHandler, PictographData } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IOptionLoader, IPositionAnalyzer } from "../contracts";

@injectable()
export class OptionLoader implements IOptionLoader {

  constructor(
    @inject(TYPES.IGridPositionDeriver) private positionMapper: any,
    @inject(TYPES.IMotionQueryHandler) private motionQueryHandler: IMotionQueryHandler,
    @inject(TYPES.IPositionAnalyzer) private positionAnalyzer: IPositionAnalyzer
  ) {}

  /**
   * Load available options based on current sequence and grid mode
   * PRESERVED: Core working logic from OptionPickerDataService
   */
  async loadOptions(sequence: PictographData[], gridMode: GridMode): Promise<PictographData[]> {
    if (!sequence || sequence.length === 0) {
      return [];
    }

    const lastBeat = sequence[sequence.length - 1]!;
    const endPosition = this.positionAnalyzer.getEndPosition(lastBeat);

    if (!endPosition || typeof endPosition !== "string") {
      return [];
    }

    try {
      // Get all available options from motion query service
      const allOptions = await this.motionQueryHandler.getNextOptionsForSequence(sequence, gridMode);

      // Filter options based on sequence context
      // The next beat's start position should match the current beat's end position
      const filteredOptions = allOptions.filter((option) => {
        if (!option.motions?.blue || !option.motions?.red) {
          return false;
        }

        // Calculate the start position of this option
        const optionStartPosition = this.positionMapper.getGridPositionFromLocations(
          option.motions.blue.startLocation,
          option.motions.red.startLocation
        );

        const optionStartPositionStr = optionStartPosition?.toString().toLowerCase();
        const targetEndPosition = endPosition.toLowerCase();

        return optionStartPositionStr === targetEndPosition;
      });

      return filteredOptions;
    } catch (error) {
      console.error("Failed to load options from sequence:", error);
      return [];
    }
  }
}
