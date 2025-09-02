/**
 * Basic types and data structures for arrow positioning services.
 */

import { MotionColor } from "$domain";

// Enhanced type definitions with comprehensive coverage
export { Location, MotionType, RotationDirection } from "$domain";
export type ArrowColor = MotionColor;

// Basic types
import type { Point } from "$domain";

export interface ArrowPosition extends Point {
  rotation: number;
}
