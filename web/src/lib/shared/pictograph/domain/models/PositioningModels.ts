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
export interface XYCoordinate {
  x: number;
  y: number;
}

/**
 * Arrow position with coordinates and rotation angle
 */
export interface ArrowPosition extends XYCoordinate {
  rotation: number;
}

// ArrowPlacementData, MotionData, PictographData are available from $domain - no need to re-export
