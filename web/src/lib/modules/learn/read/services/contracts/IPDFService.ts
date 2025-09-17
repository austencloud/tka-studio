/**
 * PDF Service Contract
 *
 * Interface for PDF processing and page conversion services.
 */

import type { PDFDocumentInfo, PDFPageData } from "../../domain";

/**
 * Service for processing PDF documents and converting pages to images
 */
export interface IPDFService {
  /**
   * Load a PDF document from a URL
   * @param url - URL to the PDF file
   * @returns Promise resolving to document info
   */
  loadPDF(url: string): Promise<PDFDocumentInfo>;

  /**
   * Convert all pages of the loaded PDF to image data URLs
   * @param onProgress - Optional callback for progress updates
   * @returns Promise resolving to array of page data
   */
  convertPagesToImages(
    onProgress?: (progress: number, stage: string) => void
  ): Promise<PDFPageData[]>;

  /**
   * Convert a specific page to an image data URL
   * @param pageNumber - Page number (1-based)
   * @param scale - Scale factor for rendering (default: 1.5)
   * @returns Promise resolving to page data
   */
  convertPageToImage(pageNumber: number, scale?: number): Promise<PDFPageData>;

  /**
   * Get information about the currently loaded PDF
   * @returns Document info or null if no PDF is loaded
   */
  getDocumentInfo(): PDFDocumentInfo | null;

  /**
   * Check if a PDF is fully cached in persistent storage
   * @param url - URL to the PDF file
   * @returns Promise resolving to true if fully cached
   */
  hasCachedPDF(url: string): Promise<boolean>;

  /**
   * Clean up resources and unload the current PDF
   */
  cleanup(): void;
}