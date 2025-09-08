/**
 * File Export Service
 *
 * Handles file export operations for the browser environment, providing
 * functionality equivalent to the desktop ImageSaver. This service manages
 * canvas-to-blob conversion and browser downloads.
 *
 * Uses the existing file-download utility for consistency with the app.
 */

import type { IFileDownloadService } from "$shared/foundation/services/contracts";
import { TYPES } from "$shared/inversify";
import { inject, injectable } from "inversify";

@injectable()
export class FileExportService {
  constructor(
    @inject(TYPES.IFileDownloadService) private fileDownloadService: IFileDownloadService
  ) {}
  /**
   * Convert canvas to blob
   * Handles both PNG and JPEG formats with quality control
   */
  async canvasToBlob(
    canvas: HTMLCanvasElement,
    format: "PNG" | "JPEG",
    quality: number = 1.0
  ): Promise<Blob> {
    if (!canvas) {
      throw new Error("Canvas is required for blob conversion");
    }

    if (!this.getSupportedFormats().includes(format)) {
      throw new Error(`Unsupported format: ${format}`);
    }

    // Validate quality parameter
    if (quality < 0 || quality > 1) {
      throw new Error(`Quality must be between 0 and 1, got: ${quality}`);
    }

    return new Promise((resolve, reject) => {
      const mimeType = format === "PNG" ? "image/png" : "image/jpeg";

      canvas.toBlob(
        (blob) => {
          if (blob) {
            resolve(blob);
          } else {
            reject(new Error(`Failed to convert canvas to ${format} blob`));
          }
        },
        mimeType,
        quality
      );
    });
  }

