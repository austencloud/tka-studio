/**
 * Word Card Export Interfaces
 *
 * Service contracts for generating, layouting, and processing sequence cards
 * for printable formats. Includes caching and batch processing capabilities.
 */

import type { SequenceData } from "$shared/domain";
import type { ExportOptions } from "$wordcard/domain";

// Local type definitions for missing domain types
interface GridLayout {
  rows: number;
  columns: number;
}

interface LayoutRecommendation {
  gridLayout: GridLayout;
  cardSize: { width: number; height: number };
  confidence: number;
}

interface Margins {
  top: number;
  right: number;
  bottom: number;
  left: number;
}

interface Page {
  id: string;
  sequences: SequenceData[];
  pageNumber: number;
}

// ============================================================================
// SEQUENCE CARD SERVICE INTERFACES
// ============================================================================

/**
 * Service for generating word card images
 */
export interface IWordCardImageService {
  /**
   * Generate image for a word card
   */
  generateWordCardImage(
    sequenceId: string,
    width: number,
    height: number
  ): Promise<HTMLCanvasElement>;

  /**
   * Batch generate word card images
   */
  batchGenerateImages(
    sequenceIds: string[],
    dimensions: { width: number; height: number }
  ): Promise<Map<string, HTMLCanvasElement>>;
}

/**
 * Service for managing word card layouts
 */
export interface IWordCardLayoutService {
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
 * Service for managing word card pages
 */
export interface IWordCardPageService {
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
export interface IWordCardBatchService {
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
 * Service for caching word card data
 */
export interface IWordCardCacheService {
  /**
   * Cache word card data
   */
  cacheWordCard(sequenceId: string, data: SequenceData): Promise<void>;

  /**
   * Get cached word card
   */
  getCachedWordCard(sequenceId: string): Promise<SequenceData | null>;

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

/**
 * Page Factory Service Interface
 * Handles page creation and layout management
 */
export interface IPageFactoryService {
  createPage(sequences: SequenceData[], config: any): any;
  createPages(sequences: SequenceData[], options: any): any;
  calculateLayout(sequences: SequenceData[]): any;
  validatePageOptions(options: any): { isValid: boolean; errors?: string[] };
}

/**
 * Printable Page Layout Service Interface
 * Handles printable page layout calculations
 */
export interface IPrintablePageLayoutService {
  calculatePageDimensions(paperSize: string, orientation: string): any;
  calculateContentArea(dimensions: any, margins: any): any;
  calculateMargins(paperSize: string): any;
  calculateLayout(request: any): any;
  validateLayout(layout: any): any;
  calculateOptimalGrid(
    aspectRatio: number,
    contentArea: any,
    cardSize: any
  ): any;
}

/**
 * Browse Service Interface
 * Handles browsing and sequence retrieval
 */
export interface IBrowseService {
  getSequences(): Promise<SequenceData[]>;
  getSequenceById(id: string): Promise<SequenceData | null>;
}

/**
 * Page Image Export Service Interface
 * Handles image export functionality
 */
export interface IPageImageExportService {
  exportPage(page: any, options: any): Promise<Blob>;
  exportPages(pages: any[], options: any): Promise<Blob[]>;
}

/**
 * Word Card Export Orchestrator Interface
 * Orchestrates the word card export process
 */
export interface IWordCardExportOrchestrator {
  exportWordCards(sequences: SequenceData[], options: any): Promise<any>;
  getExportProgress(operationId: string): any;
}
