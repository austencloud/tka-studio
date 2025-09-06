/**
 * Beta Detection Service Implementation
 *
 * Provides methods for detecting beta positions in pictographs.
 * Migrated from utils/betaDetection.ts to proper service architecture.
 */

import type { GridPosition, PictographData } from "$shared/domain";
import { TYPES } from "$shared/inversify";
import type { IBetaDetectionService } from "$shared/pictograph/services/contracts/IBetaDetectionService";
import type { IGridPositionDeriver } from "$shared/pictograph/services/contracts/positioning-interfaces";
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
    if (!pictographData.motions?.blue || !pictographData.motions?.red) {
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
    if (!pictographData.motions?.blue || !pictographData.motions?.red) {
      console.warn(
        "⚠️ PictographData missing motion data for position calculation"
      );
      return false;
    }

    const redEndLocation = pictographData.motions.red.endLocation;
    const blueEndLocation = pictographData.motions.blue.endLocation;

    // Beta detection: both props end at the same location
    return redEndLocation === blueEndLocation;
  }
}
