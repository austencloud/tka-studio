/**
 * Basic types and data structures for arrow positioning services.
 */

import type { Location, MotionData } from "$lib/domain";

// Enhanced type definitions with comprehensive coverage
export type { Location } from "$lib/domain";

export type MotionType = "static" | "pro" | "anti" | "dash" | "float";
export type RotationDirection =
  | "clockwise"
  | "counter_clockwise"
  | "no_rotation"
  | "cw"
  | "ccw"
  | "none";
export type ArrowColor = "blue" | "red";

// Basic types
export interface Point {
  x: number;
  y: number;
}

export interface ArrowPosition extends Point {
  rotation: number;
}

export interface BeatData {
  beatNumber: number;
  letter?: string;
  pictographData: {
    motions?: {
      blue?: MotionData;
      red?: MotionData;
    };
  };
}

// Grid data structures
export interface GridData {
  allHandPointsNormal: Record<Location, { coordinates: Point }>;
  allLayer2PointsNormal: Record<Location, { coordinates: Point }>;
}
