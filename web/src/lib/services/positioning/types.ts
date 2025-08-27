/**
 * Basic types and data structures for arrow positioning services.
 */

import { MotionColor } from "$lib/domain/enums";

// Enhanced type definitions with comprehensive coverage
export type { Location } from "$lib/domain";
export type { MotionType, RotationDirection } from "$lib/domain";
export type ArrowColor = MotionColor;

// Basic types
// Note: Point is now exported from positioning-interfaces.ts
import type { Point } from "../interfaces/positioning-interfaces";

// Re-export Point for backward compatibility
export type { Point };

export interface ArrowPosition extends Point {
  rotation: number;
}



