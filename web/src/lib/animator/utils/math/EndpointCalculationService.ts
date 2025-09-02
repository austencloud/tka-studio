/**
 * Endpoint Calculation Service
 *
 * Handles calculation of motion endpoints and staff angles
 * for different motion types.
 */

import type { MotionData } from "$domain";
import { MotionType, Orientation, RotationDirection } from "$domain";
import {
  mapOrientationToAngle,
  mapPositionToAngle,
} from "./AngleCalculationService.js";
import {
  calculateAntispinTargetAngle,
  calculateDashTargetAngle,
  calculateFloatStaffAngle,
  calculateProIsolationStaffAngle,
  calculateProTargetAngle,
  calculateStaticStaffAngle,
} from "./MotionCalculationService.js";

// ✅ ELIMINATED: StepEndpoints and StepDefinition - pointless reshuffling!
// Work directly with MotionData and return simple objects

export interface MotionEndpoints {
  startCenterAngle: number;
  startStaffAngle: number;
  targetCenterAngle: number;
  targetStaffAngle: number;
}

/**
 * Calculate motion endpoints directly from MotionData (NATIVE!)
 */
export function calculateMotionEndpoints(
  motionData: MotionData
): MotionEndpoints {
  const {
    startLocation,
    endLocation,
    startOrientation,
    endOrientation,
    motionType,
    rotationDirection,
    turns = 0,
  } = motionData;

  const startCenterAngle = mapPositionToAngle(startLocation);
  const startStaffAngle = mapOrientationToAngle(
    startOrientation || Orientation.IN,
    startCenterAngle
  );
  const targetCenterAngle = mapPositionToAngle(endLocation);

  let calculatedTargetStaffAngle: number;

  // Calculate target staff angle based on motion type
  switch (motionType) {
    case MotionType.PRO: {
      const numericTurns = typeof turns === "number" ? turns : 0;
      if (numericTurns > 0) {
        calculatedTargetStaffAngle = calculateProTargetAngle(
          startCenterAngle,
          targetCenterAngle,
          startStaffAngle,
          numericTurns,
          rotationDirection || RotationDirection.CLOCKWISE
        );
      } else {
        calculatedTargetStaffAngle = calculateProIsolationStaffAngle(
          targetCenterAngle,
          rotationDirection || RotationDirection.CLOCKWISE
        );
      }
      break;
    }
    case MotionType.ANTI: {
      const numericTurns = typeof turns === "number" ? turns : 0;
      calculatedTargetStaffAngle = calculateAntispinTargetAngle(
        startCenterAngle,
        targetCenterAngle,
        startStaffAngle,
        numericTurns,
        rotationDirection || RotationDirection.CLOCKWISE
      );
      break;
    }
    case MotionType.STATIC: {
      calculatedTargetStaffAngle = calculateStaticStaffAngle(
        startStaffAngle,
        endOrientation || Orientation.IN,
        targetCenterAngle
      );
      break;
    }
    case MotionType.DASH: {
      calculatedTargetStaffAngle = calculateDashTargetAngle(
        startStaffAngle,
        endOrientation || Orientation.IN,
        targetCenterAngle
      );
      break;
    }
    case MotionType.FLOAT: {
      calculatedTargetStaffAngle = calculateFloatStaffAngle(startStaffAngle);
      break;
    }
    default:
      console.warn(`Unknown motion type '${motionType}'. Treating as static.`);
      calculatedTargetStaffAngle = startStaffAngle;
      break;
  }

  // Handle explicit end orientation override (except for pro)
  if (motionType !== MotionType.PRO) {
    const endOriAngleOverride = mapOrientationToAngle(
      endOrientation || Orientation.IN,
      targetCenterAngle
    );
    // Check against enum values instead of string array
    const explicitEndOri =
      endOrientation && Object.values(Orientation).includes(endOrientation);
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

/**
 * Calculate endpoint staff angle for a motion (NATIVE MotionData!)
 */
export function calculateEndpointStaffAngle(motionData: MotionData): number {
  const endpoints = calculateMotionEndpoints(motionData);
  return endpoints.targetStaffAngle;
}
