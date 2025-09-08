/**
 * CSV Pictograph Parser Service Interface
 *
 * Interface for converting CSV rows to PictographData objects.
 * Handles row-level parsing of BoxPictographDataframe.csv data.
 */

import type { CSVRow, PictographData } from "$shared";



export interface ICSVPictographParser {
  /**
   * Convert a CSV row to PictographData object
   */
  parseCSVRowToPictograph(row: CSVRow): PictographData;

  /**
   * Parse multiple CSV rows for a letter
   */
  parseLetterPictographs(letterRows: CSVRow[]): PictographData[];

  /**
   * Validate that a CSV row has the expected structure
   */
  validateCSVRow(row: unknown): row is CSVRow;
}
