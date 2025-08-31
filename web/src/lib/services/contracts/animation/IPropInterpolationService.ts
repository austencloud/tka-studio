/**
 * Prop Interpolation Service Interface
 *
 * Interface for prop interpolation and smooth transitions.
 * Handles angle calculations and motion data extraction.
 */

import type { BeatData, MotionData } from "$domain";
import type { InterpolationResult } from "./IAnimationStateService";

// Import MotionEndpoints type for the getEndpoints method
export interface MotionEndpoints {
  startCenterAngle: number;
  startStaffAngle: number;
  targetCenterAngle: number;
  targetStaffAngle: number;
}

export interface IPropInterpolationService {
  interpolatePropAngles(
    currentBeatData: BeatData,
    beatProgress: number
  ): InterpolationResult;
  calculateInitialAngles(firstBeat: BeatData): InterpolationResult;
  getMotionData(beatData: BeatData): { blue: MotionData; red: MotionData };
  getEndpoints(beatData: BeatData): {
    blue: MotionEndpoints;
    red: MotionEndpoints;
  };
}
