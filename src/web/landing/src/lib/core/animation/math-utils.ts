// Mathematical utility functions for the pictograph animator

import { locationAngles, PI, TWO_PI, HALF_PI } from "./constants";

// Utility functions
export function normalizeAnglePositive(angle: number): number {
  return ((angle % TWO_PI) + TWO_PI) % TWO_PI;
}

export function normalizeAngleSigned(angle: number): number {
  let norm = normalizeAnglePositive(angle);
  return norm > PI ? norm - TWO_PI : norm;
}

export function mapPositionToAngle(loc: string): number {
  const l = loc?.toLowerCase();
  return locationAngles[l as keyof typeof locationAngles] ?? 0;
}

export function mapOrientationToAngle(
  ori: string,
  centerPathAngle: number
): number {
  if (!ori) return centerPathAngle + PI;
  const l = ori.toLowerCase();
  if (locationAngles.hasOwnProperty(l))
    return locationAngles[l as keyof typeof locationAngles];
  if (l === "in") return normalizeAnglePositive(centerPathAngle + PI);
  if (l === "out") return normalizeAnglePositive(centerPathAngle);
  return normalizeAnglePositive(centerPathAngle + PI);
}

export function lerp(a: number, b: number, t: number): number {
  return a * (1 - t) + b * t;
}

export function lerpAngle(a: number, b: number, t: number): number {
  const d = normalizeAngleSigned(b - a);
  return normalizeAnglePositive(a + d * t);
}

// Physics functions
export function calculateProIsolationStaffAngle(
  centerPathAngle: number,
  propRotDir: string
): number {
  return normalizeAnglePositive(centerPathAngle + PI);
}

export function calculateAntispinTargetAngle(
  startCenterAngle: number,
  endCenterAngle: number,
  startStaffAngle: number,
  turns: number,
  propRotDir: string
): number {
  let delta = normalizeAngleSigned(endCenterAngle - startCenterAngle);
  const base = -delta;
  const turn = PI * turns;
  const dir = propRotDir?.toLowerCase() === "ccw" ? -1 : 1;
  return normalizeAnglePositive(startStaffAngle + base + turn * dir);
}

export function calculateStaticStaffAngle(
  centerPathAngle: number,
  orientation: string
): number {
  return mapOrientationToAngle(orientation, centerPathAngle);
}

export function calculateDashTargetAngle(
  startCenterAngle: number,
  endCenterAngle: number,
  startStaffAngle: number,
  propRotDir: string
): number {
  return startStaffAngle;
}
