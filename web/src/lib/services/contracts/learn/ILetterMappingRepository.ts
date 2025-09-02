/**
 * Letter Mapping Repository Interface
 *
 * Contract for letter mapping management and codex configuration.
 * Handles letter mappings, categories, and validation.
 */

import type { LetterCategory, LetterMapping, LetterRow } from "$domain";

export interface ILetterMappingRepository {
  /**
   * Initialize the repository with codex configuration
   */
  initialize(): Promise<void>;

  /**
   * Get letter mapping for a specific letter
   */
  getLetterMapping(letter: string): LetterMapping | null;

  /**
   * Get all letters in a specific category
   */
  getLettersByCategory(category: LetterCategory): string[];

  /**
   * Get all letter rows from the codex
   */
  getLetterRows(): LetterRow[];

  /**
   * Get all available letters
   */
  getAllLetters(): string[];

  /**
   * Check if a letter is valid in the codex
   */
  isValidLetter(letter: string): boolean;
}
