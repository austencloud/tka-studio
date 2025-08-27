/**
 * Data Service Interfaces
 *
 * Interfaces for data loading, parsing, querying, and transformation services.
 * This includes CSV handling, letter queries, and data processing operations.
 */

import type { PictographData } from "$lib/domain";
import type { GridMode, Letter } from "$lib/domain";

// ============================================================================
// LETTER QUERY SERVICE INTERFACES
// ============================================================================

/**
 * Service for querying pictographs by letter
 *
 * Single responsibility: Query pictographs by letter using LetterMappingRepository
 * Uses shared services for CSV loading, parsing, and transformation.
 */
export interface ILetterQueryService {
  getPictographByLetter(
    letter: Letter,
    gridMode: GridMode
  ): Promise<PictographData | null>;
  getAllCodexPictographs(gridMode: GridMode): Promise<PictographData[]>;
  getAllPictographVariations(gridMode: GridMode): Promise<PictographData[]>;
  searchPictographs(
    searchTerm: string,
    gridMode: GridMode
  ): Promise<PictographData[]>;
  getPictographsByLetters(
    letters: Letter[],
    gridMode: GridMode
  ): Promise<PictographData[]>;
}

// ============================================================================
// CSV LOADING SERVICE INTERFACES
// ============================================================================

/**
 * CSV dataset structure
 */
export interface CsvDataSet {
  diamondData: string;
  boxData: string;
}

/**
 * Service for loading and caching CSV data
 *
 * Handles loading and caching of CSV data from static files or preloaded window data.
 * Provides a single source of truth for raw CSV content without parsing logic.
 */
export interface ICsvLoaderService {
  loadCsvData(): Promise<CsvDataSet>;
  getCsvData(): CsvDataSet | null;
  clearCache(): void;
}

// ============================================================================
// CSV PARSING SERVICE INTERFACES
// ============================================================================

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
 * Service for parsing CSV data
 *
 * Provides consistent CSV parsing functionality used across all data services.
 * Handles line splitting, header extraction, and row parsing with error handling.
 */
export interface ICSVParserService {
  parseCSV(csvText: string): CSVParseResult;
  parseCSVToRows(csvText: string): ParsedCsvRow[];
  validateCSVStructure(csvText: string): { isValid: boolean; errors: string[] };
  createRowFromValues(headers: string[], values: string[]): ParsedCsvRow;
}

// ============================================================================
// MOTION QUERY SERVICE
// ============================================================================

/**
 * Motion Query Parameters
 */
export interface MotionQueryParams {
  startLocation: string;
  endLocation: string;
  motionType: string;
}

/**
 * Motion Query Service Interface
 */
export interface IMotionQueryService {
  findPictographByMotionParams(
    params: MotionQueryParams,
    gridMode: GridMode
  ): Promise<PictographData | null>;
  getNextOptionsForSequence(sequence: unknown[]): Promise<PictographData[]>;
  findPictographsByLetter(letter: string): Promise<PictographData[]>;
  findPictographsByMotionType(motionType: string): Promise<PictographData[]>;
  findPictographsByStartLocation(location: string): Promise<PictographData[]>;
  findPictographsByEndLocation(location: string): Promise<PictographData[]>;
  findPictographsByGridMode(gridMode: GridMode): Promise<PictographData[]>;
  getAllPictographs(): Promise<PictographData[]>;
  getAvailableMotionTypes(): Promise<string[]>;
  getAvailableStartLocations(): Promise<string[]>;
  getAvailableEndLocations(): Promise<string[]>;
  getAvailableLetters(): Promise<string[]>;
}
