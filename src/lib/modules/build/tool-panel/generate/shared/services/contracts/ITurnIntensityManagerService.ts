import type { DifficultyLevel } from "../../domain/models";

export interface ITurnIntensityManagerService {
  allocateTurnsForBlueAndRed(): {
    blue: (number | "fl")[];
    red: (number | "fl")[];
  };

  /**
   * Get allowed turn intensity values for a given difficulty level
   * Used by UI to determine which intensity options to show
   *
   * @param level - The difficulty level
   * @returns Array of allowed turn intensity values (empty for Beginner, filtered for other levels)
   */
  getAllowedValuesForLevel(level: DifficultyLevel): number[];
}

