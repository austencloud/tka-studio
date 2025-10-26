/**
 * Prop Interpolation Service
 *
 * Focused service for angle interpolation and motion calculations.
 * Single responsibility: Motion interpolation between keyframes.
 */

import type { BeatData, MotionData, MotionEndpoints } from "$shared";
import { MotionType } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IPropInterpolator, InterpolationResult } from "../contracts";
import type { IAngleCalculator } from "../contracts/IAngleCalculator";
import type { IEndpointCalculator } from "../contracts/IEndpointCalculator";

@injectable()
export class PropInterpolator implements IPropInterpolator {
  constructor(
    @inject(TYPES.IAngleCalculator) private angleCalculator: IAngleCalculator,
    @inject(TYPES.IEndpointCalculator) private endpointCalculator: IEndpointCalculator
  ) {}

  /**
   * Calculate interpolated prop angles for current beat progress
   * Uses Cartesian interpolation for DASH motions (straight through center)
   * Uses angular interpolation for all other motions
   */
  interpolatePropAngles(
    currentBeatData: BeatData,
    beatProgress: number
  ): InterpolationResult {
    // Get motion data directly from domain beat (PURE DOMAIN!)
    const blueMotion = currentBeatData?.motions.blue;
    const redMotion = currentBeatData?.motions.red;

    if (!blueMotion) {
      throw new Error("Blue motion data is missing for current beat.");
    }

    if (!redMotion) {
      throw new Error("Red motion data is missing for current beat.");
    }

    // Calculate endpoints using native MotionData
    const blueEndpoints = this.endpointCalculator.calculateMotionEndpoints(blueMotion);
    const redEndpoints = this.endpointCalculator.calculateMotionEndpoints(redMotion);

    // Check if motions are dashes - use Cartesian interpolation for straight-through-center movement
    const blueDash = blueMotion.motionType === MotionType.DASH;
    const redDash = redMotion.motionType === MotionType.DASH;

    // Log only at beat start to show motion plan
    if (beatProgress < 0.05) {
      console.log(`🎯 Beat ${currentBeatData.letter || '?'}:`, {
        blue: `${blueMotion.motionType} ${blueMotion.startLocation}→${blueMotion.endLocation}`,
        red: `${redMotion.motionType} ${redMotion.startLocation}→${redMotion.endLocation}`
      });

      // Show ACTUAL endpoint angles being calculated
      console.log('  📐 RED ENDPOINTS:', {
        startCenter: `${(redEndpoints.startCenterAngle * 180 / Math.PI).toFixed(0)}°`,
        targetCenter: `${(redEndpoints.targetCenterAngle * 180 / Math.PI).toFixed(0)}°`,
        startStaff: `${(redEndpoints.startStaffAngle * 180 / Math.PI).toFixed(0)}°`,
        targetStaff: `${(redEndpoints.targetStaffAngle * 180 / Math.PI).toFixed(0)}°`
      });
    }

    // Interpolate blue prop
    const blueAngles = blueDash
      ? this.interpolateDashMotion(blueEndpoints, beatProgress)
      : {
          // Grid location: ALWAYS shortest path (W → N always goes W → NW → N)
          centerPathAngle: this.angleCalculator.lerpAngle(
            blueEndpoints.startCenterAngle,
            blueEndpoints.targetCenterAngle,
            beatProgress
          ),
          // Staff rotation: Use shortest path - targetStaffAngle already has rotation direction baked in
          staffRotationAngle: this.angleCalculator.lerpAngle(
            blueEndpoints.startStaffAngle,
            blueEndpoints.targetStaffAngle,
            beatProgress
          ),
          // Don't set x,y for non-dash motions - let CanvasRenderer calculate from angle
        };

    // Interpolate red prop
    const redAngles = redDash
      ? this.interpolateDashMotion(redEndpoints, beatProgress)
      : {
          // Grid location: ALWAYS shortest path
          centerPathAngle: this.angleCalculator.lerpAngle(
            redEndpoints.startCenterAngle,
            redEndpoints.targetCenterAngle,
            beatProgress
          ),
          // Staff rotation: Use shortest path - targetStaffAngle already has rotation direction baked in
          staffRotationAngle: this.angleCalculator.lerpAngle(
            redEndpoints.startStaffAngle,
            redEndpoints.targetStaffAngle,
            beatProgress
          ),
          // Don't set x,y for non-dash motions - let CanvasRenderer calculate from angle
        };

    // Log ACTUAL interpolated angle at beat midpoint to verify it's actually changing
    if (Math.abs(beatProgress - 0.5) < 0.05) {
      console.log(`  ➡️ At 50%: Red center angle = ${(redAngles.centerPathAngle * 180 / Math.PI).toFixed(0)}°`);
    }

    return {
      blueAngles,
      redAngles,
      isValid: true,
    };
  }

  /**
   * Interpolate dash motion using Cartesian coordinates
   * Dashes move in a straight line through the center, not around the circle
   * Returns angle for compatibility, but the angle will be recalculated from x,y in the renderer
   */
  private interpolateDashMotion(
    endpoints: MotionEndpoints,
    progress: number
  ): { centerPathAngle: number; staffRotationAngle: number; x?: number; y?: number } {
    // Convert start and end angles to Cartesian coordinates (unit circle)
    const startX = Math.cos(endpoints.startCenterAngle);
    const startY = Math.sin(endpoints.startCenterAngle);
    const endX = Math.cos(endpoints.targetCenterAngle);
    const endY = Math.sin(endpoints.targetCenterAngle);

    // Linear interpolation in Cartesian space (straight line through center)
    const currentX = startX + (endX - startX) * progress;
    const currentY = startY + (endY - startY) * progress;

    // Convert back to angle for compatibility
    const centerPathAngle = Math.atan2(currentY, currentX);

    // Staff rotation interpolates normally
    const staffRotationAngle = this.angleCalculator.lerpAngle(
      endpoints.startStaffAngle,
      endpoints.targetStaffAngle,
      progress
    );

    // Return x,y coordinates so renderer can use them directly
    return { centerPathAngle, staffRotationAngle, x: currentX, y: currentY };
  }

  /**
   * Calculate initial prop angles from first beat
   */
  calculateInitialAngles(firstBeat: BeatData): InterpolationResult {
    // Get motion data directly from domain beat (PURE DOMAIN!)
    const blueStartMotion = firstBeat.motions.blue;
    const redStartMotion = firstBeat.motions.red;

    if (!blueStartMotion) {
      throw new Error("Blue motion data is missing for the first beat.");
    }

    if (!redStartMotion) {
      throw new Error("Red motion data is missing for the first beat.");
    }

    const blueStartEndpoints = this.endpointCalculator.calculateMotionEndpoints(blueStartMotion);
    const redStartEndpoints = this.endpointCalculator.calculateMotionEndpoints(redStartMotion);

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
    const blueMotion = beatData?.motions.blue;
    const redMotion = beatData?.motions.red;

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
      blue: this.endpointCalculator.calculateMotionEndpoints(motionData.blue),
      red: this.endpointCalculator.calculateMotionEndpoints(motionData.red),
    };
  }
}
