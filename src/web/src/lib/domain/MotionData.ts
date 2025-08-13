/**
 * Motion Domain Models
 *
 * Immutable data structures for motion representation in TKA.
 * Handles prop and arrow motion data with type safety and serialization.
 * Based on modern desktop app's motion_data.py
 */

import { Location, MotionType, Orientation, RotationDirection } from "./enums";

export interface MotionData {
  readonly motion_type: MotionType;
  readonly prop_rot_dir: RotationDirection;
  readonly start_loc: Location;
  readonly end_loc: Location;
  readonly turns: number | "fl"; // Can be 'fl' for float motions
  readonly start_ori: Orientation;
  readonly end_ori: Orientation;
  readonly is_visible: boolean;

  // Prefloat attributes for letter determination
  readonly prefloat_motion_type?: MotionType | null;
  readonly prefloat_prop_rot_dir?: RotationDirection | null;
}

export function createMotionData(data: Partial<MotionData> = {}): MotionData {
  return {
    motion_type: data.motion_type ?? MotionType.STATIC,
    prop_rot_dir: data.prop_rot_dir ?? RotationDirection.NO_ROTATION,
    start_loc: data.start_loc ?? Location.NORTH,
    end_loc: data.end_loc ?? Location.NORTH,
    turns: data.turns ?? 0.0,
    start_ori: data.start_ori ?? Orientation.IN,
    end_ori: data.end_ori ?? Orientation.IN,
    is_visible: data.is_visible ?? true,
    prefloat_motion_type: data.prefloat_motion_type ?? null,
    prefloat_prop_rot_dir: data.prefloat_prop_rot_dir ?? null,
  };
}

export function updateMotionData(
  motion: MotionData,
  updates: Partial<MotionData>,
): MotionData {
  return {
    ...motion,
    ...updates,
  };
}

export function isValidMotion(motion: MotionData): boolean {
  // Handle 'fl' turns for float motions
  if (
    motion.turns !== "fl" &&
    typeof motion.turns === "number" &&
    motion.turns < 0
  ) {
    return false;
  }
  return true;
}

export function isFloatMotion(motion: MotionData): boolean {
  return motion.motion_type === MotionType.FLOAT;
}

export function hasPrefloatData(motion: MotionData): boolean {
  return (
    motion.prefloat_motion_type != null || motion.prefloat_prop_rot_dir != null
  );
}

export function motionDataToObject(
  motion: MotionData,
): Record<string, unknown> {
  return {
    motion_type: motion.motion_type,
    prop_rot_dir: motion.prop_rot_dir,
    start_loc: motion.start_loc,
    end_loc: motion.end_loc,
    turns: motion.turns,
    start_ori: motion.start_ori,
    end_ori: motion.end_ori,
    is_visible: motion.is_visible,
    prefloat_motion_type: motion.prefloat_motion_type,
    prefloat_prop_rot_dir: motion.prefloat_prop_rot_dir,
  };
}

export function motionDataFromObject(
  data: Record<string, unknown>,
): MotionData {
  const partialData: Record<string, unknown> = {};

  if (data.motion_type !== undefined) {
    partialData.motion_type = data.motion_type;
  }
  if (data.prop_rot_dir !== undefined) {
    partialData.prop_rot_dir = data.prop_rot_dir;
  }
  if (data.start_loc !== undefined) {
    partialData.start_loc = data.start_loc;
  }
  if (data.end_loc !== undefined) {
    partialData.end_loc = data.end_loc;
  }
  if (data.turns !== undefined) {
    partialData.turns = data.turns;
  }
  if (data.start_ori !== undefined) {
    partialData.start_ori = data.start_ori;
  }
  if (data.end_ori !== undefined) {
    partialData.end_ori = data.end_ori;
  }
  if (data.is_visible !== undefined) {
    partialData.is_visible = data.is_visible;
  }
  if (data.prefloat_motion_type !== undefined) {
    partialData.prefloat_motion_type = data.prefloat_motion_type;
  }
  if (data.prefloat_prop_rot_dir !== undefined) {
    partialData.prefloat_prop_rot_dir = data.prefloat_prop_rot_dir;
  }

  return createMotionData(partialData);
}
