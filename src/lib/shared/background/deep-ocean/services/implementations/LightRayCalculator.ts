import { injectable } from "inversify";
import type { Dimensions } from "$shared";
import type { ILightRayCalculator } from "../contracts";

@injectable()
export class LightRayCalculator implements ILightRayCalculator {
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
  }> {
    const lightRays: Array<{
      x: number;
      opacity: number;
      width: number;
      angle: number;
      phase: number;
      speed: number;
    }> = [];

    for (let i = 0; i < count; i++) {
      lightRays.push({
        x:
          (i / count) * dimensions.width +
          Math.random() * (dimensions.width / count),
        opacity: 0.05 + Math.random() * 0.15, // Subtle: 0.05-0.2 instead of 0.1-0.3
        width: 8 + Math.random() * 16, // 8-24px width
        angle: -5 + Math.random() * 10, // Slight angle variation: -5 to +5 degrees
        phase: Math.random() * Math.PI * 2, // Random starting phase
        speed: 0.001 + Math.random() * 0.002, // Very slow animation speed
      });
    }

    return lightRays;
  }

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
  }> {
    return lightRays.map((ray) => {
      const newPhase = ray.phase + ray.speed * frameMultiplier;
      // Match monolith: ray.opacity = 0.05 + Math.sin(ray.phase) * 0.05
      const baseOpacity = 0.05 + Math.sin(newPhase) * 0.05;
      return {
        ...ray,
        phase: newPhase,
        opacity: baseOpacity,
      };
    });
  }

  getLightRayCount(quality: string): number {
    switch (quality) {
      case "minimal":
        return 0; // No light rays for minimal
      case "low":
        return 2; // Reduced from 3
      case "medium":
        return 4; // Reduced from 6
      case "high":
        return 6; // Reduced from 9
      default:
        return 4;
    }
  }
}
