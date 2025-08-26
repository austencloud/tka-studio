/**
 * Animator Service Interfaces
 *
 * Defines contracts for all animator services following TKA's DI patterns.
 * These interfaces enable dependency injection and improve testability.
 */

import { createServiceInterface } from "../types";
import type { SequenceData, BeatData, MotionData } from "$lib/domain";
import type { PropState } from "$lib/components/animator/types/PropState";

// ============================================================================
// CORE ANIMATOR INTERFACES
// ============================================================================

/**
 * Interface for beat calculation service
 */
export interface IBeatCalculationService {
  calculateBeatState(
    currentBeat: number,
    beats: readonly BeatData[],
    totalBeats: number
  ): BeatCalculationResult;
  validateBeats(beats: readonly BeatData[]): boolean;
  getBeatSafely(beats: readonly BeatData[], index: number): BeatData | null;
  calculateTotalDuration(beats: readonly BeatData[]): number;
  findBeatByNumber(
    beats: readonly BeatData[],
    beatNumber: number
  ): BeatData | null;
}

export interface BeatCalculationResult {
  currentBeatIndex: number;
  beatProgress: number;
  currentBeatData: BeatData;
  isValid: boolean;
}

/**
 * Interface for prop interpolation service
 */
export interface IPropInterpolationService {
  interpolatePropAngles(
    currentBeatData: BeatData,
    beatProgress: number
  ): InterpolationResult;
  calculateInitialAngles(firstBeat: BeatData): InterpolationResult;
  getMotionData(beatData: BeatData): { blue: MotionData; red: MotionData };
  getEndpoints(beatData: BeatData): {
    blue: MotionEndpoints;
    red: MotionEndpoints;
  };
}

export interface InterpolationResult {
  blueAngles: {
    centerPathAngle: number;
    staffRotationAngle: number;
  };
  redAngles: {
    centerPathAngle: number;
    staffRotationAngle: number;
  };
  isValid: boolean;
}

/**
 * Interface for animation state service
 */
export interface IAnimationStateService {
  updatePropStates(interpolationResult: InterpolationResult): PropStates;
  getBluePropState(): PropState;
  getRedPropState(): PropState;
  getPropStates(): PropStates;
  updateBluePropState(updates: Partial<PropState>): void;
  updateRedPropState(updates: Partial<PropState>): void;
  setPropStates(blue: PropState, red: PropState): void;
  resetPropStates(): void;
}

export interface PropStates {
  blue: PropState;
  red: PropState;
}

/**
 * Interface for sequence animation orchestrator
 */
export interface ISequenceAnimationOrchestrator {
  initializeWithDomainData(sequenceData: SequenceData): boolean;
  calculateState(currentBeat: number): void;
  getMetadata(): SequenceMetadata;
  getCurrentPropStates(): PropStates;
  isInitialized(): boolean;
  dispose(): void;
}

export interface SequenceMetadata {
  word: string;
  author: string;
  totalBeats: number;
}

/**
 * Interface for animation engine (legacy wrapper)
 */
export interface ISequenceAnimationEngine {
  initializeWithDomainData(sequenceData: SequenceData): boolean;
  calculateState(currentBeat: number): void;
  getMetadata(): SequenceMetadata;
  getCurrentPropStates(): PropStates;
  isInitialized(): boolean;
  dispose(): void;
}

// ============================================================================
// MATH SERVICE INTERFACES
// ============================================================================

/**
 * Interface for angle calculation service
 */
export interface IAngleCalculationService {
  normalizeAnglePositive(angle: number): number;
  normalizeAngleSigned(angle: number): number;
  mapLocationToAngle(location: string): number;
  mapOrientationToAngle(orientation: string): number;
  lerpAngle(startAngle: number, endAngle: number, progress: number): number;
}

/**
 * Interface for motion calculation service
 */
export interface IMotionCalculationService {
  calculateProIsolationStaffAngle(
    centerPathAngle: number,
    rotationDirection: string
  ): number;
  calculateAntiIsolationStaffAngle(
    centerPathAngle: number,
    rotationDirection: string
  ): number;
  calculateStaticStaffAngle(centerPathAngle: number): number;
  calculateDashStaffAngle(
    centerPathAngle: number,
    rotationDirection: string
  ): number;
  calculateFloatStaffAngle(
    centerPathAngle: number,
    rotationDirection: string
  ): number;
}

