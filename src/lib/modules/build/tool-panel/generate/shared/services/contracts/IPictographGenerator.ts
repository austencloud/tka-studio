/**
 * Pictograph Generator Interface
 *
 * Interface for generating and retrieving pictographs by letter.
 * This is a facade over ILetterQueryHandler for the generate module.
 */

import type { PictographData } from "$shared";

export interface IPictographGenerator {
  /**
   * Get all pictographs for a specific letter
   * @param letter - The letter to get pictographs for
   * @returns Array of pictographs for the letter, or null if not found
   */
  getPictographsByLetter(letter: string): PictographData[] | null;

  /**
   * Get all available pictographs across all letters
   * @returns Array of all pictographs
   */
  getAllPictographs(): PictographData[];
}

