/**
 * Clean Codex Service Implementation
 *
 * A clean, maintainable implementation that uses proper separation of concerns.
 * No more hardcoded mappings or mixed responsibilities!
 */

import { GridMode } from "$lib/domain";
import type { PictographData } from "$lib/domain/PictographData";
import type { LetterCategory } from "$lib/domain/codex/types";
import type { ILetterMappingRepository } from "$lib/repositories/LetterMappingRepository";
import type { ILessonRepository } from "$lib/repositories/LessonRepository";
import { TYPES } from "$lib/services/inversify/types";
import { inject, injectable } from "inversify";

import type { IPictographOperationsService } from "./PictographOperationsService";
import type { ICodexService } from "./ICodexService";
import type { ILetterQueryService } from "../implementations/data/LetterQueryService";

// Re-export the interface for convenience
export type { ICodexService } from "./ICodexService";

@injectable()
export class CodexService implements ICodexService {
  private initialized = false;

  constructor(
    @inject(TYPES.ILetterMappingRepository)
    private letterMappingRepository: ILetterMappingRepository,
    @inject(TYPES.ILessonRepository)
    private lessonRepository: ILessonRepository,
    @inject(TYPES.IPictographOperationsService)
    private operationsService: IPictographOperationsService,
    @inject(TYPES.ILetterQueryService)
    private letterQueryService: ILetterQueryService
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
        this.letterMappingRepository.initialize(),
        this.lessonRepository.initialize(),
        // LetterQueryService initializes automatically when first used
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
    const pictographs = await this.letterQueryService.getAllCodexPictographs(
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

    const pictographs = await this.letterQueryService.searchPictographs(
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

    return this.letterQueryService.getPictographByLetter(
      letter,
      GridMode.DIAMOND
    );
  }

  /**
   * Get pictographs for a specific lesson type
   */
  async getPictographsForLesson(lessonType: string): Promise<PictographData[]> {
    await this.initialize();

    console.log(`📚 Getting pictographs for lesson type: ${lessonType}`);

    const letters = this.lessonRepository.getLettersForLesson(lessonType);
    if (letters.length === 0) {
      console.warn(`No letters found for lesson type: ${lessonType}`);
      return [];
    }

    const pictographs = await this.letterQueryService.getPictographsByLetters(
      letters,
      GridMode.DIAMOND
    );
    return this.sortPictographsAlphabetically(pictographs);
  }

  /**
   * Get letters organized by rows for grid display
   */
  getLettersByRow(): string[][] {
    this.ensureInitialized();

    const rows = this.letterMappingRepository.getLetterRows();
    return rows.map((row) => [...row.letters]); // Return copy to prevent mutation
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

    const allLetters = this.letterMappingRepository.getAllLetters();
    const result: Record<string, PictographData | null> = {};

    // Initialize all letters to null
    allLetters.forEach((letter) => {
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
  async getAvailableLessonTypes(): Promise<string[]> {
    await this.initialize();

    return this.lessonRepository.getAllLessonTypes();
  }

  /**
   * Get letters by category
   */
  getLettersByCategory(category: LetterCategory): string[] {
    this.ensureInitialized();

    return this.letterMappingRepository.getLettersByCategory(category);
  }

  /**
   * Check if a letter is valid in the codex
   */
  isValidLetter(letter: string): boolean {
    this.ensureInitialized();

    return this.letterMappingRepository.isValidLetter(letter);
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
