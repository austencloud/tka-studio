/**
 * EnumConversionService - Centralized enum conversion utilities
 *
 * Handles all string <-> enum conversions with proper error handling
 * and consistent behavior across the motion tester.
 */

import {
  Orientation,
  MotionType,
  Location,
  RotationDirection,
} from "$lib/domain/enums";
import type { IEnumConversionService } from "./interfaces";

export class EnumConversionService implements IEnumConversionService {
  // String to enum conversions with proper error handling

  stringToOrientation(str: string): Orientation {
    const mapping: Record<string, Orientation> = {
      in: Orientation.IN,
      out: Orientation.OUT,
      clock: Orientation.CLOCK,
      counter: Orientation.COUNTER,
    };

    const normalized = str.toLowerCase().trim();
    return mapping[normalized] ?? Orientation.IN;
  }

  stringToMotionType(str: string): MotionType {
    const mapping: Record<string, MotionType> = {
      pro: MotionType.PRO,
      anti: MotionType.ANTI,
      static: MotionType.STATIC,
      dash: MotionType.DASH,
      fl: MotionType.FLOAT,
      float: MotionType.FLOAT,
    };

    const normalized = str.toLowerCase().trim();
    return mapping[normalized] ?? MotionType.PRO;
  }

  stringToLocation(str: string): Location {
    const mapping: Record<string, Location> = {
      n: Location.NORTH,
      e: Location.EAST,
      s: Location.SOUTH,
      w: Location.WEST,
      ne: Location.NORTHEAST,
      se: Location.SOUTHEAST,
      sw: Location.SOUTHWEST,
      nw: Location.NORTHWEST,

      // Full names for completeness
      north: Location.NORTH,
      east: Location.EAST,
      south: Location.SOUTH,
      west: Location.WEST,
      northeast: Location.NORTHEAST,
      southeast: Location.SOUTHEAST,
      southwest: Location.SOUTHWEST,
      northwest: Location.NORTHWEST,
    };

    const normalized = str.toLowerCase().trim();
    return mapping[normalized] ?? Location.NORTH;
  }

  stringToRotationDirection(str: string): RotationDirection {
    const mapping: Record<string, RotationDirection> = {
      cw: RotationDirection.CLOCKWISE,
      clockwise: RotationDirection.CLOCKWISE,
      ccw: RotationDirection.COUNTER_CLOCKWISE,
      counter_clockwise: RotationDirection.COUNTER_CLOCKWISE,
      counterclockwise: RotationDirection.COUNTER_CLOCKWISE,
      noRotation: RotationDirection.NO_ROTATION,
      noRotation: RotationDirection.NO_ROTATION,
    };

    const normalized = str.toLowerCase().trim();
    return mapping[normalized] ?? RotationDirection.CLOCKWISE;
  }

  // Enum to string conversions for display purposes

  orientationToString(orientation: Orientation): string {
    switch (orientation) {
      case Orientation.IN:
        return "in";
      case Orientation.OUT:
        return "out";
      case Orientation.CLOCK:
        return "clock";
      case Orientation.COUNTER:
        return "counter";
      default:
        return "in";
    }
  }

  motionTypeToString(motionType: MotionType): string {
    switch (motionType) {
      case MotionType.PRO:
        return "pro";
      case MotionType.ANTI:
        return "anti";
      case MotionType.STATIC:
        return "static";
      case MotionType.DASH:
        return "dash";
      case MotionType.FLOAT:
        return "float";
      default:
        return "pro";
    }
  }

  locationToString(location: Location): string {
    switch (location) {
      case Location.NORTH:
        return "n";
      case Location.EAST:
        return "e";
      case Location.SOUTH:
        return "s";
      case Location.WEST:
        return "w";
      case Location.NORTHEAST:
        return "ne";
      case Location.SOUTHEAST:
        return "se";
      case Location.SOUTHWEST:
        return "sw";
      case Location.NORTHWEST:
        return "nw";

      default:
        return "n";
    }
  }

  rotationDirectionToString(rotationDirection: RotationDirection): string {
    switch (rotationDirection) {
      case RotationDirection.CLOCKWISE:
        return "cw";
      case RotationDirection.COUNTER_CLOCKWISE:
        return "ccw";
      case RotationDirection.NO_ROTATION:
        return "noRotation";
      default:
        return "cw";
    }
  }
}
