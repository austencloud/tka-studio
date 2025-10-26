/**
 * Position Analysis Service Contract
 *
 * Handles analysis of position data for end position calculations and grouping.
 * Extracted from OptionPickerService for better separation of concerns.
 */

import type { PictographData } from "$shared";
import { GridPosition, GridPositionGroup } from "$shared";

export interface IPositionAnalyzer {
  /**
   * Get the position group (Alpha, Beta, Gamma) from a GridPosition
   */
  getEndPositionGroup(endPosition: GridPosition | null | undefined): GridPositionGroup | null;

  /**
   * Calculate end position from motion data
   */
  getEndPosition(pictographData: PictographData): string | null;
}
