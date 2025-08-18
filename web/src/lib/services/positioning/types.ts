/**
 * Basic types and data structures for arrow positioning services.
 */

import type { Location, MotionData } from "$lib/domain";
import { MotionColor } from "$lib/domain/enums";

// Enhanced type definitions with comprehensive coverage
export type { Location } from "$lib/domain";
export type { MotionType, RotationDirection } from "$lib/domain";
export type ArrowColor = MotionColor;

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
