/**
 * Letter Mapping Repository
 *
 * Clean repository pattern for managing letter mappings.
 * Handles loading, caching, and querying of letter configuration data.
 */

import type {
  CodexConfiguration,
  LetterMapping,
  LetterCategory,
  LetterRow,
} from "$lib/domain/codex/types";

export interface ILetterMappingRepository {
  initialize(): Promise<void>;
  getLetterMapping(letter: string): LetterMapping | null;
  getLettersByCategory(category: LetterCategory): string[];
  getLetterRows(): LetterRow[];
  getAllLetters(): string[];
  isValidLetter(letter: string): boolean;
}

export class LetterMappingRepository implements ILetterMappingRepository {
  private configuration: CodexConfiguration | null = null;
  private initialized = false;

  async initialize(): Promise<void> {
    if (this.initialized) return;

    try {
      // Load configuration from JSON file
      const response = await fetch("/config/codex/letter-mappings.json");
      if (!response.ok) {
        throw new Error(`Failed to load letter mappings: ${response.status}`);
      }

      this.configuration = (await response.json()) as CodexConfiguration;
      this.initialized = true;
      console.log(
        "✅ Letter mapping repository initialized with",
        Object.keys(this.configuration.letters).length,
        "letters"
      );
    } catch (error) {
      console.error(
        "❌ Failed to initialize letter mapping repository:",
        error
      );
      throw error;
    }
  }

  getLetterMapping(letter: string): LetterMapping | null {
    this.ensureInitialized();
    if (!this.configuration) return null;
    return this.configuration.letters[letter] || null;
  }

  getLettersByCategory(category: LetterCategory): string[] {
    this.ensureInitialized();
    if (!this.configuration) return [];
    return [...(this.configuration.categories[category] || [])];
  }

  getLetterRows(): LetterRow[] {
    this.ensureInitialized();
    if (!this.configuration) return [];
    return [...this.configuration.rows];
  }

  getAllLetters(): string[] {
    this.ensureInitialized();
    if (!this.configuration) return [];
    return Object.keys(this.configuration.letters);
  }

  isValidLetter(letter: string): boolean {
    this.ensureInitialized();
    if (!this.configuration) return false;
    return letter in this.configuration.letters;
  }

  private ensureInitialized(): void {
    if (!this.initialized) {
      throw new Error(
        "Letter mapping repository not initialized. Call initialize() first."
      );
    }
  }
}
