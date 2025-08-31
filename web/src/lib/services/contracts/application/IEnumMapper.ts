/**
 * Enum Mapping Service Interface
 *
 * Interface for centralized enum mapping utilities.
 * Handles conversion between string values and domain enums.
 */

import type {
  GridPosition,
  Location,
  MotionType,
  Orientation,
  RotationDirection,
} from "$domain";

export interface IEnumMapper {
  mapMotionType(motionType: string): MotionType;
  mapLocation(location: string): Location;
  mapOrientation(orientation: string): Orientation;
  mapRotationDirection(rotationDirection: string): RotationDirection;
  convertToGridPosition(
    positionString: string | null | undefined
  ): GridPosition | null;
  normalizeMotionType(motionType: string): string;
  normalizeLocation(location: string): string;
  normalizeTurns(turns: number | string): number;
}
