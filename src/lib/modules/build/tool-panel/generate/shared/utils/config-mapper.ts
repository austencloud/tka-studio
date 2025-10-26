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
import { LetterType } from "$shared/foundation/domain/models/LetterType";
import type { DifficultyLevel, GenerationOptions } from "../domain";
import { DifficultyLevel as DifficultyEnum } from "../domain";

/**
 * Map LetterType enum to human-readable string
 */
export const LETTER_TYPE_TO_STRING: Record<LetterType, string> = {
  [LetterType.TYPE1]: "Dual-Shift",
  [LetterType.TYPE2]: "Shift",
  [LetterType.TYPE3]: "Cross-Shift",
  [LetterType.TYPE4]: "Dash",
  [LetterType.TYPE5]: "Dual-Dash",
  [LetterType.TYPE6]: "Static",
} as const;

/**
 * Map human-readable string to LetterType enum (reverse lookup)
 */
export const STRING_TO_LETTER_TYPE: Record<string, LetterType> = {
  "Dual-Shift": LetterType.TYPE1,
  "Shift": LetterType.TYPE2,
  "Cross-Shift": LetterType.TYPE3,
  "Dash": LetterType.TYPE4,
  "Dual-Dash": LetterType.TYPE5,
  "Static": LetterType.TYPE6,
} as const;

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
 * Convert Set<LetterType> to string[] for service layer
 */
export function letterTypesToStrings(letterTypes: Set<LetterType>): string[] {
  return Array.from(letterTypes).map((type) => LETTER_TYPE_TO_STRING[type]);
}

/**
 * Convert string[] to Set<LetterType> for UI layer
 */
export function stringsToLetterTypes(letterTypeStrings: string[]): Set<LetterType> {
  return new Set(
    letterTypeStrings
      .map((str) => STRING_TO_LETTER_TYPE[str])
      .filter((type): type is LetterType => type !== undefined)
  );
}

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
  letterTypes: Set<LetterType>;
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
  const requiresHalved = uiConfig.capType?.includes("mirrored") ||
                         uiConfig.capType?.includes("swapped") ||
                         uiConfig.capType?.includes("complementary");

  const sliceSize = requiresHalved ? "halved" : uiConfig.sliceSize;

  if (requiresHalved && uiConfig.sliceSize !== "halved") {
    console.log(`🔄 Overriding slice size to "halved" for CAP type: ${uiConfig.capType}`);
  }

  return {
    mode: uiConfig.mode as GenerationOptions["mode"],
    length: uiConfig.length,
    gridMode: uiConfig.gridMode,
    propType,
    difficulty: levelToDifficulty(uiConfig.level),
    propContinuity: uiConfig.propContinuity as GenerationOptions["propContinuity"],
    turnIntensity: uiConfig.turnIntensity,
    letterTypes: letterTypesToStrings(uiConfig.letterTypes),
    sliceSize: sliceSize as GenerationOptions["sliceSize"],
    capType: uiConfig.capType,
  };
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
    letterTypes: options.letterTypes
      ? stringsToLetterTypes(options.letterTypes)
      : new Set([
          LetterType.TYPE1,
          LetterType.TYPE2,
          LetterType.TYPE3,
          LetterType.TYPE4,
          LetterType.TYPE5,
          LetterType.TYPE6,
        ]),
    sliceSize,
    capType,
  };
}
