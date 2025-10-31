/**
 * Arrow Rotation Calculator Interface
 *
 * Calculates arrow rotation angles based on motion type and location.
 */

import type {
  GridLocation,
  MotionData,
  MotionType,
  PictographData,
} from "$shared";

export interface IArrowRotationCalculator {
  /**
   * Calculate the arrow rotation angle based on motion type and location.
   */
  calculateRotation(
    motion: MotionData,
    location: GridLocation,
    pictographData?: PictographData
  ): Promise<number>;

  getSupportedMotionTypes(): MotionType[];

  validateMotionData(motion: MotionData): boolean;
}
