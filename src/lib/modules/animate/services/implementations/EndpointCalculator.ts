/**
 * Endpoint Calculation Service
 *
 * Handles calculation of motion endpoints and staff angles
 * for different motion types.
 */

// HMR deep path test - testing file watcher in nested directory with spaces

import type { MotionData, MotionEndpoints } from "$shared";
import { MotionType, Orientation, RotationDirection } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IAngleCalculator } from "../contracts/IAngleCalculator";
import type { IEndpointCalculator } from "../contracts/IEndpointCalculator";
import type { IMotionCalculator } from "../contracts/IMotionCalculator";
import { PI } from "../../domain/math-constants.js";

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

    const startCenterAngle =
      this.angleCalculator.mapPositionToAngle(startLocation);
    const startStaffAngle = this.angleCalculator.mapOrientationToAngle(
      startOrientation || Orientation.IN,
      startCenterAngle
    );
    const targetCenterAngle =
      this.angleCalculator.mapPositionToAngle(endLocation);

    let calculatedTargetStaffAngle: number;
    let calculatedStaffRotationDelta: number;

    // Calculate target staff angle based on motion type
    switch (motionType) {
      case MotionType.PRO: {
        const numericTurns = typeof turns === "number" ? turns : 0;
        const effectiveRotDir =
          rotationDirection || RotationDirection.CLOCKWISE;

        // Calculate delta for interpolation (un-normalized)
        const centerMovement = this.angleCalculator.normalizeAngleSigned(
          targetCenterAngle - startCenterAngle
        );
        const dir =
          effectiveRotDir === RotationDirection.COUNTER_CLOCKWISE ? -1 : 1;
        const propRotation = dir * numericTurns * PI;
        const staffMovement = centerMovement; // PRO: same direction as grid movement
        calculatedStaffRotationDelta = staffMovement + propRotation;

        // Calculate normalized target angle
        calculatedTargetStaffAngle =
          this.motionCalculator.calculateProTargetAngle(
            startCenterAngle,
            targetCenterAngle,
            startStaffAngle,
            numericTurns,
            effectiveRotDir
          );
        break;
      }
      case MotionType.ANTI: {
        const numericTurns = typeof turns === "number" ? turns : 0;
        const effectiveRotDir =
          rotationDirection || RotationDirection.CLOCKWISE;

        // Calculate delta for interpolation (un-normalized)
        const centerMovement = this.angleCalculator.normalizeAngleSigned(
          targetCenterAngle - startCenterAngle
        );
        const dir =
          effectiveRotDir === RotationDirection.COUNTER_CLOCKWISE ? -1 : 1;
        const propRotation = dir * numericTurns * PI;
        const staffMovement = -centerMovement; // ANTI: opposite direction to grid movement
        calculatedStaffRotationDelta = staffMovement + propRotation;

        // Calculate normalized target angle
        calculatedTargetStaffAngle =
          this.motionCalculator.calculateAntispinTargetAngle(
            startCenterAngle,
            targetCenterAngle,
            startStaffAngle,
            numericTurns,
            effectiveRotDir
          );
        break;
      }
      case MotionType.STATIC: {
        const numericTurns = typeof turns === "number" ? turns : 0;
        const effectiveRotDir =
          rotationDirection || RotationDirection.NO_ROTATION;

        // Calculate base orientation angle (without turns)
        const baseTargetAngle = this.motionCalculator.calculateStaticStaffAngle(
          startStaffAngle,
          endOrientation || Orientation.IN,
          targetCenterAngle
        );

        // If there are turns, calculate rotation delta respecting direction
        if (
          numericTurns > 0 &&
          effectiveRotDir !== RotationDirection.NO_ROTATION
        ) {
          // STATIC with turns: rotation is determined ONLY by turns and direction
          // DO NOT add orientation change - the turns value is the total rotation
          const dir =
            effectiveRotDir === RotationDirection.COUNTER_CLOCKWISE ? -1 : 1;
          calculatedStaffRotationDelta = dir * numericTurns * PI; // 1 turn = 180° (π)
          calculatedTargetStaffAngle =
            this.angleCalculator.normalizeAnglePositive(
              startStaffAngle + calculatedStaffRotationDelta
            );
        } else {
          // No turns or NO_ROTATION: use orientation (shortest path)
          calculatedTargetStaffAngle = baseTargetAngle;
          calculatedStaffRotationDelta =
            this.angleCalculator.normalizeAngleSigned(
              calculatedTargetStaffAngle - startStaffAngle
            );
        }
        break;
      }
      case MotionType.DASH: {
        const numericTurns = typeof turns === "number" ? turns : 0;
        const effectiveRotDir =
          rotationDirection || RotationDirection.CLOCKWISE;

        calculatedTargetStaffAngle =
          this.motionCalculator.calculateDashTargetAngle(
            startStaffAngle,
            endOrientation || Orientation.IN,
            targetCenterAngle,
            numericTurns,
            effectiveRotDir
          );

        // DASH with turns: rotation is determined ONLY by turns and direction
        // DO NOT add orientation change - the turns value is the total rotation
        // This ensures multi-turn dashes rotate the full amount, not shortest path
        if (numericTurns > 0) {
          const dir =
            effectiveRotDir === RotationDirection.COUNTER_CLOCKWISE ? -1 : 1;
          calculatedStaffRotationDelta = dir * numericTurns * PI; // 1 turn = 180° (π)
        } else {
          // No turns: calculate based on orientation change only
          const baseAngle = this.motionCalculator.calculateDashTargetAngle(
            startStaffAngle,
            endOrientation || Orientation.IN,
            targetCenterAngle,
            0,
            effectiveRotDir
          );
          calculatedStaffRotationDelta =
            this.angleCalculator.normalizeAngleSigned(
              baseAngle - startStaffAngle
            );
        }
        break;
      }
      case MotionType.FLOAT: {
        calculatedTargetStaffAngle =
          this.motionCalculator.calculateFloatStaffAngle(startStaffAngle);
        // For FLOAT, no rotation
        calculatedStaffRotationDelta = 0;
        break;
      }
      default:
        console.warn(
          `Unknown motion type '${motionType}'. Treating as static.`
        );
        calculatedTargetStaffAngle = startStaffAngle;
        calculatedStaffRotationDelta = 0;
        break;
    }

    return {
      startCenterAngle,
      startStaffAngle,
      targetCenterAngle,
      targetStaffAngle: calculatedTargetStaffAngle,
      staffRotationDelta: calculatedStaffRotationDelta,
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
