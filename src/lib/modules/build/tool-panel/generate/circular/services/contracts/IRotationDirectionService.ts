/**
 * Rotation Direction Service Interface
 *
 * Determines rotation directions for blue and red props based on prop continuity.
 */
import { PropContinuity } from "../../../shared/domain/models/generate-models";

export interface RotationDirections {
  blueRotationDirection: string;
  redRotationDirection: string;
}

export interface IRotationDirectionService {
  /**
   * Determine rotation directions based on prop continuity
   * @param propContinuity - Continuous or random prop continuity
   * @returns Rotation directions for blue and red props
   */
  determineRotationDirections(propContinuity?: PropContinuity): RotationDirections;
}
