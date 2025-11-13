import {
  GridLocation,
  MotionType,
  Orientation,
  type MotionData,
  type PictographData,
} from "$shared";
import type { ISpecialPlacementService } from "$shared/pictograph/arrow/positioning/placement/services/contracts";
import type { IRotationAngleOverrideKeyGenerator } from "$shared/pictograph/arrow/positioning/key-generation/services/implementations/RotationAngleOverrideKeyGenerator";
import { injectable, inject, optional } from "inversify";
import { TYPES } from "$shared/inversify/types";

export interface IArrowRotationCalculator {
  calculateRotation(
    motion: MotionData,
    location: GridLocation,
    pictographData?: PictographData
  ): Promise<number>;
  getSupportedMotionTypes(): MotionType[];
  validateMotionData(motion: MotionData): boolean;
}

@injectable()
export class ArrowRotationCalculator implements IArrowRotationCalculator {
  /**
   * Pure algorithmic service for calculating arrow rotation angles.
   *
   * Implements rotation calculation algorithms without any UI dependencies.
   * Each motion type has its own rotation strategy based on proven algorithms.
   *
   * ROTATION OVERRIDE SYSTEM:
   * - For DASH and STATIC motions, certain pictographs require different rotation angles
   * - These overrides are flagged in special placement JSON data
   * - When override flag is present, uses override rotation maps instead of normal maps
   */

  private specialPlacementService: ISpecialPlacementService | undefined;
  private rotationOverrideKeyGenerator:
    | IRotationAngleOverrideKeyGenerator
    | undefined;

  constructor(
    @inject(TYPES.ISpecialPlacementService)
    @optional()
    specialPlacementService?: ISpecialPlacementService,
    @inject(TYPES.IRotationAngleOverrideKeyGenerator)
    @optional()
    rotationOverrideKeyGenerator?: IRotationAngleOverrideKeyGenerator
  ) {
    this.specialPlacementService = specialPlacementService ?? undefined;
    this.rotationOverrideKeyGenerator =
      rotationOverrideKeyGenerator ?? undefined;
  }

