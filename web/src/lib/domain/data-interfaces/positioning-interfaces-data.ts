/**
 * Positioning and Placement Service Interfaces
 *
 * Interfaces for arrow positioning, placement calculations, and coordinate systems.
 * This handles all spatial calculations and arrow placement logic.
 */

// ============================================================================
// IMPORTS
// ============================================================================
import type { MotionType } from "$domain";
import { Location } from "../enums";

// Re-export commonly used types
export type { Location, MotionType };

// ============================================================================
// BASIC TYPES
// ============================================================================

/**
 * Basic point interface for coordinates
 */
export interface Point {
  x: number;
  y: number;
}

/**
 * Position interface for beta offset calculations
 */
export interface Position {
  x: number;
  y: number;
}

// Import the actual types from domain-types to avoid duplicates
import type { ArrowPlacementData, MotionData, PictographData } from "$domain";

// Re-export for convenience
export type { ArrowPlacementData, MotionData, PictographData };
