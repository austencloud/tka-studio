/**
 * Hand Path Direction Detector Contract
 *
 * Determines the rotational direction of hand movement around the grid.
 * Critical for distinguishing PRO vs ANTI motions when rotation is applied.
 */

import type {
  GridLocation,
  GridMode,
  HandMotionType,
  RotationDirection,
} from "$shared";

export interface IHandPathDirectionDetector {
  /**
   * Determine if hand movement is clockwise or counter-clockwise around the grid
   *
   * Diamond: N → E → S → W → N (clockwise)
   * Box: NE → SE → SW → NW → NE (clockwise)
   *
   * @param start Starting grid location
   * @param end Ending grid location
   * @param gridMode Current grid mode
   * @returns CW, CCW, or null if no rotational direction (dash/static)
   */
  getHandPathDirection(
    start: GridLocation,
    end: GridLocation,
    gridMode: GridMode
  ): RotationDirection | null;

  /**
   * Determine the hand motion type based on start/end positions
   *
   * @param start Starting grid location
   * @param end Ending grid location
   * @param gridMode Current grid mode
   * @returns SHIFT, DASH, or STATIC
   */
  getHandMotionType(
    start: GridLocation,
    end: GridLocation,
    gridMode: GridMode
  ): HandMotionType;

  /**
   * Check if movement is a dash (opposite points)
   *
   * @param start Starting grid location
   * @param end Ending grid location
   * @param gridMode Current grid mode
   * @returns True if dash movement
   */
  isDash(start: GridLocation, end: GridLocation, gridMode: GridMode): boolean;

  /**
   * Check if movement is static (same position)
   *
   * @param start Starting grid location
   * @param end Ending grid location
   * @returns True if no movement
   */
  isStatic(start: GridLocation, end: GridLocation): boolean;

  /**
   * Check if movement is a valid shift (adjacent position)
   *
   * @param start Starting grid location
   * @param end Ending grid location
   * @param gridMode Current grid mode
   * @returns True if valid shift
   */
  isShift(start: GridLocation, end: GridLocation, gridMode: GridMode): boolean;
}
