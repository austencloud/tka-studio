/**
 * Core Domain Models for TKA
 *
 * These are the fundamental business models converted from Python to TypeScript.
 * They maintain exact compatibility with the desktop application's domain models.
 *
 * Source: src/desktop/modern/src/domain/models/core_models.py
 */

// ============================================================================
// ENUMS - Matching Python exactly
// ============================================================================

export enum MotionType {
  PRO = "pro",
  ANTI = "anti",
  FLOAT = "float",
  DASH = "dash",
  STATIC = "static",
}

export enum HandMotionType {
  SHIFT = "shift",
  DASH = "dash",
  STATIC = "static",
}

export enum HandPath {
  CLOCKWISE = "cw",
  COUNTER_CLOCKWISE = "ccw",
  DASH = "dash",
  STATIC = "static",
}

export enum RotationDirection {
  CLOCKWISE = "cw",
  COUNTER_CLOCKWISE = "ccw",
  NO_ROTATION = "no_rot",
}

export enum Orientation {
  IN = "in",
  OUT = "out",
  CLOCK = "clock",
  COUNTER = "counter",
}

export enum Location {
  NORTH = "n",
  EAST = "e",
  SOUTH = "s",
  WEST = "w",
  NORTHEAST = "ne",
  SOUTHEAST = "se",
  SOUTHWEST = "sw",
  NORTHWEST = "nw",
}

export enum GridPosition {
  // Alpha positions (radial)
  ALPHA1 = "alpha1",
  ALPHA2 = "alpha2",
  ALPHA3 = "alpha3",
  ALPHA4 = "alpha4",
  ALPHA5 = "alpha5",
  ALPHA6 = "alpha6",
  ALPHA7 = "alpha7",
  ALPHA8 = "alpha8",

  // Beta positions (same direction)
  BETA1 = "beta1",
  BETA2 = "beta2",
  BETA3 = "beta3",
  BETA4 = "beta4",
  BETA5 = "beta5",
  BETA6 = "beta6",
  BETA7 = "beta7",
  BETA8 = "beta8",

  // Gamma positions (shift)
  GAMMA1 = "gamma1",
  GAMMA2 = "gamma2",
  GAMMA3 = "gamma3",
  GAMMA4 = "gamma4",
  GAMMA5 = "gamma5",
  GAMMA6 = "gamma6",
  GAMMA7 = "gamma7",
  GAMMA8 = "gamma8",
  GAMMA9 = "gamma9",
  GAMMA10 = "gamma10",
  GAMMA11 = "gamma11",
  GAMMA12 = "gamma12",
  GAMMA13 = "gamma13",
  GAMMA14 = "gamma14",
  GAMMA15 = "gamma15",
  GAMMA16 = "gamma16",
}

export enum VTGMode {
  SPLIT_SAME = "SS",
  SPLIT_OPP = "SO",
  TOG_SAME = "TS",
  TOG_OPP = "TO",
  QUARTER_SAME = "QS",
  QUARTER_OPP = "QO",
}

export enum ElementalType {
  WATER = "water",
  FIRE = "fire",
  EARTH = "earth",
  AIR = "air",
  SUN = "sun",
  MOON = "moon",
}

export enum LetterType {
  TYPE1 = "Type1",
  TYPE2 = "Type2",
  TYPE3 = "Type3",
  TYPE4 = "Type4",
  TYPE5 = "Type5",
  TYPE6 = "Type6",
  TYPE7 = "Type7",
  TYPE8 = "Type8",
  TYPE9 = "Type9",
}

export enum ArrowColor {
  RED = "red",
  BLUE = "blue",
}

export enum GridMode {
  DIAMOND = "diamond",
  BOX = "box",
}

export enum Letter {
  A = "A",
  B = "B",
  C = "C",
  D = "D",
  E = "E",
  F = "F",
  G = "G",
  H = "H",
  I = "I",
  J = "J",
  K = "K",
  L = "L",
  M = "M",
  N = "N",
  O = "O",
  P = "P",
  Q = "Q",
  R = "R",
  S = "S",
  T = "T",
  U = "U",
  V = "V",
  W = "W",
  X = "X",
  Y = "Y",
  Z = "Z",
  Σ = "Σ",
  Δ = "Δ",
  θ = "θ",
  Ω = "Ω",
  W_DASH = "W-",
  X_DASH = "X-",
  Y_DASH = "Y-",
  Z_DASH = "Z-",
  Σ_DASH = "Σ-",
  Δ_DASH = "Δ-",
  θ_DASH = "θ-",
  Ω_DASH = "Ω-",
  Φ = "Φ",
  Ψ = "Ψ",
  Λ = "Λ",
  Φ_DASH = "Φ-",
  Ψ_DASH = "Ψ-",
  Λ_DASH = "Λ-",
  α = "α",
  β = "β",
  Γ = "Γ",
}

// ============================================================================
// INTERFACES - Core Data Structures
// ============================================================================

/**
 * Immutable motion data for props and arrows.
 * Replaces complex motion attribute dictionaries.
 */
export interface MotionData {
  motion_type: MotionType;
  prop_rot_dir: RotationDirection;
  start_loc: Location;
  end_loc: Location;
  turns: number;
  start_ori: Orientation;
  end_ori: Orientation;
}

/**
 * Data for pictograph glyphs (elemental, VTG, TKA, position).
 */
export interface GlyphData {
  // VTG glyph data
  vtg_mode?: VTGMode | null;

  // Elemental glyph data
  elemental_type?: ElementalType | null;

  // TKA glyph data
  letter_type?: LetterType | null;
  has_dash: boolean;
  turns_data?: string | null;

  // Start-to-end position glyph data
  start_position?: string | null;
  end_position?: string | null;

  // Visibility flags
  show_elemental: boolean;
  show_vtg: boolean;
  show_tka: boolean;
  show_positions: boolean;
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Convert orientation value to Orientation enum with backward compatibility.
 */
export function convertOrientation(value: any): Orientation {
  if (typeof value === "string") {
    const valueLower = value.toLowerCase().trim();
    const orientationMap: Record<string, Orientation> = {
      in: Orientation.IN,
      out: Orientation.OUT,
      clock: Orientation.CLOCK,
      counter: Orientation.COUNTER,
    };
    return orientationMap[valueLower] || Orientation.IN;
  }

  if (typeof value === "number") {
    const angleMap: Record<number, Orientation> = {
      0: Orientation.IN,
      90: Orientation.CLOCK,
      180: Orientation.OUT,
      270: Orientation.COUNTER,
    };
    return angleMap[Math.round(value)] || Orientation.IN;
  }

  return Orientation.IN;
}

/**
 * Create a default motion data object.
 */
export function createDefaultMotionData(): MotionData {
  return {
    motion_type: MotionType.PRO,
    prop_rot_dir: RotationDirection.CLOCKWISE,
    start_loc: Location.NORTH,
    end_loc: Location.EAST,
    turns: 0,
    start_ori: Orientation.IN,
    end_ori: Orientation.IN,
  };
}

/**
 * Create a default glyph data object.
 */
export function createDefaultGlyphData(): GlyphData {
  return {
    vtg_mode: null,
    elemental_type: null,
    letter_type: null,
    has_dash: false,
    turns_data: null,
    start_position: null,
    end_position: null,
    show_elemental: true,
    show_vtg: true,
    show_tka: true,
    show_positions: true,
  };
}
