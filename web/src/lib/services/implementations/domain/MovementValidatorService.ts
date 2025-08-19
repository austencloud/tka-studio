/**
 * Movement Validator Service - Validation of movement data
 *
 * Validates movement data structures, position sequences, and movement sets.
 * Ensures generated movements conform to TKA rules and constraints.
 */

import type { IMovementValidatorService } from "../../interfaces/generation-interfaces";
import type {
  MovementData,
  MovementSet,
  HandMovement,
} from "$lib/domain/MovementData";
import {
  GridPosition,
  Timing,
  Direction,
  MotionType,
  RotationDirection,
  Location,
} from "$lib/domain/enums";

export class MovementValidatorService implements IMovementValidatorService {
  validateMovement(movement: MovementData): boolean {
    const errors = this.getValidationErrors(movement);
    return errors.length === 0;
  }

  validateMovementSet(movementSet: MovementSet): boolean {
    if (!movementSet.letter || movementSet.letter.length === 0) {
      return false;
    }

    if (!movementSet.movements || movementSet.movements.length === 0) {
      return false;
    }

    if (!movementSet.pattern) {
      return false;
    }

    // Validate all movements in the set
    for (const movement of movementSet.movements) {
      if (!this.validateMovement(movement)) {
        return false;
      }

      // Check that movement belongs to the set
      if (movement.letter !== movementSet.letter) {
        return false;
      }
    }

    return true;
  }

  getValidationErrors(movement: MovementData): string[] {
    const errors: string[] = [];

    // Validate required fields
    if (!movement.letter || movement.letter.length === 0) {
      errors.push("Movement letter is required");
    }

    if (!movement.startPosition) {
      errors.push("Start position is required");
    }

    if (!movement.endPosition) {
      errors.push("End position is required");
    }

    if (!movement.timing) {
      errors.push("Timing is required");
    }

    if (!movement.direction) {
      errors.push("Direction is required");
    }

    // Validate hand movements
    errors.push(...this.validateHandMovement(movement.blueHand, "blue"));
    errors.push(...this.validateHandMovement(movement.redHand, "red"));

    // Validate enum values
    if (movement.timing && !Object.values(Timing).includes(movement.timing)) {
      errors.push(`Invalid timing: ${movement.timing}`);
    }

    if (
      movement.direction &&
      !Object.values(Direction).includes(movement.direction)
    ) {
      errors.push(`Invalid direction: ${movement.direction}`);
    }

    if (
      movement.startPosition &&
      !Object.values(GridPosition).includes(movement.startPosition)
    ) {
      errors.push(`Invalid start position: ${movement.startPosition}`);
    }

    if (
      movement.endPosition &&
      !Object.values(GridPosition).includes(movement.endPosition)
    ) {
      errors.push(`Invalid end position: ${movement.endPosition}`);
    }

    // Validate position compatibility
    if (movement.startPosition && movement.endPosition) {
      const positionError = this.validatePositionTransition(
        movement.startPosition,
        movement.endPosition
      );
      if (positionError) {
        errors.push(positionError);
      }
    }

    // Validate motion combinations
    const motionError = this.validateMotionCombination(movement);
    if (motionError) {
      errors.push(motionError);
    }

    return errors;
  }

  validatePositionSequence(positions: GridPosition[]): boolean {
    if (positions.length === 0) {
      return false;
    }

    // Check if all positions belong to the same system
    const firstSystem = this.getPositionSystem(positions[0]);
    for (const position of positions) {
      if (this.getPositionSystem(position) !== firstSystem) {
        return false;
      }
    }

    // Check for valid transitions
    for (let i = 0; i < positions.length - 1; i++) {
      const error = this.validatePositionTransition(
        positions[i],
        positions[i + 1]
      );
      if (error) {
        return false;
      }
    }

    return true;
  }

  private validateHandMovement(
    handMovement: HandMovement | null,
    handName: string
  ): string[] {
    const errors: string[] = [];

    if (!handMovement) {
      errors.push(`${handName} hand movement is required`);
      return errors;
    }

    if (!handMovement.motionType) {
      errors.push(`${handName} hand motion type is required`);
    } else if (!Object.values(MotionType).includes(handMovement.motionType)) {
      errors.push(
        `Invalid ${handName} hand motion type: ${handMovement.motionType}`
      );
    }

    if (!handMovement.rotationDirection) {
      errors.push(`${handName} hand rotation direction is required`);
    } else if (
      !Object.values(RotationDirection).includes(handMovement.rotationDirection)
    ) {
      errors.push(
        `Invalid ${handName} hand rotation direction: ${handMovement.rotationDirection}`
      );
    }

    if (!handMovement.startLocation) {
      errors.push(`${handName} hand start location is required`);
    } else if (!Object.values(Location).includes(handMovement.startLocation)) {
      errors.push(
        `Invalid ${handName} hand start location: ${handMovement.startLocation}`
      );
    }

    if (!handMovement.endLocation) {
      errors.push(`${handName} hand end location is required`);
    } else if (!Object.values(Location).includes(handMovement.endLocation)) {
      errors.push(
        `Invalid ${handName} hand end location: ${handMovement.endLocation}`
      );
    }

    return errors;
  }

