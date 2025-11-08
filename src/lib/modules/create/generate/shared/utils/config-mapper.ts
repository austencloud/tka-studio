/**
 * Config Mapper - Clean conversion between UI config and service options
 *
 * This utility provides type-safe bidirectional mapping between:
 * - UIGenerationConfig (UI state management)
 * - GenerationOptions (service layer)
 *
 * Eliminates the need for manual conversion functions and provides
 * a single source of truth for all config transformations.
 */

import { GridMode } from "$shared/pictograph/grid/domain/enums/grid-enums";
import type { DifficultyLevel, GenerationOptions } from "../domain";
import { DifficultyLevel as DifficultyEnum } from "../domain";

/**
 * Map difficulty level number to DifficultyLevel enum
 */
export const LEVEL_TO_DIFFICULTY: Record<number, DifficultyLevel> = {
  1: DifficultyEnum.BEGINNER,
  2: DifficultyEnum.INTERMEDIATE,
  3: DifficultyEnum.ADVANCED,
} as const;

/**
 * Map DifficultyLevel enum to level number (reverse lookup)
 */
export const DIFFICULTY_TO_LEVEL: Record<DifficultyLevel, number> = {
  [DifficultyEnum.BEGINNER]: 1,
  [DifficultyEnum.INTERMEDIATE]: 2,
  [DifficultyEnum.ADVANCED]: 3,
} as const;

/**
 * Convert level number to DifficultyLevel enum
 */
export function levelToDifficulty(level: number): DifficultyLevel {
  return LEVEL_TO_DIFFICULTY[level] || DifficultyEnum.INTERMEDIATE;
}

/**
 * Convert DifficultyLevel enum to level number
 */
export function difficultyToLevel(difficulty: DifficultyLevel): number {
  return DIFFICULTY_TO_LEVEL[difficulty] || 2;
}

/**
 * UI Configuration interface for state management
 * This is what the UI components work with directly
 */
export interface UIGenerationConfig {
  mode: string; // "freeform" | "circular"
  length: number;
  level: number; // 1-3
  turnIntensity: number;
  gridMode: GridMode;
  propContinuity: string; // "continuous" | "random"
  sliceSize: string; // "halved" | "quartered"
  capType: string; // CAP type for circular mode
}

/**
 * Convert UI config to service-layer GenerationOptions
 * This is the main conversion function used when calling the generation service
 */
export function uiConfigToGenerationOptions(
  uiConfig: UIGenerationConfig,
  propType: string = "fan"
): GenerationOptions {
  // Force halved mode for CAP types that only support halved (not quartered)
  const requiresHalved =
    uiConfig.capType?.includes("mirrored") ||
    uiConfig.capType?.includes("swapped") ||
    uiConfig.capType?.includes("complementary");

  const sliceSize = requiresHalved ? "halved" : uiConfig.sliceSize;

  if (requiresHalved && uiConfig.sliceSize !== "halved") {
    // Override to halved for this CAP type
  }

  const options: GenerationOptions = {
    length: uiConfig.length,
    gridMode: uiConfig.gridMode,
    propType,
    difficulty: levelToDifficulty(uiConfig.level),
    mode: uiConfig.mode
      ? (uiConfig.mode as GenerationOptions["mode"])
      : undefined,
    propContinuity: uiConfig.propContinuity
      ? (uiConfig.propContinuity as GenerationOptions["propContinuity"])
      : undefined,
    turnIntensity:
      uiConfig.turnIntensity !== undefined ? uiConfig.turnIntensity : undefined,
    sliceSize: sliceSize
      ? (sliceSize as GenerationOptions["sliceSize"])
      : undefined,
    capType: uiConfig.capType || undefined,
  };
  return options;
}

/**
 * Convert service-layer GenerationOptions back to UI config
 * Useful for loading saved configurations
 */
export function generationOptionsToUIConfig(
  options: GenerationOptions,
  sliceSize: string = "halved",
  capType: string = "strictRotated"
): UIGenerationConfig {
  return {
    mode: options.mode || "freeform",
    length: options.length,
    level: difficultyToLevel(options.difficulty),
    turnIntensity: options.turnIntensity || 1.0,
    gridMode: options.gridMode,
    propContinuity: options.propContinuity || "continuous",
    sliceSize,
    capType,
  };
}
