/**
 * Data Service Interfaces
 *
 * Service contracts for data handling, CSV parsing, and query operations.
 */

import type { PictographData } from "$domain";

// ============================================================================
// DATA CONTRACTS - MOVED TO DOMAIN
// ============================================================================
// CSV data models have been moved to domain/models/core/csv-handling/CsvModels.ts
// Import them from $domain instead

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

// ICSVPictographParserService moved to dedicated contract file

// Re-export from data interfaces for backward compatibility
export type { ICsvLoader as ICSVLoader, ICsvLoader } from "./data/ICsvLoader";
// ICSVParser moved to application/ICSVParser.ts
