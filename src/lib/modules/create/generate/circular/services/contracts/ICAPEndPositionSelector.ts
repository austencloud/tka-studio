import type { GridPosition } from "$shared";
import type { CAPType, SliceSize } from "../../domain/models/circular-models";

/**
 * Service for determining required end positions for CAP sequences
 *
 * Each CAP type has specific requirements for where a partial sequence must end
 * in order to successfully complete the circular pattern.
 */
export interface ICAPEndPositionSelector {
  /**
   * Determine the required end position for a CAP sequence
   *
   * @param capType - The type of CAP being executed
   * @param startPosition - The starting grid position
   * @param sliceSize - The slice size (only used for rotated CAP)
   * @returns The grid position where the partial sequence must end
   */
  determineEndPosition(
    capType: CAPType,
    startPosition: GridPosition,
    sliceSize: SliceSize
  ): GridPosition;
}