/**
 * Interface for endpoint calculation service
 */
export interface IEndpointCalculationService {
  calculateMotionEndpoints(motionData: MotionData): MotionEndpoints;
}

export interface MotionEndpoints {
  startCenterAngle: number;
  startStaffAngle: number;
  targetCenterAngle: number;
  targetStaffAngle: number;
}

/**
 * Interface for coordinate update service
 */
export interface ICoordinateUpdateService {
  updateCoordinatesFromAngle(propState: PropState): void;
  calculateCoordinatesFromAngle(angle: number): { x: number; y: number };
}

// ============================================================================
// CANVAS SERVICE INTERFACES
// ============================================================================

/**
 * Interface for canvas renderer
 */
export interface ICanvasRenderer {
  renderScene(
    ctx: CanvasRenderingContext2D,
    canvasSize: number,
    gridVisible: boolean,
    gridImage: HTMLImageElement | null,
    blueStaffImage: HTMLImageElement | null,
    redStaffImage: HTMLImageElement | null,
    blueProp: PropState,
    redProp: PropState
  ): void;
}

/**
 * Interface for SVG generator
 */
import { GridMode } from "$lib/domain";

export interface ISVGGenerator {
  generateGridSvg(gridMode?: GridMode): string;
  generateBlueStaffSvg(): string;
  generateRedStaffSvg(): string;
}

// ============================================================================
// UTILITY SERVICE INTERFACES
// ============================================================================

/**
 * Interface for test sequence factory
 */
export interface ITestSequenceFactory {
  createTestSequence(word?: string, author?: string): SequenceData;
  createSingleBeatTestSequence(motionType?: string): SequenceData;
  createComplexTestSequence(): SequenceData;
}

/**
 * Interface for SVG to image converter
 */
export interface ISVGToImageConverter {
  svgStringToImage(
    svgString: string,
    width: number,
    height: number
  ): Promise<HTMLImageElement>;
}

// ============================================================================
// SERVICE INTERFACE DEFINITIONS FOR DI CONTAINER
// ============================================================================

// Import implementations (will be created next)
import { BeatCalculationService } from "$lib/animator/core/services/BeatCalculationService";
import { PropInterpolationService } from "$lib/animator/core/services/PropInterpolationService";
import { AnimationStateService } from "$lib/animator/core/services/AnimationStateService";
import { SequenceAnimationOrchestrator } from "$lib/animator/core/services/SequenceAnimationOrchestrator";
import { SequenceAnimationEngine } from "$lib/animator/core/engine/sequence-animation-engine";

// Create service interfaces for DI container
export const IBeatCalculationServiceInterface = createServiceInterface(
  "IBeatCalculationService",
  BeatCalculationService
);

export const IPropInterpolationServiceInterface = createServiceInterface(
  "IPropInterpolationService",
  PropInterpolationService
);

export const IAnimationStateServiceInterface = createServiceInterface(
  "IAnimationStateService",
  AnimationStateService
);

// Create wrapper classes for services with dependencies
class SequenceAnimationOrchestratorWrapper {
  constructor(...args: unknown[]) {
    // This will be handled by the DI container registration
    return new SequenceAnimationOrchestrator(
      args[0] as IAnimationStateService,
      args[1] as IBeatCalculationService,
      args[2] as IPropInterpolationService
    );
  }
}

class SequenceAnimationEngineWrapper {
  constructor(...args: unknown[]) {
    return new SequenceAnimationEngine(
      args[0] as ISequenceAnimationOrchestrator
    );
  }
}

export const ISequenceAnimationOrchestratorInterface = createServiceInterface(
  "ISequenceAnimationOrchestrator",
  SequenceAnimationOrchestratorWrapper as new (
    ...args: unknown[]
  ) => ISequenceAnimationOrchestrator
);

export const ISequenceAnimationEngineInterface = createServiceInterface(
  "ISequenceAnimationEngine",
  SequenceAnimationEngineWrapper as new (
    ...args: unknown[]
  ) => ISequenceAnimationEngine
);
