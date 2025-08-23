/**
 * Image Format Converter Service
 *
 * Consolidates canvas-to-blob/dataURL conversion logic that was duplicated across:
 * - FileExportService.ts (canvasToBlob, canvasToDataURL methods)
 * - SequenceCardImageConversionService.ts (canvasToBlob method)
 * - PageImageExportService.ts (canvasToBlob method)
 * - Various other services with inline conversion logic
 *
 * Single responsibility: High-quality image format conversion with
 * optimization, compression, and proper error handling.
 */

import type {
  IImageFormatConverterService,
  ImageFormatOptions,
  OptimizationSettings,
} from "../../interfaces/image-format-interfaces";

export class ImageFormatConverterService
  implements IImageFormatConverterService
{
  private conversionStats = {
    totalConversions: 0,
    totalBytesProcessed: 0,
    totalCompressionSaved: 0,
    formatUsage: {} as Record<string, number>,
  };

  private readonly defaultQuality: Record<string, number> = {
    PNG: 1.0, // PNG doesn't use quality but we track it
    JPEG: 0.85, // Good balance of quality/size
    WEBP: 0.8, // WEBP can be more aggressive
  };

  /**
   * Convert Canvas to Blob
   * Consolidated from multiple duplicate implementations
   */
  async canvasToBlob(
    canvas: HTMLCanvasElement,
    options: ImageFormatOptions
  ): Promise<Blob> {
    if (!canvas) {
      throw new Error("Canvas is required for blob conversion");
    }

    if (!this.validateFormatOptions(options)) {
      throw new Error("Invalid format options provided");
    }

    const startTime = performance.now();

    try {
      const mimeType = this.getMimeType(options.format);
      const quality = this.getEffectiveQuality(options);

      const blob = await new Promise<Blob>((resolve, reject) => {
        canvas.toBlob(
          (result) => {
            if (result) {
              resolve(result);
            } else {
              reject(new Error("Canvas to Blob conversion failed"));
            }
          },
          mimeType,
          quality
        );
      });

      // Update statistics
      this.updateConversionStats(canvas, blob, options.format, startTime);

      return blob;
    } catch (error) {
      throw new Error(
        `Canvas to Blob conversion failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Convert Canvas to Data URL
   * For immediate display in UI
   */
  canvasToDataURL(
    canvas: HTMLCanvasElement,
    options: ImageFormatOptions
  ): string {
    if (!canvas) {
      throw new Error("Canvas is required for data URL conversion");
    }

    if (!this.validateFormatOptions(options)) {
      throw new Error("Invalid format options provided");
    }

    try {
      const mimeType = this.getMimeType(options.format);
      const quality = this.getEffectiveQuality(options);

      const dataURL = canvas.toDataURL(mimeType, quality);

      // Update statistics
      const estimatedSize = Math.floor(dataURL.length * 0.75); // Base64 overhead
      this.updateStatsFromSize(estimatedSize, options.format);

      return dataURL;
    } catch (error) {
      throw new Error(
        `Canvas to Data URL conversion failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Batch convert multiple canvases
   * Optimized for sequence export with memory management
   */
  async convertMultipleCanvasesToBlobs(
    canvases: HTMLCanvasElement[],
    options: ImageFormatOptions
  ): Promise<Blob[]> {
    if (!canvases || canvases.length === 0) {
      return [];
    }

    const blobs: Blob[] = [];
    const BATCH_SIZE = 3; // Smaller batches for memory efficiency

    try {
      // Process in batches to manage memory
      for (let i = 0; i < canvases.length; i += BATCH_SIZE) {
        const batch = canvases.slice(i, i + BATCH_SIZE);

        const batchPromises = batch.map((canvas) =>
          this.canvasToBlob(canvas, options)
        );

        const batchBlobs = await Promise.all(batchPromises);
        blobs.push(...batchBlobs);

        // Allow garbage collection between batches
        if (i + BATCH_SIZE < canvases.length) {
          await new Promise((resolve) => setTimeout(resolve, 0));
        }
      }

      return blobs;
    } catch (error) {
      throw new Error(
        `Batch canvas conversion failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Optimize image for specific use case
   * Applies compression, resizing, and format selection
   */
  async optimizeForUseCase(
    blob: Blob,
    optimization: OptimizationSettings
  ): Promise<Blob> {
    if (!blob) {
      throw new Error("Blob is required for optimization");
    }

    try {
      // For now, return original blob
      // In future: implement actual optimization based on use case
      switch (optimization.useCase) {
        case "web":
          // Apply web-optimized compression
          return this.optimizeForWeb(blob, optimization);
        case "print":
          // Preserve quality for print
          return this.optimizeForPrint(blob, optimization);
        case "archive":
          // Balance between quality and size
          return this.optimizeForArchive(blob, optimization);
        default:
          return blob;
      }
    } catch (error) {
      throw new Error(
        `Image optimization failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Get optimal format for content type
   * Analyzes image and recommends best format
   */
  getOptimalFormat(canvas: HTMLCanvasElement): "PNG" | "JPEG" | "WEBP" {
    if (!canvas) {
      return "PNG";
    }

    try {
      // Simple heuristic: if image has transparency, use PNG
      const ctx = canvas.getContext("2d");
      if (!ctx) {
        return "PNG";
      }

      // Check for transparency by sampling pixels
      const imageData = ctx.getImageData(
        0,
        0,
        Math.min(canvas.width, 100),
        Math.min(canvas.height, 100)
      );

      let hasTransparency = false;
      for (let i = 3; i < imageData.data.length; i += 4) {
        if (imageData.data[i] < 255) {
          hasTransparency = true;
          break;
        }
      }

      // If browser supports WEBP and no transparency, prefer WEBP
      if (!hasTransparency && this.supportsWebP()) {
        return "WEBP";
      }

      // If no transparency and larger image, prefer JPEG
      if (!hasTransparency && canvas.width * canvas.height > 250000) {
        return "JPEG";
      }

      // Default to PNG for transparency or smaller images
      return "PNG";
    } catch {
      // Fallback to PNG on any error
      return "PNG";
    }
  }

  /**
   * Validate format and quality settings
   */
  validateFormatOptions(options: ImageFormatOptions): boolean {
    if (!options) {
      return false;
    }

    const validFormats = ["PNG", "JPEG", "WEBP"];
    if (!validFormats.includes(options.format)) {
      return false;
    }

    if (
      typeof options.quality !== "number" ||
      options.quality < 0 ||
      options.quality > 1
    ) {
      return false;
    }

    return true;
  }

  /**
   * Get supported formats for current browser
   */
  getSupportedFormats(): string[] {
    const formats = ["PNG", "JPEG"];

    if (this.supportsWebP()) {
      formats.push("WEBP");
    }

    return formats;
  }

  /**
   * Estimate file size before conversion
   */
  estimateFileSize(
    canvas: HTMLCanvasElement,
    options: ImageFormatOptions
  ): number {
    if (!canvas) {
      return 0;
    }

    const pixels = canvas.width * canvas.height;

    switch (options.format) {
      case "PNG": {
        // PNG: roughly 4 bytes per pixel (uncompressed) / 3 (typical compression)
        return Math.floor((pixels * 4) / 3);
      }
      case "JPEG": {
        // JPEG: varies greatly by quality
        const jpegBase = pixels * 0.5; // Base estimate
        return Math.floor(jpegBase * options.quality);
      }
      case "WEBP": {
        // WEBP: typically 25-30% smaller than JPEG
        const webpBase = pixels * 0.35;
        return Math.floor(webpBase * options.quality);
      }
      default:
        return pixels * 4; // Fallback
    }
  }

  /**
   * Get conversion statistics
   */
  getConversionStats(): {
    totalConversions: number;
    totalBytesProcessed: number;
    averageCompressionRatio: number;
    formatUsage: Record<string, number>;
  } {
    const averageCompressionRatio =
      this.conversionStats.totalBytesProcessed > 0
        ? this.conversionStats.totalCompressionSaved /
          this.conversionStats.totalBytesProcessed
        : 0;

    return {
      totalConversions: this.conversionStats.totalConversions,
      totalBytesProcessed: this.conversionStats.totalBytesProcessed,
      averageCompressionRatio,
      formatUsage: { ...this.conversionStats.formatUsage },
    };
  }

  /**
   * Cleanup resources
   */
  cleanup(): void {
    this.conversionStats = {
      totalConversions: 0,
      totalBytesProcessed: 0,
      totalCompressionSaved: 0,
      formatUsage: {},
    };
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  /**
   * Get MIME type for format
   */
  private getMimeType(format: string): string {
    switch (format) {
      case "PNG":
        return "image/png";
      case "JPEG":
        return "image/jpeg";
      case "WEBP":
        return "image/webp";
      default:
        return "image/png";
    }
  }

  /**
   * Get effective quality (handle PNG special case)
   */
  private getEffectiveQuality(options: ImageFormatOptions): number {
    if (options.format === "PNG") {
      return 1.0; // PNG doesn't use quality
    }
    return options.quality;
  }

  /**
   * Check if browser supports WebP
   */
  private supportsWebP(): boolean {
    try {
      const canvas = document.createElement("canvas");
      canvas.width = 1;
      canvas.height = 1;
      return canvas.toDataURL("image/webp").indexOf("data:image/webp") === 0;
    } catch {
      return false;
    }
  }

  /**
   * Update conversion statistics
   */
  private updateConversionStats(
    canvas: HTMLCanvasElement,
    blob: Blob,
    format: string,
    _startTime: number
  ): void {
    this.conversionStats.totalConversions++;
    this.conversionStats.totalBytesProcessed += blob.size;

    // Track format usage
    this.conversionStats.formatUsage[format] =
      (this.conversionStats.formatUsage[format] || 0) + 1;

    // Estimate compression savings (rough calculation)
    const uncompressedSize = canvas.width * canvas.height * 4;
    const compressionSaved = Math.max(0, uncompressedSize - blob.size);
    this.conversionStats.totalCompressionSaved += compressionSaved;
  }

  /**
   * Update stats from estimated size (for DataURL)
   */
  private updateStatsFromSize(estimatedSize: number, format: string): void {
    this.conversionStats.totalConversions++;
    this.conversionStats.totalBytesProcessed += estimatedSize;

    this.conversionStats.formatUsage[format] =
      (this.conversionStats.formatUsage[format] || 0) + 1;
  }

  /**
   * Optimize for web use case
   */
  private async optimizeForWeb(
    blob: Blob,
    _optimization: OptimizationSettings
  ): Promise<Blob> {
    // For now, return original - future enhancement
    return blob;
  }

  /**
   * Optimize for print use case
   */
  private async optimizeForPrint(
    blob: Blob,
    _optimization: OptimizationSettings
  ): Promise<Blob> {
    // For now, return original - future enhancement
    return blob;
  }

  /**
   * Optimize for archive use case
   */
  private async optimizeForArchive(
    blob: Blob,
    _optimization: OptimizationSettings
  ): Promise<Blob> {
    // For now, return original - future enhancement
    return blob;
  }
}
