/**
 * Beta Detection Service Implementation
 *
 * Provides methods for detecting beta positions in pictographs.
 * Migrated from utils/betaDetection.ts to proper service architecture.
 */

import type { IBetaDetectionService, IGridPositionDeriver } from "$contracts";
import type { PictographData, Position } from "$domain";
import { TYPES } from "$inversify/types";
import { inject, injectable } from "inversify";

@injectable()
export class BetaDetectionService implements IBetaDetectionService {
  constructor(
    @inject(TYPES.IPositionMapper) private positionMapper: IGridPositionDeriver
  ) {}

  /**
   * Check if a position is a beta position
   * Beta positions are: 1, 3, 5, 7, 9, 11, 13, 15
   */
  isBetaPosition(position: Position): boolean {
    const betaPositions = [1, 3, 5, 7, 9, 11, 13, 15];
    return betaPositions.includes(position);
  }

  /**
   * Check if a pictograph starts with beta (start position is a beta position)
   */
  startsWithBeta(pictographData: PictographData): boolean {
    if (!pictographData.motions?.blue || !pictographData.motions?.red) {
      return false;
    }

    const startPosition = this.positionMapper.getPositionFromLocations(
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
