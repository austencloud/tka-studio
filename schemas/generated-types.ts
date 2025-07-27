/**
 * TypeScript types generated from TKA schemas v2
 * Based on modern desktop domain models
 *
 * GENERATED FROM: F:\CODE\TKA\schemas\
 * DO NOT EDIT - Regenerate from schemas when desktop models change
 *
 * Last updated: 2025-07-26
 */

// ==================== CORE ENUMS ====================
// (from core-enums.json)

export type MotionType = "pro" | "anti" | "float" | "dash" | "static";
export type HandMotionType = "shift" | "dash" | "static";
export type HandPath = "cw" | "ccw" | "dash" | "static";
export type RotationDirection = "cw" | "ccw" | "no_rot";
export type Orientation = "in" | "out" | "clock" | "counter";
export type Location = "n" | "e" | "s" | "w" | "ne" | "se" | "sw" | "nw";

export type GridPosition =
  | "alpha1"
  | "alpha2"
  | "alpha3"
  | "alpha4"
  | "alpha5"
  | "alpha6"
  | "alpha7"
  | "alpha8"
  | "beta1"
  | "beta2"
  | "beta3"
  | "beta4"
  | "beta5"
  | "beta6"
  | "beta7"
  | "beta8"
  | "gamma1"
  | "gamma2"
  | "gamma3"
  | "gamma4"
  | "gamma5"
  | "gamma6"
  | "gamma7"
  | "gamma8"
  | "gamma9"
  | "gamma10"
  | "gamma11"
  | "gamma12"
  | "gamma13"
  | "gamma14"
  | "gamma15"
  | "gamma16";

export type VTGMode = "SS" | "SO" | "TS" | "TO" | "QS" | "QO";
export type ElementalType = "water" | "fire" | "earth" | "air" | "sun" | "moon";
export type LetterType =
  | "Type1"
  | "Type2"
  | "Type3"
  | "Type4"
  | "Type5"
  | "Type6"
  | "Type7"
  | "Type8"
  | "Type9";
export type ArrowColor = "red" | "blue";
export type GridMode = "diamond" | "box";

// ==================== MOTION DATA ====================
// (from motion-data.json)

export interface MotionData {
  motionType: MotionType;
  propRotDir: RotationDirection;
  startLoc: Location;
  endLoc: Location;
  turns: number;
  startOri: Orientation;
  endOri: Orientation;
}

// ==================== GLYPH DATA ====================
// (from glyph-data.json)

export interface GlyphData {
  vtg_mode?: VTGMode | null;
  elemental_type?: ElementalType | null;
  letter_type?: LetterType | null;
  has_dash?: boolean;
  turns_data?: string | null;
  start_position?: string | null;
  end_position?: string | null;
  show_elemental?: boolean;
  show_vtg?: boolean;
  show_tka?: boolean;
  show_positions?: boolean;
}

// ==================== BEAT DATA ====================
// (from beat-data.json)

export interface BeatData {
  beatNumber: number;
  letter: string | null;
  duration?: number;
  blueMotion: MotionData | null;
  redMotion: MotionData | null;
  pictographData?: object | null;
  glyphData?: object | null;
  blueReversal?: boolean;
  redReversal?: boolean;
  filled?: boolean;
  tags?: string[];
  metadata?: {
    is_start_position?: boolean;
    [key: string]: any;
  } | null;
}

// ==================== SEQUENCE DATA ====================
// (from sequence-data.json)

export interface SequenceData {
  id: string;
  name: string;
  beats: BeatData[];
  createdAt?: string | null;
  updatedAt?: string | null;
  version?: string;
  length?: number;
  difficulty?: string | null;
  tags?: string[];
}

// ==================== VALIDATION HELPERS ====================

export function isValidMotionType(value: string): value is MotionType {
  return ["pro", "anti", "float", "dash", "static"].includes(value);
}

export function isValidLocation(value: string): value is Location {
  return ["n", "e", "s", "w", "ne", "se", "sw", "nw"].includes(value);
}

export function isValidGridPosition(value: string): value is GridPosition {
  return /^(alpha[1-8]|beta[1-8]|gamma(1[0-6]|[1-9]))$/.test(value);
}

// ==================== FACTORY FUNCTIONS ====================

export function createEmptyBeat(beatNumber: number): BeatData {
  return {
    beatNumber,
    letter: null,
    duration: 1.0,
    blueMotion: null,
    redMotion: null,
    blueReversal: false,
    redReversal: false,
    filled: false,
    tags: [],
    metadata: null,
  };
}

export function createEmptySequence(id: string, name: string): SequenceData {
  return {
    id,
    name,
    beats: [],
    version: "1.0",
    length: 8,
    tags: [],
  };
}
