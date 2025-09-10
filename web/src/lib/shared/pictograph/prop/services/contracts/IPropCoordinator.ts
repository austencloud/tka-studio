/**
 * Prop Coordinator Service Interface
 *
 * Handles coordination of prop rendering data calculation including
 * position, rotation, and SVG loading.
 */

import type { MotionData, PictographData, PropPlacementData } from "$shared";
import type { PropRenderData } from "../../domain/models/PropRenderData";

export interface IPropCoordinator {
  calculatePropRenderData(
    PropPlacementData: PropPlacementData,
    motionData?: MotionData,
    pictographData?: PictographData // ✅ SIMPLIFIED: Complete pictograph data contains gridMode
  ): Promise<PropRenderData>;
}
