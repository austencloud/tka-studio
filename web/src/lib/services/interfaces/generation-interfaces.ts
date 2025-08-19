/**
 * Generation Service Interfaces - Complete interface definitions
 *
 * Complete interfaces for motion generation, sequence generation, and related algorithms.
 * Updated to match exact legacy generation parameters and options.
 */

import type { BeatData, MotionData, SequenceData } from "./domain-types";
import type { GridMode, DifficultyLevel } from "./core-types";
import { PropContinuity, GenerationMode, MotionColor } from "$lib/domain/enums";

// ============================================================================
// GENERATION OPTIONS
// ============================================================================

export interface GenerationOptions {
  mode?: GenerationMode;
  length: number;
  gridMode: GridMode;
  propType: string;
  difficulty: DifficultyLevel;
  propContinuity?: PropContinuity;
  turnIntensity?: number;
  letterTypes?: string[]; // Array of letter type descriptions like ["Dual-Shift", "Shift"]
}

// ============================================================================
// GENERATION SERVICE INTERFACES
// ============================================================================

/**
 * Service for generating complete sequences
 */
export interface ISequenceGenerationService {
  generateSequence(options: GenerationOptions): Promise<SequenceData>;
  generatePatternSequence(
    pattern: GenerationMode,
    options: GenerationOptions
  ): Promise<SequenceData>;

  getGenerationStats(): {
    totalGenerated: number;
    averageGenerationTime: number;
    lastGenerated: string | null;
  };
}

/**
 * Service for generating individual motions
 */
export interface IMotionGenerationService {
  generateMotion(
    color: MotionColor,
    options: GenerationOptions,
    previousBeats: BeatData[]
  ): Promise<MotionData>;
  generateConstrainedMotion(
    color: MotionColor,
    options: GenerationOptions,
    previousBeats: BeatData[],
    constraints: {
      allowedMotionTypes?: string[];
      allowedStartLocations?: string[];
      allowedEndLocations?: string[];
    }
  ): Promise<MotionData>;
  validateMotion(
    motion: MotionData,
    color: MotionColor,
    previousBeats: BeatData[]
  ): { isValid: boolean; reasons: string[] };
}

/**
 * Service for turn intensity management
 */
export interface ITurnIntensityManagerService {
  allocateTurnsForBlueAndRed(): {
    blue: (number | "fl")[];
    red: (number | "fl")[];
  };
}

/**
 * Service for option data management and filtering
 */
export interface IOptionDataService {
  initialize(): Promise<void>;
  getNextOptions(
    sequence: BeatData[]
  ): Promise<import("$lib/domain/PictographData").PictographData[]>;
  getNextOptionsFromEndPosition(
    endPosition: string,
    gridMode: GridMode,
    options: Record<string, unknown>
  ): Promise<import("$lib/domain/PictographData").PictographData[]>;
  filterOptionsByLetterTypes(
    options: import("$lib/domain/PictographData").PictographData[],
    letterTypes: string[]
  ): import("$lib/domain/PictographData").PictographData[];
  filterOptionsByRotation(
    options: import("$lib/domain/PictographData").PictographData[],
    blueRotationDirection: string,
    redRotationDirection: string
  ): import("$lib/domain/PictographData").PictographData[];
}

/**
 * Service for orientation calculations
 */
export interface IOrientationCalculationService {
  calculateEndOrientation(motion: MotionData, color: MotionColor): string;
  updateStartOrientations(nextBeat: BeatData, lastBeat: BeatData): BeatData;
  updateEndOrientations(beat: BeatData): BeatData;
}

// ============================================================================
// MOVEMENT PATTERN GENERATION INTERFACES
// ============================================================================

import type {
  MovementData,
  MovementPattern,
  MovementSet,
} from "$lib/domain/MovementData";
import type { GridPosition } from "$lib/domain/enums";

/**
 * Service for generating TKA movement patterns from templates
 */
export interface IMovementGeneratorService {
  generateMovementSet(pattern: MovementPattern): MovementSet;

  // Standard letter generators
  generateA(): MovementSet;
  generateB(): MovementSet;
  generateC(): MovementSet;
  generateD(): MovementSet;
  generateE(): MovementSet;
  generateF(): MovementSet;
  generateG(): MovementSet;
  generateH(): MovementSet;
  generateI(): MovementSet;
  generateJ(): MovementSet;
  generateK(): MovementSet;
  generateL(): MovementSet;
  generateM(): MovementSet;
  generateN(): MovementSet;
  generateO(): MovementSet;
  generateP(): MovementSet;
  generateQ(): MovementSet;
  generateR(): MovementSet;
  generateS(): MovementSet;
  generateT(): MovementSet;
  generateU(): MovementSet;
  generateV(): MovementSet;
  generateW(): MovementSet;
  generateX(): MovementSet;
  generateY(): MovementSet;
  generateZ(): MovementSet;

  // Greek letter generators
  generateSigma(): MovementSet;
  generateDelta(): MovementSet;
  generateTheta(): MovementSet;
  generateOmega(): MovementSet;
  generatePhi(): MovementSet;
  generatePsi(): MovementSet;
  generateLambda(): MovementSet;
  generateAlpha(): MovementSet;
  generateBeta(): MovementSet;
  generateGamma(): MovementSet;

  // Dash variant generators
  generateWDash(): MovementSet;
  generateXDash(): MovementSet;
  generateYDash(): MovementSet;
  generateZDash(): MovementSet;
  generateSigmaDash(): MovementSet;
  generateDeltaDash(): MovementSet;
  generateThetaDash(): MovementSet;
  generateOmegaDash(): MovementSet;
  generatePhiDash(): MovementSet;
  generatePsiDash(): MovementSet;
  generateLambdaDash(): MovementSet;

  // Utility methods
  getAllMovementSets(): MovementSet[];
  getMovementSetByLetter(letter: string): MovementSet | undefined;
}

/**
 * Service for managing movement patterns and position sequences
 */
export interface IMovementPatternService {
  createPattern(
    letter: string,
    config: Partial<MovementPattern>
  ): MovementPattern;

  getAlphaSequence(): GridPosition[];
  getBetaSequence(): GridPosition[];
  getGammaSequence(): GridPosition[];
  getCustomSequence(positions: GridPosition[]): GridPosition[];

  createVariations(
    basePattern: MovementPattern,
    variations: Array<{
      motionCombination: [string, string];
      rotationCombination: [string, string];
    }>
  ): MovementPattern[];
}

/**
 * Service for calculating position sequences and transformations
 */
export interface IPositionCalculatorService {
  getPositionSequence(
    system: "alpha" | "beta" | "gamma",
    count: number
  ): GridPosition[];
  getNextPosition(current: GridPosition, forward: boolean): GridPosition;
  getCardinalDirections(
    startPos: GridPosition,
    endPos: GridPosition,
    motionType: string
  ): [
    import("$lib/domain/enums").Location,
    import("$lib/domain/enums").Location,
  ];

  calculatePositionPairs(
    sequence: GridPosition[]
  ): Array<[GridPosition, GridPosition]>;
}

/**
 * Service for validating generated movements
 */
export interface IMovementValidatorService {
  validateMovement(movement: MovementData): boolean;
  validateMovementSet(movementSet: MovementSet): boolean;
  getValidationErrors(movement: MovementData): string[];
  validatePositionSequence(positions: GridPosition[]): boolean;
}
