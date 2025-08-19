/**
 * EnumMappingService - Centralized enum mapping utilities
 *
 * Provides consistent string-to-enum conversion functions used across
 * all data services. Eliminates duplication of mapping logic.
 */

import {
  MotionType,
  Location,
  Orientation,
  RotationDirection,
  GridPosition,
} from "$lib/domain/enums";

export interface IEnumMappingService {
  mapMotionType(motionType: string): MotionType;
  mapLocation(location: string): Location;
  mapOrientation(orientation: string): Orientation;
  mapRotationDirection(rotationDirection: string): RotationDirection;
  convertToGridPosition(
    positionString: string | null | undefined
  ): GridPosition | null;
  getLetterType(letter: string): string;
}

export class EnumMappingService implements IEnumMappingService {
  /**
   * Map string motion type to MotionType enum
   */
  mapMotionType(motionType: string): MotionType {
    if (!motionType) return MotionType.STATIC;

    switch (motionType.toLowerCase().trim()) {
      case "pro":
        return MotionType.PRO;
      case "anti":
        return MotionType.ANTI;
      case "float":
        return MotionType.FLOAT;
      case "dash":
        return MotionType.DASH;
      case "static":
        return MotionType.STATIC;
      default:
        console.warn(
          `⚠️ mapMotionType: unknown motion type "${motionType}", defaulting to STATIC`
        );
        return MotionType.STATIC;
    }
  }

  /**
   * Map string location to Location enum
   */
  mapLocation(location: string): Location {
    if (!location) {
      console.warn(
        `⚠️ mapLocation: location is null/undefined, defaulting to NORTH`
      );
      return Location.NORTH;
    }

    switch (location.toLowerCase().trim()) {
      case "n":
        return Location.NORTH;
      case "e":
        return Location.EAST;
      case "s":
        return Location.SOUTH;
      case "w":
        return Location.WEST;
      case "ne":
        return Location.NORTHEAST;
      case "se":
        return Location.SOUTHEAST;
      case "sw":
        return Location.SOUTHWEST;
      case "nw":
        return Location.NORTHWEST;
      default:
        console.warn(
          `⚠️ mapLocation: unknown location "${location}", defaulting to NORTH`
        );
        return Location.NORTH;
    }
  }

  /**
   * Map string orientation to Orientation enum
   */
  mapOrientation(orientation: string): Orientation {
    if (!orientation) return Orientation.IN;

    switch (orientation.toLowerCase().trim()) {
      case "in":
        return Orientation.IN;
      case "out":
        return Orientation.OUT;
      case "clock":
        return Orientation.CLOCK;
      case "counter":
        return Orientation.COUNTER;
      default:
        console.warn(
          `⚠️ mapOrientation: unknown orientation "${orientation}", defaulting to IN`
        );
        return Orientation.IN;
    }
  }

  /**
   * Map string rotation direction to RotationDirection enum
   */
  mapRotationDirection(rotationDirection: string): RotationDirection {
    if (!rotationDirection) return RotationDirection.NO_ROTATION;

    switch (rotationDirection.toLowerCase().trim()) {
      case "cw":
        return RotationDirection.CLOCKWISE;
      case "ccw":
        return RotationDirection.COUNTER_CLOCKWISE;
      case "noRotation":
        return RotationDirection.NO_ROTATION;
      default:
        console.warn(
          `⚠️ mapRotationDirection: unknown rotation direction "${rotationDirection}", defaulting to NO_ROTATION`
        );
        return RotationDirection.NO_ROTATION;
    }
  }

  /**
   * Convert string position to GridPosition enum
   */
  convertToGridPosition(
    positionString: string | null | undefined
  ): GridPosition | null {
    if (!positionString) return null;

    const lowerPosition = positionString.toLowerCase().trim();
    const gridPositionValues = Object.values(GridPosition);

    for (const position of gridPositionValues) {
      if (position.toLowerCase() === lowerPosition) {
        return position as GridPosition;
      }
    }

    console.warn(
      `⚠️ convertToGridPosition: unknown position "${positionString}", returning null`
    );
    return null;
  }

  /**
   * Get letter type classification for TKA kinetic alphabet
   * Based on the 47-letter system across 6 types
   */
  getLetterType(letter: string): string {
    if (!letter) return "Unknown";

    // Type 1: Dual-Shift (A-V, 22 letters)
    const type1Letters = [
      "A",
      "B",
      "C",
      "D",
      "E",
      "F",
      "G",
      "H",
      "I",
      "J",
      "K",
      "L",
      "M",
      "N",
      "O",
      "P",
      "Q",
      "R",
      "S",
      "T",
      "U",
      "V",
    ];

    // Type 2: Shift (8 letters including Greek)
    const type2Letters = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"];

    // Type 3: Cross-Shift (8 cross variants)
    const type3Letters = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"];

    // Type 4: Dash (3 Greek dash letters)
    const type4Letters = ["Φ", "Ψ", "Λ"];

    // Type 5: Dual-Dash (3 dual dash variants)
    const type5Letters = ["Φ-", "Ψ-", "Λ-"];

    // Type 6: Static (3 static Greek letters)
    const type6Letters = ["α", "β", "Γ"];

    if (type1Letters.includes(letter)) return "Dual-Shift";
    if (type2Letters.includes(letter)) return "Shift";
    if (type3Letters.includes(letter)) return "Cross-Shift";
    if (type4Letters.includes(letter)) return "Dash";
    if (type5Letters.includes(letter)) return "Dual-Dash";
    if (type6Letters.includes(letter)) return "Static";

    console.warn(
      `⚠️ getLetterType: unknown letter "${letter}", returning Unknown`
    );
    return "Unknown";
  }

  /**
   * Normalize motion type for comparison (used in CSV matching)
   */
  normalizeMotionType(motionType: string): string {
    return motionType.toLowerCase().trim();
  }

  /**
   * Normalize location for comparison (used in CSV matching)
   */
  normalizeLocation(location: string): string {
    return location.toLowerCase().trim();
  }

  /**
   * Handle "fl" (float) turns conversion
   */
  normalizeTurns(turns: number | string): number {
    return turns === "fl" ? 0.5 : Number(turns) || 0;
  }
}
