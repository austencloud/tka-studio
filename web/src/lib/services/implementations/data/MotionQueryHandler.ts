/**
 * Motion Query Service - Motion parameter-based pictograph queries
 *
 * Single responsibility: Query pictographs by motion parameters
 * Uses shared services for CSV loading, parsing, and transformation.
 */

import type {
  CSVRow,
  ICSVLoader,
  ICSVParser,
  ICSVPictographParserService,
  IMotionQueryHandler,
} from "$contracts";
import type { ParsedCsvRow, PictographData } from "$domain";
import { GridMode } from "$domain";
import { inject, injectable } from "inversify";
import { TYPES } from "../../inversify/types";

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
    @inject(TYPES.ICSVPictographLoaderService)
    private csvPictographParser: ICSVPictographParserService
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
  async queryMotions(criteria: Record<string, any>): Promise<PictographData[]> {
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
        row.data as unknown as CSVRow
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
          row.data as unknown as CSVRow
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
      const pictograph = this.csvPictographParser.parseCSVRowToPictograph(
        row.data as unknown as CSVRow
      );
      if (pictograph) {
        pictographs.push(pictograph);
      }
    }

    console.log(
      `✅ MotionQueryHandler: Retrieved ${pictographs.length} next options`
    );
    return pictographs;
  }
}
