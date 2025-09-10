/**
 * Prop Placement Service
 *
 * Dedicated service for calculating prop placement data.
 * Follows separation of concerns by focusing only on placement calculations.
 * Returns PropPlacementData that can be attached to PropPlacementData.
 */

import type { IBetaDetectionService, IGridModeDeriver, IPropPlacementService } from "$shared";
import {
  type MotionData,
  type PictographData,
  type PropPlacementData,
  createPropPlacementFromPosition,
  GridMode,
  PropRotAngleManager,
  TYPES,
} from "$shared";
import { Point } from "fabric";
import { inject, injectable } from "inversify";
import { BetaOffsetCalculator } from "./BetaOffsetCalculator";
import { BetaPropDirectionCalculator } from "./BetaPropDirectionCalculator";
import DefaultPropPositioner from "./DefaultPropPositioner";

@injectable()
export class PropPlacementService implements IPropPlacementService {
  constructor(
    @inject(TYPES.IGridModeDeriver) private gridModeService: IGridModeDeriver,
    @inject(TYPES.IBetaDetectionService) private betaDetectionService: IBetaDetectionService
  ) {}



  async calculatePlacement(
    pictographData: PictographData,
    motionData: MotionData
  ): Promise<PropPlacementData> {
    // Compute gridMode from motion data - now synchronous!
    const gridMode =
      pictographData.motions?.blue && pictographData.motions?.red
        ? this.gridModeService.deriveGridMode(
            pictographData.motions.blue,
            pictographData.motions.red
          )
        : GridMode.DIAMOND;
    const position = await this.calculatePosition(
      pictographData,
      motionData,
      gridMode
    );

    const rotation = PropRotAngleManager.calculateRotation(
      motionData.endLocation,
      motionData.endOrientation,
      gridMode
    );

    return createPropPlacementFromPosition(position.x, position.y, rotation);
  }

  private async calculatePosition(
    pictographData: PictographData,
    motionData: MotionData,
    gridMode: GridMode
  ): Promise<{ x: number; y: number }> {
    // Calculate base position from motion data (not from existing propPlacementData)
    const basePosition = DefaultPropPositioner.calculatePosition(
      motionData.endLocation,
      gridMode
    );

    // Apply beta offset if this is a beta position
    const betaOffset = await this.calculateBetaOffset(
      pictographData,
      motionData
    );

    return {
      x: basePosition.x + betaOffset.x,
      y: basePosition.y + betaOffset.y,
    };
  }

  private async calculateBetaOffset(
    pictographData: PictographData,
    motionData: MotionData
  ): Promise<{ x: number; y: number }> {
    // Check if this pictograph ends with beta position - now synchronous!
    const needsBetaOffset = this.betaDetectionService.endsWithBeta(pictographData);

    if (!needsBetaOffset) {
      return { x: 0, y: 0 };
    }

    const redMotion = pictographData.motions?.red;
    const blueMotion = pictographData.motions?.blue;

    if (!redMotion || !blueMotion) {
      return { x: 0, y: 0 };
    }

    // Only apply beta offset if both props end at the same location
    if (redMotion.endLocation !== blueMotion.endLocation) {
      return { x: 0, y: 0 };
    }

    // Calculate direction for this specific prop
    const directionCalculator = new BetaPropDirectionCalculator({
      red: redMotion,
      blue: blueMotion,
    });

    const direction = directionCalculator.getDirectionForMotionData(motionData);

    if (!direction) {
      console.warn(
        `⚠️ Could not calculate beta direction for ${motionData.color} prop, skipping beta offset`
      );
      return { x: 0, y: 0 };
    }

    // Calculate the offset based on the direction
    const offsetCalculator = new BetaOffsetCalculator();
    const basePosition = new Point(0, 0);
    const newPosition = offsetCalculator.calculateNewPointWithOffset(
      basePosition,
      direction
    );

    // Beta offset calculated silently for performance

    return { x: newPosition.x, y: newPosition.y };
  }
}
