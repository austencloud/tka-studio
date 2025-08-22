/**
 * Motion Tester Service Interfaces
 *
 * Clean contracts for dependency injection and testability
 */

import type { MotionData } from "$lib/domain/MotionData";
import type {
  MotionType,
  Location,
  RotationDirection,
  MotionColor,
} from "$lib/domain/enums";
import type { MotionTestParams } from "./MotionParameterService";
import type {
  // AnimationState,
  // PropVisibility,
  PropStates,
} from "./AnimationControlService";

/**
 * Interface for motion parameter calculations and conversions
 * Now using proper enums throughout - no more string-based parameters!
 */
export interface IMotionParameterService {
  // Core parameter operations
  createDefaultParams(): MotionTestParams;
  updateMotionTypeForLocations(params: MotionTestParams): MotionTestParams;

  // Motion type calculations - now using enums
  getMotionType(startLocation: Location, endLocation: Location): MotionType;
  getAvailableMotionTypes(
    startLocation: Location,
    endLocation: Location
  ): MotionType[];
  calculateRotationDirection(
    motionType: MotionType,
    startLocation: Location,
    endLocation: Location
  ): RotationDirection;

  // Data conversion - no enum mapping needed anymore
  convertToMotionData(
    params: MotionTestParams,
    color?: MotionColor
  ): MotionData;
  convertMotionTestParamsToPropAttributes(
    params: MotionTestParams
  ): Record<string, unknown>;
}

/**
 * Interface for animation control and engine management
 */
export interface IAnimationControlService {
  // Engine lifecycle
  initializeEngine(
    blueParams: MotionTestParams,
    redParams: MotionTestParams
  ): Promise<boolean>;
  isEngineInitialized(): boolean;
  dispose(): void;

  // Animation control
  setProgress(progress: number): void;
  getProgress(): number;
  startAnimation(): void;
  stopAnimation(): void;
  resetAnimation(): void;
  isPlaying(): boolean;

  // State queries
  getCurrentPropStates(): PropStates;
  getCurrentBeat(): number;
  getTotalBeats(): number;

  // Prop visibility
  setPropVisibility(prop: MotionColor, visible: boolean): void;
  getPropVisibility(prop: MotionColor): boolean;
}

// YAGNI: Removed unused IEnumConversionService interface
// We use enums directly now - no string conversion needed!
