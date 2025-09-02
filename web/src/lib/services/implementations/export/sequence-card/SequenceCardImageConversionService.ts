/**
 * Sequence Card Image Conversion Service
 *
 * Handles converting SVG strings to high-quality images.
 * Single responsibility: SVG to Canvas/Blob conversion pipeline.
 */

import { injectable } from "inversify";
// Domain types
import type { SequenceCardDimensions } from "$domain";

// Behavioral contracts
import type { ISequenceCardImageConversionService } from "../../../contracts/sequence-card-export-interfaces";

@injectable()
export class SequenceCardImageConversionService
  implements ISequenceCardImageConversionService
{
  private readonly defaultQuality = 0.95;

  /**
   * Convert SVG string to Canvas
   */
  async svgToCanvas(
    svgString: string,
    dimensions: SequenceCardDimensions
  ): Promise<HTMLCanvasElement> {
    try {
      // Create canvas with proper scaling
      const canvas = document.createElement("canvas");
      const scale = dimensions.scale || 1;
      canvas.width = dimensions.width * scale;
      canvas.height = dimensions.height * scale;

      const ctx = canvas.getContext("2d");
      if (!ctx) {
        throw new Error("Could not get canvas 2D context");
      }

      // Create image from SVG
      const image = new Image();
      const svgBlob = new Blob([svgString], { type: "image/svg+xml" });
      const url = URL.createObjectURL(svgBlob);

      return new Promise((resolve, reject) => {
        image.onload = () => {
          try {
            // Draw with high quality settings
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";
            ctx.drawImage(image, 0, 0, canvas.width, canvas.height);

            URL.revokeObjectURL(url);
            resolve(canvas);
          } catch (error) {
            URL.revokeObjectURL(url);
            reject(new Error(`Failed to draw SVG to canvas: ${error}`));
          }
        };

        image.onerror = () => {
          URL.revokeObjectURL(url);
          reject(new Error("Failed to load SVG image"));
        };

        image.src = url;
      });
    } catch (error) {
      throw new Error(`SVG to Canvas conversion failed: ${error}`);
    }
  }

  /**
   * Convert Canvas to Blob
   */
  async canvasToBlob(
    canvas: HTMLCanvasElement,
    format: "PNG" | "JPEG" | "WEBP" = "PNG",
    quality?: number
  ): Promise<Blob> {
    try {
      const mimeType = this.getMimeType(format);
      const finalQuality = quality ?? this.defaultQuality;

      return new Promise((resolve, reject) => {
        canvas.toBlob(
          (blob) => {
            if (blob) {
              resolve(blob);
            } else {
              reject(new Error("Canvas to Blob conversion failed"));
            }
          },
          mimeType,
          finalQuality
        );
      });
    } catch (error) {
      throw new Error(`Canvas to Blob conversion failed: ${error}`);
    }
  }

  /**
   * Convert SVG directly to Blob (optimized pipeline)
   */
  async svgToBlob(
    svgString: string,
    dimensions: SequenceCardDimensions,
    format: "PNG" | "JPEG" | "WEBP" = "PNG",
    quality?: number
  ): Promise<Blob> {
    try {
      const canvas = await this.svgToCanvas(svgString, dimensions);
      return await this.canvasToBlob(canvas, format, quality);
    } catch (error) {
      throw new Error(`SVG to Blob conversion failed: ${error}`);
    }
  }

  /**
   * Optimize image for different use cases
   */
  async optimizeImage(
    blob: Blob,
    useCase: "web" | "print" | "archive"
  ): Promise<Blob> {
    try {
      // For now, return as-is. Future enhancement could include:
      // - Compression optimization based on use case
      // - Format conversion for optimal file size
      // - Metadata stripping for web use

      const optimizationSettings = this.getOptimizationSettings(useCase);

      // If current blob is already optimal, return it
      if (this.isBlobOptimal(blob, optimizationSettings)) {
        return blob;
      }

      // For future implementation: apply optimizations
      // For now, just return the original blob
      return blob;
    } catch (error) {
      console.warn("Image optimization failed, returning original:", error);
      return blob;
    }
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  private getMimeType(format: "PNG" | "JPEG" | "WEBP"): string {
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

  private getOptimizationSettings(useCase: "web" | "print" | "archive") {
    switch (useCase) {
      case "web":
        return {
          quality: 0.85,
          maxSize: 500 * 1024, // 500KB
          preferredFormat: "WEBP" as const,
        };
      case "print":
        return {
          quality: 0.95,
          maxSize: 2 * 1024 * 1024, // 2MB
          preferredFormat: "PNG" as const,
        };
      case "archive":
        return {
          quality: 1.0,
          maxSize: 10 * 1024 * 1024, // 10MB
          preferredFormat: "PNG" as const,
        };
      default:
        return {
          quality: 0.9,
          maxSize: 1024 * 1024, // 1MB
          preferredFormat: "PNG" as const,
        };
    }
  }

  private isBlobOptimal(
    blob: Blob,
    settings: { quality: number; maxSize: number; preferredFormat: string }
  ): boolean {
    // Simple check based on size for now
    return blob.size <= settings.maxSize;
  }
}
