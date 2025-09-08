/**
 * Pictograph Validator Service - Validation of pictograph data
 *
 * Validates pictograph data structures and position sequences.
 * Ensures generated pictographs conform to TKA rules and constraints.
 */

import type { IPictographValidatorService } from "$build/generate/services/contracts/generate-contracts";
import {
  GridLocation,
  GridPosition,
  MotionColor,
  type MotionData,
  MotionType,
  type PictographData,
  RotationDirection,
} from "$shared";
import { injectable } from "inversify";

@injectable()
export class PictographValidatorService implements IPictographValidatorService {
  validatePictograph(pictograph: PictographData): boolean {
    const errors = this.getValidationErrors(pictograph);
    return errors.length === 0;
  }

  validatePictographs(pictographs: PictographData[]): boolean {
    if (!pictographs || pictographs.length === 0) {
      return false;
    }

    // Validate all pictographs in the array
    for (const pictograph of pictographs) {
      if (!this.validatePictograph(pictograph)) {
        return false;
      }
    }

    return true;
  }

  getValidationErrors(pictograph: PictographData): string[] {
    const errors: string[] = [];

    // Validate required fields
    if (!pictograph.id || pictograph.id.length === 0) {
      errors.push("Pictograph ID is required");
    }

    // Validate motions
    if (!pictograph.motions) {
      errors.push("Motions are required");
    } else {
      // Validate blue motion if present
      if (pictograph.motions[MotionColor.BLUE]) {
        errors.push(
          ...this.validateMotionData(
            pictograph.motions[MotionColor.BLUE],
            "blue"
          )
        );
      }

      // Validate red motion if present
      if (pictograph.motions[MotionColor.RED]) {
        errors.push(
          ...this.validateMotionData(pictograph.motions[MotionColor.RED], "red")
        );
      }
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

    return true;
  }

  private validateMotionData(
    motionData: MotionData | null,
    colorName: string
  ): string[] {
    const errors: string[] = [];

    if (!motionData) {
      errors.push(`${colorName} motion data is required`);
      return errors;
    }

    if (!motionData.motionType) {
      errors.push(`${colorName} motion type is required`);
    } else if (!Object.values(MotionType).includes(motionData.motionType)) {
      errors.push(`Invalid ${colorName} motion type: ${motionData.motionType}`);
    }

    if (!motionData.rotationDirection) {
      errors.push(`${colorName} rotation direction is required`);
    } else if (
      !Object.values(RotationDirection).includes(motionData.rotationDirection)
    ) {
      errors.push(
        `Invalid ${colorName} rotation direction: ${motionData.rotationDirection}`
      );
    }

    if (!motionData.startLocation) {
      errors.push(`${colorName} start location is required`);
    } else if (
      !Object.values(GridLocation).includes(motionData.startLocation)
    ) {
      errors.push(
        `Invalid ${colorName} start location: ${motionData.startLocation}`
      );
    }

    if (!motionData.endLocation) {
      errors.push(`${colorName} end location is required`);
    } else if (!Object.values(GridLocation).includes(motionData.endLocation)) {
      errors.push(
        `Invalid ${colorName} end location: ${motionData.endLocation}`
      );
    }

    return errors;
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
}
