/**
 * Shift Location Calculator
 *
 * Handles location calculation for pro, anti, and float motions.
 * Based on the legacy desktop ShiftLocationCalculator.
 */

import type { MotionData } from "$domain";

export class ShiftLocationCalculator {
  calculateLocation(motion: MotionData): string {
    const startLocation = motion.startLocation?.toLowerCase();
    const endLocation = motion.endLocation?.toLowerCase();

    if (!startLocation || !endLocation) {
      console.warn("Missing startLocation or endLocation for shift motion");
      return "ne";
    }

    // Direction pairs mapping from the legacy Python code
    const directionPairs: Record<string, string> = {
      // North-East combinations
      "n-e": "ne",
      "e-n": "ne",

      // East-South combinations
      "e-s": "se",
      "s-e": "se",

      // South-West combinations
      "s-w": "sw",
      "w-s": "sw",

      // West-North combinations
      "w-n": "nw",
      "n-w": "nw",
    };

    const pairKey = `${startLocation}-${endLocation}`;
    const location = directionPairs[pairKey];

    if (!location) {
      console.warn(
        `Unknown direction pair: ${startLocation} -> ${endLocation}`
      );
      return "n"; // Default to north instead of center
    }

    return location;
  }
}
