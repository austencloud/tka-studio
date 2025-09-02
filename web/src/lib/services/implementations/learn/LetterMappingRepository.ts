/**
 * Letter Mapping Repository Implementation
 *
 * Service implementation for letter mapping management and codex configuration.
 * Handles letter mappings, categories, and validation.
 */

import type { ILetterMappingRepository } from "$contracts";
import {
  createLetterMapping,
  type CodexConfiguration,
  type LetterCategory,
  type LetterMapping,
  type LetterRow,
} from "$domain";
import { injectable } from "inversify";

@injectable()
export class LetterMappingRepository implements ILetterMappingRepository {
  private configuration: CodexConfiguration | null = null;
  private initialized = false;

  async initialize(): Promise<void> {
    if (this.initialized) {
      return;
    }

    try {
      // Load codex configuration
      await this.loadCodexConfiguration();
      this.initialized = true;
    } catch (error) {
      console.error("Failed to initialize LetterMappingRepository:", error);
      throw error;
    }
  }

  getLetterMapping(letter: string): LetterMapping | null {
    if (!this.initialized || !this.configuration) {
      console.warn(
        "LetterMappingRepository not initialized. Call initialize() first."
      );
      return null;
    }

    // Find letter mapping in configuration
    const letterMapping = this.configuration.letters[letter];
    if (letterMapping) {
      return letterMapping;
    }

    return null;
  }

  getLettersByCategory(category: LetterCategory): string[] {
    if (!this.initialized || !this.configuration) {
      console.warn(
        "LetterMappingRepository not initialized. Call initialize() first."
      );
      return [];
    }

    const letters: string[] = [];
    const categoryLetters = this.configuration.categories[category];
    if (categoryLetters) {
      return categoryLetters;
    }

    return letters;
  }

  getLetterRows(): LetterRow[] {
    if (!this.initialized || !this.configuration) {
      console.warn(
        "LetterMappingRepository not initialized. Call initialize() first."
      );
      return [];
    }

    return this.configuration.rows;
  }

  getAllLetters(): string[] {
    if (!this.initialized || !this.configuration) {
      console.warn(
        "LetterMappingRepository not initialized. Call initialize() first."
      );
      return [];
    }

    const letters: string[] = [];
    for (const letterKey in this.configuration.letters) {
      letters.push(letterKey);
    }

    return letters;
  }

  isValidLetter(letter: string): boolean {
    return this.getLetterMapping(letter) !== null;
  }

  private async loadCodexConfiguration(): Promise<void> {
    try {
      // TODO: Load from actual codex configuration files
      // For now, create a default configuration
      const defaultConfiguration: CodexConfiguration = {
        version: "1.0.0",
        letters: {
          A: createLetterMapping({
            startPosition: "alpha1",
            endPosition: "alpha3",
            blueMotionType: "PRO" as any,
            redMotionType: "PRO" as any,
          }),
          B: createLetterMapping({
            startPosition: "alpha1",
            endPosition: "alpha3",
            blueMotionType: "ANTI" as any,
            redMotionType: "ANTI" as any,
          }),
          F: createLetterMapping({
            startPosition: "beta1",
            endPosition: "alpha3",
            blueMotionType: "ANTI" as any,
            redMotionType: "PRO" as any,
          }),
          G: createLetterMapping({
            startPosition: "beta3",
            endPosition: "beta5",
            blueMotionType: "PRO" as any,
            redMotionType: "PRO" as any,
          }),
        },
        rows: [
          {
            index: 0,
            category: "basic" as LetterCategory,
            letters: ["A", "B"],
          },
          {
            index: 1,
            category: "extended" as LetterCategory,
            letters: ["F", "G"],
          },
        ],
        categories: {
          basic: ["A", "B"],
          extended: ["F", "G"],
          greek: [],
          dash: [],
          special: [],
          dual_dash: [],
          static: [],
        },
      };

      this.configuration = defaultConfiguration;
    } catch (error) {
      console.error("Failed to load codex configuration:", error);
      throw error;
    }
  }
}
