/**
 * Data Service Interfaces
 *
 * Service contracts for data handling, CSV parsing, and query operations.
 */

import type { PictographData } from "$domain/core/pictograph/PictographData";

// ============================================================================
// DATA CONTRACTS
// ============================================================================

export interface CsvDataSet {
  headers: string[];
  rows: string[][];
  metadata?: Record<string, any>;
  diamondData?: string;
  boxData?: string;
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
  [key: string]: string; // Allow additional properties
}

export interface CsvParseResult {
  headers: string[];
  rows: ParsedCsvRow[];
  totalRows: number;
  successfulRows: number;
  errors: Array<{
    error: string;
    rawRow: string;
    lineNumber: number;
    rowIndex?: number;
  }>;
  isValid: boolean;
}

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface ILetterQueryHandler {
  /**
   * Get all codex pictographs for a grid mode
   */
  getAllCodexPictographs(gridMode: any): Promise<PictographData[]>;

  /**
   * Search pictographs by term and grid mode
   */
  searchPictographs(
    searchTerm: string,
    gridMode: any
  ): Promise<PictographData[]>;

  /**
   * Get pictograph by letter and grid mode
   */
  getPictographByLetter(
    letter: any,
    gridMode: any
  ): Promise<PictographData | null>;

  /**
   * Get pictographs for multiple letters
   */
  getPictographsByLetters(
    letters: any[],
    gridMode: any
  ): Promise<PictographData[]>;
}

export interface IMotionQueryHandler {
  /**
   * Query motions based on criteria
   */
  queryMotions(criteria: Record<string, any>): Promise<PictographData[]>;

  /**
   * Get motion data by ID
   */
  getMotionById(motionId: string): Promise<PictographData | null>;

  /**
   * Search motions by pattern
   */
  searchMotions(pattern: string): Promise<PictographData[]>;

  /**
   * Get next options for sequence building
   */
  getNextOptionsForSequence(sequence: unknown[]): Promise<PictographData[]>;
}

export interface ICSVPictographParserService {
  /**
   * Parse CSV data into pictographs
   */
  parseCsv(csvData: string): Promise<CsvParseResult>;

  /**
   * Validate CSV format
   */
  validateCsvFormat(csvData: string): boolean;

  /**
   * Get supported CSV columns
   */
  getSupportedColumns(): string[];
}

// Re-export from data interfaces for backward compatibility
export type { ICsvLoader as ICSVLoader, ICsvLoader } from "./data/ICsvLoader";
export type { ICSVParser } from "./data/ICsvParser";
