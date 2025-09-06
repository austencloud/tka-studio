/**
 * Position Mapping Service - Correct position mapping based on hand combinations
 *
 * Maps between position names (alpha4, beta2, etc.) and hand location pairs.
 * A position represents the combination of (blue_hand_location, red_hand_location).
 */

import { injectable } from "inversify";
import { GridLocation, GridPosition } from "../../../../../domain/enums";
// import type { IGridPositionDeriver } from "../../../contracts";

// Temporary interface definition
interface IGridPositionDeriver {
  deriveGridPosition(data: any): any;
}

@injectable()
export class GridPositionDeriver implements IGridPositionDeriver {
  // Position mapping from (blue_location, red_location) to grid position
  // Using actual GridLocation enums as keys for type safety
  private readonly POSITIONS_MAP = new Map<string, GridPosition>([
    // Alpha positions - hands in opposite/complementary directions
    [`${GridLocation.SOUTH},${GridLocation.NORTH}`, GridPosition.ALPHA1],
    [
      `${GridLocation.SOUTHWEST},${GridLocation.NORTHEAST}`,
      GridPosition.ALPHA2,
    ],
    [`${GridLocation.WEST},${GridLocation.EAST}`, GridPosition.ALPHA3],
    [
      `${GridLocation.NORTHWEST},${GridLocation.SOUTHEAST}`,
      GridPosition.ALPHA4,
    ],
    [`${GridLocation.NORTH},${GridLocation.SOUTH}`, GridPosition.ALPHA5],
    [
      `${GridLocation.NORTHEAST},${GridLocation.SOUTHWEST}`,
      GridPosition.ALPHA6,
    ],
    [`${GridLocation.EAST},${GridLocation.WEST}`, GridPosition.ALPHA7],
    [
      `${GridLocation.SOUTHEAST},${GridLocation.NORTHWEST}`,
      GridPosition.ALPHA8,
    ],

    // Beta positions - both hands same direction
    [`${GridLocation.NORTH},${GridLocation.NORTH}`, GridPosition.BETA1],
    [`${GridLocation.NORTHEAST},${GridLocation.NORTHEAST}`, GridPosition.BETA2],
    [`${GridLocation.EAST},${GridLocation.EAST}`, GridPosition.BETA3],
    [`${GridLocation.SOUTHEAST},${GridLocation.SOUTHEAST}`, GridPosition.BETA4],
    [`${GridLocation.SOUTH},${GridLocation.SOUTH}`, GridPosition.BETA5],
    [`${GridLocation.SOUTHWEST},${GridLocation.SOUTHWEST}`, GridPosition.BETA6],
    [`${GridLocation.WEST},${GridLocation.WEST}`, GridPosition.BETA7],
    [`${GridLocation.NORTHWEST},${GridLocation.NORTHWEST}`, GridPosition.BETA8],

    // Gamma positions - mixed/varied combinations
    [`${GridLocation.WEST},${GridLocation.NORTH}`, GridPosition.GAMMA1],
    [
      `${GridLocation.NORTHWEST},${GridLocation.NORTHEAST}`,
      GridPosition.GAMMA2,
    ],
    [`${GridLocation.NORTH},${GridLocation.EAST}`, GridPosition.GAMMA3],
    [
      `${GridLocation.NORTHEAST},${GridLocation.SOUTHEAST}`,
      GridPosition.GAMMA4,
    ],
    [`${GridLocation.EAST},${GridLocation.SOUTH}`, GridPosition.GAMMA5],
    [
      `${GridLocation.SOUTHEAST},${GridLocation.SOUTHWEST}`,
      GridPosition.GAMMA6,
    ],
    [`${GridLocation.SOUTH},${GridLocation.WEST}`, GridPosition.GAMMA7],
    [
      `${GridLocation.SOUTHWEST},${GridLocation.NORTHWEST}`,
      GridPosition.GAMMA8,
    ],
    [`${GridLocation.EAST},${GridLocation.NORTH}`, GridPosition.GAMMA9],
    [
      `${GridLocation.SOUTHEAST},${GridLocation.NORTHEAST}`,
      GridPosition.GAMMA10,
    ],
    [`${GridLocation.SOUTH},${GridLocation.EAST}`, GridPosition.GAMMA11],
    [
      `${GridLocation.SOUTHWEST},${GridLocation.SOUTHEAST}`,
      GridPosition.GAMMA12,
    ],
    [`${GridLocation.WEST},${GridLocation.SOUTH}`, GridPosition.GAMMA13],
    [
      `${GridLocation.NORTHWEST},${GridLocation.SOUTHWEST}`,
      GridPosition.GAMMA14,
    ],
    [`${GridLocation.NORTH},${GridLocation.WEST}`, GridPosition.GAMMA15],
    [
      `${GridLocation.NORTHEAST},${GridLocation.NORTHWEST}`,
      GridPosition.GAMMA16,
    ],
  ]);

  // Reverse mapping from position to hand locations
  private readonly LOCATION_PAIRS_MAP: Record<
    GridPosition,
    [GridLocation, GridLocation]
  >;

  constructor() {
    // Build reverse mapping from the Map entries
    this.LOCATION_PAIRS_MAP = {} as Record<
      GridPosition,
      [GridLocation, GridLocation]
    >;

    this.POSITIONS_MAP.forEach((position, locationKey) => {
      const [blueLocationStr, redLocationStr] = locationKey.split(",");
      const blueLocation = blueLocationStr as GridLocation;
      const redLocation = redLocationStr as GridLocation;
      this.LOCATION_PAIRS_MAP[position] = [blueLocation, redLocation];
    });
  }

  /**
   * Get the hand location pair for a given position
   */
  getGridLocationsFromPosition(
    position: GridPosition
  ): [GridLocation, GridLocation] {
    const pair = this.LOCATION_PAIRS_MAP[position];
    if (!pair) {
      throw new Error(`No location pair found for position: ${position}`);
    }
    return pair;
  }

  /**
   * Get the position for a given hand location pair
   */
  getGridPositionFromLocations(
    blueLocation: GridLocation,
    redLocation: GridLocation
  ): GridPosition {
    const key = `${blueLocation},${redLocation}`;
    const position = this.POSITIONS_MAP.get(key);
    if (!position) {
      throw new Error(
        `No position found for locations: ${blueLocation}, ${redLocation}`
      );
    }
    return position;
  }

  // Interface method (delegates to existing method)
  deriveGridPosition(data: any): any {
    if (data.blueLocation && data.redLocation) {
      return this.getGridPositionFromLocations(
        data.blueLocation,
        data.redLocation
      );
    }
    return null;
  }
}
