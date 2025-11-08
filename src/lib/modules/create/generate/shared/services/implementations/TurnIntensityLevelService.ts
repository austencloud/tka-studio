/**
 * Turn Intensity Level Service
 *
 * Provides turn intensity values for UI display based on difficulty level.
 * This is a stateless service that can be resolved from the DI container.
 *
 * Separated from TurnIntensityManagerService which requires constructor parameters.
 */

import { injectable } from "inversify";
import { DifficultyLevel } from "../../domain/models";
import type { ITurnIntensityManagerService } from "../contracts/ITurnIntensityManagerService";

@injectable()
export class TurnIntensityLevelService implements ITurnIntensityManagerService {
  /**
   * Get allowed turn intensity values for UI display
   * Determines which intensity values should be available based on difficulty level
   */
  getAllowedValuesForLevel(level: DifficultyLevel): number[] {
    switch (level) {
      case DifficultyLevel.BEGINNER:
        return []; // No turns for level 1
      case DifficultyLevel.INTERMEDIATE:
        return [1.0, 2.0, 3.0]; // Whole numbers for level 2
      case DifficultyLevel.ADVANCED:
        return [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]; // All values for level 3 (excluding 0 and "fl" for UI)
      default:
        return [1.0, 2.0, 3.0];
    }
  }

  /**
   * Not used by UI - only needed for sequence generation
   * Throws error if called
   */
  allocateTurnsForBlueAndRed(): {
    blue: (number | "fl")[];
    red: (number | "fl")[];
  } {
    throw new Error(
      "TurnIntensityLevelService does not support allocateTurnsForBlueAndRed. " +
        "Use TurnIntensityManagerService directly for turn allocation."
    );
  }
}
