/**
 * Animator Service Interfaces
 *
 * Clean contracts for dependency injection and testability
 */

import type {
    GridLocation,
    MotionColor,
    MotionData,
    MotionType,
    RotationDirection,
} from "$shared";
import type { AnimatedMotionParams, LetterIdentificationResult, PropStates } from "../../domain";

/**
 * Interface for motion parameter calculations and conversions
 * Now using proper enums throughout - no more string-based parameters!
 */
export interface IMotionParameterService {
  // Core parameter operations
  createDefaultParams(): AnimatedMotionParams;
  updateMotionTypeForLocations(
    params: AnimatedMotionParams
  ): AnimatedMotionParams;

  // Motion type calculations - now using enums
  getMotionType(
    startLocation: GridLocation,
    endLocation: GridLocation
  ): MotionType;
  getAvailableMotionTypes(
    startLocation: GridLocation,
    endLocation: GridLocation
  ): MotionType[];
  calculateRotationDirection(
    motionType: MotionType,
    startLocation: GridLocation,
    endLocation: GridLocation
  ): RotationDirection;

  // Data conversion - no enum mapping needed anymore
  convertToMotionData(
    params: AnimatedMotionParams,
    color?: MotionColor
  ): MotionData;
  convertAnimatedMotionParamsToPropAttributes(
    params: AnimatedMotionParams
  ): Record<string, unknown>;
}

/**
 * Interface for animation control and engine management
 */
export interface IAnimationControlService {
  // Engine lifecycle
  initializeEngine(
    blueParams: AnimatedMotionParams,
    redParams: AnimatedMotionParams
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
