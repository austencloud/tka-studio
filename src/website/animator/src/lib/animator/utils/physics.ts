// utils/physics.ts - Physics calculations with VALIDATED fixes
import {
  normalizeAnglePositive,
  normalizeAngleSigned,
  mapPositionToAngle,
  mapOrientationToAngle,
  calculateTurnAngle,
} from "./math.js";
import type { SequenceStep, PropAttributes } from "../types.js";

const PI = Math.PI;

export interface StepEndpoints {
  startCenterAngle: number;
  startStaffAngle: number;
  targetCenterAngle: number;
  targetStaffAngle: number;
}

export function calculateStepEndpoints(
  stepDefinition: SequenceStep,
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

  let targetStaffAngle: number;

  switch (motion_type) {
    case "pro":
      targetStaffAngle = calculateProIsolationStaffAngle(
        targetCenterAngle,
        prop_rot_dir,
        turns
      );
      break;
    case "anti":
      targetStaffAngle = calculateAntispinTargetAngle(
        startCenterAngle,
        targetCenterAngle,
        startStaffAngle,
        turns,
        prop_rot_dir
      );
      break;
    case "static":
      targetStaffAngle = calculateStaticStaffAngle(targetCenterAngle, end_ori);
      break;
    case "dash":
      targetStaffAngle = calculateDashTargetAngle(
        startCenterAngle,
        targetCenterAngle,
        startStaffAngle,
        prop_rot_dir
      );
      break;
    default:
      console.warn(`Unknown motion type '${motion_type}'. Treating as static.`);
      targetStaffAngle = startStaffAngle;
  }

  // Override with explicit end orientation if provided
  if (motion_type !== "pro") {
    const endOriAngle = mapOrientationToAngle(
      end_ori || "in",
      targetCenterAngle
    );
    const explicitEndOri = ["n", "e", "s", "w", "in", "out"].includes(
      (end_ori || "").toLowerCase()
    );
    if (explicitEndOri) {
      targetStaffAngle = endOriAngle;
    }
  }

  return {
    startCenterAngle,
    startStaffAngle,
    targetCenterAngle,
    targetStaffAngle,
  };
}

// ✅ FIXED: Pro motion now supports turns parameter
function calculateProIsolationStaffAngle(
  centerPathAngle: number,
  propRotDir?: string,
  turns = 0
): number {
  const basePro = normalizeAnglePositive(centerPathAngle + PI);
  const additionalTurns = calculateTurnAngle(turns); // Uses 2π * turns
  return normalizeAnglePositive(basePro + additionalTurns);
}

// ✅ FIXED: Anti motion uses correct turn calculation
function calculateAntispinTargetAngle(
  startCenterAngle: number,
  endCenterAngle: number,
  startStaffAngle: number,
  turns: number,
  propRotDir?: string
): number {
  const delta = normalizeAngleSigned(endCenterAngle - startCenterAngle);
  const base = -delta;
  const turn = calculateTurnAngle(turns); // Uses 2π * turns
  const dir = propRotDir?.toLowerCase() === "ccw" ? -1 : 1;
  return normalizeAnglePositive(startStaffAngle + base + turn * dir);
}

function calculateStaticStaffAngle(
  centerPathAngle: number,
  orientation?: string
): number {
  return mapOrientationToAngle(orientation || "in", centerPathAngle);
}

function calculateDashTargetAngle(
  startCenterAngle: number,
  endCenterAngle: number,
  startStaffAngle: number,
  propRotDir?: string
): number {
  return startStaffAngle; // Dash maintains staff angle
}
