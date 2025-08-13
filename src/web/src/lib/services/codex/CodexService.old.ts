/**
 * Codex Service Implementation
 *
 * Handles codex data operations including loading and searching pictographs.
 * Loads real pictograph data from CSV files using existing infrastructure.
 */

import { GridMode } from "$lib/domain";
import type { PictographData } from "$lib/domain/PictographData";
import {
  CsvDataService,
  type ParsedCsvRow,
} from "../implementations/CsvDataService";
import { OptionDataService } from "../implementations/OptionDataService";
import type { ICodexService } from "./ICodexService";

export class CodexService implements ICodexService {
  private csvDataService: CsvDataService;
  private optionDataService: OptionDataService;
  private initialized = false;

  constructor() {
    this.csvDataService = new CsvDataService();
    this.optionDataService = new OptionDataService();
    console.log("🔧 CodexService initialized with real CSV infrastructure");
  }

  /**
   * Load all pictographs in alphabetical order
   */
  async loadAllPictographs(): Promise<PictographData[]> {
    if (!this.initialized) {
      await this.initializePictographs();
    }

    // Get pictographs from both grid modes
    const diamondPictographs = this.getAllPictographsForGridMode(
      GridMode.DIAMOND,
    );
    const boxPictographs = this.getAllPictographsForGridMode(GridMode.BOX);
    const allPictographs = [...diamondPictographs, ...boxPictographs];

    // Sort alphabetically by letter
    return allPictographs.sort((a, b) => {
      const letterA = a.letter || "";
      const letterB = b.letter || "";
      return letterA.localeCompare(letterB);
    });
  }

  /**
   * Search pictographs by letter or pattern
   */
  async searchPictographs(searchTerm: string): Promise<PictographData[]> {
    const allPictographs = await this.loadAllPictographs();

    if (!searchTerm.trim()) {
      return allPictographs;
    }

    const term = searchTerm.toLowerCase();

    return allPictographs.filter((pictograph) => {
      const letter = pictograph.letter?.toLowerCase() || "";
      const id = pictograph.id?.toLowerCase() || "";

      return (
        letter.includes(term) || id.includes(term) || letter.startsWith(term)
      );
    });
  }

  /**
   * Get a specific pictograph by letter
   */
  async getPictographByLetter(letter: string): Promise<PictographData | null> {
    const allPictographs = await this.loadAllPictographs();

    return (
      allPictographs.find(
        (pictograph) =>
          pictograph.letter?.toLowerCase() === letter.toLowerCase(),
      ) || null
    );
  }

  /**
   * Get pictographs for a specific lesson type
   */
  async getPictographsForLesson(lessonType: string): Promise<PictographData[]> {
    const allPictographs = await this.loadAllPictographs();

    // For now, return all pictographs
    // This could be filtered based on lesson requirements in the future
    console.log(`📚 Getting pictographs for lesson type: ${lessonType}`);
    return allPictographs;
  }

  /**
   * Initialize pictographs from CSV data
   */
  private async initializePictographs(): Promise<void> {
    try {
      // Load real CSV data using existing infrastructure
      await this.csvDataService.loadCsvData();
      this.initialized = true;
      console.log("✅ CodexService initialized with real CSV data");
    } catch (error) {
      console.error("❌ Failed to initialize CodexService:", error);
      this.initialized = false;
    }
  }

  /**
   * Get all pictographs for a specific grid mode
   */
  private getAllPictographsForGridMode(gridMode: GridMode): PictographData[] {
    if (!this.initialized) {
      console.warn("⚠️ CodexService not initialized");
      return [];
    }

    const csvRows = this.csvDataService.getParsedData(gridMode);

    return csvRows
      .map((row, index) =>
        this.convertCsvRowToPictographData(row, gridMode, index),
      )
      .filter(
        (pictograph): pictograph is PictographData => pictograph !== null,
      );
  }

  /**
   * Convert CSV row to PictographData using existing infrastructure
   */
  private convertCsvRowToPictographData(
    row: ParsedCsvRow,
    gridMode: GridMode,
    index: number,
  ): PictographData | null {
    try {
      // Use the public conversion method from OptionDataService
      return this.optionDataService.convertCsvRowToPictographData(
        row,
        gridMode,
        index,
      );
    } catch (error) {
      console.error(
        "❌ Error converting CSV row to PictographData:",
        error,
        row,
      );
      return null;
    }
  }

  /**
   * Get letters organized by rows for grid display (matches desktop layout)
   */
  getLettersByRow(): string[][] {
    // Standard grid layout for pictographs
    return [
      ["A", "B", "C", "D", "E", "F", "G", "H"],
      ["I", "J", "K", "L", "M", "N", "O", "P"],
      ["Q", "R", "S", "T", "U", "V", "W", "X"],
      ["Y", "Z", "Φ", "Ψ", "Λ"],
    ];
  }

  /**
   * Apply rotate operation to all pictographs
   */
  async rotateAllPictographs(
    pictographs: PictographData[],
  ): Promise<PictographData[]> {
    // TODO: Implement rotation logic
    console.warn("rotateAllPictographs not yet implemented");
    return pictographs;
  }

  /**
   * Apply mirror operation to all pictographs
   */
  async mirrorAllPictographs(
    pictographs: PictographData[],
  ): Promise<PictographData[]> {
    // TODO: Implement mirror logic
    console.warn("mirrorAllPictographs not yet implemented");
    return pictographs;
  }

  /**
   * Apply color swap operation to all pictographs
   */
  async colorSwapAllPictographs(
    pictographs: PictographData[],
  ): Promise<PictographData[]> {
    // TODO: Implement color swap logic
    console.warn("colorSwapAllPictographs not yet implemented");
    return pictographs;
  }

  /**
   * Get all pictograph data organized by letter
   */
  async getAllPictographData(): Promise<Record<string, PictographData | null>> {
    const allPictographs = await this.loadAllPictographs();
    const result: Record<string, PictographData | null> = {};

    for (const pictograph of allPictographs) {
      if (pictograph.letter) {
        result[pictograph.letter] = pictograph;
      }
    }

    return result;
  }
}
