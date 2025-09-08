/**
 * Word Card Export Interfaces
 *
 * Service contracts for generating, layouting, and processing word cards
 * for printable formats. Includes caching and batch processing capabilities.
 */

import type {
  BatchExportProgress,
  BatchOperationConfig,
  Page,
  SequenceData,
  WordCardExportOptions,
  WordCardExportResult,
} from "$shared";
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

// Import WordCardExportResult from domain models to avoid duplication
// export interface WordCardExportResult {
//   success: boolean;
//   sequenceId: string;
//   error?: Error;
// }

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
   * Calculate optimal layout for word cards
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
   * Create printable page from word cards
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
 * Service for batch processing word cards
 */
export interface IWordCardBatchService {
  /**
   * Process batch of word cards
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
    options?: WordCardExportOptions
  ): Promise<void>;

  /**
   * Retrieve image from cache
   */
  retrieveImage(
    sequenceId: string,
    options?: WordCardExportOptions
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
  exportPage(page: Page, options: WordCardExportOptions): Promise<Blob>;
  exportPages(pages: Page[], options: WordCardExportOptions): Promise<Blob[]>;
}

/**
 * Word Card Export Orchestrator Interface
 * Orchestrates the word card export process
 */
export interface IWordCardExportOrchestrator {
  exportWordCards(
    sequences: SequenceData[],
    options: WordCardExportOptions
  ): Promise<WordCardExportResult[]>;
  getExportProgress(operationId: string): BatchExportProgress;
}

/**
 * Word Card Batch Processing Service Interface
 * Handles batch processing of word cards
 */
export interface IWordCardBatchProcessingService {
  processBatch(
    sequences: SequenceData[],
    config: BatchOperationConfig,
    processor: (
      sequence: SequenceData,
      index: number
    ) => Promise<WordCardExportResult>,
    onProgress?: (progress: BatchExportProgress) => void
  ): Promise<WordCardExportResult[]>;

  cancelBatch(operationId: string): Promise<void>;
  getBatchStatus(operationId: string): BatchExportProgress | null;
}

/**
 * Word Card Export Progress Tracker Interface
 * Tracks progress of export operations
 */
export interface IWordCardExportProgressTracker {
  startTracking(operationId: string, totalItems: number): void;
  updateProgress(
    operationId: string,
    completed: number,
    currentItem?: string
  ): void;
  completeTracking(operationId: string): void;
  getProgress(operationId: string): BatchExportProgress | null;
  clearProgress(operationId: string): void;
}

/**
 * Word Card Image Generation Service Interface
 * Generates images for word cards
 */
export interface IWordCardImageGenerationService {
  generateWordCardImage(
    sequence: SequenceData,
    dimensions: { width: number; height: number }
  ): Promise<HTMLCanvasElement>;

  generateBatchImages(
    sequences: SequenceData[],
    dimensions: { width: number; height: number }
  ): Promise<Map<string, HTMLCanvasElement>>;
}

/**
 * Word Card Image Conversion Service Interface
 * Converts images between formats
 */
export interface IWordCardImageConversionService {
  convertCanvasToBlob(
    canvas: HTMLCanvasElement,
    format: string,
    quality?: number
  ): Promise<Blob>;

  convertBlobToDataUrl(blob: Blob): Promise<string>;
  resizeImage(
    canvas: HTMLCanvasElement,
    newWidth: number,
    newHeight: number
  ): HTMLCanvasElement;
}

/**
 * Sequence Card Metadata Overlay Service Interface
 * Handles metadata overlays on word cards
 */
export interface IWordCardMetadataOverlayService {
  addMetadataOverlay(
    canvas: HTMLCanvasElement,
    metadata: Record<string, unknown>,
    dimensions: { width: number; height: number }
  ): HTMLCanvasElement;

  createMetadataText(metadata: Record<string, unknown>): string;
}

/**
 * Sequence Card SVG Composition Service Interface
 * Handles SVG composition for word cards
 */
export interface IWordCardSVGCompositionService {
  composeSVG(
    sequence: SequenceData,
    dimensions: { width: number; height: number }
  ): Promise<string>;

  renderSVGToCanvas(
    svgString: string,
    dimensions: { width: number; height: number }
  ): Promise<HTMLCanvasElement>;
}
