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
    blueRotDir: string,
    redRotDir: string
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
