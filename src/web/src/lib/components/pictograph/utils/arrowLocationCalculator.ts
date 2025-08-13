/**
 * Arrow Location Calculator
 *
 * Determines arrow location based on start and end positions using the same logic
 * as the desktop app's ShiftLocationCalculator.
 */

export interface ArrowLocationInput {
  start_loc: string;
  end_loc: string;
  motion_type: string;
}

export function calculateArrowLocation(input: ArrowLocationInput): string {
  const { start_loc, end_loc, motion_type } = input;

  // Return empty string if motion state is not initialized
  if (!start_loc || !end_loc) {
    return "";
  }

  // For PRO, ANTI, FLOAT - use shift location calculation
  if (["pro", "anti", "float"].includes(motion_type)) {
    return calculateShiftLocation(start_loc, end_loc);
  }

  // For other types (DASH, STATIC), return start location
  return start_loc;
}

function calculateShiftLocation(start_loc: string, end_loc: string): string {
  const directionPairs: Record<string, string> = {
    // Diagonal combinations
    "n,e": "ne",
    "e,n": "ne",
    "e,s": "se",
    "s,e": "se",
    "s,w": "sw",
    "w,s": "sw",
    "w,n": "nw",
    "n,w": "nw",

    // Corner to cardinal combinations
    "ne,nw": "n",
    "nw,ne": "n",
    "ne,se": "e",
    "se,ne": "e",
    "sw,se": "s",
    "se,sw": "s",
    "nw,sw": "w",
    "sw,nw": "w",
  };

  const key1 = `${start_loc},${end_loc}`;
  const key2 = `${end_loc},${start_loc}`;

  return directionPairs[key1] || directionPairs[key2] || "";
}

// Constants matching the desktop app
export const LOCATIONS = {
  NORTH: "n",
  EAST: "e",
  SOUTH: "s",
  WEST: "w",
  NORTHEAST: "ne",
  SOUTHEAST: "se",
  SOUTHWEST: "sw",
  NORTHWEST: "nw",
} as const;

export const MOTION_TYPES = {
  PRO: "pro",
  ANTI: "anti",
  FLOAT: "float",
  DASH: "dash",
  STATIC: "static",
} as const;
