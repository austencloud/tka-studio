/**
 * Word Card Export Interfaces
 *
 * Service contracts for generating, layouting, and processing sequence cards
 * for printable formats. Includes caching and batch processing capabilities.
 */

import type { SequenceData } from "$shared/domain";
import type { ExportOptions, Page } from "$wordcard/domain";
import type {
  GridCalculationOptions,
  GridLayout,
  LayoutCalculationRequest,
  LayoutCalculationResult,
  LayoutRecommendation,
  LayoutValidationResult,
  PageCreationOptions,
  PageDimensions,
  PageLayoutConfig,
  PageMargins,
  Rectangle,
  WordCardGridConfig,
} from "../../domain/models/PageLayout";
import type {
  PageOrientation,
  WordCardPaperSize,
} from "../../domain/types/PageLayoutTypes";
// import type {
//     BatchExportProgress,
//     WordCardExportResult
// } from "../../domain/models/WordCardExport";

// Temporary interface definitions
interface BatchExportProgress {
  completed: number;
  total: number;
  currentItem?: string;
  stage?: string;
}

interface WordCardExportResult {
  success: boolean;
  sequenceId: string;
  error?: Error;
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
    margins: PageMargins
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
  createPage(sequences: SequenceData[], config: PageCreationOptions): Page;
  createPages(sequences: SequenceData[], options: PageCreationOptions): Page[];
  calculateLayout(sequences: SequenceData[]): LayoutCalculationResult;
  validatePageOptions(options: PageCreationOptions): LayoutValidationResult;
}

/**
 * Printable Page Layout Service Interface
 * Handles printable page layout calculations
 */
export interface IPrintablePageLayoutService {
  calculatePageDimensions(
    paperSize: WordCardPaperSize,
    orientation: PageOrientation
  ): PageDimensions;
  calculateContentArea(
    dimensions: PageDimensions,
    margins: PageMargins
  ): Rectangle;
  calculateMargins(paperSize: WordCardPaperSize): PageMargins;
  calculateLayout(request: LayoutCalculationRequest): LayoutCalculationResult;
  validateLayout(layout: PageLayoutConfig): LayoutValidationResult;
  calculateOptimalGrid(
    aspectRatio: number,
    contentArea: Rectangle,
    options?: Partial<GridCalculationOptions>
  ): WordCardGridConfig;
}

/**
 * Browse Service Interface
 * Handles browsing and sequence retrieval
 */
export interface IGalleryService {
  getSequences(): Promise<SequenceData[]>;
  getSequenceById(id: string): Promise<SequenceData | null>;
}

/**
 * Page Image Export Service Interface
 * Handles image export functionality
 */
export interface IPageImageExportService {
  exportPage(page: Page, options: ExportOptions): Promise<Blob>;
  exportPages(pages: Page[], options: ExportOptions): Promise<Blob[]>;
}

/**
 * Word Card Export Orchestrator Interface
 * Orchestrates the word card export process
 */
export interface IWordCardExportOrchestrator {
  exportWordCards(
    sequences: SequenceData[],
    options: ExportOptions
  ): Promise<WordCardExportResult[]>;
  getExportProgress(operationId: string): BatchExportProgress;
}
