import { GridLocation, Orientation } from "$shared/domain";

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
 * const angle = PropRotAngleManager.calculateRotation(GridLocation.NORTH, Orientation.IN);
 *
 * // Instance usage
 * const manager = new PropRotAngleManager({ location: GridLocation.NORTH, orientation: Orientation.IN });
 * const angle = manager.getRotationAngle();
 *
```
 */
export class PropRotAngleManager {
  private readonly location: GridLocation;
  private readonly orientation: Orientation;

  /**
   * Diamond grid angle mappings for cardinal directions (N, E, S, W)
   * Maps orientation -> location -> angle in degrees
   */
  private static readonly DIAMOND_ANGLE_MAP: Record<
    Orientation,
    Record<GridLocation, number>
  > = {
    [Orientation.IN]: {
      [GridLocation.NORTH]: 90,
      [GridLocation.SOUTH]: 270,
      [GridLocation.WEST]: 0,
      [GridLocation.EAST]: 180,
    } as Record<GridLocation, number>,
    [Orientation.OUT]: {
      [GridLocation.NORTH]: 270,
      [GridLocation.SOUTH]: 90,
      [GridLocation.WEST]: 180,
      [GridLocation.EAST]: 0,
    } as Record<GridLocation, number>,
    [Orientation.CLOCK]: {
      [GridLocation.NORTH]: 0,
      [GridLocation.SOUTH]: 180,
      [GridLocation.WEST]: 270,
      [GridLocation.EAST]: 90,
    } as Record<GridLocation, number>,
    [Orientation.COUNTER]: {
      [GridLocation.NORTH]: 180,
      [GridLocation.SOUTH]: 0,
      [GridLocation.WEST]: 90,
      [GridLocation.EAST]: 270,
    } as Record<GridLocation, number>,
  };

  /**
   * Box grid angle mappings for intercardinal directions (NE, SE, SW, NW)
   * Maps orientation -> location -> angle in degrees
   */
  private static readonly BOX_ANGLE_MAP: Record<
    Orientation,
    Record<GridLocation, number>
  > = {
    [Orientation.IN]: {
      [GridLocation.NORTHEAST]: 135,
      [GridLocation.NORTHWEST]: 45,
      [GridLocation.SOUTHWEST]: 315,
      [GridLocation.SOUTHEAST]: 225,
    } as Record<GridLocation, number>,
    [Orientation.OUT]: {
      [GridLocation.NORTHEAST]: 315,
      [GridLocation.NORTHWEST]: 225,
      [GridLocation.SOUTHWEST]: 135,
      [GridLocation.SOUTHEAST]: 45,
    } as Record<GridLocation, number>,
    [Orientation.CLOCK]: {
      [GridLocation.NORTHEAST]: 45,
      [GridLocation.NORTHWEST]: 315,
      [GridLocation.SOUTHWEST]: 225,
      [GridLocation.SOUTHEAST]: 135,
    } as Record<GridLocation, number>,
    [Orientation.COUNTER]: {
      [GridLocation.NORTHEAST]: 225,
      [GridLocation.NORTHWEST]: 135,
      [GridLocation.SOUTHWEST]: 45,
      [GridLocation.SOUTHEAST]: 315,
    } as Record<GridLocation, number>,
  };

  /**
   * Set of diamond (cardinal) locations for efficient lookup
   */
  private static readonly DIAMOND_LOCATIONS = new Set([
    GridLocation.NORTH,
    GridLocation.EAST,
    GridLocation.SOUTH,
    GridLocation.WEST,
  ]);

  constructor({
    location,
    orientation,
  }: {
    location: GridLocation;
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
      GridLocation.NORTH,
      GridLocation.EAST,
      GridLocation.SOUTH,
      GridLocation.WEST,
    ];
    const isDiamondLocation = diamondLocationValues.includes(this.location);

    const diamondAngleMap: Partial<
      Record<Orientation, Partial<Record<GridLocation, number>>>
    > = {
      [Orientation.IN]: {
        [GridLocation.NORTH]: 90,
        [GridLocation.SOUTH]: 270,
        [GridLocation.WEST]: 0,
        [GridLocation.EAST]: 180,
      },
      [Orientation.OUT]: {
        [GridLocation.NORTH]: 270,
        [GridLocation.SOUTH]: 90,
        [GridLocation.WEST]: 180,
        [GridLocation.EAST]: 0,
      },
      [Orientation.CLOCK]: {
        [GridLocation.NORTH]: 0,
        [GridLocation.SOUTH]: 180,
        [GridLocation.WEST]: 270,
        [GridLocation.EAST]: 90,
      },
      [Orientation.COUNTER]: {
        [GridLocation.NORTH]: 180,
        [GridLocation.SOUTH]: 0,
        [GridLocation.WEST]: 90,
        [GridLocation.EAST]: 270,
      },
    };

    const boxAngleMap: Partial<
      Record<Orientation, Partial<Record<GridLocation, number>>>
    > = {
      [Orientation.IN]: {
        [GridLocation.NORTHEAST]: 135,
        [GridLocation.NORTHWEST]: 45,
        [GridLocation.SOUTHWEST]: 315,
        [GridLocation.SOUTHEAST]: 225,
      },
      [Orientation.OUT]: {
        [GridLocation.NORTHEAST]: 315,
        [GridLocation.NORTHWEST]: 225,
        [GridLocation.SOUTHWEST]: 135,
        [GridLocation.SOUTHEAST]: 45,
      },
      [Orientation.CLOCK]: {
        [GridLocation.NORTHEAST]: 45,
        [GridLocation.NORTHWEST]: 315,
        [GridLocation.SOUTHWEST]: 225,
        [GridLocation.SOUTHEAST]: 135,
      },
      [Orientation.COUNTER]: {
        [GridLocation.NORTHEAST]: 225,
        [GridLocation.NORTHWEST]: 135,
        [GridLocation.SOUTHWEST]: 45,
        [GridLocation.SOUTHEAST]: 315,
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
    location: GridLocation,
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
