/**
 * Orientation Calculation Service - Complete port from legacy JsonOriCalculator
 *
 * Exact implementation of legacy orientation calculation algorithms including:
 * - Complete float orientation calculation with handpath direction
 * - Full turn orientation calculation for whole and half turns
 * - Exact motion type differentiation (PRO/STATIC vs ANTI/DASH)
 * - Complete handpath calculation for all location pairs
 */

import type { BeatData } from "$lib/domain/BeatData";
import type { MotionData } from "$lib/domain/MotionData";
import {
  Orientation,
  MotionType,
  Location,
  RotationDirection,
  HandPath,
  MotionColor,
} from "$lib/domain/enums";

export interface OrientationCalculationServiceInterface {
  calculateEndOrientation(motion: MotionData, color: MotionColor): string;
  updateStartOrientations(nextBeat: BeatData, lastBeat: BeatData): BeatData;
  updateEndOrientations(beat: BeatData): BeatData;
}

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
  calculateEndOrientation(motion: MotionData, _color: MotionColor): string {
    const motionType = motion.motion_type;
    const turns = motion.turns;
    const startOri = motion.start_ori;
    const propRotDir = motion.prop_rot_dir;
    const startLoc = motion.start_loc;
    const endLoc = motion.end_loc;

    let endOri: string;

    if (motionType === MotionType.FLOAT) {
      const handpathDirection = this.handpathCalculator.getHandRotDir(
        startLoc,
        endLoc
      );
      endOri = this.calculateFloatOrientation(startOri, handpathDirection);
    } else {
      endOri = this.calculateTurnOrientation(
        motionType,
        turns,
        startOri,
        propRotDir,
        startLoc,
        endLoc
      );
    }

    if (endOri === null || endOri === undefined) {
      throw new Error(
        "Calculated end orientation cannot be None. " +
          "Please check the input data and orientation calculator."
      );
    }

    return endOri;
  }

  /**
   * Calculate turn orientation - exact port from legacy
   */
  private calculateTurnOrientation(
    motionType: string,
    turns: number | "fl",
    startOri: string,
    propRotDir: string,
    startLoc: string,
    endLoc: string
  ): string {
    if (turns === 0 || turns === 1 || turns === 2 || turns === 3) {
      return this.calculateWholeTurnOrientation(
        motionType,
        turns as number,
        startOri,
        propRotDir
      );
    } else if (turns === "fl") {
      const handpathDirection = this.handpathCalculator.getHandRotDir(
        startLoc,
        endLoc
      );
      return this.calculateFloatOrientation(startOri, handpathDirection);
    } else {
      return this.calculateHalfTurnOrientation(
        motionType,
        turns as number,
        startOri,
        propRotDir
      );
    }
  }

  /**
   * Calculate whole turn orientation - exact port from legacy
   */
  private calculateWholeTurnOrientation(
    motionType: string,
    turns: number,
    startOri: string,
    _propRotDir: string
  ): string {
    if (motionType === MotionType.PRO || motionType === MotionType.STATIC) {
      if (turns % 2 === 0) {
        return startOri;
      } else {
        return this.switchOrientation(startOri);
      }
    } else if (
      motionType === MotionType.ANTI ||
      motionType === MotionType.DASH
    ) {
      if (turns % 2 === 0) {
        return this.switchOrientation(startOri);
      } else {
        return startOri;
      }
    }
    return startOri;
  }

  /**
   * Calculate half turn orientation - exact port from legacy
   */
  private calculateHalfTurnOrientation(
    motionType: string,
    turns: number,
    startOri: string,
    propRotDir: string
  ): string {
    let orientationMap: Record<string, string>;

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
      return startOri;
    }

    const key = `${startOri}_${propRotDir}`;
    return orientationMap[key] || startOri;
  }

  /**
   * Calculate float orientation - exact port from legacy
   */
  private calculateFloatOrientation(
    startOri: string,
    handpathDirection: string
  ): string {
    const orientationMap: Record<string, string> = {
      [`${Orientation.IN}_${HandPath.CLOCKWISE}`]: Orientation.CLOCK,
      [`${Orientation.IN}_${HandPath.COUNTER_CLOCKWISE}`]: Orientation.COUNTER,
      [`${Orientation.OUT}_${HandPath.CLOCKWISE}`]: Orientation.COUNTER,
      [`${Orientation.OUT}_${HandPath.COUNTER_CLOCKWISE}`]: Orientation.CLOCK,
      [`${Orientation.CLOCK}_${HandPath.CLOCKWISE}`]: Orientation.OUT,
      [`${Orientation.CLOCK}_${HandPath.COUNTER_CLOCKWISE}`]: Orientation.IN,
      [`${Orientation.COUNTER}_${HandPath.CLOCKWISE}`]: Orientation.IN,
      [`${Orientation.COUNTER}_${HandPath.COUNTER_CLOCKWISE}`]: Orientation.OUT,
    };

    const key = `${startOri}_${handpathDirection}`;
    return orientationMap[key] || startOri;
  }

  /**
   * Switch orientation - exact port from legacy
   */
  private switchOrientation(ori: string): string {
    const switchMap: Record<string, string> = {
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
    if (!nextBeat.pictograph_data || !lastBeat.pictograph_data) {
      throw new Error("Both beats must have pictograph_data");
    }

    const lastBlueMotion = lastBeat.pictograph_data.motions?.["blue"];
    const lastRedMotion = lastBeat.pictograph_data.motions?.["red"];

    if (!lastBlueMotion?.end_ori || !lastRedMotion?.end_ori) {
      throw new Error(
        "End orientations cannot be None. Ensure the previous beat has valid orientations."
      );
    }

    // Create updated motions with new start orientations
    const updatedMotions = { ...nextBeat.pictograph_data.motions };

    if (updatedMotions.blue) {
      updatedMotions.blue = {
        ...updatedMotions.blue,
        start_ori: lastBlueMotion.end_ori,
      };
    }

    if (updatedMotions.red) {
      updatedMotions.red = {
        ...updatedMotions.red,
        start_ori: lastRedMotion.end_ori,
      };
    }

    // Return updated beat data
    return {
      ...nextBeat,
      pictograph_data: {
        ...nextBeat.pictograph_data,
        motions: updatedMotions,
      },
    };
  }

  /**
   * Update end orientations - returns updated beat data
   */
  updateEndOrientations(beat: BeatData): BeatData {
    if (!beat.pictograph_data) {
      throw new Error("Beat must have pictograph_data");
    }

    const updatedMotions = { ...beat.pictograph_data.motions };

    // Calculate blue end orientation
    const blueMotion = beat.pictograph_data.motions?.["blue"];
    if (blueMotion) {
      const blueMotionData: MotionData = {
        motion_type: blueMotion.motion_type || MotionType.STATIC,
        prop_rot_dir: blueMotion.prop_rot_dir || RotationDirection.NO_ROTATION,
        start_loc: blueMotion.start_loc || Location.NORTH,
        end_loc: blueMotion.end_loc || Location.NORTH,
        turns: blueMotion.turns || 0,
        start_ori: blueMotion.start_ori || Orientation.IN,
        end_ori: blueMotion.end_ori || Orientation.IN,
        is_visible: blueMotion.is_visible ?? true,
      };

      const calculatedEndOri = this.calculateEndOrientation(
        blueMotionData,
        MotionColor.BLUE
      );

      updatedMotions.blue = {
        ...blueMotion,
        end_ori: calculatedEndOri as any, // Cast to match the motion's orientation type
      };
    }

    // Calculate red end orientation
    const redMotion = beat.pictograph_data.motions?.["red"];
    if (redMotion) {
      const redMotionData: MotionData = {
        motion_type: redMotion.motion_type || MotionType.STATIC,
        prop_rot_dir: redMotion.prop_rot_dir || RotationDirection.NO_ROTATION,
        start_loc: redMotion.start_loc || Location.NORTH,
        end_loc: redMotion.end_loc || Location.NORTH,
        turns: redMotion.turns || 0,
        start_ori: redMotion.start_ori || Orientation.IN,
        end_ori: redMotion.end_ori || Orientation.IN,
        is_visible: redMotion.is_visible ?? true,
      };

      const calculatedEndOri = this.calculateEndOrientation(
        redMotionData,
        MotionColor.RED
      );

      updatedMotions.red = {
        ...redMotion,
        end_ori: calculatedEndOri as any, // Cast to match the motion's orientation type
      };
    }

    // Return updated beat data
    return {
      ...beat,
      pictograph_data: {
        ...beat.pictograph_data,
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
  getHandRotDir(startLoc: string, endLoc: string): string {
    const key = `${startLoc}_${endLoc}`;
    return this.handRotDirMap.get(key) || "NO HAND ROTATION FOUND";
  }
}
