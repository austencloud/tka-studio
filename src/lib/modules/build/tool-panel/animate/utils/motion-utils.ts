/**
 * Motion parameter utilities and helper functions
 */

import { GridLocation, HandMotionType, MotionType, Orientation } from "$shared";

// Helper function to determine motion type based on start/end locations
export function getHandpath(
  startLocation: string,
  endLocation: string
): HandMotionType {
  // Normalize to lowercase for case-insensitive comparison
  const start = startLocation.toLowerCase();
  const end = endLocation.toLowerCase();

  if (start === end) {
    return HandMotionType.STATIC; // Same location = static
  }

  // Check if it's a dash motion (opposite locations)
  const opposites = [
    ["n", "s"],
    ["s", "n"],
    ["e", "w"],
    ["w", "e"],
  ];

  for (const [startOpp, endOpp] of opposites) {
    if (start === startOpp && end === endOpp) {
      return HandMotionType.DASH;
    }
  }

  // Adjacent locations = shift motion (pro/anti/float)
  return HandMotionType.SHIFT;
}

// Helper function to get available motion types for a start/end pair
export function getAvailableMotionTypes(
  startLocation: string,
  endLocation: string
): string[] {
  const motionType = getHandpath(startLocation, endLocation);

  if (motionType === HandMotionType.STATIC) {
    return [MotionType.STATIC];
  } else if (motionType === HandMotionType.DASH) {
    return [MotionType.DASH];
  } else {
    return [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT];
  }
}

// Get motion description for display
export function getMotionDescription(
  startLocation: string,
  endLocation: string,
  motionType: string,
  turns: number
): string {
  const direction =
    startLocation === endLocation
      ? "STATIC"
      : `${startLocation.toUpperCase()}→${endLocation.toUpperCase()}`;
  const rotation = getRotationDirection(
    startLocation,
    endLocation,
    motionType,
    turns
  );
  return `${direction} ${motionType.toUpperCase()} ${turns}T ${rotation}`;
}

// Get rotation direction for display
export function getRotationDirection(
  startLocation: string,
  endLocation: string,
  motionType: string,
  turns: number
): string {
  if (startLocation === endLocation) return "noRotation";
  if (motionType === MotionType.DASH) return "noRotation";
  if (turns === 0) return "noRotation";

  // Simplified rotation logic for display
  const clockwisePairs = [
    ["n", "e"],
    ["e", "s"],
    ["s", "w"],
    ["w", "n"],
  ];
  const isClockwise = clockwisePairs.some(
    ([start, end]) => start === startLocation && end === endLocation
  );

  if (motionType === MotionType.PRO) {
    return isClockwise ? "CW" : "CCW";
  } else {
    return isClockwise ? "CCW" : "CW";
  }
}

// Constants for motion parameters - using proper enums
export const LOCATIONS = [
  GridLocation.NORTH,
  GridLocation.EAST,
  GridLocation.SOUTH,
  GridLocation.WEST,
] as const;
export const MOTION_TYPES = [
  MotionType.PRO,
  MotionType.ANTI,
  MotionType.FLOAT,
  MotionType.DASH,
  MotionType.STATIC,
] as const;
export const ORIENTATIONS = [
  Orientation.IN,
  Orientation.OUT,
  Orientation.CLOCK,
  Orientation.COUNTER,
] as const;

// Visual position mapping for location display in the path grid
export const LOCATION_POSITIONS: Record<string, Record<string, string>> = {
  n: { top: "15%", left: "50%", transform: "translateX(-50%)" },
  e: { top: "50%", right: "15%", transform: "translateY(-50%)" },
  s: { bottom: "15%", left: "50%", transform: "translateX(-50%)" },
  w: { top: "50%", left: "15%", transform: "translateY(-50%)" },
};

export type LocationType = (typeof LOCATIONS)[number];
export type MotionTypeType = (typeof MOTION_TYPES)[number];
export type OrientationType = (typeof ORIENTATIONS)[number];
