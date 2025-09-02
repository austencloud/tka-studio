/**
 * Generation Service Interfaces - Complete interface definitions
 *
 * Complete interfaces for motion generation, sequence generation, and related algorithms.
 * Updated to match exact legacy generation parameters and options.
 */
// ============================================================================
// GENERATION OPTIONS
// ============================================================================
import type { DifficultyLevel, GridMode, Letter } from "$domain";
import { GenerationMode, PropContinuity } from "$domain";

// ============================================================================
// DATA CONTRACTS (Domain Models)
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

/**
 * Factory interface for creating letter generators
 */
export interface ILetterGeneratorFactory {
  createGenerator(parameters: GenerationOptions): ILetterGenerator;
}

export interface ILetterGenerator {
  generate(): LetterDerivationResult;
}

export interface LetterDerivationResult {
  letter: Letter | null;
  confidence: "exact" | "partial" | "none";
  matchedParameters: string[];
}

export interface PictographOperation {
  type: "add" | "remove" | "modify" | "reorder";
  targetIndex?: number;
  data?: Record<string, unknown>;
}
