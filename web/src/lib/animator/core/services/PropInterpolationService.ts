/**
 * Prop Interpolation Service
 *
 * Focused service for angle interpolation and motion calculations.
 * Single responsibility: Motion interpolation between keyframes.
 */

import type {
  IPropInterpolationService,
  InterpolationResult,
} from "$contracts";
import type { BeatData, MotionData } from "$domain";

import { injectable } from "inversify";
import {
  calculateMotionEndpoints,
  lerpAngle,
  type MotionEndpoints,
} from "$utils";

@injectable()
export class PropInterpolationService implements IPropInterpolationService {
  /**
   * Calculate interpolated prop angles for current beat progress
   * EXACT INTERPOLATION LOGIC FROM STANDALONE
   */
  interpolatePropAngles(
    currentBeatData: BeatData,
    beatProgress: number
  ): InterpolationResult {
    // Get motion data directly from domain beat (PURE DOMAIN!)
    const blueMotion = currentBeatData.pictographData?.motions.blue;
    const redMotion = currentBeatData.pictographData?.motions.red;

    if (!blueMotion) {
      throw new Error("Blue motion data is missing for current beat.");
    }

    if (!redMotion) {
      throw new Error("Red motion data is missing for current beat.");
    }

    // Calculate endpoints using native MotionData
    const blueEndpoints = calculateMotionEndpoints(blueMotion);
    const redEndpoints = calculateMotionEndpoints(redMotion);

    // EXACT INTERPOLATION LOGIC FROM STANDALONE
    const blueAngles = {
      centerPathAngle: lerpAngle(
        blueEndpoints.startCenterAngle,
        blueEndpoints.targetCenterAngle,
        beatProgress
      ),
      staffRotationAngle: lerpAngle(
        blueEndpoints.startStaffAngle,
        blueEndpoints.targetStaffAngle,
        beatProgress
      ),
    };

    const redAngles = {
      centerPathAngle: lerpAngle(
        redEndpoints.startCenterAngle,
        redEndpoints.targetCenterAngle,
        beatProgress
      ),
      staffRotationAngle: lerpAngle(
        redEndpoints.startStaffAngle,
        redEndpoints.targetStaffAngle,
        beatProgress
      ),
    };

    return {
      blueAngles,
      redAngles,
      isValid: true,
    };
  }

  /**
   * Calculate initial prop angles from first beat
   */
  calculateInitialAngles(firstBeat: BeatData): InterpolationResult {
    // Get motion data directly from domain beat (PURE DOMAIN!)
    const blueStartMotion = firstBeat.pictographData?.motions.blue;
    const redStartMotion = firstBeat.pictographData?.motions.red;

    if (!blueStartMotion) {
      throw new Error("Blue motion data is missing for the first beat.");
    }

    if (!redStartMotion) {
      throw new Error("Red motion data is missing for the first beat.");
    }

    const blueStartEndpoints = calculateMotionEndpoints(blueStartMotion);
    const redStartEndpoints = calculateMotionEndpoints(redStartMotion);

    return {
      blueAngles: {
        centerPathAngle: blueStartEndpoints.startCenterAngle,
        staffRotationAngle: blueStartEndpoints.startStaffAngle,
      },
      redAngles: {
        centerPathAngle: redStartEndpoints.startCenterAngle,
        staffRotationAngle: redStartEndpoints.startStaffAngle,
      },
      isValid: true,
    };
  }

  /**
   * Get motion data for debugging
   */
  getMotionData(beatData: BeatData): { blue: MotionData; red: MotionData } {
    const blueMotion = beatData.pictographData?.motions.blue;
    const redMotion = beatData.pictographData?.motions.red;

    if (!blueMotion) {
      throw new Error("Blue motion data is missing for current beat.");
    }

    if (!redMotion) {
      throw new Error("Red motion data is missing for current beat.");
    }

    return {
      blue: blueMotion,
      red: redMotion,
    };
  }

  /**
   * Calculate endpoints for debugging
   */
  getEndpoints(beatData: BeatData): {
    blue: MotionEndpoints;
    red: MotionEndpoints;
  } {
    const motionData = this.getMotionData(beatData);
    return {
      blue: calculateMotionEndpoints(motionData.blue),
      red: calculateMotionEndpoints(motionData.red),
    };
  }
}
