/**
 * Position Mapping Service - Correct position mapping based on hand combinations
 *
 * Maps between position names (alpha4, beta2, etc.) and hand location pairs.
 * A position represents the combination of (blue_hand_location, red_hand_location).
 */

import {
  Location,
  GridPosition,
  MotionType,
  RotationDirection,
  Timing,
  Direction,
} from "$lib/domain/enums";

export class PositionMappingService {
  // Position mapping from (blue_location, red_location) to grid position
  // Using actual Location enums as keys for type safety
  private readonly POSITIONS_MAP = new Map<string, GridPosition>([
    // Alpha positions - hands in opposite/complementary directions
    [`${Location.SOUTH},${Location.NORTH}`, GridPosition.ALPHA1],
    [`${Location.SOUTHWEST},${Location.NORTHEAST}`, GridPosition.ALPHA2],
    [`${Location.WEST},${Location.EAST}`, GridPosition.ALPHA3],
    [`${Location.NORTHWEST},${Location.SOUTHEAST}`, GridPosition.ALPHA4],
    [`${Location.NORTH},${Location.SOUTH}`, GridPosition.ALPHA5],
    [`${Location.NORTHEAST},${Location.SOUTHWEST}`, GridPosition.ALPHA6],
    [`${Location.EAST},${Location.WEST}`, GridPosition.ALPHA7],
    [`${Location.SOUTHEAST},${Location.NORTHWEST}`, GridPosition.ALPHA8],

    // Beta positions - both hands same direction
    [`${Location.NORTH},${Location.NORTH}`, GridPosition.BETA1],
    [`${Location.NORTHEAST},${Location.NORTHEAST}`, GridPosition.BETA2],
    [`${Location.EAST},${Location.EAST}`, GridPosition.BETA3],
    [`${Location.SOUTHEAST},${Location.SOUTHEAST}`, GridPosition.BETA4],
    [`${Location.SOUTH},${Location.SOUTH}`, GridPosition.BETA5],
    [`${Location.SOUTHWEST},${Location.SOUTHWEST}`, GridPosition.BETA6],
    [`${Location.WEST},${Location.WEST}`, GridPosition.BETA7],
    [`${Location.NORTHWEST},${Location.NORTHWEST}`, GridPosition.BETA8],

    // Gamma positions - mixed/varied combinations
    [`${Location.WEST},${Location.NORTH}`, GridPosition.GAMMA1],
    [`${Location.NORTHWEST},${Location.NORTHEAST}`, GridPosition.GAMMA2],
    [`${Location.NORTH},${Location.EAST}`, GridPosition.GAMMA3],
    [`${Location.NORTHEAST},${Location.SOUTHEAST}`, GridPosition.GAMMA4],
    [`${Location.EAST},${Location.SOUTH}`, GridPosition.GAMMA5],
    [`${Location.SOUTHEAST},${Location.SOUTHWEST}`, GridPosition.GAMMA6],
    [`${Location.SOUTH},${Location.WEST}`, GridPosition.GAMMA7],
    [`${Location.SOUTHWEST},${Location.NORTHWEST}`, GridPosition.GAMMA8],
    [`${Location.EAST},${Location.NORTH}`, GridPosition.GAMMA9],
    [`${Location.SOUTHEAST},${Location.NORTHEAST}`, GridPosition.GAMMA10],
    [`${Location.SOUTH},${Location.EAST}`, GridPosition.GAMMA11],
    [`${Location.SOUTHWEST},${Location.SOUTHEAST}`, GridPosition.GAMMA12],
    [`${Location.WEST},${Location.SOUTH}`, GridPosition.GAMMA13],
    [`${Location.NORTHWEST},${Location.SOUTHWEST}`, GridPosition.GAMMA14],
    [`${Location.NORTH},${Location.WEST}`, GridPosition.GAMMA15],
    [`${Location.NORTHEAST},${Location.NORTHWEST}`, GridPosition.GAMMA16],
  ]);

  // Reverse mapping from position to hand locations
  private readonly LOCATION_PAIRS_MAP: Record<
    GridPosition,
    [Location, Location]
  >;

  constructor() {
    // Build reverse mapping from the Map entries
    this.LOCATION_PAIRS_MAP = {} as Record<GridPosition, [Location, Location]>;

    this.POSITIONS_MAP.forEach((position, locationKey) => {
      const [blueLocationStr, redLocationStr] = locationKey.split(",");
      const blueLocation = blueLocationStr as Location;
      const redLocation = redLocationStr as Location;
      this.LOCATION_PAIRS_MAP[position] = [blueLocation, redLocation];
    });
  }

  /**
   * Get the hand location pair for a given position
   */
  getLocationPair(position: GridPosition): [Location, Location] {
    const pair = this.LOCATION_PAIRS_MAP[position];
    if (!pair) {
      throw new Error(`No location pair found for position: ${position}`);
    }
    return pair;
  }

  /**
   * Get the position for a given hand location pair
   */
  getPositionFromLocations(
    blueLocation: Location,
    redLocation: Location
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

  /**
   * Convert CSV string format to motion type enum
   */
  stringToMotionType(str: string): MotionType {
    switch (str) {
      case "pro":
        return MotionType.PRO;
      case "anti":
        return MotionType.ANTI;
      case "static":
        return MotionType.STATIC;
      case "dash":
        return MotionType.DASH;
      case "float":
        return MotionType.FLOAT;
      default:
        throw new Error(`Unknown motion type: ${str}`);
    }
  }

  /**
   * Convert CSV string format to rotation direction enum
   */
  stringToRotationDirection(str: string): RotationDirection {
    switch (str) {
      case "cw":
        return RotationDirection.CLOCKWISE;
      case "ccw":
        return RotationDirection.COUNTER_CLOCKWISE;
      case "noRotation":
        return RotationDirection.NO_ROTATION;
      default:
        throw new Error(`Unknown rotation direction: ${str}`);
    }
  }

  /**
   * Convert CSV string format to timing enum
   */
  stringToTiming(str: string): Timing {
    switch (str) {
      case "split":
        return Timing.SPLIT;
      case "tog":
        return Timing.TOG;
      case "quarter":
        return Timing.QUARTER;
      default:
        throw new Error(`Unknown timing: ${str}`);
    }
  }

  /**
   * Convert CSV string format to direction enum
   */
  stringToDirection(str: string): Direction {
    switch (str) {
      case "same":
        return Direction.SAME;
      case "opp":
        return Direction.OPP;
      default:
        throw new Error(`Unknown direction: ${str}`);
    }
  }

  /**
   * Convert CSV string format to grid position enum
   */
  stringToGridPosition(str: string): GridPosition {
    // Convert string like "alpha4" to GridPosition.ALPHA4
    const upperStr = str.toUpperCase();
    const position = GridPosition[upperStr as keyof typeof GridPosition];
    if (!position) {
      throw new Error(`Unknown grid position: ${str}`);
    }
    return position;
  }

  /**
   * Convert CSV string format to location enum
   */
  stringToLocation(str: string): Location {
    switch (str.toLowerCase()) {
      case "n":
      case "north":
        return Location.NORTH;
      case "e":
      case "east":
        return Location.EAST;
      case "s":
      case "south":
        return Location.SOUTH;
      case "w":
      case "west":
        return Location.WEST;
      case "ne":
      case "northeast":
        return Location.NORTHEAST;
      case "se":
      case "southeast":
        return Location.SOUTHEAST;
      case "sw":
      case "southwest":
        return Location.SOUTHWEST;
      case "nw":
      case "northwest":
        return Location.NORTHWEST;
      default:
        throw new Error(`Unknown location: ${str}`);
    }
  }
}
