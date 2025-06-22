/**
 * Shared type definitions for TKA applications.
 * These types ensure consistency between desktop and web applications.
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

export interface SharedSequenceType {
  id: string;
  name: string;
  word: string;
  beats: any[];
  length: number;
  total_duration: number;
  start_position?: string;
  metadata?: Record<string, any>;
}

export interface SharedBeatType {
  id: string;
  beat_number: number;
  letter?: string;
  duration: number;
  blue_motion?: any;
  red_motion?: any;
  metadata?: Record<string, any>;
}

export interface SharedMotionType {
  motion_type: MotionType;
  prop_type: PropType;
  color: Color;
  start_location: Location;
  end_location: Location;
  rotation_direction: RotationDirection;
  turns?: number;
  metadata?: Record<string, any>;
}

export interface SharedSettingsType {
  background_type: string;
  theme: string;
  window_geometry?: {
    width: number;
    height: number;
    x: number;
    y: number;
  };
  last_sequence_id?: string;
  metadata?: Record<string, any>;
}

// API Response types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface HealthCheckResponse {
  status: "healthy" | "unhealthy";
  timestamp: string;
  version: string;
}

// Export all types for easy importing
export type {
  SharedSequenceType as SequenceType,
  SharedBeatType as BeatType,
  SharedMotionType as MotionTypeData,
  SharedSettingsType as SettingsType,
};
