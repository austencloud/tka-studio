/**
 * Endpoint Calculation Service
 *
 * Handles calculation of motion endpoints and staff angles
 * for different motion types.
 */

import type { MotionData, MotionEndpoints } from "$shared";
import { MotionType, Orientation, RotationDirection } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IAngleCalculator } from "../contracts/IAngleCalculator";
import type { IEndpointCalculator } from "../contracts/IEndpointCalculator";
import type { IMotionCalculator } from "../contracts/IMotionCalculator";

// ✅ ELIMINATED: StepEndpoints and StepDefinition - pointless reshuffling!
// Work directly with MotionData and return simple objects

@injectable()
export class EndpointCalculator implements IEndpointCalculator {
  constructor(
    @inject(TYPES.IAngleCalculator) private angleCalculator: IAngleCalculator,
    @inject(TYPES.IMotionCalculator) private motionCalculator: IMotionCalculator
  ) {}

  /**
   * Calculate motion endpoints directly from MotionData (NATIVE!)
   */
  calculateMotionEndpoints(motionData: MotionData): MotionEndpoints {
  const {
    startLocation,
    endLocation,
    startOrientation,
    endOrientation,
    motionType,
    rotationDirection,
    turns = 0,
  } = motionData;

    // Logging removed - too noisy

    const startCenterAngle = this.angleCalculator.mapPositionToAngle(startLocation);
    const startStaffAngle = this.angleCalculator.mapOrientationToAngle(
      startOrientation || Orientation.IN,
      startCenterAngle
    );
    const targetCenterAngle = this.angleCalculator.mapPositionToAngle(endLocation);

    let calculatedTargetStaffAngle: number;

    // Calculate target staff angle based on motion type
    switch (motionType) {
      case MotionType.PRO: {
        const numericTurns = typeof turns === "number" ? turns : 0;
        // Always use calculateProTargetAngle, even for 0 turns
        // This ensures proper rotation from start to end position
        calculatedTargetStaffAngle = this.motionCalculator.calculateProTargetAngle(
          startCenterAngle,
          targetCenterAngle,
          startStaffAngle,
          numericTurns,
          rotationDirection || RotationDirection.CLOCKWISE
        );
        break;
      }
      case MotionType.ANTI: {
        const numericTurns = typeof turns === "number" ? turns : 0;
        calculatedTargetStaffAngle = this.motionCalculator.calculateAntispinTargetAngle(
          startCenterAngle,
          targetCenterAngle,
          startStaffAngle,
          numericTurns,
          rotationDirection || RotationDirection.CLOCKWISE
        );
        break;
      }
      case MotionType.STATIC: {
        calculatedTargetStaffAngle = this.motionCalculator.calculateStaticStaffAngle(
          startStaffAngle,
          endOrientation || Orientation.IN,
          targetCenterAngle
        );
        break;
      }
      case MotionType.DASH: {
        calculatedTargetStaffAngle = this.motionCalculator.calculateDashTargetAngle(
          startStaffAngle,
          endOrientation || Orientation.IN,
          targetCenterAngle
        );
        break;
      }
      case MotionType.FLOAT: {
        calculatedTargetStaffAngle = this.motionCalculator.calculateFloatStaffAngle(startStaffAngle);
        break;
      }
      default:
        console.warn(`Unknown motion type '${motionType}'. Treating as static.`);
        calculatedTargetStaffAngle = startStaffAngle;
        break;
    }

    // Handle explicit end orientation override (except for pro)
    if (motionType !== MotionType.PRO) {
      const endOriAngleOverride = this.angleCalculator.mapOrientationToAngle(
        endOrientation || Orientation.IN,
        targetCenterAngle
      );
      // Check against enum values instead of string array
      const explicitEndOri =
        endOrientation && Object.values(Orientation).includes(endOrientation);
      if (explicitEndOri) {
        calculatedTargetStaffAngle = endOriAngleOverride;
      }
    }

    return {
      startCenterAngle,
      startStaffAngle,
      targetCenterAngle,
      targetStaffAngle: calculatedTargetStaffAngle,
      rotationDirection: rotationDirection || RotationDirection.CLOCKWISE, // Pass through for interpolation
    };
  }

  /**
   * Calculate endpoint staff angle for a motion (NATIVE MotionData!)
   */
  calculateEndpointStaffAngle(motionData: MotionData): number {
    const endpoints = this.calculateMotionEndpoints(motionData);
    return endpoints.targetStaffAngle;
  }
}
