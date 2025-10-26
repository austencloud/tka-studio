import type { DifficultyLevel } from "../../domain/models";

/**
 * Service for converting between numeric levels and DifficultyLevel enum
 * Centralizes level conversion logic to maintain consistency across the application
 */
export interface ILevelConversionService {
	/**
	 * Convert DifficultyLevel enum to numeric value (1-3)
	 * @param level - The difficulty level enum
	 * @returns Numeric representation (1 = Beginner, 2 = Intermediate, 3 = Advanced)
	 */
	difficultyToNumber(level: DifficultyLevel): number;

	/**
	 * Convert numeric value to DifficultyLevel enum
	 * @param level - Numeric level (1-3)
	 * @returns Corresponding DifficultyLevel enum value
	 */
	numberToDifficulty(level: number): DifficultyLevel;
}
