/**
 * StartPositionUtils.ts - Utility functions for start position handling
 */

import type { PictographData } from "$domain/PictographData";
import type { BeatData } from "$domain/BeatData";
import { MotionType, Location } from "$domain/enums";
import { createBeatData } from "$domain/BeatData";

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

  // Try to extract from motion data
  if (pictographData.motions?.blue?.end_loc) {
    return mapLocationToPosition(pictographData.motions.blue.end_loc);
  }
  if (pictographData.motions?.red?.end_loc) {
    return mapLocationToPosition(pictographData.motions.red.end_loc);
  }

  // Default fallback
  return "alpha1";
}

/**
 * Map location enum to position string for CSV lookup
 */
export function mapLocationToPosition(location: Location): string {
  // Basic mapping - this would need to be enhanced based on actual position system
  const locationMap: Record<string, string> = {
    SOUTH: "alpha1",
    NORTH: "alpha1",
    EAST: "gamma11",
    WEST: "alpha1",
    // Add more mappings as needed
  };

  const locationStr =
    typeof location === "string" ? location : String(location || "");
  return locationMap[locationStr.toUpperCase()] || "alpha1";
}

/**
 * Create start position data in the format that OptionPicker expects
 */
export function createStartPositionData(
  pictographData: PictographData,
  endPosition: string
) {
  return {
    // CRITICAL: Include endPos field for OptionPicker
    endPos: endPosition,
    // Include the full pictograph data
    pictograph_data: {
      ...pictographData,
      // Ensure static motion types for start positions
      motions: {
        blue: pictographData.motions?.blue
          ? {
              ...pictographData.motions.blue,
              motion_type: MotionType.STATIC,
              end_loc: pictographData.motions.blue.start_loc,
              end_ori: pictographData.motions.blue.start_ori,
              turns: 0,
            }
          : null,
        red: pictographData.motions?.red
          ? {
              ...pictographData.motions.red,
              motion_type: MotionType.STATIC,
              end_loc: pictographData.motions.red.start_loc,
              end_ori: pictographData.motions.red.start_ori,
              turns: 0,
            }
          : null,
      },
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
    pictograph_data: pictographData,
    beat_number: 1,
    // Store end position in metadata for compatibility
    metadata: {
      end_position: extractEndPosition(pictographData),
      is_start_position: true,
    },
  });
}

/**
 * Store start position data to localStorage for OptionPicker integration
 */
export function storeStartPositionData(data: Record<string, unknown>): void {
  try {
    localStorage.setItem("start_position", JSON.stringify(data));
    console.log("🚀 StartPositionPicker: Saved start position to localStorage");
  } catch (error) {
    console.error("Failed to store start position data:", error);
  }
}

/**
 * Store preloaded options for seamless transition
 */
export function storePreloadedOptions(options: unknown[]): void {
  try {
    localStorage.setItem("preloaded_options", JSON.stringify(options || []));
    console.log(
      "🚀 StartPositionPicker: Preloaded options stored in localStorage"
    );
  } catch (error) {
    console.error("Failed to store preloaded options:", error);
  }
}
