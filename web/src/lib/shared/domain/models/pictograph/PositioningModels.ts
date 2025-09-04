/**
 * Positioning and Placement Service Interfaces
 *
 * Interfaces for arrow positioning, placement calculations, and coordinate systems.
 * This handles all spatial calculations and arrow placement logic.
 */

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
 * Position type alias for Point (layout coordinates)
 * @deprecated Use Point directly instead
 */
export type Position = Point;

/**
 * Arrow position with coordinates and rotation angle
 */
export interface ArrowPosition extends Point {
  rotation: number;
}

// ArrowPlacementData, MotionData, PictographData are available from $domain - no need to re-export
