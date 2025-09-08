/**
 * Generation Service Interfaces - Complete interface definitions
 *
 * Complete interfaces for motion generation, sequence generation, and related algorithms.
 * Updated to match exact legacy generation parameters and options.
 */
// ============================================================================
// GENERATION OPTIONS
// ============================================================================
import type { GridMode, Letter } from "$shared";

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
export enum SliceSize {
  HALVED = "halved",
  QUARTERED = "quartered",
}

// Fundamental CAP components that can be combined
export enum CAPComponent {
  ROTATED = "rotated",
  MIRRORED = "mirrored",
  SWAPPED = "swapped",
  COMPLEMENTARY = "complementary",
}

// Legacy CAP types for backward compatibility
export enum CAPType {
  STRICT_ROTATED = "strictRotated",
  STRICT_MIRRORED = "strictMirrored",
  STRICT_SWAPPED = "strictSwapped",
  STRICT_COMPLEMENTARY = "strictComplementary",
  SWAPPED_COMPLEMENTARY = "swappedComplementary",
  ROTATED_COMPLEMENTARY = "rotatedComplementary",
  MIRRORED_SWAPPED = "mirroredSwapped",
  MIRRORED_COMPLEMENTARY = "mirroredComplementary",
  ROTATED_SWAPPED = "rotatedSwapped",
  MIRRORED_ROTATED = "mirroredRotated",
  MIRRORED_COMPLEMENTARY_ROTATED = "mirroredComplementaryRotated",
}

export enum PositionSystem {
  ALPHA_TO_ALPHA = "alpha_to_alpha",
  ALPHA_TO_BETA = "alpha_to_beta",
  ALPHA_TO_GAMMA = "alpha_to_gamma",
  BETA_TO_ALPHA = "beta_to_alpha",
  BETA_TO_BETA = "beta_to_beta",
  BETA_TO_GAMMA = "beta_to_gamma",
  GAMMA_TO_ALPHA = "gamma_to_alpha",
  GAMMA_TO_BETA = "gamma_to_beta",
  GAMMA_TO_GAMMA = "gamma_to_gamma",
}

export enum DifficultyLevel {
  BEGINNER = "beginner",
  INTERMEDIATE = "intermediate",
  ADVANCED = "advanced",
}

export enum PropContinuity {
  CONTINUOUS = "continuous",
  RANDOM = "random",
}

export enum GenerationMode {
  FREEFORM = "freeform",
  CIRCULAR = "circular",
}