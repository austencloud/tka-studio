/**
 * CSV Pictograph Parser Service Interface
 *
 * Interface for converting CSV rows to PictographData objects.
 * Handles row-level parsing of BoxPictographDataframe.csv data.
 */

import type { PictographData } from "$shared";

export interface CSVRow {
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
}

export interface ICSVPictographParserService {
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