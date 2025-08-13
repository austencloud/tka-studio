/**
 * Codex Service Interface
 *
 * Defines the contract for codex data operations with desktop-like functionality.
 */

import type { PictographData } from "$lib/domain/PictographData";

export interface ICodexService {
  /**
   * Load all pictographs in alphabetical order
   */
  loadAllPictographs(): Promise<PictographData[]>;

  /**
   * Search pictographs by letter or pattern
   */
  searchPictographs(searchTerm: string): Promise<PictographData[]>;

  /**
   * Get a specific pictograph by letter
   */
  getPictographByLetter(letter: string): Promise<PictographData | null>;

  /**
   * Get pictographs for a specific lesson type
   */
  getPictographsForLesson(lessonType: string): Promise<PictographData[]>;

  /**
   * Get letters organized by rows for grid display (matches desktop layout)
   */
  getLettersByRow(): string[][];

  /**
   * Apply rotate operation to all pictographs
   */
  rotateAllPictographs(
    pictographs: PictographData[],
  ): Promise<PictographData[]>;

  /**
   * Apply mirror operation to all pictographs
   */
  mirrorAllPictographs(
    pictographs: PictographData[],
  ): Promise<PictographData[]>;

  /**
   * Apply color swap operation to all pictographs
   */
  colorSwapAllPictographs(
    pictographs: PictographData[],
  ): Promise<PictographData[]>;

  /**
   * Get all pictograph data organized by letter
   */
  getAllPictographData(): Promise<Record<string, PictographData | null>>;
}
