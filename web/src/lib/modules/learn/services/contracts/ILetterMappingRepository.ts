/**
 * Letter Mapping Repository Interface
 *
 * Contract for letter mapping management and codex configuration.
 * Handles letter mappings, categories, and validation.
 */

import type { CodexLetterMapping, CodexLetterRow } from "../../codex/domain";

export interface ICodexLetterMappingRepository {
  /**
   * Initialize the repository with codex configuration
   */
  initialize(): Promise<void>;

  /**
   * Get letter mapping for a specific letter
   */
  getLetterMapping(letter: string): CodexLetterMapping | null;

  /**
   * Get all letter rows from the codex
   */
  getLetterRows(): CodexLetterRow[];

  /**
   * Get all available letters
   */
  getAllLetters(): string[];

  /**
   * Check if a letter is valid in the codex
   */
  isValidLetter(letter: string): boolean;
}
