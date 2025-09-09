import { GridLocation, MotionType, type MotionData } from "$shared";
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

  private readonly staticRotationMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 180.0,
    [GridLocation.NORTHEAST]: 225.0,
    [GridLocation.EAST]: 270.0,
    [GridLocation.SOUTHEAST]: 315.0,
    [GridLocation.SOUTH]: 0.0,
    [GridLocation.SOUTHWEST]: 45.0,
    [GridLocation.WEST]: 90.0,
    [GridLocation.NORTHWEST]: 135.0,
  };

  private readonly proClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 225,
    [GridLocation.EAST]: 315,
    [GridLocation.SOUTH]: 45,
    [GridLocation.WEST]: 135,
    [GridLocation.NORTHEAST]: 0,
    [GridLocation.SOUTHEAST]: 90,
    [GridLocation.SOUTHWEST]: 180,
    [GridLocation.NORTHWEST]: 270,
  };

  private readonly proCounterClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 225,
    [GridLocation.EAST]: 135,
    [GridLocation.SOUTH]: 45,
    [GridLocation.WEST]: 315,
    [GridLocation.NORTHEAST]: 90,
    [GridLocation.SOUTHEAST]: 180,
    [GridLocation.SOUTHWEST]: 270,
    [GridLocation.NORTHWEST]: 0,
  };

  private readonly antiClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 315,
    [GridLocation.EAST]: 225,
    [GridLocation.SOUTH]: 135,
    [GridLocation.WEST]: 45,
    [GridLocation.NORTHEAST]: 90,
    [GridLocation.SOUTHEAST]: 180,
    [GridLocation.SOUTHWEST]: 270,
    [GridLocation.NORTHWEST]: 0,
  };

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
    [GridLocation.NORTH]: 270,
    [GridLocation.EAST]: 0,
    [GridLocation.SOUTH]: 90,
    [GridLocation.WEST]: 180,
    [GridLocation.NORTHEAST]: 315,
    [GridLocation.SOUTHEAST]: 45,
    [GridLocation.SOUTHWEST]: 135,
    [GridLocation.NORTHWEST]: 225,
  };

  private readonly dashCounterClockwiseMap: Record<GridLocation, number> = {
    [GridLocation.NORTH]: 270,
    [GridLocation.EAST]: 180,
    [GridLocation.SOUTH]: 90,
    [GridLocation.WEST]: 0,
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
        return this.calculateStaticRotation(location);
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

  private calculateStaticRotation(location: GridLocation): number {
    /**Calculate rotation for static arrows (point inward).*/
    return this.staticRotationMap[location] || 0.0;
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

    if (rotationDirection === "noRotation" || rotationDirection === "none") {
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
