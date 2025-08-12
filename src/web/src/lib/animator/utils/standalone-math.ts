/**
 * Standalone Math Functions - Ported from working standalone HTML
 *
 * These functions are exact ports from the proven working standalone animator.
 * DO NOT MODIFY - these are tested and working.
 */

// Math constants from standalone
const PI = Math.PI;
const TWO_PI = 2 * PI;
const HALF_PI = PI / 2;

// Location angles mapping from standalone
const locationAngles = {
  e: 0,
  s: HALF_PI,
  w: PI,
  n: -HALF_PI,
};

/**
 * Normalize angle to positive range [0, 2π)
 */
export function normalizeAnglePositive(angle: number): number {
  let norm = angle % TWO_PI;
  return norm < 0 ? norm + TWO_PI : norm;
}

/**
 * Normalize angle to signed range (-π, π]
 */
export function normalizeAngleSigned(angle: number): number {
  let norm = normalizeAnglePositive(angle);
  return norm > PI ? norm - TWO_PI : norm;
}

/**
 * Map grid position to angle (exact port from standalone)
 */
export function mapPositionToAngle(loc: string): number {
  const l = loc?.toLowerCase();
  return locationAngles[l as keyof typeof locationAngles] ?? 0;
}

/**
 * Map orientation to staff angle (exact port from standalone)
 */
export function mapOrientationToAngle(
  ori: string,
  centerPathAngle: number
): number {
  if (!ori) return centerPathAngle + PI;
  if (ori.toLowerCase() === "in") {
    return normalizeAnglePositive(centerPathAngle + PI);
  }
  return normalizeAnglePositive(centerPathAngle + PI);
}

/**
 * Linear interpolation
 */
export function lerp(a: number, b: number, t: number): number {
  return a * (1 - t) + b * t;
}

/**
 * Angle interpolation with proper wrapping (exact port from standalone)
 */
export function lerpAngle(a: number, b: number, t: number): number {
  const d = normalizeAngleSigned(b - a);
  return normalizeAnglePositive(a + d * t);
}

/**
 * Calculate Pro Isolation staff angle (exact port from standalone)
 */
export function calculateProIsolationStaffAngle(
  centerPathAngle: number,
  propRotDir: string
): number {
  if (propRotDir === "cw") {
    return normalizeAnglePositive(centerPathAngle - HALF_PI);
  } else if (propRotDir === "ccw") {
    return normalizeAnglePositive(centerPathAngle + HALF_PI);
  }
  return centerPathAngle;
}

/**
 * Calculate Antispin target angle (exact port from standalone)
 */
export function calculateAntispinTargetAngle(
  startCenterAngle: number,
  targetCenterAngle: number,
  startStaffAngle: number,
  propRotDir: string
): number {
  const centerAngleDelta = normalizeAngleSigned(
    targetCenterAngle - startCenterAngle
  );
  if (propRotDir === "cw") {
    return normalizeAnglePositive(startStaffAngle - centerAngleDelta);
  } else if (propRotDir === "ccw") {
    return normalizeAnglePositive(startStaffAngle + centerAngleDelta);
  }
  return startStaffAngle;
}

/**
 * Calculate static staff angle (exact port from standalone)
 */
export function calculateStaticStaffAngle(
  startStaffAngle: number,
  endOri: string,
  targetCenterAngle: number
): number {
  if (endOri?.toLowerCase() === "in") {
    return normalizeAnglePositive(targetCenterAngle + PI);
  } else if (endOri?.toLowerCase() === "out") {
    return targetCenterAngle;
  }
  return startStaffAngle;
}

/**
 * Calculate dash target angle (exact port from standalone)
 */
export function calculateDashTargetAngle(
  startStaffAngle: number,
  endOri: string,
  targetCenterAngle: number
): number {
  if (endOri?.toLowerCase() === "in") {
    return normalizeAnglePositive(targetCenterAngle + PI);
  } else if (endOri?.toLowerCase() === "out") {
    return targetCenterAngle;
  }
  return startStaffAngle;
}

/**
 * Calculate float staff angle (exact port from standalone)
 */
export function calculateFloatStaffAngle(startStaffAngle: number): number {
  return startStaffAngle;
}

// Types for step endpoints
export interface StepEndpoints {
  startCenterAngle: number;
  startStaffAngle: number;
  targetCenterAngle: number;
  targetStaffAngle: number;
}

export interface PropAttributes {
  start_loc: string;
  end_loc: string;
  start_ori?: string;
  end_ori?: string;
  motion_type: string;
  prop_rot_dir?: string;
  turns?: number;
}

export interface StepDefinition {
  blue_attributes?: PropAttributes;
  red_attributes?: PropAttributes;
}

/**
 * Calculate step endpoints (exact port from standalone)
 */
export function calculateStepEndpoints(
  stepDefinition: StepDefinition,
  propType: "blue" | "red"
): StepEndpoints | null {
  const attributes =
    propType === "blue"
      ? stepDefinition.blue_attributes
      : stepDefinition.red_attributes;

  if (!attributes) return null;

  const {
    start_loc,
    end_loc,
    start_ori,
    end_ori,
    motion_type,
    prop_rot_dir,
    turns = 0,
  } = attributes;

  const startCenterAngle = mapPositionToAngle(start_loc);
  const startStaffAngle = mapOrientationToAngle(
    start_ori || "in",
    startCenterAngle
  );
  const targetCenterAngle = mapPositionToAngle(end_loc);

  let calculatedTargetStaffAngle: number;

  switch (motion_type) {
    case "pro":
      calculatedTargetStaffAngle = calculateProIsolationStaffAngle(
        targetCenterAngle,
        prop_rot_dir || "cw"
      );
      break;
    case "anti":
      calculatedTargetStaffAngle = calculateAntispinTargetAngle(
        startCenterAngle,
        targetCenterAngle,
        startStaffAngle,
        prop_rot_dir || "cw"
      );
      break;
    case "static":
      const endOriAngleStatic = mapOrientationToAngle(
        end_ori || "in",
        targetCenterAngle
      );
      const angleDiffStatic = normalizeAngleSigned(
        endOriAngleStatic - startStaffAngle
      );
      calculatedTargetStaffAngle =
        Math.abs(angleDiffStatic) > 0.1 ? endOriAngleStatic : startStaffAngle;
      break;
    case "dash":
      calculatedTargetStaffAngle = calculateDashTargetAngle(
        startStaffAngle,
        end_ori || "in",
        targetCenterAngle
      );
      break;
    default:
      console.warn(`Unknown motion type '${motion_type}'. Treating as static.`);
      calculatedTargetStaffAngle = startStaffAngle;
      break;
  }

  // Handle explicit end orientation override (except for pro)
  if (motion_type !== "pro") {
    const endOriAngleOverride = mapOrientationToAngle(
      end_ori || "in",
      targetCenterAngle
    );
    const explicitEndOri = ["n", "e", "s", "w", "in", "out"].includes(
      (end_ori || "").toLowerCase()
    );
    if (explicitEndOri) {
      calculatedTargetStaffAngle = endOriAngleOverride;
    }
  }

  return {
    startCenterAngle,
    startStaffAngle,
    targetCenterAngle,
    targetStaffAngle: calculatedTargetStaffAngle,
  };
}
