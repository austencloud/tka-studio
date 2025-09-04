/**
 * Export Service Interfaces
 *
 * Service contracts for exporting printable pages as images and PDFs.
 * Supports both individual page and batch export operations.
 *
 * ============================================================================
 * REFACTORED STRUCTURE: This file now re-exports from focused interface files
 * ============================================================================
 */

// Note: Import types directly from $domain
// instead of re-exporting them from service contracts

// Page export services (image generation, printing)
export type {
  IPageImageExportService,
  IPrintPageService,
  ISequenceImageService
} from "./page-export-interfaces";

// PDF export services
export type { IPDFExportService } from "./pdf-export-interfaces";

// Word card services (layout, generation, caching)
export type {
  IWordCardBatchProcessingService,
  IWordCardExportOrchestrator,
  IWordCardExportProgressTracker,
  IWordCardImageConversionService,
  IWordCardImageGenerationService,
  IWordCardMetadataOverlayService,
  IWordCardSVGCompositionService
} from "./word-card-export-interfaces";

// Batch export services (large-scale operations)
export type { IBatchExportService } from "./IBatchExportService";

// ============================================================================
// MAIN ORCHESTRATOR SERVICES (kept in this file)
// ============================================================================

import type {
  BatchExportOptions,
  BatchExportResult,
  ExportResult,
  ImageExportOptions,
  PDFExportOptions,
  Page,
} from "$shared/domain";

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
 * Enhanced export service with additional features
 */
export interface IEnhancedExportService extends IExportService {
  /**
   * Export with preview generation
   */
  exportWithPreview(
    pages: Page[],
    options: ImageExportOptions | PDFExportOptions
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
