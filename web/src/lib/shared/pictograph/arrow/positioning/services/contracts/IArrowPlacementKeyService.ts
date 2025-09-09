/**
 * Arrow Placement Key Service Contract
 *
 * Generates placement keys for arrow positioning lookups.
 * Simplified version of the desktop PlacementKeyGenerator logic.
 */

import { MotionType, type MotionData, type PictographData } from "$shared";

export interface IArrowPlacementKeyService {
  generatePlacementKey(
    motionData: MotionData,
    pictographData: PictographData,
    availableKeys: string[]
  ): string;

  generateBasicKey(motionType: MotionType): string;
}
