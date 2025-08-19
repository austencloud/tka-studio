/**
 * Position Mapping Service - Correct position mapping based on hand combinations
 *
 * Maps between position names (alpha4, beta2, etc.) and hand location pairs.
 * A position represents the combination of (blue_hand_location, red_hand_location).
 */

import { Location, GridPosition } from '$lib/domain/enums';

export class PositionMappingService {
  // Position mapping from (blue_end_loc, red_end_loc) to position key
  private readonly POSITIONS_MAP: Record<string, GridPosition> = {
    // Alpha positions - hands in opposite/complementary directions
    "s,n": GridPosition.ALPHA1,
    "sw,ne": GridPosition.ALPHA2,
    "w,e": GridPosition.ALPHA3,
    "nw,se": GridPosition.ALPHA4,
    "n,s": GridPosition.ALPHA5,
    "ne,sw": GridPosition.ALPHA6,
    "e,w": GridPosition.ALPHA7,
    "se,nw": GridPosition.ALPHA8,
    
    // Beta positions - both hands same direction
    "n,n": GridPosition.BETA1,
    "ne,ne": GridPosition.BETA2,
    "e,e": GridPosition.BETA3,
    "se,se": GridPosition.BETA4,
    "s,s": GridPosition.BETA5,
    "sw,sw": GridPosition.BETA6,
    "w,w": GridPosition.BETA7,
    "nw,nw": GridPosition.BETA8,
    
    // Gamma positions - mixed/varied combinations
    "w,n": GridPosition.GAMMA1,
    "nw,ne": GridPosition.GAMMA2,
    "n,e": GridPosition.GAMMA3,
    "ne,se": GridPosition.GAMMA4,
    "e,s": GridPosition.GAMMA5,
    "se,sw": GridPosition.GAMMA6,
    "s,w": GridPosition.GAMMA7,
    "sw,nw": GridPosition.GAMMA8,
    "e,n": GridPosition.GAMMA9,
    "se,ne": GridPosition.GAMMA10,
    "s,e": GridPosition.GAMMA11,
    "sw,se": GridPosition.GAMMA12,
    "w,s": GridPosition.GAMMA13,
    "nw,sw": GridPosition.GAMMA14,
    "n,w": GridPosition.GAMMA15,
    "ne,nw": GridPosition.GAMMA16,
  };

  // Reverse mapping from position to hand locations
  private readonly LOCATION_PAIRS_MAP: Record<GridPosition, [Location, Location]>;

  constructor() {
    // Build reverse mapping
    this.LOCATION_PAIRS_MAP = {} as Record<GridPosition, [Location, Location]>;
    
    Object.entries(this.POSITIONS_MAP).forEach(([locPair, position]) => {
      const [blueStr, redStr] = locPair.split(',');
      const blueLocation = this.stringToLocation(blueStr);
      const redLocation = this.stringToLocation(redStr);
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
  getPositionFromLocations(blueLocation: Location, redLocation: Location): GridPosition {
    const key = `${this.locationToString(blueLocation)},${this.locationToString(redLocation)}`;
    const position = this.POSITIONS_MAP[key];
    if (!position) {
      throw new Error(`No position found for locations: ${blueLocation}, ${redLocation}`);
    }
    return position;
  }

  /**
   * Convert location enum to CSV string format
   */
  private locationToString(location: Location): string {
    switch (location) {
      case Location.NORTH: return 'n';
      case Location.NORTHEAST: return 'ne';
      case Location.EAST: return 'e';
      case Location.SOUTHEAST: return 'se';
      case Location.SOUTH: return 's';
      case Location.SOUTHWEST: return 'sw';
      case Location.WEST: return 'w';
      case Location.NORTHWEST: return 'nw';
      default:
        throw new Error(`Unknown location: ${location}`);
    }
  }

  /**
   * Convert CSV string format to location enum
   */
  stringToLocation(str: string): Location {
    switch (str) {
      case 'n': return Location.NORTH;
      case 'ne': return Location.NORTHEAST;
      case 'e': return Location.EAST;
      case 'se': return Location.SOUTHEAST;
      case 's': return Location.SOUTH;
      case 'sw': return Location.SOUTHWEST;
      case 'w': return Location.WEST;
      case 'nw': return Location.NORTHWEST;
      default:
        throw new Error(`Unknown location string: ${str}`);
    }
  }

  /**
   * Convert CSV string format to motion type enum
   */
  stringToMotionType(str: string): import('$lib/domain/enums').MotionType {
    switch (str) {
      case 'pro': return import('$lib/domain/enums').MotionType.PRO;
      case 'anti': return import('$lib/domain/enums').MotionType.ANTI;
      case 'static': return import('$lib/domain/enums').MotionType.STATIC;
      case 'dash': return import('$lib/domain/enums').MotionType.DASH;
      case 'float': return import('$lib/domain/enums').MotionType.FLOAT;
      default:
        throw new Error(`Unknown motion type: ${str}`);
    }
  }

  /**
   * Convert CSV string format to rotation direction enum
   */
  stringToRotationDirection(str: string): import('$lib/domain/enums').RotationDirection {
    switch (str) {
      case 'cw': return import('$lib/domain/enums').RotationDirection.CLOCKWISE;
      case 'ccw': return import('$lib/domain/enums').RotationDirection.COUNTER_CLOCKWISE;
      case 'none': return import('$lib/domain/enums').RotationDirection.NO_ROTATION;
      default:
        throw new Error(`Unknown rotation direction: ${str}`);
    }
  }

  /**
   * Convert CSV string format to timing enum
   */
  stringToTiming(str: string): import('$lib/domain/enums').Timing {
    switch (str) {
      case 'split': return import('$lib/domain/enums').Timing.SPLIT;
      case 'tog': return import('$lib/domain/enums').Timing.TOG;
      case 'quarter': return import('$lib/domain/enums').Timing.QUARTER;
      default:
        throw new Error(`Unknown timing: ${str}`);
    }
  }

  /**
   * Convert CSV string format to direction enum
   */
  stringToDirection(str: string): import('$lib/domain/enums').Direction {
    switch (str) {
      case 'same': return import('$lib/domain/enums').Direction.SAME;
      case 'opp': return import('$lib/domain/enums').Direction.OPP;
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
}
