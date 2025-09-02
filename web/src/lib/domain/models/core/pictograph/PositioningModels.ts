/**
 * Positioning and Placement Service Interfaces
 *
 * Interfaces for arrow positioning, placement calculations, and coordinate systems.
 * This handles all spatial calculations and arrow placement logic.
 */

// ============================================================================
// IMPORTS
// ============================================================================
import type { ArrowPlacementData, MotionData, PictographData } from "$domain";

// Location and MotionType are available from $domain - no need to re-export

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

// ArrowPlacementData, MotionData, PictographData are available from $domain - no need to re-export
