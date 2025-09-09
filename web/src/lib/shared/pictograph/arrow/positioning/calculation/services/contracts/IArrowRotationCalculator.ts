/**
 * Arrow Rotation Calculator Interface
 *
 * Calculates arrow rotation angles based on motion type and location.
 */

import type { GridLocation, MotionData, MotionType } from "$shared";

export interface IArrowRotationCalculator {
  /**
   * Calculate the arrow rotation angle based on motion type and location.
   */
  calculateRotation(motion: MotionData, location: GridLocation): number;
  
  getSupportedMotionTypes(): MotionType[];
  
  validateMotionData(motion: MotionData): boolean;
}
