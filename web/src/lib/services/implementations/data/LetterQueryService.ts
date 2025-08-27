/**
 * Letter Query Service - Letter-based pictograph lookups
 *
 * Single responsibility: Query pictographs by letter using LetterMappingRepository
 * Uses shared services for CSV loading, parsing, and transformation.
 */

import type { PictographData } from "$lib/domain";
import { injectable, inject } from "inversify";
import { TYPES } from "../../inversify/types";
import { GridMode, MotionType, Letter } from "$lib/domain";
import type { CSVRow } from "../movement/CSVPictographParserService";

import type { LetterMapping } from "$lib/domain/codex/types";
import type { ILetterMappingRepository } from "$lib/repositories/LetterMappingRepository";
import type { 
  ICsvLoaderService,
  ICSVParserService,
  ILetterQueryService,
  ParsedCsvRow 
} from "../../interfaces/data-interfaces";
import type { ICSVPictographParserService } from "../movement/CSVPictographParserService";

@injectable()
export class LetterQueryService implements ILetterQueryService {
  private parsedData: Record<
    Exclude<GridMode, GridMode.SKEWED>,
    ParsedCsvRow[]
  > | null = null;
  private isInitialized = false;

  constructor(
    @inject(TYPES.ILetterMappingRepository)
    private letterMappingRepository: ILetterMappingRepository,
    @inject(TYPES.ICsvLoaderService)
    private csvLoaderService: ICsvLoaderService,
    @inject(TYPES.ICSVParsingService)
    private csvParserService: ICSVParserService,
    @inject(TYPES.ICSVPictographParserService)
    private csvPictographParser: ICSVPictographParserService
  ) {}

