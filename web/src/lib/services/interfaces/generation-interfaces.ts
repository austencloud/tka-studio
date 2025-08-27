/**
 * Generation Service Interfaces - Complete interface definitions
 *
 * Complete interfaces for motion generation, sequence generation, and related algorithms.
 * Updated to match exact legacy generation parameters and options.
 */

import { GenerationMode, MotionColor, PropContinuity } from "$lib/domain/enums";
import type { DifficultyLevel, GridMode } from "./core-types";
import type { BeatData, MotionData, SequenceData } from "./domain-types";
import type { Letter } from "../../domain/Letter";

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

import type { PictographData } from "$lib/domain/PictographData";
import type { GridPosition } from "$lib/domain/enums";

/**
 * Service for generating TKA pictographs from letter patterns
 */
export interface IPictographGenerator {
  // Standard letter generators
  generateA(): PictographData[];
  generateB(): PictographData[];
  generateC(): PictographData[];
  generateD(): PictographData[];
  generateE(): PictographData[];
  generateF(): PictographData[];
  generateG(): PictographData[];
  generateH(): PictographData[];
  generateI(): PictographData[];
  generateJ(): PictographData[];
  generateK(): PictographData[];
  generateL(): PictographData[];
  generateM(): PictographData[];
  generateN(): PictographData[];
  generateO(): PictographData[];
  generateP(): PictographData[];
  generateQ(): PictographData[];
  generateR(): PictographData[];
  generateS(): PictographData[];
  generateT(): PictographData[];
  generateU(): PictographData[];
  generateV(): PictographData[];
  generateW(): PictographData[];
  generateX(): PictographData[];
  generateY(): PictographData[];
  generateZ(): PictographData[];

  // Greek letter generators
  generateSigma(): PictographData[];
  generateDelta(): PictographData[];
  generateTheta(): PictographData[];
  generateOmega(): PictographData[];
  generatePhi(): PictographData[];
  generatePsi(): PictographData[];
  generateLambda(): PictographData[];
  generateAlpha(): PictographData[];
  generateBeta(): PictographData[];
  generateGamma(): PictographData[];

  // Dash variant generators
  generateWDash(): PictographData[];
  generateXDash(): PictographData[];
  generateYDash(): PictographData[];
  generateZDash(): PictographData[];
  generateSigmaDash(): PictographData[];
  generateDeltaDash(): PictographData[];
  generateThetaDash(): PictographData[];
  generateOmegaDash(): PictographData[];
  generatePhiDash(): PictographData[];
  generatePsiDash(): PictographData[];
  generateLambdaDash(): PictographData[];

  // Utility methods
  getAllPictographs(): PictographData[];
  getPictographsByLetter(letter: string): PictographData[] | undefined;
}

/**
 * Service for managing position sequences
 */
export interface IPositionPatternService {
  getAlphaSequence(): GridPosition[];
  getBetaSequence(): GridPosition[];
  getGammaSequence(): GridPosition[];
  getCustomSequence(positions: GridPosition[]): GridPosition[];

  generatePositionSequence(
    positionSystem: string,
    length?: number
  ): GridPosition[];
}

/**
 * Service for calculating position sequences - focused on sequence generation only
 */
export interface IPositionSequenceService {
  getPositionSequence(
    system: "alpha" | "beta" | "gamma",
    count: number
  ): GridPosition[];
  getNextPosition(current: GridPosition, forward: boolean): GridPosition;
  calculatePositionPairs(
    sequence: GridPosition[]
  ): Array<[GridPosition, GridPosition]>;
}

/**
 * Service for calculating directional mappings - focused on location calculations
 */
export interface IDirectionCalculator {
  getCardinalDirections(
    startPosition: GridPosition,
    endPosition: GridPosition,
    motionType: string
  ): [
    import("$lib/domain/enums").Location,
    import("$lib/domain/enums").Location,
  ];
}

/**
 * Service for validating generated pictographs
 */
export interface IPictographValidatorService {
  validatePictograph(pictograph: PictographData): boolean;
  validatePictographs(pictographs: PictographData[]): boolean;
  getValidationErrors(pictograph: PictographData): string[];
  validatePositionSequence(positions: GridPosition[]): boolean;
}

// ============================================================================
// LETTER GENERATOR INTERFACES
// ============================================================================

/**
 * Base Letter Generator Interface
 *
 * All letter-specific generators implement this interface.
 * Provides consistent API for generating movement sets for individual letters.
 */
export interface ILetterGenerator {
  /**
   * The letter this generator handles
   */
  readonly letter: string;

  /**
   * Generate movement set for this letter
   */
  generate(): PictographData;
}

/**
 * Factory interface for creating letter generators
 */
export interface ILetterGeneratorFactory {
  /**
   * Create generator for the specified letter
   */
  createGenerator(letter: string): ILetterGenerator | null;

  /**
   * Get all supported letters
   */
  getSupportedLetters(): string[];
}

// ============================================================================
// LETTER DERIVATION INTERFACES
// ============================================================================

/**
 * Letter Derivation Result
 */
export interface LetterDerivationResult {
  letter: Letter | null;
  confidence: "exact" | "partial" | "none";
  matchedParameters: string[];
}

/**
 * Letter Deriver Interface
 */
export interface ILetterDeriver {
  deriveLetterFromMotions(
    blueMotion: MotionData,
    redMotion: MotionData
  ): LetterDerivationResult;
  deriveLetterFromPictograph(
    pictograph: PictographData
  ): LetterDerivationResult;
  validateLetterMatch(
    letter: Letter,
    blueMotion: MotionData,
    redMotion: MotionData
  ): boolean;
}
