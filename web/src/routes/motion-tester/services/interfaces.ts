/**
 * Motion Tester Service Interfaces
 *
 * Clean contracts for dependency injection and testability
 */

import type { MotionData } from "$lib/domain/MotionData";
import type {
  Orientation,
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
 */
export interface IMotionParameterService {
  // Core parameter operations
  createDefaultParams(): MotionTestParams;
  updateMotionTypeForLocations(params: MotionTestParams): MotionTestParams;

  // Motion type calculations
  getMotionType(startLoc: string, endLoc: string): string;
  getAvailableMotionTypes(startLoc: string, endLoc: string): string[];
  calculateRotationDirection(
    motionType: string,
    startLoc: string,
    endLoc: string
  ): string;

  // Enum mapping
  mapMotionTypeToEnum(motionType: string): MotionType;
  mapOrientationToEnum(orientation: string): Orientation;
  mapRotationDirectionToEnum(rotDir: string): RotationDirection;
  mapLocationToEnum(location: string): Location;

  // Data conversion
  convertToMotionData(params: MotionTestParams): MotionData;
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

/**
 * Interface for enum conversion utilities
 */
export interface IEnumConversionService {
  // String to enum conversions
  stringToOrientation(str: string): Orientation;
  stringToMotionType(str: string): MotionType;
  stringToLocation(str: string): Location;
  stringToRotationDirection(str: string): RotationDirection;

  // Enum to string conversions
  orientationToString(orientation: Orientation): string;
  motionTypeToString(motionType: MotionType): string;
  locationToString(location: Location): string;
  rotationDirectionToString(rotDir: RotationDirection): string;
}
