/**
 * Core Domain Enums
 *
 * All enumeration types used throughout the TKA domain models.
 * Centralized location for type-safe constants and values.
 * Based on modern desktop app's enums.py
 */

export enum Timing {
  TOG = "tog",
  SPLIT = "split",
}

export enum Direction {
  SAME = "same",
  OPP = "opp",
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

export enum RotationDirection {
  CLOCKWISE = "cw",
  COUNTER_CLOCKWISE = "ccw",
  NO_ROTATION = "no_rot",
}

export enum PropRotationDirection {
  CLOCKWISE = "clockwise",
  COUNTER_CLOCKWISE = "counter_clockwise",
  NO_ROT = "no_rot",
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

  // Beta positions (box)
  BETA1 = "beta1",
  BETA2 = "beta2",
  BETA3 = "beta3",
  BETA4 = "beta4",
  BETA5 = "beta5",
  BETA6 = "beta6",
  BETA7 = "beta7",
  BETA8 = "beta8",

  // Gamma positions (diamond)
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

export enum GridMode {
  DIAMOND = "diamond",
  BOX = "box",
}

export enum ArrowType {
  BLUE = "blue",
  RED = "red",
}

export enum PropType {
  STAFF = "staff",
  CLUB = "club",
  HOOP = "hoop",
  BUUGENG = "buugeng",
  FAN = "fan",
  TRIAD = "triad",
  FRACTALS = "fractals",
  MINIHOOP = "minihoop",
  BIGBALL = "bigball",
  CRYSTAL = "crystal",
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

export enum LetterType {
  TYPE1 = "Type1",
  TYPE2 = "Type2",
  TYPE3 = "Type3",
  TYPE4 = "Type4",
  TYPE5 = "Type5",
  TYPE6 = "Type6",
}
