import { GridMode, Location, Orientation } from "$domain";

/**
 * Calculates prop rotation angles based on location, orientation, and grid mode.
 * Uses static lookup tables for optimal performance.
 */
export class PropRotAngleManager {
  private readonly location: Location;
  private readonly orientation: Orientation;
  private readonly gridMode: GridMode;

  /** Diamond grid angle mappings */
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

  /** Box grid angle mappings */
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

  /** Creates a new PropRotAngleManager instance */
  constructor({
    location,
    orientation,
    gridMode,
  }: {
    location: Location;
    orientation: Orientation;
    gridMode: GridMode;
  }) {
    this.location = location;
    this.orientation = orientation;
    this.gridMode = gridMode;
  }

  /** Calculates the rotation angle in degrees */
  getRotationAngle(): number {
    const angleMap =
      this.gridMode === GridMode.DIAMOND
        ? PropRotAngleManager.DIAMOND_ANGLE_MAP
        : PropRotAngleManager.BOX_ANGLE_MAP;

    const orientationAngles = angleMap[this.orientation];
    return orientationAngles?.[this.location] ?? 0;
  }

  /** Static method for rotation angle calculation (recommended) */
  static calculateRotation(
    location: Location,
    orientation: Orientation,
    gridMode: GridMode
  ): number {
    const angleMap =
      gridMode === GridMode.DIAMOND
        ? PropRotAngleManager.DIAMOND_ANGLE_MAP
        : PropRotAngleManager.BOX_ANGLE_MAP;

    const orientationAngles = angleMap[orientation];
    return orientationAngles?.[location] ?? 0;
  }
}

export default PropRotAngleManager;
