/**
 * Rotated End Position Selector
 *
 * Determines the required end position for rotated CAPs based on:
 * - The start position
 * - The slice size (halved or quartered)
 *
 * For halved CAPs: Returns the opposite position (180° rotation)
 * For quartered CAPs: Randomly chooses between clockwise or counter-clockwise 90° rotation
 */

import { injectable } from "inversify";
import type { GridPosition } from "$shared/pictograph/grid/domain/enums/grid-enums";
import {
  HALF_POSITION_MAP,
  QUARTER_POSITION_MAP_CCW,
  QUARTER_POSITION_MAP_CW,
} from "../../domain/constants/circular-position-maps";
import { SliceSize } from "../../domain/models/circular-models";

@injectable()
export class RotatedEndPositionSelector {
  /**
   * Determine the required end position for a rotated CAP
   *
   * @param sliceSize - Whether the rotation is halved (180°) or quartered (90°)
   * @param startPosition - The starting position of the sequence
   * @returns The required end position to complete the rotation
   */
  determineRotatedEndPosition(sliceSize: SliceSize, startPosition: GridPosition): GridPosition {
    if (sliceSize === SliceSize.QUARTERED) {
      // For quartered CAPs, randomly choose between clockwise and counter-clockwise
      const cwEndPosition = QUARTER_POSITION_MAP_CW[startPosition];
      const ccwEndPosition = QUARTER_POSITION_MAP_CCW[startPosition];

      // Randomly select one
      return Math.random() < 0.5 ? cwEndPosition : ccwEndPosition;
    } else if (sliceSize === SliceSize.HALVED) {
      // For halved CAPs, use the opposite position (180° rotation)
      return HALF_POSITION_MAP[startPosition];
    }

    throw new Error(`Invalid slice size: ${sliceSize}`);
  }

  /**
   * Check if a given (start, end) position pair is valid for the slice size
   *
   * @param sliceSize - The slice size to validate against
   * @param startPosition - The start position
   * @param endPosition - The end position
   * @returns Whether the position pair is valid for the given slice size
   */
  isValidRotatedPair(
    sliceSize: SliceSize,
    startPosition: GridPosition,
    endPosition: GridPosition
  ): boolean {
    if (sliceSize === SliceSize.HALVED) {
      return HALF_POSITION_MAP[startPosition] === endPosition;
    } else if (sliceSize === SliceSize.QUARTERED) {
      const cwEndPosition = QUARTER_POSITION_MAP_CW[startPosition];
      const ccwEndPosition = QUARTER_POSITION_MAP_CCW[startPosition];
      return endPosition === cwEndPosition || endPosition === ccwEndPosition;
    }

    return false;
  }
}
