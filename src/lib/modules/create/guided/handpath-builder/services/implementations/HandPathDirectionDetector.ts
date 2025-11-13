/**
 * Hand Path Direction Detector Implementation
 *
 * Analyzes hand movement patterns to determine rotational direction and motion types.
 * Key for converting hand paths to proper MotionType (PRO/ANTI/FLOAT).
 */

import {
  GridLocation,
  GridMode,
  HandMotionType,
  RotationDirection,
} from "$shared";
import { injectable } from "inversify";
import type { IHandPathDirectionDetector } from "../contracts/IHandPathDirectionDetector";

@injectable()
export class HandPathDirectionDetector implements IHandPathDirectionDetector {
  // Clockwise progression for each grid mode
  private readonly diamondClockwise = [
    GridLocation.NORTH,
    GridLocation.EAST,
    GridLocation.SOUTH,
    GridLocation.WEST,
  ];

  private readonly boxClockwise = [
    GridLocation.NORTHEAST,
    GridLocation.SOUTHEAST,
    GridLocation.SOUTHWEST,
    GridLocation.NORTHWEST,
  ];

  getHandPathDirection(
    start: GridLocation,
    end: GridLocation,
    gridMode: GridMode
  ): RotationDirection | null {
    // No direction for static motions
    if (this.isStatic(start, end)) {
      return null;
    }

    // No rotational direction for dash motions
    if (this.isDash(start, end, gridMode)) {
      return null;
    }

    // Get clockwise order based on grid mode
    const clockwiseOrder =
      gridMode === GridMode.DIAMOND ? this.diamondClockwise : this.boxClockwise;

    const startIdx = clockwiseOrder.indexOf(start);
    const endIdx = clockwiseOrder.indexOf(end);

    // Invalid positions
    if (startIdx === -1 || endIdx === -1) {
      return null;
    }

    // Check if movement follows clockwise pattern
    const isClockwise = (startIdx + 1) % 4 === endIdx;

    return isClockwise
      ? RotationDirection.CLOCKWISE
      : RotationDirection.COUNTER_CLOCKWISE;
  }

  getHandMotionType(
    start: GridLocation,
    end: GridLocation,
    gridMode: GridMode
  ): HandMotionType {
    if (this.isStatic(start, end)) {
      return HandMotionType.STATIC;
    }

    if (this.isDash(start, end, gridMode)) {
      return HandMotionType.DASH;
    }

    // Everything else is a shift
    return HandMotionType.SHIFT;
  }

  isDash(start: GridLocation, end: GridLocation, gridMode: GridMode): boolean {
    // Dash = opposite points on the grid
    const diamondOpposites: Record<string, GridLocation> = {
      [GridLocation.NORTH]: GridLocation.SOUTH,
      [GridLocation.SOUTH]: GridLocation.NORTH,
      [GridLocation.EAST]: GridLocation.WEST,
      [GridLocation.WEST]: GridLocation.EAST,
    };

    const boxOpposites: Record<string, GridLocation> = {
      [GridLocation.NORTHEAST]: GridLocation.SOUTHWEST,
      [GridLocation.SOUTHWEST]: GridLocation.NORTHEAST,
      [GridLocation.SOUTHEAST]: GridLocation.NORTHWEST,
      [GridLocation.NORTHWEST]: GridLocation.SOUTHEAST,
    };

    const opposites =
      gridMode === GridMode.DIAMOND ? diamondOpposites : boxOpposites;

    return opposites[start] === end;
  }

  isStatic(start: GridLocation, end: GridLocation): boolean {
    return start === end;
  }

  isShift(start: GridLocation, end: GridLocation, gridMode: GridMode): boolean {
    // Not static, not dash = shift
    return !this.isStatic(start, end) && !this.isDash(start, end, gridMode);
  }
}
