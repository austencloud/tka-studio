/**
 * Motion Calculation Service
 *
 * Handles calculations for different motion types including
 * pro, anti, static, dash, and float motions.
 */

import { Orientation, RotationDirection } from "$domain";
import {
  mapOrientationToAngle,
  normalizeAnglePositive,
  normalizeAngleSigned,
} from "./AngleCalculationService.js";
import { PI, TWO_PI } from "./MathConstants.js";

/**
 * Calculate Pro Isolation staff angle using centralized enums
 */
export function calculateProIsolationStaffAngle(
  centerPathAngle: number,
  _propRotDir: RotationDirection // rotationDirection can be ignored for pro motion
): number {
  // For pro motion, staff always points toward center (angle + 180°)
  return normalizeAnglePositive(centerPathAngle + PI);
}

/**
 * Calculate Pro motion target angle with turns support
 */
export function calculateProTargetAngle(
  startCenterAngle: number,
  targetCenterAngle: number,
  startStaffAngle: number,
  turns: number,
  rotationDirection: RotationDirection
): number {
  // Calculate center path movement
  const centerMovement = normalizeAngleSigned(
    targetCenterAngle - startCenterAngle
  );

  // Calculate prop rotation direction multiplier
  const dir =
    rotationDirection === RotationDirection.COUNTER_CLOCKWISE ? -1 : 1;

  // Calculate total staff rotation
  const propRotation = dir * turns * TWO_PI;

  // For pro motion: staff rotates opposite to center path movement
  const staffMovement = -centerMovement;

  // Calculate target staff angle
  const targetStaffAngle = startStaffAngle + staffMovement + propRotation;

  return normalizeAnglePositive(targetStaffAngle);
}

/**
 * Calculate Antispin target angle using centralized enums
 */
export function calculateAntispinTargetAngle(
  startCenterAngle: number,
  targetCenterAngle: number,
  startStaffAngle: number,
  turns: number,
  rotationDirection: RotationDirection
): number {
  // Calculate center path movement
  const centerMovement = normalizeAngleSigned(
    targetCenterAngle - startCenterAngle
  );

  // Calculate prop rotation direction multiplier
  const dir =
    rotationDirection === RotationDirection.COUNTER_CLOCKWISE ? -1 : 1;

  // Calculate total prop rotation
  const propRotation = dir * turns * TWO_PI;

  // For antispin: staff rotates same direction as center path movement
  const staffMovement = centerMovement;

  // Calculate target staff angle
  const targetStaffAngle = startStaffAngle + staffMovement + propRotation;

  return normalizeAnglePositive(targetStaffAngle);
}

/**
 * Calculate static motion staff angle
 */
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

  // Only change if the difference is significant
  return Math.abs(angleDiff) > 0.1 ? endOriAngle : startStaffAngle;
}

/**
 * Calculate dash target angle using centralized enums
 */
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

/**
 * Calculate float motion staff angle (no change)
 */
export function calculateFloatStaffAngle(startStaffAngle: number): number {
  return startStaffAngle;
}
