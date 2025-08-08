// Sequence processing and data validation utilities

import type { StepDefinition, StepEndpoints } from "./types";
import {
  mapPositionToAngle,
  mapOrientationToAngle,
  normalizeAngleSigned,
  calculateProIsolationStaffAngle,
  calculateAntispinTargetAngle,
  calculateStaticStaffAngle,
  calculateDashTargetAngle,
} from "./math-utils";

// Core logic for calculating step endpoints
export function calculateStepEndpoints(
  stepDefinition: StepDefinition,
  propType: string
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

  let calculatedTargetStaffAngle;

  switch (motion_type) {
    case "pro":
      calculatedTargetStaffAngle = calculateProIsolationStaffAngle(
        targetCenterAngle,
        prop_rot_dir
      );
      break;
    case "anti":
      calculatedTargetStaffAngle = calculateAntispinTargetAngle(
        startCenterAngle,
        targetCenterAngle,
        startStaffAngle,
        turns,
        prop_rot_dir
      );
      break;
    case "static":
      let targetStaticAngle = startStaffAngle;
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
        startCenterAngle,
        targetCenterAngle,
        startStaffAngle,
        prop_rot_dir
      );
      break;
    default:
      console.warn(`Unknown motion type '${motion_type}'. Treating as static.`);
      calculatedTargetStaffAngle = startStaffAngle;
      break;
  }

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

// Process and validate sequence data
export function processSequenceData(sequenceArray: any[]): {
  parsedSteps: StepDefinition[];
  totalBeats: number;
} {
  console.log("🎵 SEQUENCE: Processing sequence data...", {
    length: sequenceArray.length,
  });
  if (!Array.isArray(sequenceArray) || sequenceArray.length < 2) {
    throw new Error(
      "Invalid sequence data: Must be an array with at least 2 elements (metadata + start state)."
    );
  }

  if (
    typeof sequenceArray[0] !== "object" ||
    typeof sequenceArray[1] !== "object"
  ) {
    throw new Error(
      "Invalid sequence data: First two elements must be objects."
    );
  }

  const parsedSteps = sequenceArray.map((step, index) => ({
    ...step,
    arrayIndex: index,
  }));
  const totalBeats = parsedSteps.length - 2;

  console.log("🎵 SEQUENCE: Parsed steps:", parsedSteps.length);
  console.log("🎵 SEQUENCE: Total beats:", totalBeats);

  if (totalBeats <= 0) {
    throw new Error("Sequence has no animation steps.");
  }

  console.log("✅ SEQUENCE: Processing complete!");

  return { parsedSteps, totalBeats };
}
