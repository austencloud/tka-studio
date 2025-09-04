/**
 * TKA Image Export File Interfaces
 *
 * Service contracts for file operations, downloads, and browser export
 * functionality in the TKA image export system.
 */

// ============================================================================
// FILE EXPORT SERVICES
// ============================================================================

/**
 * File export service for browser downloads
 * Equivalent to desktop ImageSaver
 */
export interface IFileExportService {
  /**
   * Export canvas as blob
   */
  canvasToBlob(
    canvas: HTMLCanvasElement,
    format: "PNG" | "JPEG" | "WebP",
    quality?: number
  ): Promise<Blob>;

  /**
   * Convert canvas to data URL for immediate display
   */
  canvasToDataURL(
    canvas: HTMLCanvasElement,
    format: "PNG" | "JPEG" | "WebP",
    quality?: number
  ): string;

  /**
   * Download blob as file
   */
  downloadBlob(blob: Blob, filename: string): Promise<void>;

  /**
   * Generate versioned filename
   */
  generateVersionedFilename(
    word: string,
    format: string,
    timestamp?: Date
  ): string;

  /**
   * Validate filename
   */
  validateFilename(filename: string): boolean;

  /**
   * Get supported export formats
   */
  getSupportedFormats(): string[];
}

// ============================================================================
// SERVICE INTERFACE SYMBOLS
// ============================================================================

export const IFileExportServiceInterface = Symbol.for("IFileExportService");
