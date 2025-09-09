/**
 * Arrow Location Calculator Interface
 *
 * Calculates arrow locations based on motion data and pictograph context.
 */

import type { GridLocation, MotionData, MotionType, PictographData } from "$shared";

export interface IArrowLocationCalculator {
  /**
   * Calculate the arrow location based on motion type and data.
   */
  calculateLocation(
    motion: MotionData,
    pictographData?: PictographData
  ): GridLocation;
  
  getSupportedMotionTypes(): MotionType[];
  
  validateMotionData(motion: MotionData): boolean;
  
  isBlueArrowMotion(
    motion: MotionData,
    pictographData: PictographData
  ): boolean;
}