  /**
   * Download blob as file using the app's file download utility
   * Matches desktop save functionality
   */
  async downloadBlob(blob: Blob, filename: string): Promise<void> {
    if (!blob) {
      throw new Error("Blob is required for download");
    }

    if (!this.validateFilename(filename)) {
      throw new Error(`Invalid filename: ${filename}`);
    }

    try {
      // Use the FileDownloadService for consistency
      const result = await this.fileDownloadService.downloadBlob(blob, filename);
      if (!result.success) {
        throw new Error(result.error?.message || "Download failed");
      }
    } catch (error) {
      throw new Error(
        `Download failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Generate versioned filename
   * Matches desktop filename generation with versioning
   */
  generateVersionedFilename(
    word: string,
    format: string,
    timestamp?: Date
  ): string {
    // Sanitize word for filename use
    const sanitizedWord = this.sanitizeForFilename(word) || "sequence";

    // Use provided timestamp or current time
    const date = timestamp || new Date();
    const dateString = date.toISOString().slice(0, 10).replace(/-/g, ""); // YYYYMMDD

    // Generate version number (in real implementation, this would check for existing files)
    const version = 1;

    // Format extension
    const extension = format.toLowerCase();

    return `${sanitizedWord}_v${version}_${dateString}.${extension}`;
  }

  /**
   * Validate filename
   * Checks for valid characters and reasonable length
   */
  validateFilename(filename: string): boolean {
    if (!filename || typeof filename !== "string") {
      return false;
    }

    // Check length
    if (filename.length === 0 || filename.length > 255) {
      return false;
    }

    // Check for invalid characters (Windows-compatible)
    // eslint-disable-next-line no-control-regex
    const invalidChars = /[<>:"/\\|?*\x00-\x1f]/;
    if (invalidChars.test(filename)) {
      return false;
    }

    // Check for reserved names (Windows)
    const reservedNames = /^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)/i;
    if (reservedNames.test(filename)) {
      return false;
    }

    // Must have an extension
    if (!filename.includes(".")) {
      return false;
    }

    return true;
  }

  /**
   * Get supported export formats
   */
  getSupportedFormats(): string[] {
    return ["PNG", "JPEG"];
  }

  /**
   * Sanitize string for use in filename
   */
  private sanitizeForFilename(input: string): string {
    if (!input) return "";

    return (
      input
        // eslint-disable-next-line no-control-regex
        .replace(/[<>:"/\\|?*\x00-\x1f]/g, "") // Remove invalid characters
        .replace(/\s+/g, "_") // Replace spaces with underscores
        .replace(/_{2,}/g, "_") // Replace multiple underscores with single
        .replace(/^_|_$/g, "") // Remove leading/trailing underscores
        .toLowerCase() // Use lowercase for consistency
        .slice(0, 100)
    ); // Limit length
  }

  /**
   * Get MIME type for format
   */
  getMimeType(format: "PNG" | "JPEG" | "WebP"): string {
    switch (format) {
      case "PNG":
        return "image/png";
      case "JPEG":
        return "image/jpeg";
      case "WebP":
        return "image/webp";
      default:
        throw new Error(`Unknown format: ${format}`);
    }
  }

  /**
   * Estimate file size for canvas export
   */
  estimateFileSize(
    canvas: HTMLCanvasElement,
    format: "PNG" | "JPEG",
    quality: number = 1.0
  ): number {
    const pixels = canvas.width * canvas.height;

    if (format === "PNG") {
      // PNG: roughly 3-4 bytes per pixel for typical pictographs
      return pixels * 3.5;
    } else {
      // JPEG: varies greatly with quality, roughly 0.5-3 bytes per pixel
      const baseSize = pixels * 1.5;
      return baseSize * quality;
    }
  }

  /**
   * Check if file size is reasonable for download
   */
  validateFileSize(estimatedSize: number): {
    valid: boolean;
    sizeMB: number;
    warning?: string;
  } {
    const sizeMB = estimatedSize / (1024 * 1024);

    if (sizeMB > 100) {
      return {
        valid: false,
        sizeMB,
        warning: "File size exceeds 100MB limit",
      };
    }

    if (sizeMB > 10) {
      return {
        valid: true,
        sizeMB,
        warning: "Large file size may take time to download",
      };
    }

    return { valid: true, sizeMB };
  }

  /**
   * Create download with progress tracking (for large files)
   */
  async downloadWithProgress(
    canvas: HTMLCanvasElement,
    filename: string,
    format: "PNG" | "JPEG" = "PNG",
    quality: number = 1.0,
    onProgress?: (progress: number) => void
  ): Promise<void> {
    // Report conversion start
    onProgress?.(0);

    // Convert canvas to blob
    const blob = await this.canvasToBlob(canvas, format, quality);
    onProgress?.(50);

    // Validate file size
    const sizeValidation = this.validateFileSize(blob.size);
    if (!sizeValidation.valid) {
      throw new Error(sizeValidation.warning || "File size validation failed");
    }

    // Download file
    await this.downloadBlob(blob, filename);
    onProgress?.(100);
  }

  /**
   * Export canvas as data URL (for previews)
   */
  canvasToDataURL(
    canvas: HTMLCanvasElement,
    format: "PNG" | "JPEG" | "WebP" = "PNG",
    quality: number = 1.0
  ): string {
    if (!canvas) {
      throw new Error("Canvas is required for data URL conversion");
    }

    const mimeType = this.getMimeType(format);
    return canvas.toDataURL(mimeType, quality);
  }

  /**
   * Batch export multiple canvases
   */
  async batchExport(
    canvases: HTMLCanvasElement[],
    baseFilename: string,
    format: "PNG" | "JPEG" = "PNG",
    quality: number = 1.0,
    onProgress?: (current: number, total: number) => void
  ): Promise<void> {
    if (!canvases || canvases.length === 0) {
      throw new Error("At least one canvas is required for batch export");
    }

    for (let i = 0; i < canvases.length; i++) {
      const canvas = canvases[i];
      const filename =
        canvases.length === 1
          ? `${baseFilename}.${format.toLowerCase()}`
          : `${baseFilename}_${i + 1}.${format.toLowerCase()}`;

      await this.downloadWithProgress(canvas, filename, format, quality);
      onProgress?.(i + 1, canvases.length);
    }
  }

  /**
   * Debug method to test export functionality
   */
  async testExport(): Promise<{ success: boolean; error?: string }> {
    try {
      // Create a simple test canvas
      const canvas = document.createElement("canvas");
      canvas.width = 100;
      canvas.height = 100;

      const ctx = canvas.getContext("2d");
      if (!ctx) {
        return {
          success: false,
          error: "Failed to get 2D context from test canvas",
        };
      }
      ctx.fillStyle = "red";
      ctx.fillRect(10, 10, 80, 80);

      // Test blob conversion
      const blob = await this.canvasToBlob(canvas, "PNG");

      if (blob.size === 0) {
        return { success: false, error: "Generated blob is empty" };
      }

      // Test filename generation
      const filename = this.generateVersionedFilename("test", "PNG");
      if (!this.validateFilename(filename)) {
        return { success: false, error: "Generated filename is invalid" };
      }

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }
}
