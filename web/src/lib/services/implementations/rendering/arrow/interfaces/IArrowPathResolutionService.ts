/**
 * Arrow Path Resolution Service Interface
 *
 * Responsible for determining the correct SVG file path based on motion data.
 */

import type { MotionData } from "$lib/domain";
import type { ArrowPlacementData } from "$lib/domain/ArrowPlacementData";

export interface IArrowPathResolutionService {
  /**
   * Get arrow SVG path based on motion type and properties
   */
  getArrowPath(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): string | null;

  /**
   * Get the correct arrow SVG path based on motion data (optimized version)
   */
  getArrowSvgPath(motionData: MotionData | undefined): string;
}
