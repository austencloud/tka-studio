/**
 * Prop Interpolation Service Interface
 *
 * Interface for prop interpolation and smooth transitions.
 * Handles angle calculations and motion data extraction.
 */

import type { BeatData, MotionData, MotionEndpoints } from "$shared";
import type { InterpolationResult } from "./IAnimationStateManager";

export interface IPropInterpolator {
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
