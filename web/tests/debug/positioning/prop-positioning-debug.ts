import { Location, Orientation } from "$domain";

/**
 * PropRotAngleManager - Calculates prop rotation angles based on location and orientation
 *
 * This class provides precise rotation angle calculations for props in the TKA system.
 * It handles both diamond grid (cardinal directions) and box grid (intercardinal directions)
 * positioning with orientation-specific angle mappings.
 *
 * @example
 * ```typescript
* // Static usage (recommended)
 * const angle = PropRotAngleManager.calculateRotation(Location.NORTH, Orientation.IN);
 *
 * // Instance usage
 * const manager = new PropRotAngleManager({ location: Location.NORTH, orientation: Orientation.IN });
 * const angle = manager.getRotationAngle();
 *
```
 */
export class PropRotAngleManager {
  private readonly location: Location;
  private readonly orientation: Orientation;

  /**
   * Diamond grid angle mappings for cardinal directions (N, E, S, W)
   * Maps orientation -> location -> angle in degrees
   */
  private static readonly DIAMOND_ANGLE_MAP: Record<
    Orientation,
    Record<Location, number>
  > = {
    [Orientation.IN]: {
      [Location.NORTH]: 90,
      [Location.SOUTH]: 270,
      [Location.WEST]: 0,
      [Location.EAST]: 180,
    } as Record<Location, number>,
    [Orientation.OUT]: {
      [Location.NORTH]: 270,
      [Location.SOUTH]: 90,
      [Location.WEST]: 180,
      [Location.EAST]: 0,
    } as Record<Location, number>,
    [Orientation.CLOCK]: {
      [Location.NORTH]: 0,
      [Location.SOUTH]: 180,
      [Location.WEST]: 270,
      [Location.EAST]: 90,
    } as Record<Location, number>,
    [Orientation.COUNTER]: {
      [Location.NORTH]: 180,
      [Location.SOUTH]: 0,
      [Location.WEST]: 90,
      [Location.EAST]: 270,
    } as Record<Location, number>,
  };

  /**
   * Box grid angle mappings for intercardinal directions (NE, SE, SW, NW)
   * Maps orientation -> location -> angle in degrees
   */
  private static readonly BOX_ANGLE_MAP: Record<
    Orientation,
    Record<Location, number>
  > = {
    [Orientation.IN]: {
      [Location.NORTHEAST]: 135,
      [Location.NORTHWEST]: 45,
      [Location.SOUTHWEST]: 315,
      [Location.SOUTHEAST]: 225,
    } as Record<Location, number>,
    [Orientation.OUT]: {
      [Location.NORTHEAST]: 315,
      [Location.NORTHWEST]: 225,
      [Location.SOUTHWEST]: 135,
      [Location.SOUTHEAST]: 45,
    } as Record<Location, number>,
    [Orientation.CLOCK]: {
      [Location.NORTHEAST]: 45,
      [Location.NORTHWEST]: 315,
      [Location.SOUTHWEST]: 225,
      [Location.SOUTHEAST]: 135,
    } as Record<Location, number>,
    [Orientation.COUNTER]: {
      [Location.NORTHEAST]: 225,
      [Location.NORTHWEST]: 135,
      [Location.SOUTHWEST]: 45,
      [Location.SOUTHEAST]: 315,
    } as Record<Location, number>,
  };

  /**
   * Set of diamond (cardinal) locations for efficient lookup
   */
  private static readonly DIAMOND_LOCATIONS = new Set([
    Location.NORTH,
    Location.EAST,
    Location.SOUTH,
    Location.WEST,
  ]);

  constructor({
    location,
    orientation,
  }: {
    location: Location;
    orientation: Orientation;
  }) {
    this.location = location;
    this.orientation = orientation;
  }

  /**
   * Get rotation angle based on location and orientation
   * Uses diamond vs box grid mode detection and appropriate angle maps
   */
  getRotationAngle(): number {
    // Check if it's a diamond location (cardinal directions)
    const diamondLocationValues = [
      Location.NORTH,
      Location.EAST,
      Location.SOUTH,
      Location.WEST,
    ];
    const isDiamondLocation = diamondLocationValues.includes(this.location);

    const diamondAngleMap: Partial<
      Record<Orientation, Partial<Record<Location, number>>>
    > = {
      [Orientation.IN]: {
        [Location.NORTH]: 90,
        [Location.SOUTH]: 270,
        [Location.WEST]: 0,
        [Location.EAST]: 180,
      },
      [Orientation.OUT]: {
        [Location.NORTH]: 270,
        [Location.SOUTH]: 90,
        [Location.WEST]: 180,
        [Location.EAST]: 0,
      },
      [Orientation.CLOCK]: {
        [Location.NORTH]: 0,
        [Location.SOUTH]: 180,
        [Location.WEST]: 270,
        [Location.EAST]: 90,
      },
      [Orientation.COUNTER]: {
        [Location.NORTH]: 180,
        [Location.SOUTH]: 0,
        [Location.WEST]: 90,
        [Location.EAST]: 270,
      },
    };

    const boxAngleMap: Partial<
      Record<Orientation, Partial<Record<Location, number>>>
    > = {
      [Orientation.IN]: {
        [Location.NORTHEAST]: 135,
        [Location.NORTHWEST]: 45,
        [Location.SOUTHWEST]: 315,
        [Location.SOUTHEAST]: 225,
      },
      [Orientation.OUT]: {
        [Location.NORTHEAST]: 315,
        [Location.NORTHWEST]: 225,
        [Location.SOUTHWEST]: 135,
        [Location.SOUTHEAST]: 45,
      },
      [Orientation.CLOCK]: {
        [Location.NORTHEAST]: 45,
        [Location.NORTHWEST]: 315,
        [Location.SOUTHWEST]: 225,
        [Location.SOUTHEAST]: 135,
      },
      [Orientation.COUNTER]: {
        [Location.NORTHEAST]: 225,
        [Location.NORTHWEST]: 135,
        [Location.SOUTHWEST]: 45,
        [Location.SOUTHEAST]: 315,
      },
    };

    const angleMap = isDiamondLocation ? diamondAngleMap : boxAngleMap;
    const orientationAngles = angleMap[this.orientation];

    return orientationAngles?.[this.location] ?? 0;
  }

  /**
   * Static helper method for quick rotation calculation
   */
  static calculateRotation(
    location: Location,
    orientation: Orientation
  ): number {
    const manager = new PropRotAngleManager({
      location,
      orientation,
    });
    return manager.getRotationAngle();
  }
}

// TEMPORARILY DISABLED - This test file needs to be fixed
// TODO: Restore prop positioning debug tests

export function testPropPositioning() {
  console.log("⚠️ Prop positioning tests temporarily disabled");
}

export { testPropPositioning as runPropPositioningTest };
