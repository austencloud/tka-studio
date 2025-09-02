/**
 * Batch Export Interfaces
 *
 * Service contracts for handling large-scale export operations with
 * progress monitoring, cancellation, and resource management.
 */

import type {
  ExportProgress,
  BatchExportOptions,
  BatchExportResult,
  ImageExportOptions,
  PDFExportOptions,
  Page,
} from "$domain";

// ============================================================================
// BATCH EXPORT SERVICES
// ============================================================================

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
    results: Array<{ success: boolean; error?: Error }>;
  };

  /**
   * Cleanup batch export resources
   */
  cleanup(): Promise<void>;
}
