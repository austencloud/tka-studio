/**
 * CSV Parsing Domain Types
 *
 * Domain types for CSV parsing results and row structures.
 * These represent the core data structures used across the application.
 */

/**
 * Parsed CSV row structure
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

/**
 * CSV parsing result structure
 */
export interface CSVParseResult {
  headers: string[];
  rows: ParsedCsvRow[];
  totalRows: number;
  successfulRows: number;
  errors: Array<{ rowIndex: number; error: string; rawRow: string }>;
}
/**
 * CSV dataset structure
 */
export interface CsvDataSet {
  diamondData: string;
  boxData: string;
}
