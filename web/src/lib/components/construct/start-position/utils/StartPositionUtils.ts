/**
 * StartPositionUtils.ts - Utility functions for start position handling
 */

import type { BeatData } from "$domain/BeatData";
import { createBeatData } from "$domain/BeatData";
import { MotionType } from "$domain/enums";
import type { PictographData } from "$domain/PictographData";

/**
 * Extract end position from pictograph data
 * This determines where the start position ends, which becomes the starting point for next options
 */
export function extractEndPosition(pictographData: PictographData): string {
  // For start positions, the end position is typically the same as start position
  // since they're static motions, but we need to map to position keys that exist in CSV

  // Default mappings based on legacy desktop patterns
  const defaultEndPositions: Record<string, string> = {
    α: "alpha1", // Alpha start position ends at alpha1
    β: "beta5", // Beta start position ends at beta5
    Γ: "gamma11", // Gamma start position ends at gamma11
  };

  // Try to get from letter first
  if (pictographData.letter && defaultEndPositions[pictographData.letter]) {
    return defaultEndPositions[pictographData.letter] || "alpha1";
  }

  // Default fallback
  return "alpha1";
}

/**
 * Create start position data in the format that OptionPicker expects
 */
export function createStartPositionData(
  pictographData: PictographData,
  endPosition: string
) {
  return {
    // CRITICAL: Include endPosition field for OptionPicker
    endPosition: endPosition,
    // Include the full pictograph data
    pictographData: {
      ...pictographData,
      // Ensure static motion types for start positions - filter out null values
      motions: Object.fromEntries(
        Object.entries({
          blue: pictographData.motions?.blue
            ? {
                ...pictographData.motions.blue,
                motionType: MotionType.STATIC,
                endLocation: pictographData.motions.blue.startLocation,
                endOrientation: pictographData.motions.blue.startOrientation,
                turns: 0,
              }
            : null,
          red: pictographData.motions?.red
            ? {
                ...pictographData.motions.red,
                motionType: MotionType.STATIC,
                endLocation: pictographData.motions.red.startLocation,
                endOrientation: pictographData.motions.red.startOrientation,
                turns: 0,
              }
            : null,
        }).filter(([_, value]) => value !== null)
      ),
    },
  };
}

/**
 * Create beat data from pictograph data for start position
 */
export function createStartPositionBeat(
  pictographData: PictographData
): BeatData {
  return createBeatData({
    pictographData: pictographData,
    beatNumber: 0,
  });
}

/**
 * Store start position data to localStorage for OptionPicker integration
 */
export function storeStartPositionData(data: Record<string, unknown>): void {
  try {
    localStorage.setItem("startPosition", JSON.stringify(data));
  } catch (error) {
    console.error("Failed to store start position data:", error);
  }
}

/**
 * Store preloaded options data to localStorage
 */
export function storePreloadedOptions(options: Record<string, unknown>): void {
  try {
    localStorage.setItem("preloadedOptions", JSON.stringify(options));
  } catch (error) {
    console.error("Failed to store preloaded options:", error);
  }
}

/**
 * Map location to position for compatibility
 */
export function mapLocationToPosition(location: string): string {
  // Simple mapping for now - can be enhanced based on requirements
  const locationToPositionMap: Record<string, string> = {
    N: "alpha1",
    NE: "alpha2",
    E: "alpha3",
    SE: "alpha4",
    S: "alpha5",
    SW: "alpha6",
    W: "alpha7",
    NW: "alpha8",
  };

  return locationToPositionMap[location] || location;
}