  private validatePositionTransition(
    start: GridPosition,
    end: GridPosition
  ): string | null {
    const startSystem = this.getPositionSystem(start);
    const endSystem = this.getPositionSystem(end);

    // Allow transitions within same system or to different systems for special patterns
    if (startSystem === endSystem) {
      return null; // Same system transitions are generally valid
    }

    // Cross-system transitions are valid for certain movement types
    return null;
  }

  private validateMotionCombination(movement: MovementData): string | null {
    const { blueHand, redHand, timing, direction } = movement;

    // Static motions should have no rotation
    if (
      blueHand.motionType === MotionType.STATIC &&
      blueHand.rotationDirection !== RotationDirection.NO_ROTATION
    ) {
      return "Static blue motion should have no rotation";
    }

    if (
      redHand.motionType === MotionType.STATIC &&
      redHand.rotationDirection !== RotationDirection.NO_ROTATION
    ) {
      return "Static red motion should have no rotation";
    }

    // Dash motions should have no rotation
    if (
      blueHand.motionType === MotionType.DASH &&
      blueHand.rotationDirection !== RotationDirection.NO_ROTATION
    ) {
      return "Dash blue motion should have no rotation";
    }

    if (
      redHand.motionType === MotionType.DASH &&
      redHand.rotationDirection !== RotationDirection.NO_ROTATION
    ) {
      return "Dash red motion should have no rotation";
    }

    // Static motions should have same start and end locations
    if (
      blueHand.motionType === MotionType.STATIC &&
      blueHand.startLocation !== blueHand.endLocation
    ) {
      return "Static blue motion should have same start and end location";
    }

    if (
      redHand.motionType === MotionType.STATIC &&
      redHand.startLocation !== redHand.endLocation
    ) {
      return "Static red motion should have same start and end location";
    }

    // Direction validation
    if (direction === Direction.SAME) {
      // For same direction, both hands should generally move in coordinated fashion
      // This is pattern-specific, so we'll be lenient here
    }

    if (direction === Direction.OPP) {
      // For opposite direction, hands should move in opposition
      // This is pattern-specific, so we'll be lenient here
    }

    if (direction === Direction.NONE) {
      // For no direction constraint
      if (timing !== Timing.NONE) {
        return "Direction NONE should only be used with timing NONE";
      }
    }

    return null;
  }

  private getPositionSystem(
    position: GridPosition
  ): "alpha" | "beta" | "gamma" {
    const posStr = position.toString();
    if (posStr.startsWith("alpha")) return "alpha";
    if (posStr.startsWith("beta")) return "beta";
    if (posStr.startsWith("gamma")) return "gamma";
    throw new Error(`Unknown position system for: ${position}`);
  }

  /**
   * Check if a movement follows standard TKA conventions
   */
  isStandardMovement(movement: MovementData): boolean {
    const errors = this.getValidationErrors(movement);
    if (errors.length > 0) {
      return false;
    }

    // Additional checks for standard movements
    const { timing, direction } = movement;

    // Standard movements should have recognized timing and direction
    if (timing === Timing.NONE && direction !== Direction.NONE) {
      return false;
    }

    if (direction === Direction.NONE && timing !== Timing.NONE) {
      return false;
    }

    return true;
  }

  /**
   * Validate that all movements in a set follow the same pattern
   */
  validatePatternConsistency(movementSet: MovementSet): string[] {
    const errors: string[] = [];
    const { movements, pattern } = movementSet;

    if (movements.length === 0) {
      errors.push("Movement set must contain at least one movement");
      return errors;
    }

    const firstMovement = movements[0];

    // Check that all movements have the same timing and direction
    for (const movement of movements) {
      if (movement.timing !== firstMovement.timing) {
        errors.push(
          `Inconsistent timing in movement set: expected ${firstMovement.timing}, got ${movement.timing}`
        );
      }

      if (movement.direction !== firstMovement.direction) {
        errors.push(
          `Inconsistent direction in movement set: expected ${firstMovement.direction}, got ${movement.direction}`
        );
      }

      if (movement.letter !== pattern.letter) {
        errors.push(
          `Movement letter ${movement.letter} does not match pattern letter ${pattern.letter}`
        );
      }
    }

    return errors;
  }
}
