/**
 * Basic types and data structures for arrow positioning services.
 */

import { MotionColor } from "$domain/enums";

// Enhanced type definitions with comprehensive coverage
export type { Location, MotionType, RotationDirection } from "$domain";
export type ArrowColor = MotionColor;

// Basic types
// Note: Point is now exported from positioning-interfaces.ts
import type { Point } from "../../contracts/positioning-interfaces";

// Re-export Point for backward compatibility
export type { Point };

export interface ArrowPosition extends Point {
  rotation: number;
}
