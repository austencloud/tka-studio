/**
 * Image Format Converter Service - SIMPLIFIED
 *
 * Uses native browser APIs + file-saver for clean, simple image conversion.
 * Replaces 400+ lines of over-engineered conversion logic with ~30 lines.
 */

import * as pkg from "file-saver";
import { injectable } from "inversify";
import type { IImageFormatConverterService } from "../contracts";
// Define missing types locally for now
interface ImageFormatOptions {
  format: "png" | "jpeg" | "webp";
  quality?: number;
  compression?: number;
}

interface OptimizationSettings {
  enableCompression: boolean;
  quality: number;
  progressive?: boolean;
}
const { saveAs } = pkg;

@injectable()
export class ImageFormatConverterService
  implements IImageFormatConverterService
{
  /**
   * Convert Canvas to Blob using native browser API
   */
  async canvasToBlob(
    canvas: HTMLCanvasElement,
    options: ImageFormatOptions
  ): Promise<Blob> {
    if (!canvas) throw new Error("Canvas is required");

    return new Promise((resolve, reject) => {
      canvas.toBlob(
        (blob) =>
          blob ? resolve(blob) : reject(new Error("Conversion failed")),
        this.getMimeType(options.format),
        options.quality
      );
    });
  }

  /**
   * Convert Canvas to Data URL using native browser API
   */
  canvasToDataURL(
    canvas: HTMLCanvasElement,
    options: ImageFormatOptions
  ): string {
    if (!canvas) throw new Error("Canvas is required");
    return canvas.toDataURL(this.getMimeType(options.format), options.quality);
  }

  /**
   * Batch convert multiple canvases
   */
  async convertMultipleCanvasesToBlobs(
    canvases: HTMLCanvasElement[],
    options: ImageFormatOptions
  ): Promise<Blob[]> {
    return Promise.all(
      canvases.map((canvas) => this.canvasToBlob(canvas, options))
    );
  }

  /**
   * Download blob as file using file-saver
   */
  downloadBlob(blob: Blob, filename: string): void {
    saveAs(blob, filename);
  }

  // Simple implementations for interface compatibility
  async optimizeForUseCase(
    blob: Blob,
    _optimization: OptimizationSettings
  ): Promise<Blob> {
    return blob; // No optimization needed for dance notation
  }

  getOptimalFormat(_canvas: HTMLCanvasElement): "PNG" | "JPEG" | "WEBP" {
    return "PNG"; // PNG is fine for dance diagrams
  }

  validateFormatOptions(options: ImageFormatOptions): boolean {
    return options && ["PNG", "JPEG", "WEBP"].includes(options.format);
  }

  getSupportedFormats(): string[] {
    return ["PNG", "JPEG", "WEBP"];
  }

  estimateFileSize(
    _canvas: HTMLCanvasElement,
    _options: ImageFormatOptions
  ): number {
    return 100000; // Rough estimate - not critical for this app
  }

  getConversionStats() {
    return {
      totalConversions: 0,
      totalBytesProcessed: 0,
      averageCompressionRatio: 0,
      formatUsage: {},
    };
  }

  cleanup(): void {
    // No cleanup needed
  }

  private getMimeType(format: string): string {
    const mimeTypes: Record<string, string> = {
      PNG: "image/png",
      JPEG: "image/jpeg",
      WEBP: "image/webp",
    };
    return mimeTypes[format] || "image/png";
  }
}
