import { GridLocation, GridMode, Orientation } from "$shared/domain";

/**
 * Calculates prop rotation angles based on location, orientation, and grid mode.
 * Uses static lookup tables for optimal performance.
 */
export class PropRotAngleManager {
  private readonly location: GridLocation;
  private readonly orientation: Orientation;
  private readonly gridMode: GridMode;

  /** Diamond grid angle mappings */
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

  /** Box grid angle mappings */
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

  /** Creates a new PropRotAngleManager instance */
  constructor({
    location,
    orientation,
    gridMode,
  }: {
    location: GridLocation;
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
    location: GridLocation,
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
