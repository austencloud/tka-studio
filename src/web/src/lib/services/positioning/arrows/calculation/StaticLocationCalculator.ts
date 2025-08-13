/**
 * Static Location Calculator
 *
 * Handles location calculation for static motions.
 * Based on the legacy desktop StaticLocationCalculator.
 */

import type { MotionData } from "$lib/domain";

export class StaticLocationCalculator {
  calculateLocation(motion: MotionData): string {
    // Static motions typically stay at their original location
    const location = motion.start_loc?.toLowerCase();

    if (!location) {
      console.warn("Missing start_loc for static motion");
      return "center";
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
      center: "center",
    };

    const mappedLocation = locationMap[location];

    if (!mappedLocation) {
      console.warn(`Unknown static location: ${location}`);
      return "center";
    }

    return mappedLocation;
  }
}