  // Static arrow rotation for RADIAL orientations (IN/OUT) - Diamond Mode
  private readonly staticRadialClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 0,
    [GridLocation.EAST]: 90,
    [GridLocation.SOUTH]: 180,
    [GridLocation.WEST]: 270,
    [GridLocation.NORTHEAST]: 45,
    [GridLocation.SOUTHEAST]: 135,
    [GridLocation.SOUTHWEST]: 225,
    [GridLocation.NORTHWEST]: 315,
  };

  private readonly staticRadialCounterClockwiseMap: Record<
    GridLocation,
    number
  > = {
    [GridLocation.NORTH]: 0,
    [GridLocation.EAST]: 90,
    [GridLocation.SOUTH]: 180,
    [GridLocation.WEST]: 270,
    [GridLocation.NORTHEAST]: 45,
    [GridLocation.SOUTHEAST]: 135,
    [GridLocation.SOUTHWEST]: 225,
    [GridLocation.NORTHWEST]: 315,
  };

  // Static arrow rotation for NON-RADIAL orientations (CLOCK/COUNTER) - Box Mode
  private readonly staticNonRadialClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 180,
    [GridLocation.EAST]: 270,
    [GridLocation.SOUTH]: 0,
    [GridLocation.WEST]: 90,
    [GridLocation.NORTHEAST]: 225,
    [GridLocation.SOUTHEAST]: 315,
    [GridLocation.SOUTHWEST]: 45,
    [GridLocation.NORTHWEST]: 135,
  };

  private readonly staticNonRadialCounterClockwiseMap: Record<
    GridLocation,
    number
  > = {
    [GridLocation.NORTH]: 180,
    [GridLocation.EAST]: 270,
    [GridLocation.SOUTH]: 0,
    [GridLocation.WEST]: 90,
    [GridLocation.NORTHEAST]: 135,
    [GridLocation.SOUTHEAST]: 45,
    [GridLocation.SOUTHWEST]: 315,
    [GridLocation.NORTHWEST]: 225,
  };

  // PRO rotation angles - FIXED to match legacy implementation
  private readonly proClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 315,
    [GridLocation.EAST]: 45,
    [GridLocation.SOUTH]: 135,
    [GridLocation.WEST]: 225,
    [GridLocation.NORTHEAST]: 0,
    [GridLocation.SOUTHEAST]: 90,
    [GridLocation.SOUTHWEST]: 180,
    [GridLocation.NORTHWEST]: 270,
  };

  private readonly proCounterClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 45,
    [GridLocation.EAST]: 135,
    [GridLocation.SOUTH]: 225,
    [GridLocation.WEST]: 315,
    [GridLocation.NORTHEAST]: 90,
    [GridLocation.SOUTHEAST]: 180,
    [GridLocation.SOUTHWEST]: 270,
    [GridLocation.NORTHWEST]: 0,
  };

  // ANTI rotation angles - ANTI clockwise = PRO counter-clockwise
  private readonly antiClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 45,
    [GridLocation.EAST]: 135,
    [GridLocation.SOUTH]: 225,
    [GridLocation.WEST]: 315,
    [GridLocation.NORTHEAST]: 90,
    [GridLocation.SOUTHEAST]: 180,
    [GridLocation.SOUTHWEST]: 270,
    [GridLocation.NORTHWEST]: 0,
  };

  // ANTI counter-clockwise = PRO clockwise
  private readonly antiCounterClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 315,
    [GridLocation.EAST]: 45,
    [GridLocation.SOUTH]: 135,
    [GridLocation.WEST]: 225,
    [GridLocation.NORTHEAST]: 0,
    [GridLocation.SOUTHEAST]: 90,
    [GridLocation.SOUTHWEST]: 180,
    [GridLocation.NORTHWEST]: 270,
  };

  private readonly dashClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 0,
    [GridLocation.EAST]: 90,
    [GridLocation.SOUTH]: 180,
    [GridLocation.WEST]: 270,
    [GridLocation.NORTHEAST]: 45,
    [GridLocation.SOUTHEAST]: 135,
    [GridLocation.SOUTHWEST]: 225,
    [GridLocation.NORTHWEST]: 315,
  };

  private readonly dashCounterClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 0,
    [GridLocation.EAST]: 90,
    [GridLocation.SOUTH]: 180,
    [GridLocation.WEST]: 270,
    [GridLocation.NORTHEAST]: 45,
    [GridLocation.SOUTHEAST]: 135,
    [GridLocation.SOUTHWEST]: 225,
    [GridLocation.NORTHWEST]: 315,
  };

  private readonly dashNoRotationMap: Record<string, number> = {
    [`${GridLocation.NORTH},${GridLocation.SOUTH}`]: 90,
    [`${GridLocation.EAST},${GridLocation.WEST}`]: 180,
    [`${GridLocation.SOUTH},${GridLocation.NORTH}`]: 270,
    [`${GridLocation.WEST},${GridLocation.EAST}`]: 0,
    [`${GridLocation.SOUTHEAST},${GridLocation.NORTHWEST}`]: 225,
    [`${GridLocation.SOUTHWEST},${GridLocation.NORTHEAST}`]: 315,
    [`${GridLocation.NORTHWEST},${GridLocation.SOUTHEAST}`]: 45,
    [`${GridLocation.NORTHEAST},${GridLocation.SOUTHWEST}`]: 135,
  };

  // FLOAT rotation angles - based on handpath direction (start → end location movement)
  // Clockwise handpath: S→W, W→N, N→E, E→S, NE→SE, SE→SW, SW→NW, NW→NE
  private readonly floatClockwiseHandpathMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 315,
    [GridLocation.EAST]: 45,
    [GridLocation.SOUTH]: 135,
    [GridLocation.WEST]: 225,
    [GridLocation.NORTHEAST]: 0,
    [GridLocation.SOUTHEAST]: 90,
    [GridLocation.SOUTHWEST]: 180,
    [GridLocation.NORTHWEST]: 270,
  };

  // Counter-clockwise handpath: W→S, N→W, E→N, S→E, NE→NW, NW→SW, SW→SE, SE→NE
  private readonly floatCounterClockwiseHandpathMap: Record<
    GridLocation,
    number
  > = {
    [GridLocation.NORTH]: 135,
    [GridLocation.EAST]: 225,
    [GridLocation.SOUTH]: 315,
    [GridLocation.WEST]: 45,
    [GridLocation.NORTHEAST]: 180,
    [GridLocation.SOUTHEAST]: 270,
    [GridLocation.SOUTHWEST]: 0,
    [GridLocation.NORTHWEST]: 90,
  };

  // ROTATION OVERRIDE MAPS - Used when rotation_override flag is set
  // These are DIFFERENT angles used for specific pictograph configurations

  // Static from RADIAL (IN/OUT) override angles
  private readonly staticRadialOverrideMap: Record<
    GridLocation,
    Record<string, number>
  > = {
    [GridLocation.NORTH]: { cw: 180, ccw: 180 },
    [GridLocation.EAST]: { cw: 270, ccw: 270 },
    [GridLocation.SOUTH]: { cw: 0, ccw: 0 },
    [GridLocation.WEST]: { cw: 90, ccw: 90 },
    [GridLocation.NORTHEAST]: { cw: 225, ccw: 135 },
    [GridLocation.SOUTHEAST]: { cw: 315, ccw: 45 },
    [GridLocation.SOUTHWEST]: { cw: 45, ccw: 315 },
    [GridLocation.NORTHWEST]: { cw: 135, ccw: 225 },
  };

  // Static from NON-RADIAL (CLOCK/COUNTER) override angles
  private readonly staticNonRadialOverrideMap: Record<
    GridLocation,
    Record<string, number>
  > = {
    [GridLocation.NORTH]: { cw: 0, ccw: 0 },
    [GridLocation.EAST]: { cw: 90, ccw: 270 },
    [GridLocation.SOUTH]: { cw: 180, ccw: 180 },
    [GridLocation.WEST]: { cw: 270, ccw: 90 },
    [GridLocation.NORTHEAST]: { cw: 45, ccw: 315 },
    [GridLocation.SOUTHEAST]: { cw: 135, ccw: 225 },
    [GridLocation.SOUTHWEST]: { cw: 225, ccw: 135 },
    [GridLocation.NORTHWEST]: { cw: 315, ccw: 45 },
  };

  async calculateRotation(
    motion: MotionData,
    location: GridLocation,
    pictographData?: PictographData
  ): Promise<number> {
    /**
     * Calculate arrow rotation angle based on motion type and location.
     *
     * Args:
     *     motion: Motion data containing type and rotation direction
     *     location: Calculated arrow location
     *     pictographData: Optional pictograph data for rotation override checking
     *
     * Returns:
     *     Rotation angle in degrees (0-360)
     */
    const motionType = motion.motionType?.toLowerCase();

    switch (motionType) {
      case "static":
        return await this.calculateStaticRotation(
          motion,
          location,
          pictographData
        );
      case "pro":
        return this.calculateProRotation(motion, location);
      case "anti":
        return this.calculateAntiRotation(motion, location);
      case "dash":
        return await this.calculateDashRotation(
          motion,
          location,
          pictographData
        );
      case "float":
        return this.calculateFloatRotation(motion, location);
      default:
        console.warn(`Unknown motion type: ${motionType}, returning 0.0`);
        return 0.0;
    }
  }

  private async calculateStaticRotation(
    motion: MotionData,
    location: GridLocation,
    pictographData?: PictographData
  ): Promise<number> {
    /**
     * Calculate rotation for static arrows.
     * Uses different rotation maps based on whether orientation is radial (IN/OUT) or non-radial (CLOCK/COUNTER).
     * Radial = Diamond mode, Non-radial = Box mode.
     *
     * ROTATION OVERRIDE CHECK:
     * For specific pictographs, rotation override flag may be set in special placements.
     * When override is active, uses different rotation angles.
     */
    const startOrientation = motion.startOrientation;
    const rotationDirection = motion.rotationDirection?.toLowerCase();

    // Determine if this is a radial orientation (IN/OUT) or non-radial (CLOCK/COUNTER)
    const isRadial =
      startOrientation === Orientation.IN ||
      startOrientation === Orientation.OUT;

    // STEP 1: Check for rotation override
    if (
      pictographData &&
      this.specialPlacementService &&
      this.rotationOverrideKeyGenerator
    ) {
      try {
        const overrideKey =
          this.rotationOverrideKeyGenerator.generateRotationAngleOverrideKey(
            motion,
            pictographData
          );
        const hasOverride =
          await this.specialPlacementService.hasRotationAngleOverride(
            motion,
            pictographData,
            overrideKey
          );

        if (hasOverride) {
          // Use override rotation maps
          return this.getRotationFromOverrideMap(
            isRadial,
            location,
            rotationDirection || ""
          );
        }
      } catch (error) {
        // If override check fails, fall through to normal rotation
        console.warn("Rotation override check failed:", error);
      }
    }

    // STEP 2: Use normal rotation maps (no override)
    let rotationMap: Record<GridLocation, number>;

    if (isRadial) {
      // Diamond mode - use radial maps
      if (rotationDirection === "clockwise" || rotationDirection === "cw") {
        rotationMap = this.staticRadialClockwiseMap;
      } else {
        rotationMap = this.staticRadialCounterClockwiseMap;
      }
    } else {
      // Box mode - use non-radial maps
      if (rotationDirection === "clockwise" || rotationDirection === "cw") {
        rotationMap = this.staticNonRadialClockwiseMap;
      } else {
        rotationMap = this.staticNonRadialCounterClockwiseMap;
      }
    }

    return rotationMap[location] || 0.0;
  }

  private getRotationFromOverrideMap(
    isRadial: boolean,
    location: GridLocation,
    rotationDirection: string
  ): number {
    /**
     * Get rotation angle from override maps.
     * Override maps have conditional angles based on rotation direction.
     */
    const overrideMap = isRadial
      ? this.staticRadialOverrideMap
      : this.staticNonRadialOverrideMap;

    const angleValue = overrideMap[location];

    if (typeof angleValue === "number") {
      return angleValue;
    } else if (typeof angleValue === "object") {
      // Angle depends on rotation direction
      const dir =
        rotationDirection === "clockwise" || rotationDirection === "cw"
          ? "cw"
          : "ccw";
      return angleValue[dir] || 0.0;
    }

    return 0.0;
  }

  private calculateProRotation(
    motion: MotionData,
    location: GridLocation
  ): number {
    /**Calculate rotation for PRO arrows based on rotation direction.*/
    const rotationDirection = motion.rotationDirection?.toLowerCase();
    if (rotationDirection === "clockwise" || rotationDirection === "cw") {
      return this.proClockwiseMap[location] || 0.0;
    } else {
      return this.proCounterClockwiseMap[location] || 0.0;
    }
  }

  private calculateAntiRotation(
    motion: MotionData,
    location: GridLocation
  ): number {
    /**Calculate rotation for ANTI arrows based on rotation direction.*/
    const rotationDirection = motion.rotationDirection?.toLowerCase();
    if (rotationDirection === "clockwise" || rotationDirection === "cw") {
      return this.antiClockwiseMap[location] || 0.0;
    } else {
      return this.antiCounterClockwiseMap[location] || 0.0;
    }
  }

  private async calculateDashRotation(
    motion: MotionData,
    location: GridLocation,
    pictographData?: PictographData
  ): Promise<number> {
    /**
     * Calculate rotation for DASH arrows with special NO_ROTATION handling.
     *
     * ROTATION OVERRIDE CHECK:
     * Dash arrows can also have rotation overrides for specific pictographs.
     */
    const rotationDirection = motion.rotationDirection?.toLowerCase();

    // STEP 1: Check for rotation override
    if (
      pictographData &&
      this.specialPlacementService &&
      this.rotationOverrideKeyGenerator
    ) {
      try {
        const overrideKey =
          this.rotationOverrideKeyGenerator.generateRotationAngleOverrideKey(
            motion,
            pictographData
          );
        const hasOverride =
          await this.specialPlacementService.hasRotationAngleOverride(
            motion,
            pictographData,
            overrideKey
          );

        if (hasOverride) {
          // For dash, override uses same logic as STATIC radial override
          // (This matches legacy behavior - dash overrides use radial maps)
          return this.getRotationFromOverrideMap(
            true, // Dash overrides always use radial maps
            location,
            rotationDirection || ""
          );
        }
      } catch (error) {
        // If override check fails, fall through to normal rotation
        console.warn("Dash rotation override check failed:", error);
      }
    }

    // STEP 2: Use normal rotation maps (no override)
    if (
      rotationDirection === "norotation" ||
      rotationDirection === "none" ||
      rotationDirection === "no_rotation"
    ) {
      const key = `${motion.startLocation},${motion.endLocation}`;
      return this.dashNoRotationMap[key] || 0.0;
    }

    if (rotationDirection === "clockwise" || rotationDirection === "cw") {
      return this.dashClockwiseMap[location] || 0.0;
    } else {
      return this.dashCounterClockwiseMap[location] || 0.0;
    }
  }

  private calculateFloatRotation(
    motion: MotionData,
    location: GridLocation
  ): number {
    /**
     * Calculate rotation for FLOAT arrows.
     *
     * IMPORTANT: Float rotation is based on HANDPATH DIRECTION, not prop rotation direction!
     * Handpath direction is determined by the motion from start location to end location.
     */
    const handpathDirection = this.getHandpathDirection(
      motion.startLocation,
      motion.endLocation
    );

    // Use handpath direction to select the correct rotation map
    if (handpathDirection === "cw") {
      return this.floatClockwiseHandpathMap[location] || 0.0;
    } else if (handpathDirection === "ccw") {
      return this.floatCounterClockwiseHandpathMap[location] || 0.0;
    }

    // Fallback for static/dash movements (shouldn't happen for float)
    return 0.0;
  }

  /**
   * Determine handpath direction based on start and end locations.
   * Matches legacy HandpathCalculator logic.
   */
  private getHandpathDirection(
    startLoc: GridLocation,
    endLoc: GridLocation
  ): "cw" | "ccw" | "dash" | "static" {
    // Clockwise pairs (cardinal)
    const clockwisePairs = [
      [GridLocation.SOUTH, GridLocation.WEST],
      [GridLocation.WEST, GridLocation.NORTH],
      [GridLocation.NORTH, GridLocation.EAST],
      [GridLocation.EAST, GridLocation.SOUTH],
    ];

    // Counter-clockwise pairs (cardinal)
    const counterClockwisePairs = [
      [GridLocation.WEST, GridLocation.SOUTH],
      [GridLocation.NORTH, GridLocation.WEST],
      [GridLocation.EAST, GridLocation.NORTH],
      [GridLocation.SOUTH, GridLocation.EAST],
    ];

    // Diagonal clockwise pairs
    const diagonalClockwise = [
      [GridLocation.NORTHEAST, GridLocation.SOUTHEAST],
      [GridLocation.SOUTHEAST, GridLocation.SOUTHWEST],
      [GridLocation.SOUTHWEST, GridLocation.NORTHWEST],
      [GridLocation.NORTHWEST, GridLocation.NORTHEAST],
    ];

    // Diagonal counter-clockwise pairs
    const diagonalCounterClockwise = [
      [GridLocation.NORTHEAST, GridLocation.NORTHWEST],
      [GridLocation.NORTHWEST, GridLocation.SOUTHWEST],
      [GridLocation.SOUTHWEST, GridLocation.SOUTHEAST],
      [GridLocation.SOUTHEAST, GridLocation.NORTHEAST],
    ];

    // Check clockwise
    for (const [start, end] of [...clockwisePairs, ...diagonalClockwise]) {
      if (startLoc === start && endLoc === end) {
        return "cw";
      }
    }

    // Check counter-clockwise
    for (const [start, end] of [
      ...counterClockwisePairs,
      ...diagonalCounterClockwise,
    ]) {
      if (startLoc === start && endLoc === end) {
        return "ccw";
      }
    }

    // Check if static (same location)
    if (startLoc === endLoc) {
      return "static";
    }

    // Otherwise it's a dash movement
    return "dash";
  }

  getSupportedMotionTypes(): MotionType[] {
    /**Get list of motion types supported by this calculator.*/
    return [
      MotionType.STATIC,
      MotionType.PRO,
      MotionType.ANTI,
      MotionType.DASH,
      MotionType.FLOAT,
    ];
  }

  validateMotionData(motion: MotionData): boolean {
    /**Validate that motion data is suitable for rotation calculation.*/
    if (!motion) {
      return false;
    }

    const motionType = motion.motionType?.toLowerCase();
    if (!this.getSupportedMotionTypes().includes(motionType as MotionType)) {
      return false;
    }

    if (!motion.rotationDirection) {
      return false;
    }

    return true;
  }
}
