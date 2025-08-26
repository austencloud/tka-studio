/**
 * Options Service for OptionPicker using ONLY Svelte 5 Runes
 *
 * Provides functionality for generating, filtering, sorting, and grouping pictograph options.
 * Complete port from legacy system without any stores - pure runes and functions.
 */

import {
  getLetterType,
  GridPosition,
  GridPositionGroup,
  Letter,
  LetterType,
  OptionPickerReversalFilter,
  OptionPickerSortMethod,
} from "$lib/domain";
import type { PictographData } from "$lib/domain/PictographData";
import { resolve } from "$lib/services/bootstrap";
import type { IPositionMapper } from "$lib/services/interfaces/movement/IPositionMapper";

/**
 * Helper function to compute endPosition from motion data
 */
function getEndPosition(option: PictographData): string | null {
  if (option.motions?.blue && option.motions?.red) {
    const positionService = resolve("IPositionMapper") as IPositionMapper;
    const position = positionService.getPositionFromLocations(
      option.motions.blue.endLocation,
      option.motions.red.endLocation
    );
    return position?.toString() || null;
  }
  return null;
}

/**
 * Union type for all possible group key values returned by determineGroupKey
 */
export type OptionPickerGroupKey =
  | LetterType
  | GridPosition
  | GridPositionGroup
  | OptionPickerReversalFilter
  | "Unknown"
  | "all";

/**
 * Determine reversal category for an option
 */
export function determineReversalCategory(
  sequence: PictographData[],
  option: PictographData
): OptionPickerReversalFilter {
  // Simplified reversal detection
  if (!sequence || sequence.length === 0) {
    return OptionPickerReversalFilter.ALL;
  }

  const lastBeat = sequence[sequence.length - 1];
  if (!lastBeat?.motions?.red || !lastBeat?.motions?.blue) {
    return OptionPickerReversalFilter.ALL;
  }

  if (!option?.motions?.red || !option?.motions?.blue) {
    return OptionPickerReversalFilter.ALL;
  }

  // Check if rotation directions continue or reverse
  const redContinuous =
    lastBeat.motions.red.rotationDirection ===
    option.motions.red.rotationDirection;
  const blueContinuous =
    lastBeat.motions.blue.rotationDirection ===
    option.motions.blue.rotationDirection;

  if (redContinuous && blueContinuous) {
    return OptionPickerReversalFilter.CONTINUOUS;
  } else if (redContinuous || blueContinuous) {
    return OptionPickerReversalFilter.ONE_REVERSAL;
  } else {
    return OptionPickerReversalFilter.TWO_REVERSALS;
  }
}

/**
 * Determine group key for an option based on sort method
 */
export function determineGroupKey(
  option: PictographData,
  sortMethod: OptionPickerSortMethod,
  sequence: PictographData[]
): OptionPickerGroupKey {
  switch (sortMethod) {
    case OptionPickerSortMethod.LETTER_TYPE:
      if (!option.letter) {
        throw new Error("Option letter is required for letter type grouping");
      }
      return getLetterType(option.letter);
    case OptionPickerSortMethod.END_POSITION: {
      const endPosition = getEndPosition(option);
      if (typeof endPosition === "string") {
        // Try to match to GridPosition enum, fallback to GridPositionGroup
        const gridPosition = Object.values(GridPosition).find(
          (pos) => pos === endPosition
        );
        if (gridPosition) return gridPosition as GridPosition;

        // Try to match to GridPositionGroup (alpha, beta, gamma)
        const gridGroup = Object.values(GridPositionGroup).find(
          (positionGroup) => endPosition.startsWith(positionGroup)
        );
        if (gridGroup) return gridGroup as GridPositionGroup;
      }

      return "Unknown";
    }
    case OptionPickerSortMethod.REVERSALS:
      return determineReversalCategory(sequence, option);
    default:
      return "all";
  }
}

/**
 * Get sorted group keys based on sort method
 */
export function getSortedGroupKeys(
  keys: OptionPickerGroupKey[],
  sortMethod: OptionPickerSortMethod
): OptionPickerGroupKey[] {
  switch (sortMethod) {
    case OptionPickerSortMethod.LETTER_TYPE:
      return keys.sort((a, b) => {
        const order = [
          LetterType.TYPE1,
          LetterType.TYPE2,
          LetterType.TYPE3,
          LetterType.TYPE4,
          LetterType.TYPE5,
          LetterType.TYPE6,
        ];
        return order.indexOf(a as LetterType) - order.indexOf(b as LetterType);
      });
    case OptionPickerSortMethod.END_POSITION:
      return keys.sort((a, b) => {
        // Sort grid positions logically
        return String(a).localeCompare(String(b));
      });
    case OptionPickerSortMethod.REVERSALS:
      return keys.sort((a, b) => {
        const order = [
          OptionPickerReversalFilter.CONTINUOUS,
          OptionPickerReversalFilter.ONE_REVERSAL,
          OptionPickerReversalFilter.TWO_REVERSALS,
          OptionPickerReversalFilter.ALL,
        ];
        return (
          order.indexOf(a as OptionPickerReversalFilter) -
          order.indexOf(b as OptionPickerReversalFilter)
        );
      });
    default:
      return keys.sort();
  }
}

