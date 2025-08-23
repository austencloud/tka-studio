/**
 * Motion Query Service - Motion parameter-based pictograph queries
 *
 * Single responsibility: Query pictographs by motion parameters
 * Uses shared services for CSV loading, parsing, and transformation.
 */

import type { PictographData } from "$lib/domain";
import { GridMode } from "$lib/domain";
import type { ICsvLoaderService } from "./CsvLoaderService";
import type { ICSVParserService, ParsedCsvRow } from "./CSVParserService";
import type { IPictographTransformationService } from "./PictographTransformationService";

export interface MotionQueryParams {
  startLocation: string;
  endLocation: string;
  motionType: string;
}

export interface IMotionQueryService {
  findPictographByMotionParams(
    params: MotionQueryParams,
    gridMode: GridMode
  ): Promise<PictographData | null>;
  getNextOptionsForSequence(sequence: unknown[]): Promise<PictographData[]>;
}

export class MotionQueryService implements IMotionQueryService {
  private parsedData: Record<
    Exclude<GridMode, GridMode.SKEWED>,
    ParsedCsvRow[]
  > | null = null;
  private isInitialized = false;

  constructor(
    private csvLoaderService: ICsvLoaderService,
    private csvParserService: ICSVParserService,
    private pictographTransformationService: IPictographTransformationService
  ) {}

  /**
   * Initialize CSV data if not already loaded
   */
  private async ensureInitialized(): Promise<void> {
    if (this.isInitialized) {
      return;
    }

    try {
      // Load raw CSV data
      const csvData = await this.csvLoaderService.loadCsvData();

      // Parse CSV data using shared service
      const diamondParseResult = this.csvParserService.parseCSV(
        csvData.diamondData
      );
      const boxParseResult = this.csvParserService.parseCSV(csvData.boxData);

      this.parsedData = {
        [GridMode.DIAMOND]: diamondParseResult.rows,
        [GridMode.BOX]: boxParseResult.rows,
        // SKEWED mode doesn't have separate data - it uses both diamond and box
      };

      this.isInitialized = true;
      console.log("✅ MotionQueryService: CSV data loaded and parsed");
    } catch (error) {
      console.error("❌ MotionQueryService: Error loading CSV data:", error);
      throw new Error(
        `Failed to load CSV data: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Find pictograph by motion parameters
   */
  async findPictographByMotionParams(
    params: MotionQueryParams,
    gridMode: GridMode
  ): Promise<PictographData | null> {
    await this.ensureInitialized();

    if (!this.parsedData) {
      console.error("❌ No parsed CSV data available");
      return null;
    }

    // For SKEWED mode, default to diamond data
    const actualGridMode =
      gridMode === GridMode.SKEWED ? GridMode.DIAMOND : gridMode;
    const csvRows = this.parsedData[actualGridMode];
    if (!csvRows || csvRows.length === 0) {
      console.error(`❌ No CSV data available for grid mode: ${gridMode}`);
      return null;
    }

    console.log(`🔍 Searching for motion parameters:`, params);

    // Find matching rows based on motion parameters
    const matchingRows = csvRows.filter((row) => {
      return this.matchesMotionParams(row, params);
    });

    if (matchingRows.length === 0) {
      console.warn("⚠️ No matching pictographs found for motion parameters");
      return null;
    }

    // Use the first matching row
    const matchingRow = matchingRows[0];
    console.log(`✅ Found exact match for letter "${matchingRow.letter}"`);

    // Transform CSV row to PictographData using shared service
    return this.pictographTransformationService.convertCsvRowToPictographData(
      matchingRow,
      gridMode.toString()
    );
  }

  /**
   * Get next options for sequence building (placeholder implementation)
   */
  async getNextOptionsForSequence(
    _sequence: unknown[]
  ): Promise<PictographData[]> {
    await this.ensureInitialized();

    if (!this.parsedData) {
      console.error("❌ No parsed CSV data available");
      return [];
    }

    // For now, return all available pictographs for diamond mode
    // This would need more sophisticated logic based on sequence context
    const csvRows = this.parsedData[GridMode.DIAMOND] || [];
    const pictographs: PictographData[] = [];

    for (const row of csvRows.slice(0, 20)) {
      // Limit to first 20 for performance
      const pictograph =
        this.pictographTransformationService.convertCsvRowToPictographData(
          row,
          GridMode.DIAMOND.toString()
        );
      if (pictograph) {
        pictographs.push(pictograph);
      }
    }

    console.log(
      `✅ MotionQueryService: Retrieved ${pictographs.length} next options`
    );
    return pictographs;
  }

  /**
   * Check if a CSV row matches the given motion parameters
   */
  private matchesMotionParams(
    row: ParsedCsvRow,
    params: MotionQueryParams
  ): boolean {
    // Extract motion data for both blue and red
    const rowStartLocation = row.blueStartLocation || row.redStartLocation;
    const rowEndLocation = row.blueEndLocation || row.redEndLocation;
    const rowMotionType = row.blueMotionType || row.redMotionType;

    // Normalize and compare
    const startMatch =
      (rowStartLocation?.toLowerCase().trim() || "") ===
      (params.startLocation?.toLowerCase().trim() || "");
    const endMatch =
      (rowEndLocation?.toLowerCase().trim() || "") ===
      (params.endLocation?.toLowerCase().trim() || "");
    const motionMatch =
      (rowMotionType?.toLowerCase().trim() || "") ===
      (params.motionType?.toLowerCase().trim() || "");

    return startMatch && endMatch && motionMatch;
  }
}
