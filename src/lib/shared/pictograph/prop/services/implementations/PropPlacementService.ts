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
    // Use gridMode from motion data if available (supports single-motion pictographs in Guided mode)
    // Fall back to deriving from full pictograph data only if not set in motion
    const gridMode =
      motionData.gridMode ??
      (pictographData.motions?.blue && pictographData.motions?.red
        ? this.gridModeService.deriveGridMode(
            pictographData.motions.blue,
            pictographData.motions.red
          )
        : GridMode.DIAMOND);
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
    // Beta offset is applied when BOTH props share the same orientation TYPE:
    // - BOTH radial (IN/IN, IN/OUT, OUT/IN, OUT/OUT) → APPLY offset
    // - BOTH non-radial (CLOCK/CLOCK, CLOCK/COUNTER, COUNTER/CLOCK, COUNTER/COUNTER) → APPLY offset
    // - HYBRID (one radial + one non-radial) → SKIP offset
    //
    // This applies to ALL prop types (unilateral AND bilateral)
    const redEndOri = redMotion.endOrientation;
    const blueEndOri = blueMotion.endOrientation;

    // Define radial and non-radial orientations
    const radialOrientations = [Orientation.IN, Orientation.OUT];
    const nonRadialOrientations = [Orientation.CLOCK, Orientation.COUNTER];

    const redIsRadial = radialOrientations.includes(redEndOri);
    const blueIsRadial = radialOrientations.includes(blueEndOri);
    const redIsNonRadial = nonRadialOrientations.includes(redEndOri);
    const blueIsNonRadial = nonRadialOrientations.includes(blueEndOri);

    // Check if one is radial and one is non-radial (hybrid orientation)
    const hybridOrientation =
      (redIsRadial && blueIsNonRadial) || (redIsNonRadial && blueIsRadial);

    // Skip beta offset when hybrid (one radial, one non-radial)
    if (hybridOrientation) {
      return { x: 0, y: 0 };
    }

    // Skip beta offset for UNILATERAL props when both props have same orientation TYPE
    // but DIFFERENT specific orientations (OUT/IN or CLOCK/COUNTER)
    // Bilateral props always get the offset (unless hybrid)
    const bothRadial = redIsRadial && blueIsRadial;
    const bothNonRadial = redIsNonRadial && blueIsNonRadial;
    const sameTypeButDifferentOrientation =
      (bothRadial && redEndOri !== blueEndOri) ||
      (bothNonRadial && redEndOri !== blueEndOri);

    if (
      sameTypeButDifferentOrientation &&
      isUnilateralProp(motionData.propType)
    ) {
      return { x: 0, y: 0 };
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
