/**
 * Beta Offset Calculator
 *
 * Converts direction values to pixel offsets for beta prop positioning.
 * Based on legacy beta offset calculation logic.
 */

import type { Direction } from "./BetaPropDirectionCalculator";
import {
  UP,
  DOWN,
  LEFT,
  RIGHT,
  UPRIGHT,
  DOWNRIGHT,
  UPLEFT,
  DOWNLEFT,
} from "./BetaPropDirectionCalculator";

export interface Position {
  x: number;
  y: number;
}

export class BetaOffsetCalculator {
  // Standard offset distance (matches legacy 25 pixel separation)
  private readonly OFFSET_DISTANCE = 25;

  /**
   * Calculate new position with offset based on direction
   */
  calculateNewPositionWithOffset(
    currentPosition: Position,
    direction: Direction,
  ): Position {
    const offset = this.getOffsetForDirection(direction);

    return {
      x: currentPosition.x + offset.x,
      y: currentPosition.y + offset.y,
    };
  }

  /**
   * Get pixel offset for a given direction
   */
  private getOffsetForDirection(direction: Direction): Position {
    const distance = this.OFFSET_DISTANCE;

    switch (direction) {
      case UP:
        return { x: 0, y: -distance };
      case DOWN:
        return { x: 0, y: distance };
      case LEFT:
        return { x: -distance, y: 0 };
      case RIGHT:
        return { x: distance, y: 0 };
      case UPRIGHT:
        return { x: distance, y: -distance };
      case DOWNRIGHT:
        return { x: distance, y: distance };
      case UPLEFT:
        return { x: -distance, y: -distance };
      case DOWNLEFT:
        return { x: -distance, y: distance };
      default:
        console.warn(`Unknown direction: ${direction}`);
        return { x: 0, y: 0 };
    }
  }

  /**
   * Calculate beta separation offsets for both props
   * Returns offsets for blue and red props based on their calculated directions
   */
  calculateBetaSeparationOffsets(
    blueDirection: Direction | null,
    redDirection: Direction | null,
  ): { blue: Position; red: Position } {
    const blueOffset = blueDirection
      ? this.getOffsetForDirection(blueDirection)
      : { x: 0, y: 0 };

    const redOffset = redDirection
      ? this.getOffsetForDirection(redDirection)
      : { x: 0, y: 0 };

    return {
      blue: blueOffset,
      red: redOffset,
    };
  }
}
