/**
 * CSV Pictograph Loader Service - Loads pictograph data from CSV files
 *
 * Simple service for loading pictograph data from CSV files.
 * Can be enhanced with actual CSV loading functionality as needed.
 */

import type { PictographData } from "$domain";
import { Letter } from "$domain";
import { injectable } from "inversify";

export interface ICSVPictographLoaderService {
  getPictographsForLetter(letter: Letter): PictographData[];
  getAvailableLetters(): Letter[];
  getPictographCounts(): Record<Letter, number>;
  clearCache(): void;
}

@injectable()
export class CSVPictographLoaderService implements ICSVPictographLoaderService {
  private readonly pictographCache = new Map<Letter, PictographData[]>();
  private readonly availableLetters = Object.values(Letter);

  constructor() {
    // Initialize with empty cache
  }

  /**
   * Get pictographs for a specific letter
   */
  getPictographsForLetter(letter: Letter): PictographData[] {
    if (this.pictographCache.has(letter)) {
      return this.pictographCache.get(letter) || [];
    }

    // TODO: Implement actual CSV loading
    // For now, return empty array
    const pictographs: PictographData[] = [];
    this.pictographCache.set(letter, pictographs);
    return pictographs;
  }

  /**
   * Get all available letters
   */
  getAvailableLetters(): Letter[] {
    return [...this.availableLetters];
  }

  /**
   * Get pictograph counts for each letter
   */
  getPictographCounts(): Record<Letter, number> {
    const counts: Record<Letter, number> = {} as Record<Letter, number>;
    for (const letter of this.availableLetters) {
      counts[letter] = this.getPictographsForLetter(letter).length;
    }
    return counts;
  }

  /**
   * Clear the pictograph cache
   */
  clearCache(): void {
    this.pictographCache.clear();
  }
}
