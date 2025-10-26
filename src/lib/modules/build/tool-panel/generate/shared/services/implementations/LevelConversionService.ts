import { DifficultyLevel } from "../../domain/models";
import type { ILevelConversionService } from "../contracts/ILevelConversionService";

/**
 * Implementation of ILevelConversionService
 * Handles bidirectional conversion between numeric levels and DifficultyLevel enum
 */
export class LevelConversionService implements ILevelConversionService {
	/**
	 * Convert DifficultyLevel enum to numeric value
	 */
	difficultyToNumber(level: DifficultyLevel): number {
		switch (level) {
			case DifficultyLevel.BEGINNER:
				return 1;
			case DifficultyLevel.INTERMEDIATE:
				return 2;
			case DifficultyLevel.ADVANCED:
				return 3;
			default:
				return 2; // Default to intermediate if unknown
		}
	}

	/**
	 * Convert numeric value to DifficultyLevel enum
	 */
	numberToDifficulty(level: number): DifficultyLevel {
		switch (level) {
			case 1:
				return DifficultyLevel.BEGINNER;
			case 2:
				return DifficultyLevel.INTERMEDIATE;
			case 3:
				return DifficultyLevel.ADVANCED;
			default:
				return DifficultyLevel.INTERMEDIATE; // Default to intermediate for invalid values
		}
	}
}
