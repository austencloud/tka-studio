/**
 * Motion parameter utilities and helper functions
 */

// Helper function to determine motion type based on start/end locations
export function getMotionType(startLoc: string, endLoc: string): string {
  if (startLoc === endLoc) {
    return "static"; // Same location = static
  }

  // Check if it's a dash motion (opposite locations)
  const opposites = [
    ["n", "s"],
    ["s", "n"],
    ["e", "w"],
    ["w", "e"],
  ];

  for (const [start, end] of opposites) {
    if (startLoc === start && endLoc === end) {
      return "dash";
    }
  }

  // Adjacent locations = shift motion (pro/anti/float)
  return "pro"; // Default to pro for shift motions
}

// Helper function to get available motion types for a start/end pair
export function getAvailableMotionTypes(
  startLoc: string,
  endLoc: string,
): string[] {
  const motionType = getMotionType(startLoc, endLoc);

  if (motionType === "static") {
    return ["static"];
  } else if (motionType === "dash") {
    return ["dash"];
  } else {
    // Shift motions can be pro, anti, or float
    return ["pro", "anti", "float"];
  }
}

// Get motion description for display
export function getMotionDescription(
  startLoc: string,
  endLoc: string,
  motionType: string,
  turns: number,
): string {
  const direction =
    startLoc === endLoc
      ? "STATIC"
      : `${startLoc.toUpperCase()}→${endLoc.toUpperCase()}`;
  const rotation = getRotationDirection(startLoc, endLoc, motionType, turns);
  return `${direction} ${motionType.toUpperCase()} ${turns}T ${rotation}`;
}

// Get rotation direction for display
export function getRotationDirection(
  startLoc: string,
  endLoc: string,
  motionType: string,
  turns: number,
): string {
  if (startLoc === endLoc) return "NO_ROT";
  if (motionType === "dash") return "NO_ROT";
  if (turns === 0) return "NO_ROT";

  // Simplified rotation logic for display
  const clockwisePairs = [
    ["n", "e"],
    ["e", "s"],
    ["s", "w"],
    ["w", "n"],
  ];
  const isClockwise = clockwisePairs.some(
    ([start, end]) => start === startLoc && end === endLoc,
  );

  if (motionType === "pro") {
    return isClockwise ? "CW" : "CCW";
  } else {
    return isClockwise ? "CCW" : "CW";
  }
}

// Constants for motion parameters
export const LOCATIONS = ["n", "e", "s", "w"] as const;
export const MOTION_TYPES = ["pro", "anti", "float", "dash"] as const;
export const ORIENTATIONS = ["in", "out", "clock", "counter"] as const;

// Visual position mapping for location display in the path grid
export const LOCATION_POSITIONS: Record<string, any> = {
  n: { top: "15%", left: "50%", transform: "translateX(-50%)" },
  e: { top: "50%", right: "15%", transform: "translateY(-50%)" },
  s: { bottom: "15%", left: "50%", transform: "translateX(-50%)" },
  w: { top: "50%", left: "15%", transform: "translateY(-50%)" },
};

export type Location = (typeof LOCATIONS)[number];
export type MotionType = (typeof MOTION_TYPES)[number];
export type Orientation = (typeof ORIENTATIONS)[number];
