/**
 * Special Placement Service Contract
 */

import type { MotionData, PictographData } from "$shared";
import type { Point } from "fabric";

export interface ISpecialPlacementService {
  getSpecialAdjustment(
    motionData: MotionData,
    pictographData: PictographData,
    arrowColor?: string,
    attributeKey?: string
  ): Promise<Point | null>;

  hasRotationAngleOverride(
    motionData: MotionData,
    pictographData: PictographData,
    rotationOverrideKey: string
  ): Promise<boolean>;
}
