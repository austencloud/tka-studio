/**
 * CSVDataService - Refactored implementation using shared microservices
 * 
 * This refactored version eliminates duplication by using shared CSV loading
 * and parsing services while maintaining the existing interface.
 */

import { GridMode } from "$lib/domain";
import type {
  ICSVLoaderService,
  ICSVParserService,
} from "../../interfaces/application-interfaces";

declare global {
  interface Window {
    csvData?: CsvDataSet;
  }
}

export interface CsvDataSet {
  diamondData: string;
  boxData: string;
}

export interface ParsedCsvRow {
  letter: string;
  startPosition: string;
  endPosition: string;
  timing: string;
  direction: string;
  blueMotionType: string;
  blueRotationDirection: string;
  blueStartLocation: string;
  blueEndLocation: string;
  redMotionType: string;
  redRotationDirection: string;
  redStartLocation: string;
  redEndLocation: string;
  [key: string]: string;
}

export class CsvDataServiceRefactored {
  private parsedData: Record<GridMode, ParsedCsvRow[]> | null = null;
  private isInitialized = false;

  constructor(
    private csvLoaderService: ICSVLoaderService,
    private csvParserService: ICSVParserService
  ) {}

  /**
   * Load CSV data using shared CSV loader service
   */
  async loadCsvData(): Promise<void> {
    if (this.isInitialized) {
      return; // Already loaded
    }

    try {
      console.log("🔄 Loading CSV data using shared services...");

      // Use shared CSV loader service
      const datasetResult = await this.csvLoaderService.loadCSVDataSet();
      
      if (!datasetResult.success || !datasetResult.data) {
        throw new Error(datasetResult.error || "Failed to load CSV dataset");
      }

      console.log(`📁 CSV data loaded from sources: diamond=${datasetResult.sources.diamond}, box=${datasetResult.sources.box}`);

      // Parse both datasets using shared parser service
      const diamondParseResult = this.csvParserService.parseCSV(datasetResult.data.diamondData);
      const boxParseResult = this.csvParserService.parseCSV(datasetResult.data.boxData);

      // Convert to ParsedCsvRow format for compatibility
      this.parsedData = {
        [GridMode.DIAMOND]: this.convertToCompatibleFormat(diamondParseResult.rows),
        [GridMode.BOX]: this.convertToCompatibleFormat(boxParseResult.rows),
      };

      // Log parsing statistics
      const totalErrors = diamondParseResult.errors.length + boxParseResult.errors.length;
      const totalRows = diamondParseResult.totalRows + boxParseResult.totalRows;
      const successfulRows = diamondParseResult.successfulRows + boxParseResult.successfulRows;

      console.log(`✅ CSV parsing complete: ${successfulRows}/${totalRows} rows successful, ${totalErrors} errors`);

      if (totalErrors > 0) {
        console.warn(`⚠️ CSV parsing had ${totalErrors} errors - check data quality`);
      }

      this.isInitialized = true;
    } catch (error) {
      console.error("❌ Error loading CSV data:", error);
      throw new Error(
        `Failed to load CSV data: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Get CSV data (delegates to shared loader service)
   */
  getCsvData(): CsvDataSet | null {
    // Delegate to shared service for consistency
    if (this.csvLoaderService.isDataCached()) {
      // Return cached data if available
      return null; // Would need to expose this from shared service
    }
    return null;
  }

  /**
   * Get parsed data for a specific grid mode
   */
  getParsedData(gridMode: GridMode): ParsedCsvRow[] {
    if (!this.parsedData) {
      console.warn("⚠️ CSV data not loaded yet, returning empty array");
      return [];
    }
    return this.parsedData[gridMode] || [];
  }

  /**
   * Get available options for a given end position
   */
  getNextOptions(
    endPosition: string,
    gridMode: GridMode = GridMode.DIAMOND
  ): ParsedCsvRow[] {
    if (!this.parsedData) {
      console.warn("⚠️ CSV data not loaded yet, returning empty array");
      return [];
    }

    try {
      const dataset = this.parsedData[gridMode];

      // Filter options where startPosition matches the endPosition
      const matchingOptions = dataset.filter(
        (row) => row.startPosition === endPosition
      );

      console.log(`🔍 Found ${matchingOptions.length} options for end position "${endPosition}" in ${gridMode} mode`);

      return matchingOptions;
    } catch (error) {
      console.error("❌ Error getting next options:", error);
      return [];
    }
  }

  /**
   * Get all available letters for a specific grid mode
   */
  getAvailableLetters(gridMode: GridMode = GridMode.DIAMOND): string[] {
    if (!this.parsedData) {
      return [];
    }

    const dataset = this.parsedData[gridMode];
    const letters = [...new Set(dataset.map(row => row.letter))];
    return letters.sort();
  }

  /**
   * Get options filtered by letter
   */
  getOptionsByLetter(
    letter: string,
    gridMode: GridMode = GridMode.DIAMOND
  ): ParsedCsvRow[] {
    if (!this.parsedData) {
      return [];
    }

    const dataset = this.parsedData[gridMode];
    return dataset.filter(row => row.letter === letter);
  }

  /**
   * Get options filtered by multiple criteria
   */
  getFilteredOptions(
    criteria: {
      gridMode?: GridMode;
      startPosition?: string;
      endPosition?: string;
      letter?: string;
      motionType?: string;
    }
  ): ParsedCsvRow[] {
    if (!this.parsedData) {
      return [];
    }

    const gridMode = criteria.gridMode || GridMode.DIAMOND;
    let dataset = this.parsedData[gridMode];

    // Apply filters
    if (criteria.startPosition) {
      dataset = dataset.filter(row => row.startPosition === criteria.startPosition);
    }

    if (criteria.endPosition) {
      dataset = dataset.filter(row => row.endPosition === criteria.endPosition);
    }

    if (criteria.letter) {
      dataset = dataset.filter(row => row.letter === criteria.letter);
    }

    if (criteria.motionType) {
      dataset = dataset.filter(row => 
        row.blueMotionType === criteria.motionType || 
        row.redMotionType === criteria.motionType
      );
    }

    return dataset;
  }

  /**
   * Get statistics about the loaded data
   */
  getDataStatistics(): {
    isLoaded: boolean;
    diamondRows: number;
    boxRows: number;
    totalRows: number;
    uniqueLetters: {
      diamond: number;
      box: number;
    };
  } {
    if (!this.parsedData) {
      return {
        isLoaded: false,
        diamondRows: 0,
        boxRows: 0,
        totalRows: 0,
        uniqueLetters: { diamond: 0, box: 0 }
      };
    }

    const diamondRows = this.parsedData[GridMode.DIAMOND].length;
    const boxRows = this.parsedData[GridMode.BOX].length;

    return {
      isLoaded: true,
      diamondRows,
      boxRows,
      totalRows: diamondRows + boxRows,
      uniqueLetters: {
        diamond: this.getAvailableLetters(GridMode.DIAMOND).length,
        box: this.getAvailableLetters(GridMode.BOX).length
      }
    };
  }

  /**
   * Check if the service is initialized
   */
  isReady(): boolean {
    return this.isInitialized && this.parsedData !== null;
  }

  /**
   * Clear all cached data
   */
  clearCache(): void {
    this.parsedData = null;
    this.isInitialized = false;
    this.csvLoaderService.clearCache();
  }

  /**
   * Debug method to inspect specific position data
   */
  debugPosition(
    position: string,
    gridMode: GridMode = GridMode.DIAMOND
  ): void {
    if (!this.parsedData) {
      console.log("❌ No data loaded");
      return;
    }

    const dataset = this.parsedData[gridMode];
    const startMatches = dataset.filter(row => row.startPosition === position);
    const endMatches = dataset.filter(row => row.endPosition === position);

    console.log(`🔍 Debug position "${position}" in ${gridMode} mode:`);
    console.log(`  - ${startMatches.length} rows with this start position`);
    console.log(`  - ${endMatches.length} rows with this end position`);
    
    if (startMatches.length > 0) {
      console.log("  - Start position matches:", startMatches.map(r => r.letter));
    }
    if (endMatches.length > 0) {
      console.log("  - End position matches:", endMatches.map(r => r.letter));
    }
  }

  /**
   * Convert shared parser result to compatible ParsedCsvRow format
   */
  private convertToCompatibleFormat(rows: Record<string, string>[]): ParsedCsvRow[] {
    return rows.map(row => ({
      letter: row.letter || "",
      startPosition: row.startPosition || "",
      endPosition: row.endPosition || "",
      timing: row.timing || "",
      direction: row.direction || "",
      blueMotionType: row.blueMotionType || "",
      blueRotationDirection: row.blueRotationDirection || "",
      blueStartLocation: row.blueStartLocation || row.blueStartLoc || "",
      blueEndLocation: row.blueEndLocation || row.blueendLocation || "",
      redMotionType: row.redMotionType || "",
      redRotationDirection: row.redRotationDirection || "",
      redStartLocation: row.redStartLocation || row.redStartLoc || "",
      redEndLocation: row.redEndLocation || row.redendLocation || "",
      ...row // Include all other fields
    }));
  }
}
