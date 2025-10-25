/**
 * Pictograph Filter Service
 *
 * Handles all filtering logic for pictograph selection during sequence generation.
 * Single Responsibility: Filter pictographs by various criteria (rotation, continuity, letter types).
 */

import { injectable } from "inversify";
import type { PictographData, BeatData } from "$shared";
import { RotationDirection } from "$shared/pictograph/shared/domain/enums/pictograph-enums";

// Legacy constants for rotation directions
const ROTATION_DIRS = {
  CLOCKWISE: RotationDirection.CLOCKWISE,
  COUNTER_CLOCKWISE: RotationDirection.COUNTER_CLOCKWISE,
  noRotation: RotationDirection.NO_ROTATION,
} as const;

export interface IPictographFilterService {
  /**
   * Filter pictographs by continuity - next beat's start position must match last beat's end position
   */
  filterByContinuity(options: PictographData[], lastBeat: BeatData | null): PictographData[];

  /**
   * Filter pictographs by rotation direction for continuous prop continuity
   */
  filterByRotation(
    options: PictographData[],
    blueRotationDirection: string,
    redRotationDirection: string
  ): PictographData[];

  /**
   * Filter pictographs by letter types (Type1, Type2, Type3)
   * TODO: Implement when letter type logic is ready
   */
  filterByLetterTypes(options: PictographData[], letterTypes: string[]): PictographData[];

  /**
   * Filter for start positions (where startPosition === endPosition)
   */
  filterStartPositions(options: PictographData[]): PictographData[];

  /**
   * Select random item from array
   */
  selectRandom<T>(array: T[]): T;
}

@injectable()
export class PictographFilterService implements IPictographFilterService {
  /**
   * Filter by continuity - next beat's start position must match last beat's end position
   */
  filterByContinuity(options: PictographData[], lastBeat: BeatData | null): PictographData[] {
    if (!lastBeat) {
      return options; // No filtering needed for first beat
    }

    const lastEndPosition = lastBeat.endPosition?.toLowerCase();

    const filtered = options.filter((option: PictographData) => {
      const optionStartPosition = option.startPosition?.toLowerCase();
      return optionStartPosition === lastEndPosition;
    });

    console.log(`🔗 Filtered for continuity: ${filtered.length} options match end position "${lastEndPosition}"`);

    // If filtering eliminates all options, return original options (legacy behavior)
    if (filtered.length === 0) {
      console.warn(`⚠️ No options match end position "${lastEndPosition}", using all options`);
      return options;
    }

    return filtered;
  }

  /**
   * Filter options by rotation direction - exact port from legacy filter_options_by_rotation()
   * Filters pictographs to match the given rotation directions for continuous prop continuity.
   * Options must have rotation directions that match OR are NO_ROTATION.
   */
  filterByRotation(
    options: PictographData[],
    blueRotDir: string,
    redRotDir: string
  ): PictographData[] {
    const filtered = options.filter((option: PictographData) => {
      const blueMotionRotDir = option.motions.blue?.rotationDirection;
      const redMotionRotDir = option.motions.red?.rotationDirection;

      // Check if blue rotation matches (either matches target or is NO_ROTATION)
      const blueMatches =
        blueMotionRotDir === blueRotDir ||
        blueMotionRotDir === ROTATION_DIRS.noRotation;

      // Check if red rotation matches (either matches target or is NO_ROTATION)
      const redMatches =
        redMotionRotDir === redRotDir ||
        redMotionRotDir === ROTATION_DIRS.noRotation;

      return blueMatches && redMatches;
    });

    // If filtering eliminates all options, return original options (legacy behavior)
    return filtered.length > 0 ? filtered : options;
  }

  /**
   * Filter by letter types - placeholder for future implementation
   */
  filterByLetterTypes(options: PictographData[], _letterTypes: string[]): PictographData[] {
    // TODO: Implement letter type filtering when logic is ready
    console.log(`🔍 Letter type filtering not yet implemented`);
    return options;
  }

  /**
   * Filter for start positions - static pictographs where startPosition === endPosition
   */
  filterStartPositions(options: PictographData[]): PictographData[] {
    const filtered = options.filter((option: PictographData) => {
      const startPos = option.startPosition?.toLowerCase();
      const endPos = option.endPosition?.toLowerCase();
      return startPos === endPos;
    });

    if (filtered.length === 0) {
      throw new Error("No valid start positions found in options");
    }

    console.log(`📍 Found ${filtered.length} valid start positions`);
    return filtered;
  }

  /**
   * Select random item from array - simple utility for random selection
   */
  selectRandom<T>(array: T[]): T {
    if (array.length === 0) {
      throw new Error("Cannot choose from empty array");
    }
    return array[Math.floor(Math.random() * array.length)];
  }
}
