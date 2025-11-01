/**
 * Keyboard Arrow Adjustment Service Contract
 *
 * Handles manual arrow position adjustments via WASD keyboard controls.
 * Applies adjustments to beat data and updates the pictograph.
 */

import type { BeatData } from "$shared";

export interface IKeyboardArrowAdjustmentService {
  /**
   * Handle WASD movement for the currently selected arrow
   * @param key - The WASD key pressed
   * @param increment - The pixel increment to move (5, 20, or 200)
   * @param selectedArrow - The currently selected arrow data
   * @param beatData - The beat data to update
   * @returns Updated beat data with arrow adjustment applied
   */
  handleWASDMovement(
    key: 'w' | 'a' | 's' | 'd',
    increment: number,
    selectedArrow: { motionData: any; color: string; pictographData: any },
    beatData: BeatData
  ): BeatData;

  /**
   * Calculate adjustment vector based on key direction
   * @param key - The WASD key pressed
   * @param increment - The pixel increment
   * @returns Adjustment coordinates {x, y}
   */
  calculateAdjustment(key: 'w' | 'a' | 's' | 'd', increment: number): { x: number; y: number };
}
