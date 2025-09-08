/**
 * Beta Offset Calculator Interface
 *
 * Provides methods for calculating pixel offsets for beta prop positioning.
 */

import type { Point } from "fabric";
import type { VectorDirection } from "../implementations/BetaPropDirectionCalculator";

export interface IBetaOffsetCalculator {
  /**
   * Calculate new position with offset based on direction
   */
  calculateNewPointWithOffset(
    currentPoint: Point,
    direction: VectorDirection
  ): Point;

  /**
   * Calculate beta separation offsets for both props
   * Returns offsets for blue and red props based on their calculated directions
   */
  calculateBetaSeparationOffsets(
    blueDirection: VectorDirection | null,
    redDirection: VectorDirection | null
  ): { blue: Point; red: Point };
}
