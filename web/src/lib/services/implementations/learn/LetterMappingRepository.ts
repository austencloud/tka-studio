/**
 * Letter Mapping Repository Implementation
 *
 * Service implementation for letter mapping management and codex configuration.
 * Handles letter mappings, categories, and validation.
 */

import type { ILetterMappingRepository } from "$contracts/learn/ILetterMappingRepository";
import {
  createLetterMapping,
  createLetterRow,
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
    for (const row of this.configuration.letterRows) {
      const mapping = row.letters.find((l) => l.letter === letter);
      if (mapping) {
        return mapping;
      }
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
    for (const row of this.configuration.letterRows) {
      for (const letterMapping of row.letters) {
        if (letterMapping.category === category) {
          letters.push(letterMapping.letter);
        }
      }
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

    return this.configuration.letterRows;
  }

  getAllLetters(): string[] {
    if (!this.initialized || !this.configuration) {
      console.warn(
        "LetterMappingRepository not initialized. Call initialize() first."
      );
      return [];
    }

    const letters: string[] = [];
    for (const row of this.configuration.letterRows) {
      for (const letterMapping of row.letters) {
        letters.push(letterMapping.letter);
      }
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
        letterRows: [
          createLetterRow({
            id: "row-1",
            name: "Basic Letters Row 1",
            letters: [
              createLetterMapping({
                letter: "A",
                category: "BASIC" as LetterCategory,
                difficulty: 1,
                description: "Basic letter A",
              }),
              createLetterMapping({
                letter: "B",
                category: "BASIC" as LetterCategory,
                difficulty: 1,
                description: "Basic letter B",
              }),
            ],
          }),
          createLetterRow({
            id: "row-2",
            name: "Advanced Letters Row 1",
            letters: [
              createLetterMapping({
                letter: "F",
                category: "ADVANCED" as LetterCategory,
                difficulty: 2,
                description: "Advanced letter F",
              }),
              createLetterMapping({
                letter: "G",
                category: "ADVANCED" as LetterCategory,
                difficulty: 2,
                description: "Advanced letter G",
              }),
            ],
          }),
        ],
      };

      this.configuration = defaultConfiguration;
    } catch (error) {
      console.error("Failed to load codex configuration:", error);
      throw error;
    }
  }
}
