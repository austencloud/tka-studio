/**
 * Endpoint Calculator Service Contract
 *
 * Handles calculation of motion endpoints and staff angles
 * for different motion types.
 */

import type { MotionData, MotionEndpoints } from "$shared";

export interface IEndpointCalculator {
  /**
   * Calculate motion endpoints directly from MotionData
   */
  calculateMotionEndpoints(motionData: MotionData): MotionEndpoints;

  /**
   * Calculate endpoint staff angle for a motion
   */
  calculateEndpointStaffAngle(motionData: MotionData): number;
}

