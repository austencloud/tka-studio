/**
 * Standalone Math Functions - Ported from working standalone HTML
 *
 * These functions are exact ports from the proven working standalone animator.
 * DO NOT MODIFY - these are tested and working.
 */

import type { PropAttributes } from "../types/core.js";

// Re-export PropAttributes for other modules
export type { PropAttributes };

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
  const l = ori.toLowerCase();

  // Check for cardinal directions first
  if (locationAngles.hasOwnProperty(l)) {
    return locationAngles[l as keyof typeof locationAngles];
  }

  if (l === "in") {
    return normalizeAnglePositive(centerPathAngle + PI);
  }

  if (l === "out") {
    return normalizeAnglePositive(centerPathAngle);
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
  _propRotDir: string // propRotDir can be ignored for pro motion
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
  propRotDir: string
): number {
  console.log(
    "🔧 [PRO DEBUG] ===== CALCULATING PRO TARGET ANGLE WITH TURNS ====="
  );
  console.log("🔧 [PRO DEBUG] Input parameters:");
  console.log(
    "🔧 [PRO DEBUG]   startCenterAngle:",
    startCenterAngle,
    "radians",
    ((startCenterAngle * 180) / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [PRO DEBUG]   targetCenterAngle:",
    targetCenterAngle,
    "radians",
    ((targetCenterAngle * 180) / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [PRO DEBUG]   startStaffAngle:",
    startStaffAngle,
    "radians",
    ((startStaffAngle * 180) / PI).toFixed(1),
    "degrees"
  );
  console.log("🔧 [PRO DEBUG]   turns:", turns);
  console.log("🔧 [PRO DEBUG]   propRotDir:", propRotDir);

  // For pro motions with turns, use similar calculation to anti but with positive delta
  let delta = normalizeAngleSigned(targetCenterAngle - startCenterAngle);
  const base = delta; // Pro motions use positive delta (opposite of anti)
  const turn = PI * turns;
  const dir = propRotDir?.toLowerCase() === "ccw" ? -1 : 1;
  const result = normalizeAnglePositive(startStaffAngle + base + turn * dir);

  console.log("🔧 [PRO DEBUG] Calculation steps:");
  console.log(
    "🔧 [PRO DEBUG]   delta (target - start):",
    delta,
    "radians",
    ((delta * 180) / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [PRO DEBUG]   base (delta):",
    base,
    "radians",
    ((base * 180) / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [PRO DEBUG]   turn (PI * turns):",
    turn,
    "radians",
    ((turn * 180) / PI).toFixed(1),
    "degrees"
  );
  console.log("🔧 [PRO DEBUG]   dir (rotation direction):", dir);
  console.log(
    "🔧 [PRO DEBUG]   raw result (start + base + turn * dir):",
    startStaffAngle + base + turn * dir
  );
  console.log(
    "🔧 [PRO DEBUG]   normalized result:",
    result,
    "radians",
    ((result * 180) / PI).toFixed(1),
    "degrees"
  );

  return result;
}

/**
 * Calculate Antispin target angle (exact port from standalone)
 */
export function calculateAntispinTargetAngle(
  startCenterAngle: number,
  targetCenterAngle: number,
  startStaffAngle: number,
  turns: number,
  propRotDir: string
): number {
  console.log("🔧 [ANTI DEBUG] ===== CALCULATING ANTI-SPIN TARGET ANGLE =====");
  console.log("🔧 [ANTI DEBUG] Input parameters:");
  console.log(
    "🔧 [ANTI DEBUG]   startCenterAngle:",
    startCenterAngle,
    "radians",
    ((startCenterAngle * 180) / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [ANTI DEBUG]   targetCenterAngle:",
    targetCenterAngle,
    "radians",
    ((targetCenterAngle * 180) / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [ANTI DEBUG]   startStaffAngle:",
    startStaffAngle,
    "radians",
    ((startStaffAngle * 180) / PI).toFixed(1),
    "degrees"
  );
  console.log("🔧 [ANTI DEBUG]   turns:", turns);
  console.log("🔧 [ANTI DEBUG]   propRotDir:", propRotDir);

  let delta = normalizeAngleSigned(targetCenterAngle - startCenterAngle);
  const base = -delta;
  const turn = PI * turns;
  const dir = propRotDir?.toLowerCase() === "ccw" ? -1 : 1;
  const result = normalizeAnglePositive(startStaffAngle + base + turn * dir);

  console.log("🔧 [ANTI DEBUG] Calculation steps:");
  console.log(
    "🔧 [ANTI DEBUG]   delta (target - start):",
    delta,
    "radians",
    ((delta * 180) / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [ANTI DEBUG]   base (-delta):",
    base,
    "radians",
    ((base * 180) / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [ANTI DEBUG]   turn (PI * turns):",
    turn,
    "radians",
    ((turn * 180) / PI).toFixed(1),
    "degrees"
  );
  console.log("🔧 [ANTI DEBUG]   dir (rotation direction):", dir);
  console.log(
    "🔧 [ANTI DEBUG]   raw result (start + base + turn * dir):",
    startStaffAngle + base + turn * dir
  );
  console.log(
    "🔧 [ANTI DEBUG]   normalized result:",
    result,
    "radians",
    ((result * 180) / PI).toFixed(1),
    "degrees"
  );

  return result;
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

// PropAttributes is imported from core.ts to avoid duplication

export interface StepDefinition {
  beat?: number;
  letter?: string;
  letter_type?: string;
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

  // Debug logging removed to reduce console clutter
  // console.log("🔧 [ENDPOINT DEBUG] ===== CALCULATING STEP ENDPOINTS =====");
  // console.log("🔧 [ENDPOINT DEBUG] Motion type:", motion_type);
  // console.log("🔧 [ENDPOINT DEBUG] Prop type:", propType);
  // console.log("🔧 [ENDPOINT DEBUG] Motion attributes:", {
  //   start_loc,
  //   end_loc,
  //   start_ori,
  //   end_ori,
  //   motion_type,
  //   prop_rot_dir,
  //   turns,
  // });

  switch (motion_type) {
    case "pro":
      // console.log("🔧 [ENDPOINT DEBUG] Processing PRO motion");
      if (turns > 0) {
        // console.log("🔧 [ENDPOINT DEBUG] PRO motion with turns:", turns);
        calculatedTargetStaffAngle = calculateProTargetAngle(
          startCenterAngle,
          targetCenterAngle,
          startStaffAngle,
          turns,
          prop_rot_dir || "cw"
        );
      } else {
        // console.log("🔧 [ENDPOINT DEBUG] PRO motion isolation (zero turns)");
        calculatedTargetStaffAngle = calculateProIsolationStaffAngle(
          targetCenterAngle,
          prop_rot_dir || "cw"
        );
      }
      break;
    case "anti":
      // console.log("🔧 [ENDPOINT DEBUG] Processing ANTI motion");
      calculatedTargetStaffAngle = calculateAntispinTargetAngle(
        startCenterAngle,
        targetCenterAngle,
        startStaffAngle,
        turns || 0,
        prop_rot_dir || "cw"
      );
      break;
    case "static":
      // console.log("🔧 [ENDPOINT DEBUG] Processing STATIC motion");
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
      // console.log("🔧 [ENDPOINT DEBUG] Processing DASH motion");
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

  // console.log(
  //   "🔧 [ENDPOINT DEBUG] Calculated target staff angle:",
  //   calculatedTargetStaffAngle,
  //   "radians",
  //   ((calculatedTargetStaffAngle * 180) / PI).toFixed(1),
  //   "degrees"
  // );

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
