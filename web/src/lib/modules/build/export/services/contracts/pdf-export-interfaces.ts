/**
 * PDF Export Interfaces
 *
 * Service contracts for exporting pages as PDF documents.
 * Supports both individual page and multi-page PDF generation.
 */

import type { ExportResult } from "$shared/domain";
import type { Page } from "../../../../word-card/domain";

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
    options: any
  ): Promise<ExportResult>;

  /**
   * Export individual page as PDF
   */
  exportPageToPDF(page: Page, options: any): Promise<ExportResult>;

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
  validatePDFOptions(options: any): boolean;

  /**
   * Get recommended PDF settings
   */
  getRecommendedPDFSettings(pageCount: number): any;
}
