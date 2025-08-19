/**
 * Turn Intensity Manager Service - Exact port from legacy
 *
 * Handles turn allocation for sequence generation based on level and intensity.
 * Direct port of legacy TurnIntensityManager.allocate_turns_for_blue_and_red()
 */

export interface TurnAllocation {
  blue: (number | "fl")[];
  red: (number | "fl")[];
}

export class TurnIntensityManagerService {
  private wordLength: number;
  private level: number;
  private maxTurnIntensity: number;

  constructor(wordLength: number, level: number, maxTurnIntensity: number) {
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

  private randomChoice<T>(array: T[]): T {
    if (array.length === 0) {
      throw new Error("Cannot choose from empty array");
    }
    return array[Math.floor(Math.random() * array.length)];
  }
}
