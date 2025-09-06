/**
 * Clean Codex Service Implementation
 *
 * A clean, maintainable implementation that uses proper separation of concerns.
 * No more hardcoded mappings or mixed responsibilities!
 */

import { GridMode, Letter, type PictographData } from "$shared/domain";
import type { ILetterQueryHandler } from "$shared/foundation/services/contracts/data/data-interfaces";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IQuizRepoManager } from "../../../quiz/services/contracts";
import type { CodexLetterRow } from "../../domain";
import type { ICodexPictographUpdater } from "../contracts/ICodexPictographUpdater";
import type { ICodexService } from "../contracts/ICodexService";
// import type { ICodexLetterMappingRepo } from "../contracts/ICodexLetterMappingRepo";

// Temporary interface definition
interface ICodexLetterMappingRepo {
  getMapping(letter: string): Promise<any>;
  getAllMappings(): Promise<any[]>;
  initialize(): Promise<void>;
  getLetterRows(): Promise<any[]>;
  getAllLetters(): Promise<any[]>;
  isValidLetter(letter: string): boolean;
}

@injectable()
export class CodexService implements ICodexService {
  private initialized = false;

  constructor(
    @inject(TYPES.ICodexLetterMappingRepo)
    private letterMappingRepo: ICodexLetterMappingRepo,
    @inject(TYPES.IQuizRepoManager)
    private lessonRepo: IQuizRepoManager,
    @inject(TYPES.ICodexPictographUpdater)
    private operationsService: ICodexPictographUpdater,
    @inject(TYPES.ILetterQueryHandler)
    private LetterQueryHandler: ILetterQueryHandler
  ) {
    console.log(
      "🔧 Clean CodexService initialized with proper dependency injection"
    );
  }

  /**
   * Initialize the service and all dependencies
   */
  private async initialize(): Promise<void> {
    if (this.initialized) return;

    try {
      console.log("🚀 Initializing clean CodexService...");

      // Initialize all repositories and services
      await Promise.all([
        this.letterMappingRepo.initialize(),
        this.lessonRepo.initialize(),
        // LetterQueryHandler initializes automatically when first used
      ]);

      this.initialized = true;
      console.log("✅ Clean CodexService fully initialized");
    } catch (error) {
      console.error("❌ Failed to initialize clean CodexService:", error);
      throw error;
    }
  }

  /**
   * Load all pictographs in alphabetical order
   */
  async loadAllPictographs(): Promise<PictographData[]> {
    await this.initialize();

    console.log("🔍 Loading all codex pictographs...");
    const pictographs = await this.LetterQueryHandler.getAllCodexPictographs(
      GridMode.DIAMOND
    );
    console.log(
      `📊 Loaded ${pictographs.length} pictographs from codex query service`
    );
    const sortedPictographs = this.sortPictographsAlphabetically(pictographs);
    console.log(
      `✅ Sorted ${sortedPictographs.length} pictographs alphabetically`
    );
    return sortedPictographs;
  }

  /**
   * Search pictographs by letter or pattern
   */
  async searchPictographs(searchTerm: string): Promise<PictographData[]> {
    await this.initialize();

    const pictographs = await this.LetterQueryHandler.searchPictographs(
      searchTerm,
      GridMode.DIAMOND
    );
    return this.sortPictographsAlphabetically(pictographs);
  }

  /**
   * Get a specific pictograph by letter
   */
  async getPictographByLetter(letter: string): Promise<PictographData | null> {
    await this.initialize();

    return this.LetterQueryHandler.getPictographByLetter(
      letter as Letter,
      GridMode.DIAMOND
    );
  }

  /**
   * Get pictographs for a specific lesson type
   */
  async getPictographsForLesson(lessonType: string): Promise<PictographData[]> {
    await this.initialize();

    console.log(`📚 Getting pictographs for lesson type: ${lessonType}`);

    const letters = await this.lessonRepo.getLettersForLesson(lessonType);
    if (letters.length === 0) {
      console.warn(`No letters found for lesson type: ${lessonType}`);
      return [];
    }

    const pictographs = await this.LetterQueryHandler.getPictographsByLetters(
      letters as Letter[],
      GridMode.DIAMOND
    );
    return this.sortPictographsAlphabetically(pictographs);
  }

  /**
   * Get letters organized by rows for grid display
   */
  async getLettersByRow(): Promise<string[][]> {
    this.ensureInitialized();

    const rows = await this.letterMappingRepo.getLetterRows();
    return (rows as CodexLetterRow[]).map((row) => [...row.letters]); // Return copy to prevent mutation
  }

  /**
   * Apply rotate operation to all pictographs
   */
  async rotateAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]> {
    await this.initialize();

    return this.operationsService.rotateAllPictographs(pictographs);
  }

  /**
   * Apply mirror operation to all pictographs
   */
  async mirrorAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]> {
    await this.initialize();

    return this.operationsService.mirrorAllPictographs(pictographs);
  }

  /**
   * Apply color swap operation to all pictographs
   */
  async colorSwapAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]> {
    await this.initialize();

    return this.operationsService.colorSwapAllPictographs(pictographs);
  }

  /**
   * Get all pictograph data organized by letter
   */
  async getAllPictographData(): Promise<Record<string, PictographData | null>> {
    await this.initialize();

    const allLetters = await this.letterMappingRepo.getAllLetters();
    const result: Record<string, PictographData | null> = {};

    // Initialize all letters to null
    (allLetters as string[]).forEach((letter) => {
      result[letter] = null;
    });

    // Load actual pictographs
    const pictographs = await this.loadAllPictographs();
    pictographs.forEach((pictograph) => {
      if (pictograph.letter) {
        result[pictograph.letter] = pictograph;
      }
    });

    return result;
  }

  // Additional clean helper methods

  /**
   * Get available lesson types
   */
  async getAvailableQuizTypes(): Promise<string[]> {
    await this.initialize();

    return await this.lessonRepo.getAllQuizTypes();
  }

  /**
   * Check if a letter is valid in the codex
   */
  isValidLetter(letter: string): boolean {
    this.ensureInitialized();

    return this.letterMappingRepo.isValidLetter(letter);
  }

  // Private helper methods

  private sortPictographsAlphabetically(
    pictographs: PictographData[]
  ): PictographData[] {
    return [...pictographs].sort((a, b) => {
      const letterA = a.letter || "";
      const letterB = b.letter || "";
      return letterA.localeCompare(letterB);
    });
  }

  private ensureInitialized(): void {
    if (!this.initialized) {
      throw new Error(
        "CodexService not initialized. Methods will auto-initialize, but sync methods require prior initialization."
      );
    }
  }
}
