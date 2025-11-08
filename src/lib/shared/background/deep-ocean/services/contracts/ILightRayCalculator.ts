import type { Dimensions } from "$shared";

/**
 * Contract for light ray calculations and management
 */
export interface ILightRayCalculator {
  /**
   * Initialize light rays for the given dimensions
   */
  initializeLightRays(
    dimensions: Dimensions,
    count: number
  ): Array<{
    x: number;
    opacity: number;
    width: number;
    angle: number;
    phase: number;
    speed: number;
  }>;

  /**
   * Update light ray animations
   */
  updateLightRays(
    lightRays: Array<{
      x: number;
      opacity: number;
      width: number;
      angle: number;
      phase: number;
      speed: number;
    }>,
    frameMultiplier: number
  ): Array<{
    x: number;
    opacity: number;
    width: number;
    angle: number;
    phase: number;
    speed: number;
  }>;

  /**
   * Get optimal light ray count for quality level
   */
  getLightRayCount(quality: string): number;
}