/**
 * Get sorter function for options based on sort method
 */
export function getSorter(
  sortMethod: OptionPickerSortMethod,
  sequence: PictographData[]
): (a: PictographData, b: PictographData) => number {
  switch (sortMethod) {
    case OptionPickerSortMethod.LETTER_TYPE:
      return (a, b) => {
        const typeA = getLetterType(a.letter || Letter.A); // Default to Type1
        const typeB = getLetterType(b.letter || Letter.A); // Default to Type1
        if (typeA !== typeB) {
          return typeA.localeCompare(typeB);
        }
        // Within same type, sort by letter
        const letterA = a.letter || "";
        const letterB = b.letter || "";
        return letterA.localeCompare(letterB);
      };
    case OptionPickerSortMethod.END_POSITION:
      return (a, b) => {
        const endPosA = String(getEndPosition(a) || "");
        const endPosB = String(getEndPosition(b) || "");
        if (endPosA !== endPosB) {
          return endPosA.localeCompare(endPosB);
        }
        // Within same end position, sort by letter
        const letterA = a.letter || "";
        const letterB = b.letter || "";
        return letterA.localeCompare(letterB);
      };
    case OptionPickerSortMethod.REVERSALS:
      return (a, b) => {
        const reversalA = determineReversalCategory(sequence, a);
        const reversalB = determineReversalCategory(sequence, b);
        if (reversalA !== reversalB) {
          return reversalA.localeCompare(reversalB);
        }
        // Within same reversal category, sort by letter
        const letterA = a.letter || "";
        const letterB = b.letter || "";
        return letterA.localeCompare(letterB);
      };
    default:
      // Default sort by letter
      return (a, b) => {
        const letterA = a.letter || "";
        const letterB = b.letter || "";
        return letterA.localeCompare(letterB);
      };
  }
}

/**
 * Filter options based on reversal filter
 */
export function filterByReversals(
  options: PictographData[],
  sequence: PictographData[],
  filter: OptionPickerReversalFilter
): PictographData[] {
  if (filter === OptionPickerReversalFilter.ALL) {
    return options;
  }

  return options.filter((option) => {
    const category = determineReversalCategory(sequence, option);
    return category === filter;
  });
}

/**
 * Get display name for a group key
 */
export function getGroupDisplayName(
  groupKey: OptionPickerGroupKey,
  sortMethod: OptionPickerSortMethod
): string {
  switch (sortMethod) {
    case OptionPickerSortMethod.LETTER_TYPE:
      switch (groupKey) {
        case LetterType.TYPE1:
          return "Type 1: Dual-Shift";
        case LetterType.TYPE2:
          return "Type 2: Shift";
        case LetterType.TYPE3:
          return "Type 3: Cross-Shift";
        case LetterType.TYPE4:
          return "Type 4: Dash";
        case LetterType.TYPE5:
          return "Type 5: Dual-Dash";
        case LetterType.TYPE6:
          return "Type 6: Static";
        default:
          return String(groupKey);
      }
    case OptionPickerSortMethod.END_POSITION:
      return `End Position: ${groupKey}`;
    case OptionPickerSortMethod.REVERSALS:
      switch (groupKey) {
        case OptionPickerReversalFilter.CONTINUOUS:
          return "Continuous";
        case OptionPickerReversalFilter.ONE_REVERSAL:
          return "One Reversal";
        case OptionPickerReversalFilter.TWO_REVERSALS:
          return "Two Reversals";
        default:
          return String(groupKey);
      }
    default:
      return String(groupKey);
  }
}

/**
 * Get summary statistics for options
 */
export function getOptionsSummary(options: PictographData[]): {
  total: number;
  byType: Record<string, number>;
  byEndPosition: Record<string, number>;
} {
  const summary = {
    total: options.length,
    byType: {} as Record<string, number>,
    byEndPosition: {} as Record<string, number>,
  };

  options.forEach((option) => {
    // Count by type
    const type = getLetterType(option.letter || Letter.A);
    summary.byType[type] = (summary.byType[type] || 0) + 1;

    // Count by end position
    const endPos = String(getEndPosition(option) || "Unknown");
    summary.byEndPosition[endPos] = (summary.byEndPosition[endPos] || 0) + 1;
  });

  return summary;
}
