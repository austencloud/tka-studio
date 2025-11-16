/**
 * Filter Service Implementation
 *
 * Handles filtering of pictograph options by type, end position, and reversals.
 * Extracted from OptionPickerService for better separation of concerns.
 */

import type { PictographData, Letter } from "$shared";
import { getLetterType, GridPositionGroup, LetterType } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type {
  EndPositionFilter,
  ReversalFilter,
  TypeFilter,
} from "../../domain";
import type { IPositionAnalyzer, IReversalChecker } from "../contracts";
import type { IOptionFilter } from "../contracts";

@injectable()
export class OptionFilter implements IOptionFilter {
  constructor(
    @inject(TYPES.IReversalChecker) private ReversalChecker: IReversalChecker,
    @inject(TYPES.IPositionAnalyzer) private positionAnalyzer: IPositionAnalyzer
  ) {}

  /**
   * Apply type filtering to options
   */
  applyTypeFiltering(
    options: PictographData[],
    typeFilter: TypeFilter
  ): PictographData[] {
    return options.filter((option) => {
      const letterType = this.getLetterType(option.letter);

      switch (letterType) {
        case LetterType.TYPE1:
          return typeFilter.type1;
        case LetterType.TYPE2:
          return typeFilter.type2;
        case LetterType.TYPE3:
          return typeFilter.type3;
        case LetterType.TYPE4:
          return typeFilter.type4;
        case LetterType.TYPE5:
          return typeFilter.type5;
        case LetterType.TYPE6:
          return typeFilter.type6;
        default:
          return true; // Include unknown types by default
      }
    });
  }

  /**
   * Apply end position filtering to options
   */
  applyEndPositionFiltering(
    options: PictographData[],
    endPositionFilter: EndPositionFilter
  ): PictographData[] {
    return options.filter((option) => {
      const endPositionGroup = this.positionAnalyzer.getEndPositionGroup(
        option.endPosition
      );

      switch (endPositionGroup) {
        case GridPositionGroup.ALPHA:
          return endPositionFilter.alpha;
        case GridPositionGroup.BETA:
          return endPositionFilter.beta;
        case GridPositionGroup.GAMMA:
          return endPositionFilter.gamma;
        default:
          return true; // Include unknown positions by default
      }
    });
  }

  /**
   * Apply reversal filtering to options
   */
  applyReversalFiltering(
    options: PictographData[],
    reversalFilter: ReversalFilter
  ): PictographData[] {
    return options.filter((option) => {
      const reversalCount = this.ReversalChecker.getReversalCount(option);

      switch (reversalCount) {
        case 0:
          return reversalFilter.continuous;
        case 1:
          return reversalFilter["1-reversal"];
        case 2:
          return reversalFilter["2-reversals"];
        default:
          return true; // Include unknown reversal counts by default
      }
    });
  }

  /**
   * Filter pictographs by letter type
   */
  filterPictographsByType(
    pictographs: PictographData[],
    letterType: string
  ): PictographData[] {
    return pictographs.filter(
      (p: PictographData) =>
        this.getLetterTypeFromString(p.letter) === letterType
    );
  }

  /**
   * Determine letter type from letter string using shared infrastructure
   */
  private getLetterType(letter: string | null | undefined): string {
    if (!letter) return LetterType.TYPE1;

    try {
      // Use the existing shared getLetterType function
      const letterEnum = letter as Letter;
      const letterType = getLetterType(letterEnum);
      return letterType; // Returns LetterType enum value (e.g., "Type1")
    } catch (error) {
      // Fallback for invalid letters
      console.warn(
        `Failed to determine letter type for "${letter}", defaulting to TYPE1:`,
        error
      );
      return LetterType.TYPE1;
    }
  }

  /**
   * Helper function to convert string letter to Letter enum and get type
   * Uses shared infrastructure instead of duplicated logic
   */
  private getLetterTypeFromString(letter: string | null | undefined): string {
    // Delegate to the main getLetterType method which now uses shared infrastructure
    return this.getLetterType(letter);
  }
}
