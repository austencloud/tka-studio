/**
 * Angle Calculation Service
 *
 * Handles all angle-related calculations including normalization,
 * position mapping, and orientation mapping.
 */

import { Location, Orientation } from "$domain";
import { HALF_PI, LOCATION_ANGLES, PI, TWO_PI } from "./MathConstants.js";

/**
 * Normalize angle to positive range [0, 2π)
 */
export function normalizeAnglePositive(angle: number): number {
  const norm = angle % TWO_PI;
  return norm < 0 ? norm + TWO_PI : norm;
}

/**
 * Normalize angle to signed range (-π, π]
 */
export function normalizeAngleSigned(angle: number): number {
  const norm = normalizeAnglePositive(angle);
  return norm > PI ? norm - TWO_PI : norm;
}

/**
 * Map grid position to angle using centralized enums
 */
export function mapPositionToAngle(loc: Location): number {
  return LOCATION_ANGLES[loc] ?? 0;
}

/**
 * Map orientation to staff angle using centralized enums
 */
export function mapOrientationToAngle(
  ori: Orientation,
  centerPathAngle: number
): number {
  if (!ori) return centerPathAngle + PI;

  // Handle standard orientations
  if (ori === Orientation.IN) {
    return normalizeAnglePositive(centerPathAngle + PI);
  }

  if (ori === Orientation.OUT) {
    return normalizeAnglePositive(centerPathAngle);
  }

  if (ori === Orientation.CLOCK) {
    return normalizeAnglePositive(centerPathAngle + HALF_PI);
  }

  if (ori === Orientation.COUNTER) {
    return normalizeAnglePositive(centerPathAngle - HALF_PI);
  }

  return normalizeAnglePositive(centerPathAngle + PI);
}

/**
 * Linear interpolation between two values
 */
export function lerp(a: number, b: number, t: number): number {
  return a * (1 - t) + b * t;
}

/**
 * Angular interpolation (handles wraparound)
 */
export function lerpAngle(a: number, b: number, t: number): number {
  const d = normalizeAngleSigned(b - a);
  return normalizeAnglePositive(a + d * t);
}
