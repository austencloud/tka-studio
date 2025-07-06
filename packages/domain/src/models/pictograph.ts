/**
 * Pictograph Domain Models for TKA
 *
 * These models represent the pure business logic for pictograph rendering and positioning.
 * They integrate with the existing modern architecture and eliminate UI coupling.
 *
 * Source: src/desktop/modern/src/domain/models/pictograph_models.py
 */

import type { MotionData } from "./core.js";
import { GridMode } from "./core.js";

// ============================================================================
// ENUMS
// ============================================================================

export enum ArrowType {
  BLUE = "blue",
  RED = "red",
}

export enum PropType {
  // Hand props
  HAND = "hand",

  // Staff variants
  STAFF = "staff",
  SIMPLESTAFF = "simplestaff",
  BIGSTAFF = "bigstaff",

  // Club variants
  CLUB = "club",

  // Buugeng variants
  BUUGENG = "buugeng",
  BIGBUUGENG = "bigbuugeng",
  FRACTALGENG = "fractalgeng",

  // Ring variants
  EIGHTRINGS = "eightrings",
  BIG_EIGHT_RINGS = "bigeightrings",

  // Hoop variants
  MINIHOOP = "minihoop",
  BIGHOOP = "bighoop",

  // Star variants
  DOUBLESTAR = "doublestar",
  BIGDOUBLESTAR = "bigdoublestar",

  // Other props
  FAN = "fan",
  TRIAD = "triad",
  QUIAD = "quiad",
  SWORD = "sword",
  GUITAR = "guitar",
  UKULELE = "ukulele",
  CHICKEN = "chicken",
  TRIQUETRA = "triquetra",
  TRIQUETRA2 = "triquetra2",
}

// ============================================================================
// INTERFACES
// ============================================================================

/**
 * Immutable data for an arrow in a pictograph.
 * Replaces objects.arrow.arrow.Arrow (with UI coupling)
 */
export interface ArrowData {
  // Core identity
  id: string;
  arrow_type: ArrowType;

  // Motion reference
  motion_data?: MotionData | null;

  // Visual properties
  color: string;
  turns: number;
  is_mirrored: boolean;

  // Position data (calculated by positioning system)
  location?: string | null;
  position_x: number;
  position_y: number;
  rotation_angle: number;

  // State flags
  is_visible: boolean;
  is_selected: boolean;
}

/**
 * Immutable data for a prop in a pictograph.
 * Replaces objects.prop.prop.Prop (with UI coupling)
 */
export interface PropData {
  // Core identity
  id: string;
  prop_type: PropType;

  // Motion reference
  motion_data?: MotionData | null;

  // Visual properties
  color: string;
  orientation: string;
  rotation_direction: string;

  // Position data (calculated by positioning system)
  location?: string | null;
  position_x: number;
  position_y: number;

  // State flags
  is_visible: boolean;
  is_selected: boolean;
}

/**
 * Immutable data for the pictograph grid system.
 * Replaces base_widgets.pictograph.elements.grid.grid_data.GridData
 */
export interface GridData {
  // Grid configuration
  grid_mode: GridMode;
  center_x: number;
  center_y: number;
  radius: number;

  // Grid points (calculated positions)
  grid_points: Record<string, [number, number]>;
}

/**
 * Immutable data for a complete pictograph.
 * Replaces base_widgets.pictograph.pictograph.Pictograph (QGraphicsScene)
 *
 * This is the main pictograph model that contains all the data needed
 * to render a pictograph without any UI coupling.
 */
export interface PictographData {
  // Core identity
  id: string;

  // Grid configuration
  grid_data: GridData;

  // Arrows and props
  arrows: Record<string, ArrowData>; // "blue", "red"
  props: Record<string, PropData>; // "blue", "red"

  // Letter and position data
  letter?: string | null;
  start_position?: string | null;
  end_position?: string | null;

  // Visual state
  is_blank: boolean;
  is_mirrored: boolean;

  // Metadata
  metadata: Record<string, any>;
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Generate a simple UUID-like string for testing/development.
 */
function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36);
}

/**
 * Create a default arrow data object.
 */
export function createDefaultArrowData(
  arrowType: ArrowType = ArrowType.BLUE
): ArrowData {
  return {
    id: generateId(),
    arrow_type: arrowType,
    motion_data: null,
    color: arrowType === ArrowType.BLUE ? "blue" : "red",
    turns: 0,
    is_mirrored: false,
    location: null,
    position_x: 0,
    position_y: 0,
    rotation_angle: 0,
    is_visible: true,
    is_selected: false,
  };
}

/**
 * Create a default prop data object.
 */
export function createDefaultPropData(color: string = "blue"): PropData {
  return {
    id: generateId(),
    prop_type: PropType.STAFF,
    motion_data: null,
    color,
    orientation: "in",
    rotation_direction: "cw",
    location: null,
    position_x: 0,
    position_y: 0,
    is_visible: true,
    is_selected: false,
  };
}

/**
 * Create a default grid data object.
 */
export function createDefaultGridData(): GridData {
  return {
    grid_mode: GridMode.DIAMOND,
    center_x: 0,
    center_y: 0,
    radius: 100,
    grid_points: {},
  };
}

/**
 * Create a default pictograph data object.
 */
export function createDefaultPictographData(): PictographData {
  return {
    id: generateId(),
    grid_data: createDefaultGridData(),
    arrows: {
      blue: createDefaultArrowData(ArrowType.BLUE),
      red: createDefaultArrowData(ArrowType.RED),
    },
    props: {
      blue: createDefaultPropData("blue"),
      red: createDefaultPropData("red"),
    },
    letter: null,
    start_position: null,
    end_position: null,
    is_blank: false,
    is_mirrored: false,
    metadata: {},
  };
}
