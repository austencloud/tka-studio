/**
 * Motion Parameter Service Interface
 *
 * Interface for motion parameter calculations and conversions.
 * Uses proper domain types - no more string-based parameters!
 */

import type {
  Location,
  MotionColor,
  MotionData,
  MotionType,
  RotationDirection,
} from "$shared/domain";
import type { AnimatedMotionParams } from "../../domain";

export interface IMotionParameterService {
  // Core parameter operations
  createDefaultParams(): AnimatedMotionParams;
  updateMotionTypeForLocations(
    params: AnimatedMotionParams
  ): AnimatedMotionParams;

  // Motion type calculations - now using enums
  getMotionType(startLocation: Location, endLocation: Location): MotionType;
  getAvailableMotionTypes(
    startLocation: Location,
    endLocation: Location
  ): MotionType[];

  // Rotation calculations
  calculateRotationDirection(
    motionType: MotionType,
    startLocation: Location,
    endLocation: Location
  ): RotationDirection;

  // Conversion utilities
  convertAnimatedMotionParamsToPropAttributes(
    params: AnimatedMotionParams
  ): Record<string, unknown>;
  convertToMotionData(
    params: AnimatedMotionParams,
    color: MotionColor
  ): MotionData;
}
