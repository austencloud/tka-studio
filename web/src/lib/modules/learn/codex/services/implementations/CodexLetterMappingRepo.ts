/**
 * Letter Mapping Repo Implementation
 *
 * Service implementation for letter mapping management and codex configuration.
 * Handles letter mappings, categories, and validation.
 */

import { MotionType } from "$shared/domain";
import { injectable } from "inversify";
import type {
  CodexConfig,
  CodexLetterMapping,
  CodexLetterRow,
} from "../../domain";
import { createLetterMapping } from "../../domain";
import type { ICodexLetterMappingRepo } from "../contracts";

@injectable()
export class CodexLetterMappingRepo implements ICodexLetterMappingRepo {
  private configuration: CodexConfig | null = null;
  private initialized = false;

  async initialize(): Promise<void> {
    if (this.initialized) {
      return;
    }

    try {
      // Load codex configuration
      await this.loadCodexConfig();
      this.initialized = true;
    } catch (error) {
      console.error("Failed to initialize CodexLetterMappingRepo:", error);
      throw error;
    }
  }

  getLetterMapping(letter: string): CodexLetterMapping | null {
    if (!this.initialized || !this.configuration) {
      console.warn(
        "CodexLetterMappingRepo not initialized. Call initialize() first."
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

  getLetterRows(): CodexLetterRow[] {
    if (!this.initialized || !this.configuration) {
      console.warn(
        "CodexLetterMappingRepo not initialized. Call initialize() first."
      );
      return [];
    }

    return this.configuration.rows;
  }

  getAllLetters(): string[] {
    if (!this.initialized || !this.configuration) {
      console.warn(
        "CodexLetterMappingRepo not initialized. Call initialize() first."
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

  private async loadCodexConfig(): Promise<void> {
    try {
      // Load from actual codex configuration file
      const response = await fetch("/data/learn/letter-mappings.json");
      if (!response.ok) {
        throw new Error(`Failed to fetch letter mappings: ${response.status}`);
      }

      const data = await response.json();

      // Convert the JSON data to our internal format
      const letters: Record<string, CodexLetterMapping> = {};
      for (const [letter, mapping] of Object.entries(data.letters)) {
        const letterData = mapping as {
          startPosition: string;
          endPosition: string;
          blueMotion: string;
          redMotion: string;
        };
        letters[letter] = createLetterMapping({
          startPosition: letterData.startPosition,
          endPosition: letterData.endPosition,
          blueMotionType: this.mapMotionString(letterData.blueMotion),
          redMotionType: this.mapMotionString(letterData.redMotion),
        });
      }

      this.configuration = {
        version: "1.0.0",
        letters,
        rows: data.rows,
        categories: data.categories,
      };

      console.log(
        `✅ Loaded ${Object.keys(letters).length} letters from codex configuration`
      );
    } catch (error) {
      console.error("Failed to load codex configuration:", error);
      throw error;
    }
  }

  private mapMotionString(motionString: string | unknown): MotionType {
    const motionStr =
      typeof motionString === "string" ? motionString : String(motionString);
    switch (motionStr.toLowerCase()) {
      case "pro":
        return MotionType.PRO;
      case "anti":
        return MotionType.ANTI;
      case "static":
        return MotionType.STATIC;
      case "dash":
        return MotionType.DASH;
      default:
        console.warn(`Unknown motion type: ${motionStr}, defaulting to PRO`);
        return MotionType.PRO;
    }
  }
}
