/**
 * Pictograph Query Service
 *
 * Handles querying and filtering pictographs from CSV data based on
 * letter mappings and lesson configurations.
 */

import { GridMode } from "$lib/domain";
import type { PictographData } from "$lib/domain/PictographData";
import type { LetterMapping } from "$lib/domain/codex/types";
import {
  CsvDataService,
  type ParsedCsvRow,
} from "../implementations/CsvDataService";
import { OptionDataService } from "../implementations/OptionDataService";
import type { ILetterMappingRepository } from "$lib/repositories/LetterMappingRepository";

export interface IPictographQueryService {
  initialize(): Promise<void>;
  getPictographByLetter(
    letter: string,
    gridMode: GridMode
  ): Promise<PictographData | null>;
  getPictographsByLetters(
    letters: string[],
    gridMode: GridMode
  ): Promise<PictographData[]>;
  getAllCodexPictographs(gridMode: GridMode): Promise<PictographData[]>;
  searchPictographs(
    searchTerm: string,
    gridMode: GridMode
  ): Promise<PictographData[]>;
}

export class PictographQueryService implements IPictographQueryService {
  private csvDataService: CsvDataService;
  private optionDataService: OptionDataService;
  private initialized = false;

  constructor(private letterMappingRepository: ILetterMappingRepository) {
    this.csvDataService = new CsvDataService();
    this.optionDataService = new OptionDataService();
  }

  async initialize(): Promise<void> {
    if (this.initialized) return;

    try {
      // Initialize dependencies
      await this.letterMappingRepository.initialize();
      await this.csvDataService.loadCsvData();

      this.initialized = true;
      console.log("✅ Pictograph query service initialized");
    } catch (error) {
      console.error("❌ Failed to initialize pictograph query service:", error);
      throw error;
    }
  }

  async getPictographByLetter(
    letter: string,
    gridMode: GridMode
  ): Promise<PictographData | null> {
    this.ensureInitialized();

    const mapping = this.letterMappingRepository.getLetterMapping(letter);
    if (!mapping) {
      console.warn(`No mapping found for letter: ${letter}`);
      return null;
    }

    const csvRow = this.findMatchingCsvRow(letter, mapping, gridMode);
    if (!csvRow) {
      console.warn(
        `No CSV data found for letter ${letter} in ${gridMode} mode`
      );
      return null;
    }

    return this.convertCsvRowToPictographData(csvRow, gridMode, 0);
  }

  async getPictographsByLetters(
    letters: string[],
    gridMode: GridMode
  ): Promise<PictographData[]> {
    this.ensureInitialized();

    const pictographs: PictographData[] = [];

    for (let i = 0; i < letters.length; i++) {
      const letter = letters[i];
      const pictograph = await this.getPictographByLetter(letter, gridMode);
      if (pictograph) {
        pictographs.push(pictograph);
      }
    }

    return pictographs;
  }

  async getAllCodexPictographs(gridMode: GridMode): Promise<PictographData[]> {
    this.ensureInitialized();

    const allLetters = this.letterMappingRepository.getAllLetters();
    return this.getPictographsByLetters(allLetters, gridMode);
  }

  async searchPictographs(
    searchTerm: string,
    gridMode: GridMode
  ): Promise<PictographData[]> {
    this.ensureInitialized();

    if (!searchTerm.trim()) {
      return this.getAllCodexPictographs(gridMode);
    }

    const term = searchTerm.toLowerCase();
    const allLetters = this.letterMappingRepository.getAllLetters();

    // Filter letters that match the search term
    const matchingLetters = allLetters.filter(
      (letter) =>
        letter.toLowerCase().includes(term) ||
        letter.toLowerCase().startsWith(term)
    );

    return this.getPictographsByLetters(matchingLetters, gridMode);
  }

  private findMatchingCsvRow(
    letter: string,
    mapping: LetterMapping,
    gridMode: GridMode
  ): ParsedCsvRow | null {
    const csvRows = this.csvDataService.getParsedData(gridMode);

    return (
      csvRows.find(
        (row) =>
          row.letter === letter &&
          row.startPos === mapping.startPos &&
          row.endPos === mapping.endPos &&
          row.blueMotionType === mapping.blueMotion &&
          row.redMotionType === mapping.redMotion
      ) || null
    );
  }

  private convertCsvRowToPictographData(
    row: ParsedCsvRow,
    gridMode: GridMode,
    index: number
  ): PictographData | null {
    try {
      return this.optionDataService.convertCsvRowToPictographData(row, index);
    } catch (error) {
      console.error(
        "❌ Error converting CSV row to PictographData:",
        error,
        row
      );
      return null;
    }
  }

  private ensureInitialized(): void {
    if (!this.initialized) {
      throw new Error(
        "Pictograph query service not initialized. Call initialize() first."
      );
    }
  }
}
