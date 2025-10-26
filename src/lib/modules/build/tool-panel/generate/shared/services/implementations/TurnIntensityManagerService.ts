/**
 * Turn Intensity Manager Service - Exact port from legacy
 *
 * Handles turn allocation for sequence generation based on level and intensity.
 * Direct port of legacy TurnIntensityManager.allocate_turns_for_blue_and_red()
 */

import { injectable, unmanaged } from "inversify";
import { DifficultyLevel } from "../../domain/models";
import type { ITurnIntensityManagerService } from "../contracts/ITurnIntensityManagerService";

export interface TurnAllocation {
  blue: (number | "fl")[];
  red: (number | "fl")[];
}

@injectable()
export class TurnIntensityManagerService implements ITurnIntensityManagerService {
  private wordLength: number;
  private level: number;
  private maxTurnIntensity: number;

  constructor(
    @unmanaged() wordLength: number,
    @unmanaged() level: number,
    @unmanaged() maxTurnIntensity: number
  ) {
    this.wordLength = wordLength;
    this.level = level;
    this.maxTurnIntensity = maxTurnIntensity;
  }

  /**
   * Allocate turns for blue and red - exact port from legacy
   */
  allocateTurnsForBlueAndRed(): TurnAllocation {
    let possibleTurns: (number | "fl")[];

    // Exact logic from legacy
    if (this.level === 2) {
      possibleTurns = [0, 1, 2, 3];
    } else if (this.level === 3) {
      possibleTurns = [0, 0.5, 1, 1.5, 2, 2.5, 3, "fl"];
    } else {
      possibleTurns = [0];
    }

    const turnsBlue: (number | "fl")[] = [];
    const turnsRed: (number | "fl")[] = [];

    for (let i = 0; i < this.wordLength; i++) {
      // Filter possible turns by max intensity - exact logic from legacy
      const validTurns = possibleTurns.filter((t) => {
        if (t === "fl") return true;
        return typeof t === "number" && t <= this.maxTurnIntensity;
      });

      // Random selection - exact logic from legacy
      const turnBlue = this.randomChoice(validTurns);
      const turnRed = this.randomChoice(validTurns);

      turnsBlue.push(turnBlue);
      turnsRed.push(turnRed);
    }

    return {
      blue: turnsBlue,
      red: turnsRed,
    };
  }

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

  private randomChoice<T>(array: T[]): T {
    if (array.length === 0) {
      throw new Error("Cannot choose from empty array");
    }
    return array[Math.floor(Math.random() * array.length)];
  }
}
