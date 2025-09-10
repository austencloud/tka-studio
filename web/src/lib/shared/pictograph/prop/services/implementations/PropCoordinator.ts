/**
 * Prop Coordinator Service
 *
 * Orchestrates prop rendering by coordinating placement calculation and SVG loading.
 * Focuses on rendering coordination rather than placement calculation logic.
 * Uses PropPlacementService for placement calculations following separation of concerns.
 */

import type { IPropPlacementService } from "$shared";
import {
  type MotionData,
  type PictographData,
  type PropPlacementData,
  TYPES,
} from "$shared";
import { inject, injectable } from "inversify";
import type { PropRenderData } from "../../domain/models/PropRenderData";
import type { IPropCoordinator } from "../contracts/IPropCoordinator";
import type { IPropSvgLoader } from "../contracts/IPropSvgLoader";

@injectable()
export class PropCoordinator implements IPropCoordinator {
  constructor(
    @inject(TYPES.IPropPlacementService) private placementService: IPropPlacementService,
    @inject(TYPES.IPropSvgLoader) private svgLoader: IPropSvgLoader
  ) {}

  async calculatePropRenderData(
    propPlacementData: PropPlacementData,
    motionData?: MotionData,
    pictographData?: PictographData
  ): Promise<PropRenderData> {
    try {
      // ✅ SIMPLIFIED: Only need pictographData and motionData for placement calculation
      if (!pictographData) {
        throw new Error(
          "PictographData is required for prop placement calculation"
        );
      }

      if (!motionData) {
        throw new Error(
          "MotionData is required for prop placement calculation"
        );
      }

      const placementData = await this.placementService.calculatePlacement(
        pictographData,
        motionData
      );

      // Use fast SVG loader - direct approach like arrows
      return await this.svgLoader.loadPropSvg(placementData, motionData);
    } catch (error) {
      console.error("❌ PropCoordinator.calculatePropRenderData error:", error);
      return {
        position: { x: 475, y: 475 },
        rotation: 0,
        svgData: null,
        loaded: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }
}
