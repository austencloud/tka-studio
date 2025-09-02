/**
 * Orientation Calculation Service - Complete port from legacy JsonOriCalculator
 *
 * Exact implementation of legacy orientation calculation algorithms including:
 * - Complete float orientation calculation with handpath direction
 * - Full turn orientation calculation for whole and half turns
 * - Exact motion type differentiation (PRO/STATIC vs ANTI/DASH)
 * - Complete handpath calculation for all location pairs
 */

import type { BeatData, MotionData } from "$domain";
import {
  createMotionData,
  HandPath,
  Location,
  MotionColor,
  MotionType,
  Orientation,
  PropType,
  RotationDirection,
} from "$domain";
import { injectable } from "inversify";

export interface OrientationCalculationServiceInterface {
  calculateEndOrientation(motion: MotionData, color: MotionColor): Orientation;
  updateStartOrientations(nextBeat: BeatData, lastBeat: BeatData): BeatData;
  updateEndOrientations(beat: BeatData): BeatData;
}

@injectable()
export class OrientationCalculationService
  implements OrientationCalculationServiceInterface
{
  private handpathCalculator: HandpathCalculator;

  constructor() {
    this.handpathCalculator = new HandpathCalculator();
  }

  /**
   * Calculate end orientation - exact port from legacy calculate_end_ori()
   */
  calculateEndOrientation(
    motion: MotionData,
    _color: MotionColor
  ): Orientation {
    const motionType = motion.motionType;
    const turns = motion.turns;
    const startOrientation = motion.startOrientation;
    const propRotDir = motion.rotationDirection;
    const startLocation = motion.startLocation;
    const endLocation = motion.endLocation;

    let endOrientation: Orientation;

    if (motionType === MotionType.FLOAT) {
      const handpathDirection = this.handpathCalculator.getHandRotDir(
        startLocation,
        endLocation
      ) as HandPath;
      endOrientation = this.calculateFloatOrientation(
        startOrientation,
        handpathDirection
      );
    } else {
      endOrientation = this.calculateTurnOrientation(
        motionType,
        turns,
        startOrientation,
        propRotDir,
        startLocation,
        endLocation
      );
    }

    if (endOrientation === null || endOrientation === undefined) {
      throw new Error(
        "Calculated end orientation cannot be None. " +
          "Please check the input data and orientation calculator."
      );
    }

    return endOrientation;
  }

  /**
   * Calculate turn orientation - exact port from legacy
   */
  private calculateTurnOrientation(
    motionType: MotionType,
    turns: number | "fl",
    startOrientation: Orientation,
    propRotDir: RotationDirection,
    startLocation: Location,
    endLocation: Location
  ): Orientation {
    if (turns === 0 || turns === 1 || turns === 2 || turns === 3) {
      return this.calculateWholeTurnOrientation(
        motionType,
        turns as number,
        startOrientation,
        propRotDir
      );
    } else if (turns === "fl") {
      const handpathDirection = this.handpathCalculator.getHandRotDir(
        startLocation,
        endLocation
      ) as HandPath;
      return this.calculateFloatOrientation(
        startOrientation,
        handpathDirection
      );
    } else {
      return this.calculateHalfTurnOrientation(
        motionType,
        turns as number,
        startOrientation,
        propRotDir
      );
    }
  }

  /**
   * Calculate whole turn orientation - exact port from legacy
   */
  private calculateWholeTurnOrientation(
    motionType: MotionType,
    turns: number,
    startOrientation: Orientation,
    _propRotDir: RotationDirection
  ): Orientation {
    if (motionType === MotionType.PRO || motionType === MotionType.STATIC) {
      if (turns % 2 === 0) {
        return startOrientation;
      } else {
        return this.switchOrientation(startOrientation);
      }
    } else if (
      motionType === MotionType.ANTI ||
      motionType === MotionType.DASH
    ) {
      if (turns % 2 === 0) {
        return this.switchOrientation(startOrientation);
      } else {
        return startOrientation;
      }
    }
    return startOrientation;
  }

  /**
   * Calculate half turn orientation - exact port from legacy
   */
  private calculateHalfTurnOrientation(
    motionType: MotionType,
    turns: number,
    startOrientation: Orientation,
    propRotDir: RotationDirection
  ): Orientation {
    let orientationMap: Record<string, Orientation>;

    if (motionType === MotionType.ANTI || motionType === MotionType.DASH) {
      orientationMap = {
        [`${Orientation.IN}_${RotationDirection.CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.CLOCK : Orientation.COUNTER,
        [`${Orientation.IN}_${RotationDirection.COUNTER_CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.COUNTER : Orientation.CLOCK,
        [`${Orientation.OUT}_${RotationDirection.CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.COUNTER : Orientation.CLOCK,
        [`${Orientation.OUT}_${RotationDirection.COUNTER_CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.CLOCK : Orientation.COUNTER,
        [`${Orientation.CLOCK}_${RotationDirection.CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.OUT : Orientation.IN,
        [`${Orientation.CLOCK}_${RotationDirection.COUNTER_CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.IN : Orientation.OUT,
        [`${Orientation.COUNTER}_${RotationDirection.CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.IN : Orientation.OUT,
        [`${Orientation.COUNTER}_${RotationDirection.COUNTER_CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.OUT : Orientation.IN,
      };
    } else if (
      motionType === MotionType.PRO ||
      motionType === MotionType.STATIC
    ) {
      orientationMap = {
        [`${Orientation.IN}_${RotationDirection.CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.COUNTER : Orientation.CLOCK,
        [`${Orientation.IN}_${RotationDirection.COUNTER_CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.CLOCK : Orientation.COUNTER,
        [`${Orientation.OUT}_${RotationDirection.CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.CLOCK : Orientation.COUNTER,
        [`${Orientation.OUT}_${RotationDirection.COUNTER_CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.COUNTER : Orientation.CLOCK,
        [`${Orientation.CLOCK}_${RotationDirection.CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.IN : Orientation.OUT,
        [`${Orientation.CLOCK}_${RotationDirection.COUNTER_CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.OUT : Orientation.IN,
        [`${Orientation.COUNTER}_${RotationDirection.CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.OUT : Orientation.IN,
        [`${Orientation.COUNTER}_${RotationDirection.COUNTER_CLOCKWISE}`]:
          turns % 2 === 0.5 ? Orientation.IN : Orientation.OUT,
      };
    } else {
      return startOrientation;
    }

    const key = `${startOrientation}_${propRotDir}`;
    return orientationMap[key] || startOrientation;
  }

  /**
   * Calculate float orientation - exact port from legacy
   */
  private calculateFloatOrientation(
    startOrientation: Orientation,
    handpathDirection: HandPath
  ): Orientation {
    const orientationMap: Record<string, Orientation> = {
      [`${Orientation.IN}_${HandPath.CLOCKWISE}`]: Orientation.CLOCK,
      [`${Orientation.IN}_${HandPath.COUNTER_CLOCKWISE}`]: Orientation.COUNTER,
      [`${Orientation.OUT}_${HandPath.CLOCKWISE}`]: Orientation.COUNTER,
      [`${Orientation.OUT}_${HandPath.COUNTER_CLOCKWISE}`]: Orientation.CLOCK,
      [`${Orientation.CLOCK}_${HandPath.CLOCKWISE}`]: Orientation.OUT,
      [`${Orientation.CLOCK}_${HandPath.COUNTER_CLOCKWISE}`]: Orientation.IN,
      [`${Orientation.COUNTER}_${HandPath.CLOCKWISE}`]: Orientation.IN,
      [`${Orientation.COUNTER}_${HandPath.COUNTER_CLOCKWISE}`]: Orientation.OUT,
    };

    const key = `${startOrientation}_${handpathDirection}`;
    return orientationMap[key] || startOrientation;
  }

  /**
   * Switch orientation - exact port from legacy
   */
  private switchOrientation(ori: Orientation): Orientation {
    const switchMap: Record<string, Orientation> = {
      [Orientation.IN]: Orientation.OUT,
      [Orientation.OUT]: Orientation.IN,
      [Orientation.CLOCK]: Orientation.COUNTER,
      [Orientation.COUNTER]: Orientation.CLOCK,
    };
    return switchMap[ori] || ori;
  }

  /**
   * Update start orientations - returns updated beat data
   */
  updateStartOrientations(nextBeat: BeatData, lastBeat: BeatData): BeatData {
    if (!nextBeat.pictographData || !lastBeat.pictographData) {
      throw new Error("Both beats must have pictographData");
    }

    const lastBlueMotion = lastBeat.pictographData.motions?.["blue"];
    const lastRedMotion = lastBeat.pictographData.motions?.["red"];

    if (!lastBlueMotion?.endOrientation || !lastRedMotion?.endOrientation) {
      throw new Error(
        "End orientations cannot be None. Ensure the previous beat has valid orientations."
      );
    }

    // Create updated motions with new start orientations
    const updatedMotions = { ...nextBeat.pictographData.motions };

    if (updatedMotions.blue) {
      updatedMotions.blue = {
        ...updatedMotions.blue,
        startOrientation: lastBlueMotion.endOrientation,
      };
    }

    if (updatedMotions.red) {
      updatedMotions.red = {
        ...updatedMotions.red,
        startOrientation: lastRedMotion.endOrientation,
      };
    }

    // Return updated beat data
    return {
      ...nextBeat,
      pictographData: {
        ...nextBeat.pictographData,
        motions: updatedMotions,
      },
    };
  }

  /**
   * Update end orientations - returns updated beat data
   */
  updateEndOrientations(beat: BeatData): BeatData {
    if (!beat.pictographData) {
      throw new Error("Beat must have pictographData");
    }

    const updatedMotions = { ...beat.pictographData.motions };

    // Calculate blue end orientation
    const blueMotion = beat.pictographData.motions?.["blue"];
    if (blueMotion) {
      const blueMotionData: MotionData = createMotionData({
        motionType: blueMotion.motionType || MotionType.STATIC,
        rotationDirection:
          blueMotion.rotationDirection || RotationDirection.NO_ROTATION,
        startLocation: blueMotion.startLocation || Location.NORTH,
        endLocation: blueMotion.endLocation || Location.NORTH,
        turns: blueMotion.turns || 0,
        startOrientation: blueMotion.startOrientation || Orientation.IN,
        endOrientation: blueMotion.endOrientation || Orientation.IN,
        isVisible: blueMotion.isVisible ?? true,
        color: MotionColor.BLUE,
        propType: PropType.STAFF, // Default prop type
        arrowLocation: blueMotion.startLocation || Location.NORTH, // Will be calculated
      });

      const calculatedEndOri = this.calculateEndOrientation(
        blueMotionData,
        MotionColor.BLUE
      );

      updatedMotions.blue = {
        ...blueMotion,
        endOrientation: calculatedEndOri,
      };
    }

    // Calculate red end orientation
    const redMotion = beat.pictographData.motions?.["red"];
    if (redMotion) {
      const redMotionData: MotionData = createMotionData({
        motionType: redMotion.motionType || MotionType.STATIC,
        rotationDirection:
          redMotion.rotationDirection || RotationDirection.NO_ROTATION,
        startLocation: redMotion.startLocation || Location.NORTH,
        endLocation: redMotion.endLocation || Location.NORTH,
        turns: redMotion.turns || 0,
        startOrientation: redMotion.startOrientation || Orientation.IN,
        endOrientation: redMotion.endOrientation || Orientation.IN,
        isVisible: redMotion.isVisible ?? true,
        color: MotionColor.RED,
        propType: PropType.STAFF, // Default prop type
        arrowLocation: redMotion.startLocation || Location.NORTH, // Will be calculated
      });

      const calculatedEndOri = this.calculateEndOrientation(
        redMotionData,
        MotionColor.RED
      );

      updatedMotions.red = {
        ...redMotion,
        endOrientation: calculatedEndOri,
      };
    }

    // Return updated beat data
    return {
      ...beat,
      pictographData: {
        ...beat.pictographData,
        motions: updatedMotions,
      },
    };
  }
}

/**
 * Handpath Calculator - Exact port from legacy HandpathCalculator
 *
 * Calculates hand rotation direction based on start and end locations.
 * Complete mapping of all location pairs to handpath directions.
 */
class HandpathCalculator {
  private handRotDirMap: Map<string, string>;

  constructor() {
    // Exact pairs from legacy HandpathCalculator
    const clockwisePairs = [
      [Location.SOUTH, Location.WEST],
      [Location.WEST, Location.NORTH],
      [Location.NORTH, Location.EAST],
      [Location.EAST, Location.SOUTH],
    ];

    const counterClockwisePairs = [
      [Location.WEST, Location.SOUTH],
      [Location.NORTH, Location.WEST],
      [Location.EAST, Location.NORTH],
      [Location.SOUTH, Location.EAST],
    ];

    const diagonalClockwise = [
      [Location.NORTHEAST, Location.SOUTHEAST],
      [Location.SOUTHEAST, Location.SOUTHWEST],
      [Location.SOUTHWEST, Location.NORTHWEST],
      [Location.NORTHWEST, Location.NORTHEAST],
    ];

    const diagonalCounterClockwise = [
      [Location.NORTHEAST, Location.NORTHWEST],
      [Location.NORTHWEST, Location.SOUTHWEST],
      [Location.SOUTHWEST, Location.SOUTHEAST],
      [Location.SOUTHEAST, Location.NORTHEAST],
    ];

    const dashPairs = [
      [Location.SOUTH, Location.NORTH],
      [Location.WEST, Location.EAST],
      [Location.NORTH, Location.SOUTH],
      [Location.EAST, Location.WEST],
      [Location.NORTHEAST, Location.SOUTHWEST],
      [Location.SOUTHEAST, Location.NORTHWEST],
      [Location.SOUTHWEST, Location.NORTHEAST],
      [Location.NORTHWEST, Location.SOUTHEAST],
    ];

    const staticPairs = [
      [Location.NORTH, Location.NORTH],
      [Location.EAST, Location.EAST],
      [Location.SOUTH, Location.SOUTH],
      [Location.WEST, Location.WEST],
      [Location.NORTHEAST, Location.NORTHEAST],
      [Location.SOUTHEAST, Location.SOUTHEAST],
      [Location.SOUTHWEST, Location.SOUTHWEST],
      [Location.NORTHWEST, Location.NORTHWEST],
    ];

    // Build the complete map
    this.handRotDirMap = new Map();

    // Add all mappings
    clockwisePairs.concat(diagonalClockwise).forEach(([start, end]) => {
      this.handRotDirMap.set(`${start}_${end}`, HandPath.CLOCKWISE);
    });

    counterClockwisePairs
      .concat(diagonalCounterClockwise)
      .forEach(([start, end]) => {
        this.handRotDirMap.set(`${start}_${end}`, HandPath.COUNTER_CLOCKWISE);
      });

    dashPairs.forEach(([start, end]) => {
      this.handRotDirMap.set(`${start}_${end}`, HandPath.DASH);
    });

    staticPairs.forEach(([start, end]) => {
      this.handRotDirMap.set(`${start}_${end}`, HandPath.STATIC);
    });
  }

  /**
   * Get hand rotation direction - exact port from legacy
   */
  getHandRotDir(startLocation: string, endLocation: string): string {
    const key = `${startLocation}_${endLocation}`;
    return this.handRotDirMap.get(key) || "NO HAND ROTATION FOUND";
  }
}
