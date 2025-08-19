/**
 * CSVParserService - Centralized CSV parsing utilities
 * 
 * Provides consistent CSV parsing functionality used across all data services.
 * Handles line splitting, header extraction, and row parsing with error handling.
 */

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
  // Add index signature to make it compatible with Record<string, string>
  [key: string]: string;
}

export interface CSVParseResult {
  headers: string[];
  rows: ParsedCsvRow[];
  totalRows: number;
  successfulRows: number;
  errors: Array<{ rowIndex: number; error: string; rawRow: string }>;
}

export interface ICSVParserService {
  parseCSV(csvText: string): CSVParseResult;
  parseCSVToRows(csvText: string): ParsedCsvRow[];
  validateCSVStructure(csvText: string): { isValid: boolean; errors: string[] };
  createRowFromValues(headers: string[], values: string[]): ParsedCsvRow;
}

export class CSVParserService implements ICSVParserService {
  /**
   * Parse CSV text into structured result with detailed error reporting
   */
  parseCSV(csvText: string): CSVParseResult {
    const result: CSVParseResult = {
      headers: [],
      rows: [],
      totalRows: 0,
      successfulRows: 0,
      errors: []
    };

    try {
      const lines = csvText.trim().split("\n");
      
      if (lines.length < 2) {
        result.errors.push({
          rowIndex: 0,
          error: "CSV must have at least header and one data row",
          rawRow: csvText
        });
        return result;
      }

      // Parse headers
      result.headers = lines[0].split(",").map(h => h.trim());
      result.totalRows = lines.length - 1; // Exclude header

      // Parse data rows
      for (let i = 1; i < lines.length; i++) {
        try {
          const values = lines[i].split(",").map(v => v.trim());
          const row = this.createRowFromValues(result.headers, values);
          
          if (this.isValidRow(row)) {
            result.rows.push(row);
            result.successfulRows++;
          } else {
            result.errors.push({
              rowIndex: i,
              error: "Row validation failed - missing required fields",
              rawRow: lines[i]
            });
          }
        } catch (error) {
          result.errors.push({
            rowIndex: i,
            error: error instanceof Error ? error.message : "Unknown parsing error",
            rawRow: lines[i]
          });
        }
      }

      return result;
    } catch (error) {
      result.errors.push({
        rowIndex: 0,
        error: `CSV parsing failed: ${error instanceof Error ? error.message : "Unknown error"}`,
        rawRow: csvText.substring(0, 100) + "..."
      });
      return result;
    }
  }

  /**
   * Simple CSV parsing that returns only successful rows (legacy compatibility)
   */
  parseCSVToRows(csvText: string): ParsedCsvRow[] {
    const result = this.parseCSV(csvText);
    
    if (result.errors.length > 0) {
      console.warn(`⚠️ CSV parsing had ${result.errors.length} errors out of ${result.totalRows} rows`);
      result.errors.forEach(error => {
        console.warn(`⚠️ Row ${error.rowIndex}: ${error.error}`);
      });
    }

    return result.rows;
  }

  /**
   * Validate CSV structure before parsing
   */
  validateCSVStructure(csvText: string): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (!csvText || csvText.trim().length === 0) {
      errors.push("CSV text is empty");
      return { isValid: false, errors };
    }

    const lines = csvText.trim().split("\n");
    
    if (lines.length < 2) {
      errors.push("CSV must have at least a header row and one data row");
      return { isValid: false, errors };
    }

    // Check header structure
    const headers = lines[0].split(",").map(h => h.trim());
    const requiredHeaders = ["letter", "startPosition", "endPosition"];
    
    for (const required of requiredHeaders) {
      if (!headers.includes(required)) {
        errors.push(`Missing required header: ${required}`);
      }
    }

    // Check for consistent column count
    const headerCount = headers.length;
    for (let i = 1; i < Math.min(lines.length, 10); i++) { // Check first 10 rows
      const columnCount = lines[i].split(",").length;
      if (columnCount !== headerCount) {
        errors.push(`Row ${i} has ${columnCount} columns, expected ${headerCount}`);
      }
    }

    return { isValid: errors.length === 0, errors };
  }

  /**
   * Create a ParsedCsvRow from headers and values
   */
  createRowFromValues(headers: string[], values: string[]): ParsedCsvRow {
    const row: Record<string, string> = {};

    headers.forEach((header, index) => {
      row[header] = values[index] || "";
    });

    // Ensure required fields exist with defaults
    return {
      letter: row.letter || "",
      startPosition: row.startPosition || "",
      endPosition: row.endPosition || "",
      timing: row.timing || "",
      direction: row.direction || "",
      blueMotionType: row.blueMotionType || "",
      blueRotationDirection: row.blueRotationDirection || "",
      blueStartLocation: row.blueStartLocation || row.blueStartLoc || "", // Handle variations
      blueEndLocation: row.blueEndLocation || row.blueendLocation || "", // Handle variations
      redMotionType: row.redMotionType || "",
      redRotationDirection: row.redRotationDirection || "",
      redStartLocation: row.redStartLocation || row.redStartLoc || "", // Handle variations
      redEndLocation: row.redEndLocation || row.redendLocation || "", // Handle variations
      ...row // Include all other fields
    } as ParsedCsvRow;
  }

  /**
   * Validate that a row has required fields
   */
  private isValidRow(row: ParsedCsvRow): boolean {
    return !!(row.letter && row.startPosition && row.endPosition);
  }

  /**
   * Get column mapping for different CSV formats (if needed)
   */
  getColumnMapping(headers: string[]): Record<string, string> {
    const mapping: Record<string, string> = {};
    
    // Handle common variations in column names
    const variations: Record<string, string[]> = {
      blueStartLocation: ["blueStartLocation", "blueStartLoc", "blue_start_location"],
      blueEndLocation: ["blueEndLocation", "blueendLocation", "blue_end_location"],
      redStartLocation: ["redStartLocation", "redStartLoc", "red_start_location"],
      redEndLocation: ["redEndLocation", "redendLocation", "red_end_location"]
    };

    for (const [standardName, variants] of Object.entries(variations)) {
      for (const variant of variants) {
        if (headers.includes(variant)) {
          mapping[standardName] = variant;
          break;
        }
      }
    }

    return mapping;
  }
}
