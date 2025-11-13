/**
 * Swipe Detection Service Contract
 *
 * Handles touch/pointer gesture recognition for hand path drawing.
 * Converts raw pointer events into semantic swipe gestures between grid positions.
 */

import type { GridLocation, GridMode } from "$shared";
import type { GridPositionPoint, SwipeGesture } from "../../domain";

export interface ISwipeDetectionService {
  /**
   * Find the closest grid position to screen coordinates
   *
   * @param x Screen X coordinate
   * @param y Screen Y coordinate
   * @param gridPositions Available grid positions with coordinates
   * @returns Closest grid location
   */
  findClosestGridPosition(
    x: number,
    y: number,
    gridPositions: readonly GridPositionPoint[]
  ): GridLocation | null;

  /**
   * Detect if pointer has moved significantly from start position
   *
   * @param startX Starting X coordinate
   * @param startY Starting Y coordinate
   * @param currentX Current X coordinate
   * @param currentY Current Y coordinate
   * @param threshold Movement threshold in pixels
   * @returns True if moved beyond threshold
   */
  hasMovedSignificantly(
    startX: number,
    startY: number,
    currentX: number,
    currentY: number,
    threshold: number
  ): boolean;

  /**
   * Calculate velocity of swipe gesture
   *
   * @param startX Starting X coordinate
   * @param startY Starting Y coordinate
   * @param endX Ending X coordinate
   * @param endY Ending Y coordinate
   * @param durationMs Duration in milliseconds
   * @returns Velocity in pixels per millisecond
   */
  calculateVelocity(
    startX: number,
    startY: number,
    endX: number,
    endY: number,
    durationMs: number
  ): number;

  /**
   * Build a complete swipe gesture from tracking data
   *
   * @param startLocation Starting grid location
   * @param endLocation Ending grid location
   * @param velocity Swipe velocity
   * @param duration Swipe duration
   * @param gridMode Current grid mode
   * @returns Complete swipe gesture with motion type
   */
  buildSwipeGesture(
    startLocation: GridLocation,
    endLocation: GridLocation,
    velocity: number,
    duration: number,
    gridMode: GridMode
  ): SwipeGesture;
}
