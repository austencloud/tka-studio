/**
 * Static Location Calculator
 *
 * Handles location calculation for static motions.
 * Based on the legacy desktop StaticLocationCalculator.
 */

import type { MotionData } from "$domain";

export class StaticLocationCalculator {
  calculateLocation(motion: MotionData): string {
    // Static motions typically stay at their original location
    const location = motion.startLocation?.toLowerCase();

    if (!location) {
      console.warn("Missing startLocation for static motion");
      return "n"; // Default to north instead of center
    }

    // Map standard directions
    const locationMap: Record<string, string> = {
      n: "n",
      ne: "ne",
      e: "e",
      se: "se",
      s: "s",
      sw: "sw",
      w: "w",
      nw: "nw",
    };

    const mappedLocation = locationMap[location];

    if (!mappedLocation) {
      console.warn(`Unknown static location: ${location}`);
      return "n"; // Default to north instead of center
    }

    return mappedLocation;
  }
}
