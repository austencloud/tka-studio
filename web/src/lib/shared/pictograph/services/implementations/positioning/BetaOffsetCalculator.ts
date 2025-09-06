/**
 * Beta Offset Calculator
 *
 * Converts direction values to pixel offsets for beta prop positioning.
 * Based on legacy beta offset calculation logic.
 */

import type { IBetaOffsetCalculator } from "$shared/pictograph/services/contracts/positioning-interfaces";
import { Point } from "fabric";
import { injectable } from "inversify";
import {
  DOWN,
  DOWNLEFT,
  DOWNRIGHT,
  LEFT,
  RIGHT,
  UP,
  UPLEFT,
  UPRIGHT,
  type Direction,
} from "./BetaPropDirectionCalculator";

@injectable()
export class BetaOffsetCalculator implements IBetaOffsetCalculator {
  // Standard offset distance (matches legacy 25 pixel separation)
  private readonly OFFSET_DISTANCE = 25;

  /**
   * Calculate new position with offset based on direction
   */
  calculateNewPointWithOffset(
    currentPoint: Point,
    direction: Direction
  ): Point {
    const offset = this.getOffsetForDirection(direction);

    return new Point(currentPoint.x + offset.x, currentPoint.y + offset.y);
  }

  /**
   * Get pixel offset for a given direction
   */
  private getOffsetForDirection(direction: Direction): Point {
    const distance = this.OFFSET_DISTANCE;

    switch (direction) {
      case UP:
        return new Point(0, -distance);
      case DOWN:
        return new Point(0, distance);
      case LEFT:
        return new Point(-distance, 0);
      case RIGHT:
        return new Point(distance, 0);
      case UPRIGHT:
        return new Point(distance, -distance);
      case DOWNRIGHT:
        return new Point(distance, distance);
      case UPLEFT:
        return new Point(-distance, -distance);
      case DOWNLEFT:
        return new Point(-distance, distance);
      default:
        console.warn(`Unknown direction: ${direction}`);
        return new Point(0, 0);
    }
  }

  /**
   * Calculate beta separation offsets for both props
   * Returns offsets for blue and red props based on their calculated directions
   */
  calculateBetaSeparationOffsets(
    blueDirection: Direction | null,
    redDirection: Direction | null
  ): { blue: Point; red: Point } {
    const blueOffset = blueDirection
      ? this.getOffsetForDirection(blueDirection)
      : new Point(0, 0);

    const redOffset = redDirection
      ? this.getOffsetForDirection(redDirection)
      : new Point(0, 0);

    return {
      blue: blueOffset,
      red: redOffset,
    };
  }
}
