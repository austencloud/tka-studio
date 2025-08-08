/**
 * Prop-specific calculation utilities
 * Updated to use the new sequence interpretation configuration system
 */

import type { PropRotDir } from "../../types/core.js";
import { PI, TWO_PI } from "./constants.js";
import { normalizeAnglePositive, mapOrientationToAngle } from "./angles.js";
import {
  getOrientationAngle,
  getRotationMultiplier,
  degreesToRadians,
  normalizeAngle,
} from "../../config/sequence-interpretation.js";

export function calculateProIsolationStaffAngle(
  startOri: string | undefined,
  endOri: string | undefined,
  propRotDir: PropRotDir,
  turns: number | undefined,
  t: number
): number {
  const startAngle = getOrientationAngle(startOri);
  const endAngle = getOrientationAngle(endOri);
  const numTurns = turns ?? 0;

  // Special case: 0 turns is a "float" - handle differently
  if (numTurns === 0) {
    // For 0 turns (float), the staff should rotate 90 degrees
    // in the same direction as the center path rotation to cancel visual rotation
    const baseRotation = startAngle;
    const floatRotation =
      degreesToRadians(90) * getRotationMultiplier(propRotDir);
    return normalizeAngle(baseRotation + floatRotation * t);
  }

  // Calculate total rotation for non-zero turns
  // Special case for pro motion with 0 turns: perform 90-degree isolation
  if (numTurns === 0) {
    // For isolation with 0 turns, add 90 degrees (π/2) in the specified direction
    const isolationRotation = propRotDir === "ccw" ? -PI / 2 : PI / 2;
    return normalizeAnglePositive(startAngle + isolationRotation * t);
  }

  // For non-zero turns, use orientation-based interpolation
  let totalRotation = endAngle - startAngle;

  if (propRotDir === "cw") {
    totalRotation += numTurns * TWO_PI;
    if (totalRotation < 0) totalRotation += TWO_PI;
  } else if (propRotDir === "ccw") {
    totalRotation -= numTurns * TWO_PI;
    if (totalRotation > 0) totalRotation -= TWO_PI;
  }

  return normalizeAngle(startAngle + totalRotation * t);
}

export function calculateAntispinTargetAngle(
  centerPathAngle: number,
  startOri: string | undefined,
  endOri: string | undefined,
  propRotDir: PropRotDir,
  turns: number | undefined,
  t: number
): number {
  const startAngle = mapOrientationToAngle(
    (startOri as "in" | "out" | "n" | "e" | "s" | "w") || "in"
  );
  const numTurns = turns ?? 0;

  // For antispin, we need to calculate based on hand movement direction
  // The prop rotates opposite to the hand's movement around the center

  // Calculate the base antispin rotation (opposite to hand movement)
  // For 0 turns, this should be exactly 90 degrees (π/2) opposite to prop_rot_dir
  let baseRotation: number;

  if (propRotDir === "cw") {
    totalRotation += numTurns * TWO_PI;
  } else if (propRotDir === "ccw") {
    totalRotation -= numTurns * TWO_PI;
  }

  const staffAngle = startAngle + totalRotation * t;
  return normalizeAnglePositive(staffAngle - centerPathAngle);
}

export function calculateStaticStaffAngle(
  centerPathAngle: number,
  startOri: string | undefined
): number {
  const startAngle = getOrientationAngle(startOri);
  // For static motion, maintain fixed orientation relative to grid
  return normalizeAngle(startAngle - centerPathAngle);
}

export function calculateDashTargetAngle(
  centerPathAngle: number,
  startOri: string | undefined,
  endOri: string | undefined,
  t: number
): number {
  const startAngle = getOrientationAngle(startOri);
  const endAngle = getOrientationAngle(endOri);

  // Calculate the shortest path between orientations
  let angleDiff = endAngle - startAngle;
  if (angleDiff > PI) {
    angleDiff -= TWO_PI;
  }
  if (angleDiff < -PI) {
    angleDiff += TWO_PI;
  }

  // Interpolate between start and end orientations
  const staffAngle = startAngle + angleDiff * t;

  // Adjust for center path rotation to maintain orientation relative to grid
  return normalizeAngle(staffAngle - centerPathAngle);
}

export function calculateFloatStaffAngle(
  startOri: string | undefined,
  endOri: string | undefined,
  t: number
): number {
  const startAngle = getOrientationAngle(startOri);
  const endAngle = getOrientationAngle(endOri);

  let angleDiff = endAngle - startAngle;
  if (angleDiff > PI) angleDiff -= TWO_PI;
  if (angleDiff < -PI) angleDiff += TWO_PI;

  const staffAngle = startAngle + angleDiff * t;
  return normalizeAngle(staffAngle);
}
