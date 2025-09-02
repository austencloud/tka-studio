/**
 * Beta Detection Service Interface
 * 
 * Provides methods for detecting beta positions in pictographs.
 * Beta positions are specific dance positions that require special handling.
 */

import type { PictographData, Position } from "$domain";

export interface IBetaDetectionService {
  /**
   * Check if a position is a beta position
   */
  isBetaPosition(position: Position): boolean;

  /**
   * Check if a pictograph starts with beta (start position is a beta position)
   */
  startsWithBeta(pictographData: PictographData): boolean;

  /**
   * Check if a pictograph ends with beta (end position is a beta position)
   */
  endsWithBeta(pictographData: PictographData): boolean;
}
