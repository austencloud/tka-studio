/**
 * Orientation Calculation Service
 *
 * Implements the motion orientation calculation logic from legacy and modern desktop apps.
 * Calculates end orientation based on motion type, turns, start orientation, and prop rotation direction.
 */

import {
  Orientation,
  MotionType,
  RotationDirection,
  Location,
} from "$lib/domain/enums";
import type { MotionData } from "$lib/domain/MotionData";

export class OrientationCalculationService {
  /**
   * Calculate end orientation for a motion based on motion type, turns, and start orientation
   */
  calculateEndOrientation(motion: MotionData): Orientation {
    // Handle float case separately (requires special handpath direction calculation)
    if (motion.motion_type === MotionType.FLOAT) {
      return this.calculateFloatOrientation(motion);
    }

    // Validate turns
    if (motion.turns === "fl") {
      return motion.start_ori; // Float handled separately earlier
    }
    const validTurns = [0, 0.5, 1, 1.5, 2, 2.5, 3];
    if (!validTurns.includes(motion.turns)) {
      console.warn(
        `Invalid turns value: ${motion.turns}. Using start orientation.`,
      );
      return motion.start_ori;
    }

    // Whole turn or half turn
    if (motion.turns % 1 === 0) {
      // Whole turns: 0, 1, 2, 3
      return this.calculateWholeTurnOrientation(
        motion.motion_type,
        motion.turns,
        motion.start_ori,
      );
    } else {
      // Half turns: 0.5, 1.5, 2.5
      return this.calculateHalfTurnOrientation(
        motion.motion_type,
        motion.turns,
        motion.start_ori,
        motion.prop_rot_dir,
      );
    }
  }

  /**
   * Switch orientation between complementary pairs
   */
  switchOrientation(orientation: Orientation): Orientation {
    const orientationMap = {
      [Orientation.IN]: Orientation.OUT,
      [Orientation.OUT]: Orientation.IN,
      [Orientation.CLOCK]: Orientation.COUNTER,
      [Orientation.COUNTER]: Orientation.CLOCK,
    };
    return orientationMap[orientation] || orientation;
  }

  /**
   * Calculate orientation for whole turns (0, 1, 2, 3)
   */
  private calculateWholeTurnOrientation(
    motionType: MotionType,
    turns: number,
    startOri: Orientation,
  ): Orientation {
    if (motionType === MotionType.PRO || motionType === MotionType.STATIC) {
      // PRO/STATIC: even turns keep orientation, odd turns switch
      return turns % 2 === 0 ? startOri : this.switchOrientation(startOri);
    } else if (
      motionType === MotionType.ANTI ||
      motionType === MotionType.DASH
    ) {
      // ANTI/DASH: even turns switch orientation, odd turns keep
      return turns % 2 === 0 ? this.switchOrientation(startOri) : startOri;
    }

    return startOri;
  }

  /**
   * Calculate orientation for half turns (0.5, 1.5, 2.5)
   */
  private calculateHalfTurnOrientation(
    motionType: MotionType,
    turns: number,
    startOri: Orientation,
    propRotDir: RotationDirection,
  ): Orientation {
    // Convert prop rotation direction to string for mapping
    const rotDir =
      propRotDir === RotationDirection.CLOCKWISE
        ? "cw"
        : propRotDir === RotationDirection.COUNTER_CLOCKWISE
          ? "ccw"
          : "cw";

    let orientationMap: Record<string, Orientation>;

    if (motionType === MotionType.ANTI || motionType === MotionType.DASH) {
      orientationMap = {
        [`${Orientation.IN}_cw`]:
          turns % 2 === 0.5 ? Orientation.CLOCK : Orientation.COUNTER,
        [`${Orientation.IN}_ccw`]:
          turns % 2 === 0.5 ? Orientation.COUNTER : Orientation.CLOCK,
        [`${Orientation.OUT}_cw`]:
          turns % 2 === 0.5 ? Orientation.COUNTER : Orientation.CLOCK,
        [`${Orientation.OUT}_ccw`]:
          turns % 2 === 0.5 ? Orientation.CLOCK : Orientation.COUNTER,
        [`${Orientation.CLOCK}_cw`]:
          turns % 2 === 0.5 ? Orientation.OUT : Orientation.IN,
        [`${Orientation.CLOCK}_ccw`]:
          turns % 2 === 0.5 ? Orientation.IN : Orientation.OUT,
        [`${Orientation.COUNTER}_cw`]:
          turns % 2 === 0.5 ? Orientation.IN : Orientation.OUT,
        [`${Orientation.COUNTER}_ccw`]:
          turns % 2 === 0.5 ? Orientation.OUT : Orientation.IN,
      };
    } else if (
      motionType === MotionType.PRO ||
      motionType === MotionType.STATIC
    ) {
      orientationMap = {
        [`${Orientation.IN}_cw`]:
          turns % 2 === 0.5 ? Orientation.COUNTER : Orientation.CLOCK,
        [`${Orientation.IN}_ccw`]:
          turns % 2 === 0.5 ? Orientation.CLOCK : Orientation.COUNTER,
        [`${Orientation.OUT}_cw`]:
          turns % 2 === 0.5 ? Orientation.CLOCK : Orientation.COUNTER,
        [`${Orientation.OUT}_ccw`]:
          turns % 2 === 0.5 ? Orientation.COUNTER : Orientation.CLOCK,
        [`${Orientation.CLOCK}_cw`]:
          turns % 2 === 0.5 ? Orientation.IN : Orientation.OUT,
        [`${Orientation.CLOCK}_ccw`]:
          turns % 2 === 0.5 ? Orientation.OUT : Orientation.IN,
        [`${Orientation.COUNTER}_cw`]:
          turns % 2 === 0.5 ? Orientation.OUT : Orientation.IN,
        [`${Orientation.COUNTER}_ccw`]:
          turns % 2 === 0.5 ? Orientation.IN : Orientation.OUT,
      };
    } else {
      return startOri;
    }

    const key = `${startOri}_${rotDir}`;
    return orientationMap[key] || startOri;
  }

  /**
   * Calculate orientation for float motions (simplified for now)
   * TODO: Implement proper handpath direction calculation
   */
  private calculateFloatOrientation(motion: MotionData): Orientation {
    // For now, return a simple calculation
    // In the full implementation, this would use handpath direction calculation
    console.log("🌊 Float orientation calculation (simplified)");
    return motion.start_ori;
  }

  /**
   * Create motion data with properly calculated end orientation
   */
  createMotionWithCalculatedOrientation(
    motionType: MotionType,
    propRotDir: RotationDirection,
    startLoc: Location,
    endLoc: Location,
    turns: number = 0,
    startOri: Orientation = Orientation.IN,
  ): MotionData {
    // Create initial motion data
    const motion: MotionData = {
      motion_type: motionType,
      prop_rot_dir: propRotDir,
      start_loc: startLoc,
      end_loc: endLoc,
      turns,
      start_ori: startOri,
      end_ori: startOri, // Will be calculated
      is_visible: true,
      prefloat_motion_type: null,
      prefloat_prop_rot_dir: null,
    };

    // Return new object with calculated end orientation (immutability / readonly safety)
    return { ...motion, end_ori: this.calculateEndOrientation(motion) };
  }
}
