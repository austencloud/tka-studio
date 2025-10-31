/**
 * Prop Placement Service
 *
 * Dedicated service for calculating prop placement data.
 * Follows separation of concerns by focusing only on placement calculations.
 * Returns PropPlacementData that can be attached to PropPlacementData.
 */

import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import { GridMode } from "../../../grid/domain/enums/grid-enums";
import type { IGridModeDeriver } from "../../../grid/services/contracts/IGridModeDeriver";
import {
  Orientation,
  VectorDirection,
} from "../../../shared/domain/enums/pictograph-enums";
import type { MotionData } from "../../../shared/domain/models/MotionData";
import type { PictographData } from "../../../shared/domain/models/PictographData";
import {
  getBetaOffsetSize,
  isUnilateralProp,
} from "../../domain/enums/PropClassification";
import { createPropPlacementFromPosition } from "../../domain/factories/createPropPlacementData";
import type { PropPlacementData } from "../../domain/models/PropPlacementData";
import type { IBetaDetectionService } from "../contracts/IBetaDetectionService";
import type { IPropPlacementService } from "../contracts/IPropPlacementService";
import { BetaPropDirectionCalculator } from "./BetaPropDirectionCalculator";
import DefaultPropPositioner from "./DefaultPropPositioner";
import { PropRotAngleManager } from "./PropRotAngleManager";

@injectable()
export class PropPlacementService implements IPropPlacementService {
  constructor(
    @inject(TYPES.IGridModeDeriver) private gridModeService: IGridModeDeriver,
    @inject(TYPES.IBetaDetectionService)
    private betaDetectionService: IBetaDetectionService
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
      motionData,
      gridMode
    );

    return {
      x: basePosition.x + betaOffset.x,
      y: basePosition.y + betaOffset.y,
    };
  }

  private async calculateBetaOffset(
    pictographData: PictographData,
    motionData: MotionData,
    gridMode: GridMode
  ): Promise<{ x: number; y: number }> {
    // Check if this pictograph ends with beta position - now synchronous!
    const needsBetaOffset =
      this.betaDetectionService.endsWithBeta(pictographData);

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

    // ORIENTATION-BASED BETA SKIP LOGIC (from desktop legacy)
    // Unilateral props skip beta offset when they end with:
    // 1. DIFFERENT radial orientations (IN/OUT or OUT/IN) - but NOT (IN/IN) or (OUT/OUT)
    // 2. DIFFERENT non-radial orientations (CLOCK/COUNTER or COUNTER/CLOCK) - but NOT (CLOCK/CLOCK) or (COUNTER/COUNTER)
    const redPropType = redMotion.propType;
    const bluePropType = blueMotion.propType;

    const bothPropsUnilateral =
      isUnilateralProp(redPropType) && isUnilateralProp(bluePropType);

    if (bothPropsUnilateral) {
      const redEndOri = redMotion.endOrientation;
      const blueEndOri = blueMotion.endOrientation;

      // Check if both are radial orientations BUT DIFFERENT
      const differentRadial =
        (redEndOri === Orientation.IN && blueEndOri === Orientation.OUT) ||
        (redEndOri === Orientation.OUT && blueEndOri === Orientation.IN);

      // Check if both are non-radial orientations BUT DIFFERENT
      const differentNonRadial =
        (redEndOri === Orientation.CLOCK &&
          blueEndOri === Orientation.COUNTER) ||
        (redEndOri === Orientation.COUNTER && blueEndOri === Orientation.CLOCK);

      // Skip beta offset ONLY when orientations are DIFFERENT within same category
      if (differentRadial || differentNonRadial) {
        return { x: 0, y: 0 };
      }
    }

    // Calculate direction for this specific prop
    const directionCalculator = new BetaPropDirectionCalculator(
      {
        red: redMotion,
        blue: blueMotion,
      },
      pictographData.letter || undefined
    );

    const direction = directionCalculator.getDirectionForMotionData(motionData);

    if (!direction) {
      return { x: 0, y: 0 };
    }

    // Calculate the offset based on the direction and prop type
    const offset = this.getOffsetForDirection(
      direction,
      motionData.propType,
      gridMode
    );
    return { x: offset.x, y: offset.y };
  }

  /**
   * Get pixel offset for a given direction
   * Offset distance varies by prop type based on desktop legacy calculations:
   * - Large props (club, eightrings): 15.83px (diamond) / 11.20px (box)
   * - Medium props (doublestar): 19px (diamond) / 13.43px (box)
   * - Default props: 21.11px (diamond) / 14.93px (box)
   * Box mode uses diagonal compensation (÷√2) to achieve equal visual spacing.
   */
  private getOffsetForDirection(
    direction: VectorDirection,
    propType: string,
    gridMode: GridMode
  ): {
    x: number;
    y: number;
  } {
    // Get prop-type-specific offset distance with grid mode scaling
    const distance = getBetaOffsetSize(propType, gridMode);

    switch (direction) {
      case VectorDirection.UP:
        return { x: 0, y: -distance };
      case VectorDirection.DOWN:
        return { x: 0, y: distance };
      case VectorDirection.LEFT:
        return { x: -distance, y: 0 };
      case VectorDirection.RIGHT:
        return { x: distance, y: 0 };
      case VectorDirection.UPRIGHT:
        return { x: distance, y: -distance };
      case VectorDirection.DOWNRIGHT:
        return { x: distance, y: distance };
      case VectorDirection.UPLEFT:
        return { x: -distance, y: -distance };
      case VectorDirection.DOWNLEFT:
        return { x: -distance, y: distance };
      default:
        return { x: 0, y: 0 };
    }
  }
}