  /**
   * Initialize CSV data and letter mapping repository if not already loaded
   */
  private async ensureInitialized(): Promise<void> {
    if (this.isInitialized) {
      return;
    }

    try {
      // Initialize letter mapping repository first
      if (
        this.letterMappingRepository &&
        typeof this.letterMappingRepository.initialize === "function"
      ) {
        await this.letterMappingRepository.initialize();
      }

      // Load raw CSV data
      const csvData = await this.csvLoaderService.loadCsvData();

      // Parse CSV data using shared service
      const diamondParseResult = this.csvParserService.parseCSV(
        csvData.diamondData
      );
      const boxParseResult = this.csvParserService.parseCSV(csvData.boxData);

      // Only log significant parsing errors (not empty row issues)
      const significantDiamondErrors = diamondParseResult.errors.filter(
        (error) =>
          !error.error.includes("missing required fields") ||
          (error.rawRow &&
            error.rawRow.trim() !== "" &&
            !error.rawRow.split(",").every((v) => v.trim() === ""))
      );
      const significantBoxErrors = boxParseResult.errors.filter(
        (error) =>
          !error.error.includes("missing required fields") ||
          (error.rawRow &&
            error.rawRow.trim() !== "" &&
            !error.rawRow.split(",").every((v) => v.trim() === ""))
      );

      if (significantDiamondErrors.length > 0) {
        console.warn(
          `⚠️ Diamond CSV parsing errors (${significantDiamondErrors.length} significant):`
        );
        significantDiamondErrors.slice(0, 3).forEach((error, index) => {
          console.warn(
            `  Error ${index + 1}: Row ${error.rowIndex} - ${error.error}`
          );
          console.warn(`  Raw row: ${error.rawRow.substring(0, 100)}...`);
        });
      }
      if (significantBoxErrors.length > 0) {
        console.warn(
          `⚠️ Box CSV parsing errors (${significantBoxErrors.length} significant):`
        );
        significantBoxErrors.slice(0, 3).forEach((error, index) => {
          console.warn(
            `  Error ${index + 1}: Row ${error.rowIndex} - ${error.error}`
          );
          console.warn(`  Raw row: ${error.rawRow.substring(0, 100)}...`);
        });
      }

      this.parsedData = {
        [GridMode.DIAMOND]: diamondParseResult.rows,
        [GridMode.BOX]: boxParseResult.rows,
        // SKEWED mode doesn't have separate data - it uses both diamond and box
      };

      this.isInitialized = true;
    } catch (error) {
      console.error("❌ LetterQueryService: Error loading CSV data:", error);
      throw new Error(
        `Failed to load CSV data: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Get a specific pictograph by letter using LetterMappingRepository
   */
  async getPictographByLetter(
    letter: Letter,
    gridMode: GridMode
  ): Promise<PictographData | null> {
    if (!this.letterMappingRepository) {
      console.error(
        "❌ LetterMappingRepository not available for getPictographByLetter"
      );
      return null;
    }

    await this.ensureInitialized();

    try {
      // Convert Letter enum to string for repository lookup
      const letterString = letter.toString();

      // Get letter mapping from repository
      const mapping =
        this.letterMappingRepository.getLetterMapping(letterString);
      if (!mapping) {
        console.warn(`⚠️ No letter mapping found for letter: ${letterString}`);
        return null;
      }

      // Find matching CSV row
      const csvRow = this.findMatchingCsvRowByMapping(
        letterString,
        mapping,
        gridMode
      );
      if (!csvRow) {
        console.warn(`⚠️ No CSV data found for letter ${letter}`);
        return null;
      }

      // Transform CSV row to PictographData using existing service
      return this.csvPictographParser.parseCSVRowToPictograph(csvRow as CSVRow);
    } catch (error) {
      console.error(`❌ Error getting pictograph for letter ${letter}:`, error);
      return null;
    }
  }

  /**
   * Get all pictographs from the codex using LetterMappingRepository
   */
  async getAllCodexPictographs(gridMode: GridMode): Promise<PictographData[]> {
    if (!this.letterMappingRepository) {
      console.error(
        "❌ LetterMappingRepository not available for getAllCodexPictographs"
      );
      return [];
    }

    await this.ensureInitialized();

    try {
      const allLetters = this.letterMappingRepository.getAllLetters();

      const pictographs: PictographData[] = [];
      for (const letterString of allLetters) {
        const letter = letterString as Letter; // Convert string to Letter enum
        const pictograph = await this.getPictographByLetter(letter, gridMode);
        if (pictograph) {
          pictographs.push(pictograph);
        }
      }

      return pictographs;
    } catch (error) {
      console.error("❌ Error getting all codex pictographs:", error);
      return [];
    }
  }

  /**
   * Get ALL pictograph variations from CSV data (not limited by letter mappings)
   * This returns every row in the CSV as a separate pictograph, including multiple variations per letter
   */
  async getAllPictographVariations(
    gridMode: GridMode
  ): Promise<PictographData[]> {
    await this.ensureInitialized();

    try {
      if (!this.parsedData) {
        console.error("❌ No parsed CSV data available");
        return [];
      }

      // For SKEWED mode, default to diamond data
      const actualGridMode =
        gridMode === GridMode.SKEWED ? GridMode.DIAMOND : gridMode;
      const csvRows = this.parsedData[actualGridMode];
      if (!csvRows || csvRows.length === 0) {
        console.error(`❌ No CSV data available for grid mode: ${gridMode}`);
        return [];
      }

      const pictographs: PictographData[] = [];
      for (let i = 0; i < csvRows.length; i++) {
        const row = csvRows[i];
        try {
          const pictograph = this.csvPictographParser.parseCSVRowToPictograph(
            row as CSVRow
          );
          if (pictograph) {
            pictographs.push(pictograph);
          }
        } catch (error) {
          console.warn(
            `⚠️ Failed to convert CSV row ${i} (letter: ${row.letter}):`,
            error
          );
        }
      }

      return pictographs;
    } catch (error) {
      console.error("❌ Error getting all pictograph variations:", error);
      return [];
    }
  }

  /**
   * Search pictographs by letter patterns
   */
  async searchPictographs(
    searchTerm: string,
    gridMode: GridMode
  ): Promise<PictographData[]> {
    if (!this.letterMappingRepository) {
      console.error(
        "❌ LetterMappingRepository not available for searchPictographs"
      );
      return [];
    }

    await this.ensureInitialized();

    try {
      const allLetters = this.letterMappingRepository.getAllLetters();
      const matchingLetters = allLetters.filter((letter) =>
        letter.toLowerCase().includes(searchTerm.toLowerCase())
      );

      const pictographs: PictographData[] = [];
      for (const letterString of matchingLetters) {
        const letter = letterString as Letter; // Convert string to Letter enum
        const pictograph = await this.getPictographByLetter(letter, gridMode);
        if (pictograph) {
          pictographs.push(pictograph);
        }
      }

      return pictographs;
    } catch (error) {
      console.error(
        `❌ Error searching pictographs for "${searchTerm}":`,
        error
      );
      return [];
    }
  }

  /**
   * Get pictographs for multiple letters
   */
  async getPictographsByLetters(
    letters: Letter[],
    gridMode: GridMode
  ): Promise<PictographData[]> {
    await this.ensureInitialized();

    const pictographs: PictographData[] = [];
    for (const letter of letters) {
      const pictograph = await this.getPictographByLetter(letter, gridMode);
      if (pictograph) {
        pictographs.push(pictograph);
      }
    }

    return pictographs;
  }

  /**
   * Find matching CSV row by letter mapping
   */
  private findMatchingCsvRowByMapping(
    letter: string,
    mapping: LetterMapping,
    gridMode: GridMode
  ): ParsedCsvRow | null {
    if (!this.parsedData) {
      return null;
    }

    // For SKEWED mode, default to diamond data
    const actualGridMode =
      gridMode === GridMode.SKEWED ? GridMode.DIAMOND : gridMode;
    const csvRows = this.parsedData[actualGridMode];
    if (!csvRows) {
      return null;
    }

    // Handle the mismatch between JSON config and LetterMapping interface
    const mappingData = mapping as LetterMapping & {
      blueMotion?: MotionType;
      redMotion?: MotionType;
    };
    const matchingRow = csvRows.find(
      (row) =>
        row.letter === letter &&
        row.startPosition === mapping.startPosition &&
        row.endPosition === mapping.endPosition &&
        row.blueMotionType ===
          (mappingData.blueMotion || mappingData.blueMotionType) &&
        row.redMotionType ===
          (mappingData.redMotion || mappingData.redMotionType)
    );

    return matchingRow || null;
  }
}
