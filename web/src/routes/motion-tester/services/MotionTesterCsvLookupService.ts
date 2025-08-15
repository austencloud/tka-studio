/**
 * Motion Tester CSV Lookup Service
 * 
 * Integrates the Motion Tester with the proven CSV data pipeline.
 * Finds matching pictographs from CSV data based on motion parameters,
 * replacing the hardcoded "T" letter with dynamic letter detection.
 */

import type { PictographData } from "$lib/domain";
import { GridMode } from "$lib/domain";
import type { ParsedCsvRow } from "$lib/services/implementations/CsvDataService";
import type { MotionTestParams } from "./MotionParameterService";

export interface IMotionTesterCsvLookupService {
  findMatchingPictograph(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
    gridMode: GridMode
  ): Promise<PictographData | null>;
  
  findMatchingCsvRow(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
    gridMode: GridMode
  ): Promise<ParsedCsvRow | null>;
}

export class MotionTesterCsvLookupService implements IMotionTesterCsvLookupService {
  constructor(
    private csvDataService: any, // ICsvDataService
    private optionDataService: any // IOptionDataService
  ) {}

  /**
   * Find matching pictograph from CSV data based on motion parameters
   */
  async findMatchingPictograph(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
    gridMode: GridMode
  ): Promise<PictographData | null> {
    try {
      // First find the matching CSV row
      const matchingRow = await this.findMatchingCsvRow(blueParams, redParams, gridMode);
      
      if (!matchingRow) {
        console.warn("🔍 No matching CSV row found for motion parameters:", {
          blue: blueParams,
          red: redParams,
          gridMode
        });
        return null;
      }

      console.log("✅ Found matching CSV row:", matchingRow);

      // Convert CSV row to PictographData using existing proven pipeline
      const pictographData = this.optionDataService.convertCsvRowToPictographData(
        matchingRow,
        gridMode,
        0 // index
      );

      if (pictographData) {
        // Update the ID to indicate it's from Motion Tester
        pictographData.id = `motion-tester-csv-${matchingRow.letter}-${Date.now()}`;
        
        // Update metadata to indicate source
        pictographData.metadata = {
          ...pictographData.metadata,
          source: "motion_tester_csv_lookup",
          original_csv_row: matchingRow
        };

        console.log(`🎯 Successfully created pictograph for letter "${matchingRow.letter}":`, pictographData);
      }

      return pictographData;
    } catch (error) {
      console.error("❌ Error finding matching pictograph:", error);
      return null;
    }
  }

  /**
   * Find matching CSV row based on motion parameters
   */
  async findMatchingCsvRow(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
    gridMode: GridMode
  ): Promise<ParsedCsvRow | null> {
    try {
      // Ensure CSV data is loaded
      await this.csvDataService.loadCsvData();
      
      if (!this.csvDataService.isReady()) {
        console.error("❌ CSV data service not ready");
        return null;
      }

      // Get parsed CSV data for the grid mode
      const csvRows = this.csvDataService.getParsedData(gridMode);
      
      if (!csvRows || csvRows.length === 0) {
        console.error(`❌ No CSV data available for grid mode: ${gridMode}`);
        return null;
      }

      console.log(`🔍 Searching ${csvRows.length} CSV rows for matching motion parameters...`);
      console.log("🔍 Blue params:", blueParams);
      console.log("🔍 Red params:", redParams);

      // Find exact match based on motion parameters
      const matchingRow = csvRows.find(row => {
        const blueMatch = this.matchesMotionParams(row, "blue", blueParams);
        const redMatch = this.matchesMotionParams(row, "red", redParams);
        
        return blueMatch && redMatch;
      });

      if (matchingRow) {
        console.log(`✅ Found exact match for letter "${matchingRow.letter}":`, matchingRow);
        return matchingRow;
      }

      // If no exact match, try to find closest match (for debugging)
      console.warn("⚠️ No exact match found, looking for partial matches...");
      this.logPartialMatches(csvRows, blueParams, redParams);

      return null;
    } catch (error) {
      console.error("❌ Error finding matching CSV row:", error);
      return null;
    }
  }

  /**
   * Check if CSV row matches motion parameters for a specific color
   */
  private matchesMotionParams(
    row: ParsedCsvRow,
    color: "blue" | "red",
    params: MotionTestParams
  ): boolean {
    const csvMotionType = row[`${color}MotionType`];
    const csvStartLoc = row[`${color}StartLoc`];
    const csvEndLoc = row[`${color}EndLoc`];
    const csvPropRotDir = row[`${color}PropRotDir`];

    // Normalize values for comparison
    const motionTypeMatch = this.normalizeMotionType(csvMotionType) === this.normalizeMotionType(params.motionType);
    const startLocMatch = this.normalizeLocation(csvStartLoc) === this.normalizeLocation(params.startLoc);
    const endLocMatch = this.normalizeLocation(csvEndLoc) === this.normalizeLocation(params.endLoc);
    const propRotDirMatch = this.normalizePropRotDir(csvPropRotDir) === this.normalizePropRotDir(params.propRotDir);

    return motionTypeMatch && startLocMatch && endLocMatch && propRotDirMatch;
  }

  /**
   * Normalize motion type for comparison
   */
  private normalizeMotionType(motionType: string): string {
    return motionType.toLowerCase().trim();
  }

  /**
   * Normalize location for comparison
   */
  private normalizeLocation(location: string): string {
    return location.toLowerCase().trim();
  }

  /**
   * Normalize prop rotation direction for comparison
   */
  private normalizePropRotDir(propRotDir: string): string {
    const normalized = propRotDir.toLowerCase().trim();
    // Handle common variations
    if (normalized === "clockwise" || normalized === "cw") return "cw";
    if (normalized === "counterclockwise" || normalized === "ccw" || normalized === "counter_clockwise") return "ccw";
    if (normalized === "no_rotation" || normalized === "no_rot" || normalized === "none") return "no_rot";
    return normalized;
  }

  /**
   * Log partial matches for debugging
   */
  private logPartialMatches(
    csvRows: ParsedCsvRow[],
    blueParams: MotionTestParams,
    redParams: MotionTestParams
  ): void {
    console.log("🔍 Looking for partial matches...");
    
    // Find rows that match blue params only
    const blueMatches = csvRows.filter(row => this.matchesMotionParams(row, "blue", blueParams));
    if (blueMatches.length > 0) {
      console.log(`🔵 Found ${blueMatches.length} rows matching blue params:`, blueMatches.map(r => r.letter));
    }

    // Find rows that match red params only
    const redMatches = csvRows.filter(row => this.matchesMotionParams(row, "red", redParams));
    if (redMatches.length > 0) {
      console.log(`🔴 Found ${redMatches.length} rows matching red params:`, redMatches.map(r => r.letter));
    }

    // Show some example rows for comparison
    console.log("📊 Sample CSV rows for comparison:");
    csvRows.slice(0, 3).forEach(row => {
      console.log(`Letter ${row.letter}:`, {
        blue: { motionType: row.blueMotionType, startLoc: row.blueStartLoc, endLoc: row.blueEndLoc, propRotDir: row.bluePropRotDir },
        red: { motionType: row.redMotionType, startLoc: row.redStartLoc, endLoc: row.redEndLoc, propRotDir: row.redPropRotDir }
      });
    });
  }
}
