import type { CsvParseResult, ParsedCsvRow } from "../data-interfaces";

/**
 * CSV Parser Service Interface
 *
 * Interface for CSV parsing service that provides consistent CSV parsing functionality
 * used across all data services. Handles line splitting, header extraction, and row
 * parsing with error handling.
 */

/**
 * Service for parsing CSV data
 *
 * Provides consistent CSV parsing functionality used across all data services.
 * Handles line splitting, header extraction, and row parsing with error handling.
 */
export interface ICSVParser {
  parseCSV(csvText: string): CsvParseResult;
  parseCSVToRows(csvText: string): ParsedCsvRow[];
  validateCSVStructure(csvText: string): { isValid: boolean; errors: string[] };
  createRowFromValues(headers: string[], values: string[]): ParsedCsvRow;
}
