/**
 * Special Placement Orientation Key Generator Contract
 */

import type { MotionData, PictographData } from "$shared";

export interface ISpecialPlacementOriKeyGenerator {
  generateOrientationKey(
    motionData: MotionData,
    pictographData: PictographData
  ): string;
}
