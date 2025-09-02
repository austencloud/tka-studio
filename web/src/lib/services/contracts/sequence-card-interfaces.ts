/**
 * Sequence Card Export Interfaces
 *
 * Service contracts for generating, layouting, and processing sequence cards
 * for printable formats. Includes caching and batch processing capabilities.
 */

import type { ExportOptions, SequenceData, Page } from "$domain";

// ============================================================================
// SEQUENCE CARD LAYOUT TYPES
// ============================================================================

export interface GridLayout {
  rows: number;
  columns: number;
  cardWidth: number;
  cardHeight: number;
  spacing: { horizontal: number; vertical: number };
}

export interface LayoutRecommendation {
  rows: number;
  columns: number;
  efficiency: number;
  description: string;
}

export interface Margins {
  top: number;
  right: number;
  bottom: number;
  left: number;
}

// ============================================================================
// SEQUENCE CARD SERVICE INTERFACES
// ============================================================================

/**
 * Service for generating sequence card images
 */
export interface ISequenceCardImageService {
  /**
   * Generate image for a sequence card
   */
  generateSequenceCardImage(
    sequenceId: string,
    width: number,
    height: number
  ): Promise<HTMLCanvasElement>;

  /**
   * Batch generate sequence card images
   */
  batchGenerateImages(
    sequenceIds: string[],
    dimensions: { width: number; height: number }
  ): Promise<Map<string, HTMLCanvasElement>>;
}

/**
 * Service for managing sequence card layouts
 */
export interface ISequenceCardLayoutService {
  /**
   * Calculate optimal layout for sequence cards
   */
  calculateLayout(
    cardCount: number,
    pageSize: { width: number; height: number },
    margins: Margins
  ): GridLayout;

  /**
   * Get layout recommendations
   */
  getLayoutRecommendations(cardCount: number): LayoutRecommendation[];
}

/**
 * Service for managing sequence card pages
 */
export interface ISequenceCardPageService {
  /**
   * Create printable page from sequence cards
   */
  createPage(
    sequences: SequenceData[],
    layout: GridLayout,
    pageNumber: number
  ): Promise<Page>;

  /**
   * Generate multiple pages
   */
  generatePages(sequences: SequenceData[], layout: GridLayout): Promise<Page[]>;
}

/**
 * Service for batch processing sequence cards
 */
export interface ISequenceCardBatchService {
  /**
   * Process batch of sequence cards
   */
  processBatch(
    sequences: SequenceData[],
    batchSize: number,
    processor: (batch: SequenceData[]) => Promise<void>
  ): Promise<void>;

  /**
   * Get batch processing status
   */
  getBatchStatus(): {
    total: number;
    processed: number;
    remaining: number;
    isProcessing: boolean;
  };
}

/**
 * Service for caching sequence card data
 */
export interface ISequenceCardCacheService {
  /**
   * Cache sequence card data
   */
  cacheSequenceCard(sequenceId: string, data: SequenceData): Promise<void>;

  /**
   * Get cached sequence card
   */
  getCachedSequenceCard(sequenceId: string): Promise<SequenceData | null>;

  /**
   * Store image in cache
   */
  storeImage(
    sequenceId: string,
    imageBlob: Blob,
    options?: ExportOptions
  ): Promise<void>;

  /**
   * Retrieve image from cache
   */
  retrieveImage(
    sequenceId: string,
    options?: ExportOptions
  ): Promise<Blob | null>;

  /**
   * Clear cache
   */
  clearCache(): Promise<void>;

  /**
   * Get cache statistics
   */
  getCacheStats(): {
    entryCount: number;
    totalSize: number;
    hitRate: number;
  };
}
