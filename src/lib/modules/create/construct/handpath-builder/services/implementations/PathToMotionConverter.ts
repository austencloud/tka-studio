/**
 * Path to Motion Converter Implementation
 *
 * Core conversion logic from hand paths to MotionData.
 * Implements the PRO/ANTI determination based on hand path direction.
 */

import {
  createMotionData,
  GridLocation,
  GridMode,
  HandMotionType,
  type MotionData,
  MotionType,
  Orientation,
  type PropType,
  RotationDirection,
} from "$shared";
import { inject, injectable } from "inversify";
import { TYPES } from "$lib/shared/inversify/types";
import type { HandPath, HandPathSegment } from "../../domain";
import type { IHandPathDirectionDetector } from "../contracts/IHandPathDirectionDetector";
import type { IPathToMotionConverter } from "../contracts/IPathToMotionConverter";

@injectable()
export class PathToMotionConverter implements IPathToMotionConverter {
  constructor(
    @inject(TYPES.IHandPathDirectionDetector)
    private handPathDirectionDetector: IHandPathDirectionDetector
  ) {}

  convertSegmentToMotion(
    segment: HandPathSegment,
    rotationDirection: RotationDirection,
    propType: PropType
  ): MotionData {
    const motionType = this.determineMotionType(segment, rotationDirection);

    return createMotionData({
      motionType,
      rotationDirection,
      startLocation: segment.startLocation,
      endLocation: segment.endLocation,
      turns: 0.0, // Default to 0 turns for hand sequences
      startOrientation: Orientation.IN, // Default orientation
      endOrientation: Orientation.IN,
      propType,
      color:
        segment.handMotionType === HandMotionType.STATIC
          ? (segment.handMotionType as any) // Will be determined by context
          : (rotationDirection as any), // Placeholder - actual color from HandPath
      gridMode: GridMode.DIAMOND, // Will be overridden by actual grid mode
      isVisible: true,
      // arrowLocation will be calculated by existing services
      arrowLocation: segment.startLocation, // Placeholder
    });
  }

  convertHandPathToMotions(
    handPath: HandPath,
    rotationDirection: RotationDirection,
    propType: PropType
  ): MotionData[] {
    return handPath.segments.map((segment) => {
      const motion = this.convertSegmentToMotion(
        segment,
        rotationDirection,
        propType
      );

      // Apply correct color and grid mode from hand path
      return createMotionData({
        ...motion,
        color: handPath.handColor,
        gridMode: handPath.gridMode,
      });
    });
  }

  determineMotionType(
    segment: HandPathSegment,
    rotationDirection: RotationDirection
  ): MotionType {
    // STATIC motion type
    if (segment.handMotionType === HandMotionType.STATIC) {
      return MotionType.STATIC;
    }

    // DASH motion type
    if (segment.handMotionType === HandMotionType.DASH) {
      return MotionType.DASH;
    }

    // SHIFT motions - depends on rotation direction
    if (rotationDirection === RotationDirection.NO_ROTATION) {
      return MotionType.FLOAT;
    }

    // Determine hand path direction
    // We need to infer grid mode - for now assume DIAMOND (will be passed via HandPath)
    const handPathDirection =
      this.handPathDirectionDetector.getHandPathDirection(
        segment.startLocation,
        segment.endLocation,
        GridMode.DIAMOND // TODO: Pass grid mode through segment
      );

    // If hand path has no rotational direction, default to FLOAT
    if (!handPathDirection) {
      return MotionType.FLOAT;
    }

    // PRO: rotation matches hand path direction
    // ANTI: rotation opposes hand path direction
    if (handPathDirection === rotationDirection) {
      return MotionType.PRO;
    } else {
      return MotionType.ANTI;
    }
  }
}
