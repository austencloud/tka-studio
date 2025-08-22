/**
 * IGridModeDerivationService - Interface for grid mode determination
 */

import type { GridMode } from "../../../domain/enums";
import type { MotionData } from "../../../domain/MotionData";

export interface IGridModeDerivationService {
  /**
   * Determine grid mode from motion start/end locations
   * Cardinal locations (N, E, S, W) = DIAMOND mode
   * Intercardinal locations (NE, SE, SW, NW) = BOX mode
   */
  deriveGridMode(blueMotion: MotionData, redMotion: MotionData): GridMode;

  /**
   * Check if motion uses cardinal locations
   */
  usesCardinalLocations(motion: MotionData): boolean;

  /**
   * Check if motion uses intercardinal locations
   */
  usesIntercardinalLocations(motion: MotionData): boolean;
}
