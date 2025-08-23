/**
 * SVG to Canvas Converter Service
 *
 * Consolidates SVG-to-Canvas conversion logic that was duplicated across:
 * - BeatRenderingService.ts (drawSVGToCanvas method)
 * - SequenceCardImageGenerationService.ts (svgToCanvas method)
 * - SequenceCardImageConversionService.ts (svgToCanvas method)
 * - PageImageExportService.ts (canvas conversion logic)
 *
 * Single responsibility: High-quality SVG to Canvas conversion with
 * proper error handling, memory management, and quality settings.
 */

import type {
  ISVGToCanvasConverterService,
  RenderQualitySettings,
  SVGConversionOptions,
} from "../../interfaces/svg-conversion-interfaces";

export class SVGToCanvasConverterService
  implements ISVGToCanvasConverterService
{
  private defaultQuality: RenderQualitySettings = {
    antialiasing: true,
    smoothScaling: true,
    imageSmoothingQuality: "high",
    scale: 1,
  };

  private activeConversions = 0;
  private totalMemoryUsed = 0;
  private peakMemoryUsed = 0;
  private conversionCache = new Map<string, HTMLCanvasElement>();
  private readonly MAX_CACHE_SIZE = 50;

  /**
   * Convert SVG string to Canvas
   * Consolidated from multiple duplicate implementations
   */
  async convertSVGStringToCanvas(
    svgString: string,
    options: SVGConversionOptions
  ): Promise<HTMLCanvasElement> {
    if (!svgString || svgString.trim().length === 0) {
      throw new Error("SVG string cannot be empty");
    }

    if (!this.validateSVG(svgString)) {
      throw new Error("Invalid SVG content provided");
    }

    this.activeConversions++;

    try {
      // Check cache first
      const cacheKey = this.generateCacheKey(svgString, options);
      const cached = this.conversionCache.get(cacheKey);
      if (cached) {
        return this.cloneCanvas(cached);
      }

      // Create canvas with proper dimensions
      const canvas = document.createElement("canvas");
      const quality = options.quality || this.defaultQuality;

      canvas.width = options.width * quality.scale;
      canvas.height = options.height * quality.scale;

      const ctx = canvas.getContext("2d");
      if (!ctx) {
        throw new Error("Could not get 2D context from canvas");
      }

      // Set quality settings
      this.applyQualitySettings(ctx, quality);

      // Clear background
      if (options.backgroundColor) {
        ctx.fillStyle = options.backgroundColor;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
      }

      // Convert SVG to image and draw to canvas
      await this.drawSVGToCanvas(ctx, svgString, canvas.width, canvas.height);

      // Cache result if cache isn't full
      if (this.conversionCache.size < this.MAX_CACHE_SIZE) {
        this.conversionCache.set(cacheKey, this.cloneCanvas(canvas));
      }

      // Update memory tracking
      const memoryUsed = canvas.width * canvas.height * 4; // RGBA bytes
      this.totalMemoryUsed += memoryUsed;
      this.peakMemoryUsed = Math.max(this.peakMemoryUsed, this.totalMemoryUsed);

      return canvas;
    } catch (error) {
      throw new Error(
        `SVG to Canvas conversion failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    } finally {
      this.activeConversions--;
    }
  }

  /**
   * Convert SVG element to Canvas
   * For when you already have an SVGElement instance
   */
  async convertSVGElementToCanvas(
    svgElement: SVGElement,
    options: SVGConversionOptions
  ): Promise<HTMLCanvasElement> {
    if (!svgElement) {
      throw new Error("SVG element is required");
    }

    try {
      // Serialize SVG element to string
      const serializer = new XMLSerializer();
      const svgString = serializer.serializeToString(svgElement);

      // Use string conversion method
      return await this.convertSVGStringToCanvas(svgString, options);
    } catch (error) {
      throw new Error(
        `SVG element to Canvas conversion failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Batch convert multiple SVG strings
   * Optimized for sequence rendering with memory management
   */
  async convertMultipleSVGsToCanvases(
    svgStrings: string[],
    options: SVGConversionOptions
  ): Promise<HTMLCanvasElement[]> {
    if (!svgStrings || svgStrings.length === 0) {
      return [];
    }

    const canvases: HTMLCanvasElement[] = [];
    const BATCH_SIZE = 5; // Process in chunks to manage memory

    try {
      // Process in batches to avoid memory spikes
      for (let i = 0; i < svgStrings.length; i += BATCH_SIZE) {
        const batch = svgStrings.slice(i, i + BATCH_SIZE);

        const batchPromises = batch.map((svg) =>
          this.convertSVGStringToCanvas(svg, options)
        );

        const batchCanvases = await Promise.all(batchPromises);
        canvases.push(...batchCanvases);

        // Allow garbage collection between batches
        if (i + BATCH_SIZE < svgStrings.length) {
          await new Promise((resolve) => setTimeout(resolve, 0));
        }
      }

      return canvases;
    } catch (error) {
      // Cleanup any partial results
      canvases.forEach((canvas) => this.releaseCanvasMemory(canvas));
      throw new Error(
        `Batch SVG conversion failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Set default quality settings for all conversions
   */
  setDefaultQuality(settings: RenderQualitySettings): void {
    this.defaultQuality = { ...settings };
  }

  /**
   * Get current quality settings
   */
  getQualitySettings(): RenderQualitySettings {
    return { ...this.defaultQuality };
  }

  /**
   * Validate SVG content before conversion
   */
  validateSVG(svgContent: string | SVGElement): boolean {
    try {
      if (typeof svgContent === "string") {
        // Basic SVG string validation
        const trimmed = svgContent.trim();
        return (
          trimmed.includes("<svg") &&
          trimmed.includes("</svg>") &&
          !trimmed.includes("<script") // Security check
        );
      } else {
        // SVG element validation
        return svgContent instanceof SVGElement;
      }
    } catch {
      return false;
    }
  }

  /**
   * Get memory usage statistics
   */
  getMemoryUsage(): {
    activeConversions: number;
    totalMemoryUsed: number;
    peakMemoryUsed: number;
  } {
    return {
      activeConversions: this.activeConversions,
      totalMemoryUsed: this.totalMemoryUsed,
      peakMemoryUsed: this.peakMemoryUsed,
    };
  }

  /**
   * Cleanup resources and cancel pending operations
   */
  cleanup(): void {
    this.conversionCache.clear();
    this.totalMemoryUsed = 0;
    this.peakMemoryUsed = 0;
    this.activeConversions = 0;
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  /**
   * Core SVG to Canvas drawing logic
   * Consolidated from multiple duplicate implementations
   */
  private async drawSVGToCanvas(
    ctx: CanvasRenderingContext2D,
    svgString: string,
    width: number,
    height: number
  ): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        // Create image from SVG
        const img = new Image();

        // Create blob URL for the SVG
        const svgBlob = new Blob([svgString], {
          type: "image/svg+xml;charset=utf-8",
        });
        const url = URL.createObjectURL(svgBlob);

        img.onload = () => {
          try {
            // Draw image to canvas
            ctx.drawImage(img, 0, 0, width, height);
            URL.revokeObjectURL(url);
            resolve();
          } catch (error) {
            URL.revokeObjectURL(url);
            reject(new Error(`Failed to draw SVG to canvas: ${error}`));
          }
        };

        img.onerror = () => {
          URL.revokeObjectURL(url);
          reject(new Error("Failed to load SVG as image"));
        };

        img.src = url;
      } catch (error) {
        reject(new Error(`SVG image creation failed: ${error}`));
      }
    });
  }

  /**
   * Apply quality settings to canvas context
   */
  private applyQualitySettings(
    ctx: CanvasRenderingContext2D,
    quality: RenderQualitySettings
  ): void {
    ctx.imageSmoothingEnabled = quality.antialiasing;
    if (quality.antialiasing) {
      ctx.imageSmoothingQuality = quality.imageSmoothingQuality;
    }
  }

  /**
   * Generate cache key for SVG/options combination
   */
  private generateCacheKey(
    svgString: string,
    options: SVGConversionOptions
  ): string {
    // Create a simple hash of the SVG and key options
    const keyData = `${svgString}-${options.width}-${options.height}-${
      options.backgroundColor || ""
    }-${JSON.stringify(options.quality || this.defaultQuality)}`;

    // Simple hash function
    let hash = 0;
    for (let i = 0; i < keyData.length; i++) {
      const char = keyData.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return hash.toString();
  }

  /**
   * Clone a canvas for cache usage
   */
  private cloneCanvas(source: HTMLCanvasElement): HTMLCanvasElement {
    const clone = document.createElement("canvas");
    clone.width = source.width;
    clone.height = source.height;

    const ctx = clone.getContext("2d");
    if (ctx) {
      ctx.drawImage(source, 0, 0);
    }

    return clone;
  }

  /**
   * Release memory tracking for a canvas
   */
  private releaseCanvasMemory(canvas: HTMLCanvasElement): void {
    const memoryUsed = canvas.width * canvas.height * 4;
    this.totalMemoryUsed = Math.max(0, this.totalMemoryUsed - memoryUsed);
  }
}
