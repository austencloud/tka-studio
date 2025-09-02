/**
 * Page Export Interfaces
 *
 * Service contracts for exporting page elements as images and preparing
 * pages for printing. Handles both individual page and sequence image exports.
 */

import type {
  BatchExportResult,
  ExportProgress,
  ExportResult,
  ImageExportOptions,
} from "$domain";

// ============================================================================
// PAGE IMAGE EXPORT SERVICES
// ============================================================================

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
  ): Promise<ExportResult>;

  /**
   * Export multiple page elements as individual images
   */
  exportPagesAsImages(
    pageElements: HTMLElement[],
    options: ImageExportOptions,
    onProgress?: (progress: ExportProgress) => void
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

/**
 * Service for preparing pages for print
 */
export interface IPrintPageService {
  /**
   * Prepare page for print output
   */
  preparePage(page: HTMLElement): HTMLElement;

  /**
   * Prepare multiple pages for printing
   */
  preparePagesForPrint(pageElements: HTMLElement[]): HTMLElement[];

  /**
   * Clean up after printing
   */
  cleanupAfterPrint(): void;
}
