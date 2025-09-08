/**
 * Motion Query Service - Motion parameter-based pictograph queries
 *
 * Single responsibility: Query pictographs by motion parameters
 * Uses shared services for CSV loading, parsing, and transformation.
 */

import type { CSVRow, ICSVPictographParser } from "$shared";
import { GridMode, type PictographData } from "$shared";
import { inject, injectable } from "inversify";
import type { ParsedCsvRow } from "../../../../../modules/build/generate/domain";
import type { ICSVLoader, IMotionQueryHandler } from "../../../../foundation";
import { TYPES } from "../../../../inversify";

// Temporary interface definition
interface ICSVParser {
  parseCSV(csvText: string): { rows: ParsedCsvRow[] };
}

@injectable()
export class MotionQueryHandler implements IMotionQueryHandler {
  private parsedData: Record<
    Exclude<GridMode, GridMode.SKEWED>,
    ParsedCsvRow[]
  > | null = null;
  private isInitialized = false;

  constructor(
    @inject(TYPES.ICSVLoader)
    private csvLoaderService: ICSVLoader,
    @inject(TYPES.ICSVParser)
    private CSVParser: ICSVParser,
    @inject(TYPES.ICSVPictographParserService)
    private csvPictographParser: ICSVPictographParser
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
      const csvData = await this.csvLoaderService.loadCSVDataSet();

      // Parse CSV data using shared service
      const diamondParseResult = this.CSVParser.parseCSV(
        csvData.data?.diamondData || ""
      );
      const boxParseResult = this.CSVParser.parseCSV(
        csvData.data?.boxData || ""
      );

      this.parsedData = {
        [GridMode.DIAMOND]: diamondParseResult.rows,
        [GridMode.BOX]: boxParseResult.rows,
        // SKEWED mode doesn't have separate data - it uses both diamond and box
      };

      this.isInitialized = true;
      console.log("✅ MotionQueryHandler: CSV data loaded and parsed");
    } catch (error) {
      console.error("❌ MotionQueryHandler: Error loading CSV data:", error);
      throw new Error(
        `Failed to load CSV data: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Query motions based on criteria
   */
  async queryMotions(
    criteria: Record<string, unknown>
  ): Promise<PictographData[]> {
    await this.ensureInitialized();

    if (!this.parsedData) {
      console.error("❌ No parsed CSV data available");
      return [];
    }

    // Simple implementation - filter based on criteria
    const gridMode = criteria.gridMode || GridMode.DIAMOND;
    const actualGridMode =
      gridMode === GridMode.SKEWED ? GridMode.DIAMOND : gridMode;
    const csvRows =
      this.parsedData[actualGridMode as keyof typeof this.parsedData] || [];
    const pictographs: PictographData[] = [];

    for (const row of csvRows.slice(0, 50)) {
      // Limit for performance
      const pictograph = this.csvPictographParser.parseCSVRowToPictograph(
        row as unknown as CSVRow
      );
      if (pictograph) {
        pictographs.push(pictograph);
      }
    }

    return pictographs;
  }

  /**
   * Get motion data by ID
   */
  async getMotionById(motionId: string): Promise<PictographData | null> {
    await this.ensureInitialized();

    if (!this.parsedData) {
      console.error("❌ No parsed CSV data available");
      return null;
    }

    // Search through all grid modes for the motion ID
    for (const gridMode of [GridMode.DIAMOND, GridMode.BOX]) {
      const csvRows =
        this.parsedData[gridMode as keyof typeof this.parsedData] || [];
      for (const row of csvRows) {
        const pictograph = this.csvPictographParser.parseCSVRowToPictograph(
          row as unknown as CSVRow
        );
        if (pictograph && pictograph.id === motionId) {
          return pictograph;
        }
      }
    }

    return null;
  }

  /**
   * Search motions by pattern
   */
  async searchMotions(pattern: string): Promise<PictographData[]> {
    await this.ensureInitialized();

    if (!this.parsedData) {
      console.error("❌ No parsed CSV data available");
      return [];
    }

    const pictographs: PictographData[] = [];
    const lowerPattern = pattern.toLowerCase();

    // Search through all grid modes
    for (const gridMode of [GridMode.DIAMOND, GridMode.BOX]) {
      const csvRows =
        this.parsedData[gridMode as keyof typeof this.parsedData] || [];
      for (const row of csvRows.slice(0, 100)) {
        // Limit for performance
        const data = row;
        // Search in letter, motion types, and locations
        if (
          data.letter?.toLowerCase().includes(lowerPattern) ||
          data.blueMotionType?.toLowerCase().includes(lowerPattern) ||
          data.redMotionType?.toLowerCase().includes(lowerPattern) ||
          data.blueStartLocation?.toLowerCase().includes(lowerPattern) ||
          data.redStartLocation?.toLowerCase().includes(lowerPattern)
        ) {
          const pictograph = this.csvPictographParser.parseCSVRowToPictograph(
            row as CSVRow
          );
          if (pictograph) {
            pictographs.push(pictograph);
          }
        }
      }
    }

    return pictographs;
  }

  /**
   * Get next options for sequence building - contextual filtering based on sequence
   */
  async getNextOptionsForSequence(
    sequence: unknown[]
  ): Promise<PictographData[]> {
    try {
      console.log("🔍 MotionQueryHandler: getNextOptionsForSequence called with sequence length:", sequence.length);
      await this.ensureInitialized();

      if (!this.parsedData) {
        console.error("❌ No parsed CSV data available");
        return [];
      }

      // Get all available pictographs for diamond mode
      const csvRows = this.parsedData[GridMode.DIAMOND] || [];
      console.log(`🔍 MotionQueryHandler: Found ${csvRows.length} CSV rows`);

      // Parse all available pictographs
      const allPictographs: PictographData[] = [];
      for (const row of csvRows) {
        try {
          const pictograph = this.csvPictographParser.parseCSVRowToPictograph(
            row as unknown as CSVRow
          );
          if (pictograph) {
            allPictographs.push(pictograph);
          }
        } catch (parseError) {
          console.warn("⚠️ MotionQueryHandler: Failed to parse row:", parseError);
          // Continue with other rows
        }
      }

      console.log(`🔍 MotionQueryHandler: Parsed ${allPictographs.length} total pictographs`);

      // If no sequence context, return first 20 (fallback for empty sequences)
      if (!sequence || sequence.length === 0) {
        console.log("🔍 MotionQueryHandler: No sequence context, returning first 20");
        return allPictographs.slice(0, 20);
      }

      // TODO: Implement proper contextual filtering based on sequence
      // For now, return all available options to see the full dataset
      // This should be replaced with proper filtering logic based on:
      // - End position of last beat
      // - Valid transitions
      // - Letter type constraints
      console.log("🔍 MotionQueryHandler: Returning all available options for analysis");
      return allPictographs;
    } catch (error) {
      console.error(
        "❌ MotionQueryHandler: Error in getNextOptionsForSequence:",
        error
      );
      throw error; // Re-throw to let caller handle it
    }
  }
}