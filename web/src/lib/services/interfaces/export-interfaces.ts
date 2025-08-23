/**
 * Export Service Interfaces
 *
 * Service contracts for exporting printable pages as images and PDFs.
 * Supports both individual page and batch export operations.
 */

import type { Page } from "../../domain/PageLayoutTypes";
import type { ExportOptions, ExportResult, SequenceData } from "./domain-types";

// ============================================================================
// EXPORT CONFIGURATION TYPES
// ============================================================================

export interface ImageExportOptions {
  format: "PNG" | "JPEG" | "WebP";
  quality: number; // 0-1 for JPEG/WebP
  width?: number;
  height?: number;
  scale: number; // Device pixel ratio multiplier
  backgroundColor?: string;
}

export interface PDFExportOptions {
  orientation: "portrait" | "landscape";
  paperSize: "A4" | "Letter" | "Legal" | "Tabloid";
  margin: {
    top: number;
    right: number;
    bottom: number;
    left: number;
  };
  enablePageNumbers: boolean;
  quality: "low" | "medium" | "high";
}

export interface BatchExportOptions {
  batchSize: number;
  enableProgressReporting: boolean;
  memoryOptimization: boolean;
  filenameTemplate: string; // e.g., "sequence-cards-{pageNumber}.pdf"
  outputFormat: "individual" | "combined";
}

// ============================================================================
// EXPORT RESULT TYPES
// ============================================================================

// ExportResult is imported from domain layer via domain-types.ts
// Service layer extends it with additional service-specific properties

export interface ServiceExportResult extends ExportResult {
  filename: string;
  metadata: {
    format: string;
    size: number; // bytes
    dimensions?: { width: number; height: number };
    pageCount?: number;
    processingTime: number; // milliseconds
  };
}

export interface BatchExportResult {
  totalPages: number;
  successCount: number;
  failureCount: number;
  results: ServiceExportResult[];
  totalProcessingTime: number;
  errors: Error[];
}

export interface ExportProgress {
  current: number;
  total: number;
  percentage: number;
  currentPage?: number;
  currentOperation: string;
  estimatedTimeRemaining?: number;
}

// ============================================================================
// SERVICE INTERFACES
// ============================================================================

/**
 * Main export service for handling different export types
 */
export interface IExportService {
  /**
   * Export single page as image
   */
  exportPageAsImage(
    pageElement: HTMLElement,
    options: ImageExportOptions
  ): Promise<ExportResult>;

  /**
   * Export pages as PDF
   */
  exportAsPDF(pages: Page[], options: PDFExportOptions): Promise<ExportResult>;

  /**
   * Export batch of pages
   */
  exportBatch(
    pages: Page[],
    options: BatchExportOptions & (ImageExportOptions | PDFExportOptions)
  ): Promise<BatchExportResult>;
}

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

/**
 * Enhanced export service with additional features
 */
export interface IEnhancedExportService extends IExportService {
  /**
   * Export with preview generation
   */
  exportWithPreview(
    pages: Page[],
    options: ExportOptions
  ): Promise<ExportResult & { preview: Blob }>;

  /**
   * Get export capabilities
   */
  getExportCapabilities(): {
    supportedFormats: string[];
    maxPageCount: number;
    maxFileSize: number;
  };
}

/**
 * Service for exporting individual pages as images
 */
export interface IPageImageExportService {
  /**
   * Export a single page element as an image
   */
  exportPageAsImage(
    pageElement: HTMLElement,
    options: ImageExportOptions
  ): Promise<ServiceExportResult>;

  /**
   * Export multiple page elements as individual images
   */
  exportPagesAsImages(
    pageElements: HTMLElement[],
    options: ImageExportOptions
  ): Promise<BatchExportResult>;

  /**
   * Get supported image formats
   */
  getSupportedFormats(): string[];

  /**
   * Validate export options
   */
  validateExportOptions(options: ImageExportOptions): boolean;

  /**
   * Get recommended settings for different use cases
   */
  getRecommendedSettings(
    useCase: "print" | "web" | "archive"
  ): ImageExportOptions;

  /**
   * Cancel ongoing export operation
   */
  cancelExport(): void;
}

/**
 * Service for exporting pages as PDFs
 */
export interface IPDFExportService {
  /**
   * Export pages as a single PDF document
   */
  exportPagesToPDF(
    pages: Page[],
    options: PDFExportOptions
  ): Promise<ExportResult>;

  /**
   * Export individual page as PDF
   */
  exportPageToPDF(page: Page, options: PDFExportOptions): Promise<ExportResult>;

  /**
   * Get PDF generation capabilities
   */
  getPDFCapabilities(): {
    maxPageCount: number;
    supportedPaperSizes: string[];
    supportedOrientations: string[];
  };

  /**
   * Validate PDF export options
   */
  validatePDFOptions(options: PDFExportOptions): boolean;

  /**
   * Get recommended PDF settings
   */
  getRecommendedPDFSettings(pageCount: number): PDFExportOptions;
}

/**
 * Service for batch export operations
 */
export interface IBatchExportService {
  /**
   * Export large number of pages in batches
   */
  exportInBatches(
    pages: Page[],
    options: BatchExportOptions & (ImageExportOptions | PDFExportOptions)
  ): Promise<BatchExportResult>;

  /**
   * Monitor batch export progress
   */
  onProgress(callback: (progress: ExportProgress) => void): void;

  /**
   * Cancel ongoing batch export
   */
  cancelBatchExport(): Promise<void>;

  /**
   * Get current batch export status
   */
  getBatchStatus(): {
    isRunning: boolean;
    progress: ExportProgress;
    results: ExportResult[];
  };

  /**
   * Cleanup batch export resources
   */
  cleanup(): Promise<void>;
}

/**
 * Service for preparing pages for print
 */
export interface IPrintPageService {
  /**
   * Prepare page for print output
   */
  preparePage(page: Page): HTMLElement;

  /**
   * Prepare multiple pages for printing
   */
  preparePagesForPrint(pageElements: HTMLElement[]): HTMLElement[];

  /**
   * Clean up after printing
   */
  cleanupAfterPrint(): void;
}

/**
 * Service for loading and generating sequence images
 */
export interface ISequenceImageService {
  /**
   * Load sequence image from URL or generate placeholder
   */
  loadSequenceImage(sequenceId: string): Promise<HTMLImageElement | null>;

  /**
   * Generate placeholder image for sequence
   */
  generatePlaceholderImage(
    sequenceName: string,
    beatCount: number,
    width: number,
    height: number
  ): Promise<HTMLCanvasElement>;

  /**
   * Cache sequence image
   */
  cacheSequenceImage(sequenceId: string, imageBlob: Blob): Promise<void>;

  /**
   * Clear image cache
   */
  clearImageCache(): Promise<void>;

  /**
   * Get cache statistics
   */
  getCacheStats(): {
    entryCount: number;
    totalSize: number;
    hitRate: number;
  };
}

// ============================================================================
// HELPER TYPES
// ============================================================================

interface GridLayout {
  rows: number;
  columns: number;
  cardWidth: number;
  cardHeight: number;
  spacing: { horizontal: number; vertical: number };
}

interface LayoutRecommendation {
  rows: number;
  columns: number;
  efficiency: number;
  description: string;
}

interface Margins {
  top: number;
  right: number;
  bottom: number;
  left: number;
}
