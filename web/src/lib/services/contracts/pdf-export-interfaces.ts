/**
 * PDF Export Interfaces
 *
 * Service contracts for exporting pages as PDF documents.
 * Supports both individual page and multi-page PDF generation.
 */

import type { ExportResult } from "$domain";
import type { PDFExportOptions } from "$domain/data-interfaces/export-config-interfaces";
import type { Page } from "../../domain/sequence-card/PageLayoutTypes";

// ============================================================================
// PDF EXPORT SERVICES
// ============================================================================

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
