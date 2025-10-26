/**
 * Motion Calculation Service
 *
 * Handles calculations for different motion types including
 * pro, anti, static, dash, and float motions.
 */

import { Orientation, RotationDirection } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import { PI, TWO_PI } from "../../domain/math-constants.js";
import type { IAngleCalculator } from "../contracts/IAngleCalculator";
import type { IMotionCalculator } from "../contracts/IMotionCalculator";
import { mapOrientationToAngle, normalizeAnglePositive, normalizeAngleSigned } from "./AngleCalculator";

// ============================================================================
// Standalone utility functions (exported for use by domain layer)
// ============================================================================

export function calculateProIsolationStaffAngle(
  centerPathAngle: number,
  _propRotDir: RotationDirection
): number {
  return normalizeAnglePositive(centerPathAngle + PI);
}

export function calculateProTargetAngle(
  startCenterAngle: number,
  targetCenterAngle: number,
  startStaffAngle: number,
  turns: number,
  rotationDirection: RotationDirection
): number {
  const centerMovement = normalizeAngleSigned(targetCenterAngle - startCenterAngle);
  const dir = rotationDirection === RotationDirection.COUNTER_CLOCKWISE ? -1 : 1;
  const propRotation = dir * turns * TWO_PI;
  const staffMovement = -centerMovement;
  const targetStaffAngle = startStaffAngle + staffMovement + propRotation;
  return normalizeAnglePositive(targetStaffAngle);
}

export function calculateAntispinTargetAngle(
  startCenterAngle: number,
  targetCenterAngle: number,
  startStaffAngle: number,
  turns: number,
  rotationDirection: RotationDirection
): number {
  const centerMovement = normalizeAngleSigned(targetCenterAngle - startCenterAngle);
  const dir = rotationDirection === RotationDirection.COUNTER_CLOCKWISE ? -1 : 1;
  const propRotation = dir * turns * TWO_PI;
  const staffMovement = centerMovement;
  const targetStaffAngle = startStaffAngle + staffMovement + propRotation;
  return normalizeAnglePositive(targetStaffAngle);
}

export function calculateStaticStaffAngle(
  startStaffAngle: number,
  endOrientation: Orientation,
  targetCenterAngle: number
): number {
  if (!endOrientation) {
    return startStaffAngle;
  }

  const endOriAngle = mapOrientationToAngle(endOrientation, targetCenterAngle);
  const angleDiff = normalizeAngleSigned(endOriAngle - startStaffAngle);

  return Math.abs(angleDiff) > 0.1 ? endOriAngle : startStaffAngle;
}

export function calculateDashTargetAngle(
  startStaffAngle: number,
  endOrientation: Orientation,
  targetCenterAngle: number
): number {
  if (endOrientation === Orientation.IN) {
    return normalizeAnglePositive(targetCenterAngle + PI);
  } else if (endOrientation === Orientation.OUT) {
    return targetCenterAngle;
  }
  return startStaffAngle;
}

export function calculateFloatStaffAngle(startStaffAngle: number): number {
  return startStaffAngle;
}

// ============================================================================
// Service class (delegates to standalone functions)
// ============================================================================

@injectable()
export class MotionCalculator implements IMotionCalculator {
  constructor(
    @inject(TYPES.IAngleCalculator) private angleCalculator: IAngleCalculator
  ) {}

  /**
   * Calculate Pro Isolation staff angle using centralized enums
   */
  calculateProIsolationStaffAngle(
    centerPathAngle: number,
    propRotDir: RotationDirection
  ): number {
    return calculateProIsolationStaffAngle(centerPathAngle, propRotDir);
  }

  /**
   * Calculate Pro motion target angle with turns support
   */
  calculateProTargetAngle(
    startCenterAngle: number,
    targetCenterAngle: number,
    startStaffAngle: number,
    turns: number,
    rotationDirection: RotationDirection
  ): number {
    return calculateProTargetAngle(
      startCenterAngle,
      targetCenterAngle,
      startStaffAngle,
      turns,
      rotationDirection
    );
  }

  /**
   * Calculate Antispin target angle using centralized enums
   */
  calculateAntispinTargetAngle(
    startCenterAngle: number,
    targetCenterAngle: number,
    startStaffAngle: number,
    turns: number,
    rotationDirection: RotationDirection
  ): number {
    return calculateAntispinTargetAngle(
      startCenterAngle,
      targetCenterAngle,
      startStaffAngle,
      turns,
      rotationDirection
    );
  }

  /**
   * Calculate static motion staff angle
   */
  calculateStaticStaffAngle(
    startStaffAngle: number,
    endOrientation: Orientation,
    targetCenterAngle: number
  ): number {
    return calculateStaticStaffAngle(startStaffAngle, endOrientation, targetCenterAngle);
  }

  /**
   * Calculate dash target angle using centralized enums
   */
  calculateDashTargetAngle(
    startStaffAngle: number,
    endOrientation: Orientation,
    targetCenterAngle: number
  ): number {
    return calculateDashTargetAngle(startStaffAngle, endOrientation, targetCenterAngle);
  }

  /**
   * Calculate float motion staff angle (no change)
   */
  calculateFloatStaffAngle(startStaffAngle: number): number {
    return calculateFloatStaffAngle(startStaffAngle);
  }
}
