/**
 * Core Domain Enums
 *
 * All enumeration types used throughout the TKA domain models.
 * Centralized location for type-safe constants and values.
 * Based on modern desktop app's enums.py
 */

export enum VTGTiming {
  TOG = "tog",
  SPLIT = "split",
  QUARTER = "quarter",
  NONE = "none",
}

export enum VTGDirection {
  SAME = "same",
  OPP = "opp",
  NONE = "none",
}

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

export enum MotionColor {
  BLUE = "blue",
  RED = "red",
}

export enum RotationDirection {
  CLOCKWISE = "cw",
  COUNTER_CLOCKWISE = "ccw",
  NO_ROTATION = "noRotation",
}

export enum Orientation {
  IN = "in",
  OUT = "out",
  CLOCK = "clock",
  COUNTER = "counter",
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
}



export enum GlyphType {
  TKA = "tka",
  REVERSALS = "reversals",
  VTG = "vtg",
  ELEMENTAL = "elemental",
  POSITIONS = "positions",
}

