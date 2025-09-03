/**
 * Prop Placement Service
 *
 * Dedicated service for calculating prop placement data.
 * Follows separation of concerns by focusing only on placement calculations.
 * Returns PropPlacementData that can be attached to PropPlacementData.
 */

import type { MotionData, PictographData, PropPlacementData } from "$domain";
import { createPropPlacementFromPosition, GridMode } from "$domain";

import type { IBetaDetectionService, IGridModeDeriver } from "$contracts";
import { DefaultPropPositioner, PropRotAngleManager } from "$implementations";
import { injectable } from "inversify";
import { BetaOffsetCalculator } from "./BetaOffsetCalculator";
import { BetaPropDirectionCalculator } from "./BetaPropDirectionCalculator";

export interface IPropPlacementService {
  calculatePlacement(
    pictographData: PictographData,
    motionData: MotionData
  ): Promise<PropPlacementData>;
}

@injectable()
export class PropPlacementService implements IPropPlacementService {
  private gridModeService: IGridModeDeriver | null = null;
  private betaDetectionService: IBetaDetectionService | null = null;

  private async getGridModeService(): Promise<IGridModeDeriver> {
    if (!this.gridModeService) {
      const { resolve, TYPES } = await import(
        "$lib/services/inversify/container"
      );
      this.gridModeService = resolve<IGridModeDeriver>(TYPES.IGridModeDeriver);
    }
    return this.gridModeService;
  }

  private async getBetaDetectionService(): Promise<IBetaDetectionService> {
    if (!this.betaDetectionService) {
      const { resolve, TYPES } = await import(
        "$lib/services/inversify/container"
      );
      this.betaDetectionService = resolve<IBetaDetectionService>(
        TYPES.IBetaDetectionService
      );
    }
    return this.betaDetectionService;
  }

  async calculatePlacement(
    pictographData: PictographData,
    motionData: MotionData
  ): Promise<PropPlacementData> {
    // Compute gridMode from motion data
    const gridModeService = await this.getGridModeService();
    const gridMode =
      pictographData.motions?.blue && pictographData.motions?.red
        ? gridModeService.deriveGridMode(
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
    // Check if this pictograph ends with beta position
    const betaDetectionService = await this.getBetaDetectionService();
    const needsBetaOffset = betaDetectionService.endsWithBeta(pictographData);

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
    const basePosition = { x: 0, y: 0 };
    const newPosition = offsetCalculator.calculateNewPositionWithOffset(
      basePosition,
      direction
    );

    console.log(
      `🎯 Beta offset calculated for ${motionData.color} prop: direction=${direction}, offset=(${newPosition.x}, ${newPosition.y})`
    );

    return { x: newPosition.x, y: newPosition.y };
  }
}
