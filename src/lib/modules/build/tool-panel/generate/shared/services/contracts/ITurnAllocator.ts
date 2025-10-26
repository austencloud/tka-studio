/**
 * Turn Allocation Calculator Interface
 *
 * Calculates turn distribution across beats based on level and turn intensity.
 */

export interface TurnAllocation {
  blue: (number | "fl")[];
  red: (number | "fl")[];
}

export interface ITurnAllocator {
  /**
   * Allocate turns for a sequence
   * @param beatsToGenerate - Number of beats to generate
   * @param level - Difficulty level (1-3)
   * @param turnIntensity - Turn intensity (0-3)
   * @returns Promise resolving to blue and red turn allocations
   */
  allocateTurns(
    beatsToGenerate: number,
    level: number,
    turnIntensity: number
  ): Promise<TurnAllocation>;
}
