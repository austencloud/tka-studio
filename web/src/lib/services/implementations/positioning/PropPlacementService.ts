/**
 * Prop Placement Service
 *
 * Dedicated service for calculating prop placement data.
 * Follows separation of concerns by focusing only on placement calculations.
 * Returns PropPlacementData that can be attached to PropPlacementData.
 */

import type {
  MotionData,
  PictographData,
  PropPlacementData,
} from "$lib/domain";
import { GridMode } from "$lib/domain/enums";
import { createPropPlacementFromPosition } from "$lib/domain/PropPlacementData";
import { endsWithBeta } from "$lib/utils/betaDetection";

import { DefaultPropPositioner } from "../../DefaultPropPositioner";
import type { IGridModeDeriver } from "../../interfaces/movement/IGridModeDeriver";
import { PropRotAngleManager } from "../../PropRotAngleManager";
import { BetaOffsetCalculator } from "./BetaOffsetCalculator";
import { BetaPropDirectionCalculator } from "./BetaPropDirectionCalculator";

export interface IPropPlacementService {
  calculatePlacement(
    pictographData: PictographData,
    motionData: MotionData
  ): Promise<PropPlacementData>;
}

export class PropPlacementService implements IPropPlacementService {
  private gridModeService: IGridModeDeriver | null = null;

  private async getGridModeService(): Promise<IGridModeDeriver> {
    if (!this.gridModeService) {
      const { resolve, TYPES } = await import(
        "$lib/services/inversify/container"
      );
      this.gridModeService = resolve<IGridModeDeriver>(TYPES.IGridModeDeriver);
    }
    return this.gridModeService;
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
    const position = this.calculatePosition(
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

  private calculatePosition(
    pictographData: PictographData,
    motionData: MotionData,
    gridMode: GridMode
  ): { x: number; y: number } {
    // Prop data is now embedded in motionData
    const propPlacement = motionData.propPlacementData;

    if (!propPlacement) {
      throw new Error(
        `❌ No prop placement data found for color: ${motionData.color}`
      );
    }

    const basePosition = DefaultPropPositioner.calculatePosition(
      motionData.endLocation,
      gridMode
    );

    const betaOffset = this.calculateBetaOffset(pictographData, motionData);

    return {
      x: basePosition.x + betaOffset.x,
      y: basePosition.y + betaOffset.y,
    };
  }

  private calculateBetaOffset(
    pictographData: PictographData,
    motionData: MotionData
  ): { x: number; y: number } {
    // Prop data is now embedded in motionData
    const propPlacement = motionData.propPlacementData;
    const needsBetaOffset = endsWithBeta(pictographData);

    if (!needsBetaOffset) {
      return { x: 0, y: 0 };
    }

    const redMotion = pictographData.motions?.red;
    const blueMotion = pictographData.motions?.blue;

    if (!redMotion || !blueMotion) {
      return { x: 0, y: 0 };
    }

    if (redMotion.endLocation !== blueMotion.endLocation) {
      return { x: 0, y: 0 };
    }

    if (!propPlacement) {
      throw new Error(
        `❌ No prop placement data found for color: ${motionData.color}`
      );
    }

    const directionCalculator = new BetaPropDirectionCalculator({
      red: redMotion,
      blue: blueMotion,
    });

    // ✅ FIXED: Use the specific motion data for this prop instead of trying to guess from PropPlacementData
    const direction = directionCalculator.getDirectionForMotionData(motionData);

    if (!direction) {
      throw new Error(
        `❌ Could not calculate direction for ${motionData.color} prop in beta position`
      );
    }

    const offsetCalculator = new BetaOffsetCalculator();
    const basePosition = { x: 0, y: 0 };
    const newPosition = offsetCalculator.calculateNewPositionWithOffset(
      basePosition,
      direction
    );

    return { x: newPosition.x, y: newPosition.y };
  }
}
