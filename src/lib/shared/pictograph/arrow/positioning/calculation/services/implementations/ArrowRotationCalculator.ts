import {
  GridLocation,
  MotionType,
  Orientation,
  type MotionData,
} from "$shared";
import { injectable } from "inversify";

export interface IArrowRotationCalculator {
  calculateRotation(motion: MotionData, location: GridLocation): number;
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
   */

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
    [GridLocation.EAST]: 270,
    [GridLocation.SOUTH]: 180,
    [GridLocation.WEST]: 90,
    [GridLocation.NORTHEAST]: 315,
    [GridLocation.SOUTHEAST]: 225,
    [GridLocation.SOUTHWEST]: 135,
    [GridLocation.NORTHWEST]: 45,
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
    [GridLocation.EAST]: 90,
    [GridLocation.SOUTH]: 0,
    [GridLocation.WEST]: 270,
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
    [GridLocation.NORTHEAST]: 315,
    [GridLocation.SOUTHEAST]: 45,
    [GridLocation.SOUTHWEST]: 135,
    [GridLocation.NORTHWEST]: 225,
  };

  private readonly dashCounterClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 0,
    [GridLocation.EAST]: 90,
    [GridLocation.SOUTH]: 180,
    [GridLocation.WEST]: 270,
    [GridLocation.NORTHEAST]: 225,
    [GridLocation.SOUTHEAST]: 135,
    [GridLocation.SOUTHWEST]: 45,
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

  calculateRotation(motion: MotionData, location: GridLocation): number {
    /**
     * Calculate arrow rotation angle based on motion type and location.
     *
     * Args:
     *     motion: Motion data containing type and rotation direction
     *     location: Calculated arrow location
     *
     * Returns:
     *     Rotation angle in degrees (0-360)
     */
    const motionType = motion.motionType?.toLowerCase();

    switch (motionType) {
      case "static":
        return this.calculateStaticRotation(motion, location);
      case "pro":
        return this.calculateProRotation(motion, location);
      case "anti":
        return this.calculateAntiRotation(motion, location);
      case "dash":
        return this.calculateDashRotation(motion, location);
      case "float":
        return this.calculateFloatRotation(motion, location);
      default:
        console.warn(`Unknown motion type: ${motionType}, returning 0.0`);
        return 0.0;
    }
  }

  private calculateStaticRotation(
    motion: MotionData,
    location: GridLocation
  ): number {
    /**
     * Calculate rotation for static arrows.
     * Uses different rotation maps based on whether orientation is radial (IN/OUT) or non-radial (CLOCK/COUNTER).
     * Radial = Diamond mode, Non-radial = Box mode.
     */
    const startOrientation = motion.startOrientation;
    const rotationDirection = motion.rotationDirection?.toLowerCase();

    // Determine if this is a radial orientation (IN/OUT) or non-radial (CLOCK/COUNTER)
    const isRadial =
      startOrientation === Orientation.IN ||
      startOrientation === Orientation.OUT;

    // Select the appropriate rotation map
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

  private calculateDashRotation(
    motion: MotionData,
    location: GridLocation
  ): number {
    /**Calculate rotation for DASH arrows with special NO_ROTATION handling.*/
    const rotationDirection = motion.rotationDirection?.toLowerCase();

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
    /**Calculate rotation for FLOAT arrows (similar to PRO).*/
    return this.calculateProRotation(motion, location);
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
