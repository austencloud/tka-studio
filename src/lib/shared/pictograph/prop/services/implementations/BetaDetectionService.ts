/**
 * Beta Detection Service Implementation
 *
 * Provides methods for detecting beta positions in pictographs.
 * Migrated from utils/betaDetection.ts to proper service architecture.
 */

import type { IGridPositionDeriver } from "$shared";
import type {
  GridPosition,
  IBetaDetectionService,
  PictographData,
} from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";

@injectable()
export class BetaDetectionService implements IBetaDetectionService {
  constructor(
    @inject(TYPES.IGridPositionDeriver)
    private positionMapper: IGridPositionDeriver
  ) {}

  /**
   * Check if a grid position is a beta position
   * Beta positions are the BETA enum values
   */
  isBetaPosition(position: GridPosition): boolean {
    return position.toString().startsWith("beta");
  }

  /**
   * Check if a pictograph starts with beta (start position is a beta position)
   */
  startsWithBeta(pictographData: PictographData): boolean {
    if (!pictographData.motions.blue || !pictographData.motions.red) {
      return false;
    }

    const startPosition = this.positionMapper.getGridPositionFromLocations(
      pictographData.motions.blue.startLocation,
      pictographData.motions.red.startLocation
    );

    return this.isBetaPosition(startPosition);
  }

  /**
   * Check if a pictograph ends with beta (end position is a beta position)
   */
  endsWithBeta(pictographData: PictographData): boolean {
    if (!pictographData.motions.blue || !pictographData.motions.red) {
      // No motion data = can't end with beta position
      // This is expected in some contexts (static pictographs, loading states)
      return false;
    }

    const redEndLocation = pictographData.motions.red.endLocation;
    const blueEndLocation = pictographData.motions.blue.endLocation;

    // Beta detection: both props end at the same location
    return redEndLocation === blueEndLocation;
  }
}
