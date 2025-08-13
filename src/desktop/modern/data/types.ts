/**
 * Shared type definitions for TKA applications.
 * Core enums that ensure consistency between desktop and web applications.
 */

export enum MotionType {
  PRO = "pro",
  ANTI = "anti",
  FLOAT = "float",
  DASH = "dash",
  STATIC = "static",
}

export enum RotationDirection {
  CLOCKWISE = "cw",
  COUNTER_CLOCKWISE = "ccw",
  NO_ROTATION = "no_rot",
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

export enum PropType {
  STAFF = "staff",
  CLUB = "club",
  BUUGENG = "buugeng",
  FAN = "fan",
  TRIAD = "triad",
  MINIHOOP = "minihoop",
  BIGBALL = "bigball",
  FRACTALS = "fractals",
}

export enum Color {
  BLUE = "blue",
  RED = "red",
}
