/**
 * Beta Detection Utilities
 *
 * Functions to detect beta conditions based on GridPosition enum values
 */

import type { PictographData } from "$domain";
import { GridPosition } from "$domain";
import type { IPositionMapper } from "$lib/services/contracts/positioning-interfaces";
import { resolve, TYPES } from "$lib/services/inversify/container";

/**
 * Check if a grid position is a beta position
 */
export function isBetaPosition(position: string | GridPosition): boolean {
  const positionStr =
    typeof position === "string" ? position : String(position);
  return positionStr.toLowerCase().startsWith("beta");
}

/**
 * Check if a pictograph ends with beta (end position is a beta position)
 *
 * Computes end position from motion data using PositionMapper
 */
export function endsWithBeta(pictographData: PictographData): boolean {
  const positionService = resolve<IPositionMapper>(TYPES.IPositionMapper);

  if (!pictographData.motions?.blue || !pictographData.motions?.red) {
    console.warn(
      "⚠️ PictographData missing motion data for position calculation"
    );
    return false;
  }

  const endPosition = positionService.getPositionFromLocations(
    pictographData.motions.blue.endLocation,
    pictographData.motions.red.endLocation
  );

  return isBetaPosition(endPosition);
}

/**
 * Check if a pictograph starts with beta (start position is a beta position)
 *
 * Computes start position from motion data using PositionMapper
 */
export function startsWithBeta(pictographData: PictographData): boolean {
  const positionService = resolve<IPositionMapper>(TYPES.IPositionMapper);

  if (!pictographData.motions?.blue || !pictographData.motions?.red) {
    return false;
  }

  const startPosition = positionService.getPositionFromLocations(
    pictographData.motions.blue.startLocation,
    pictographData.motions.red.startLocation
  );

  return isBetaPosition(startPosition);
}

/**
 * Get all beta positions from the GridPosition enum
 */
export function getAllBetaPositions(): GridPosition[] {
  return Object.values(GridPosition).filter((position) =>
    isBetaPosition(position)
  );
}
