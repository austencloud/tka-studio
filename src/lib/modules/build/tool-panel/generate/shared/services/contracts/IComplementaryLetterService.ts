/**
 * Complementary Letter Service Interface
 * 
 * Provides complementary letter mappings for CAP (Circular Arrangement Pattern) generation.
 * Complementary letters are pairs that flip when applying complementary transformations.
 */
export interface IComplementaryLetterService {
  /**
   * Get the complementary letter for a given letter
   * @param letter - The input letter
   * @returns The complementary letter
   * @throws Error if no complementary mapping exists for the letter
   */
  getComplementaryLetter(letter: string): string;
}

