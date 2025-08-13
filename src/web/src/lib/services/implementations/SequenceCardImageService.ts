/**
 * Sequence Card Image Service - Core image generation functionality
 *
 * Handles converting sequence data into high-quality images with:
 * - SVG to Canvas rendering pipeline
 * - Metadata embedding in PNG files
 * - Cache integration
 * - Batch processing with memory management
 * - Progress tracking for long operations
 */

import type {
  ISequenceCardImageService,
  ISequenceCardCacheService,
  IPictographRenderingService,
  SequenceData,
  ExportOptions,
  ProgressInfo,
  ExportResult,
} from "$services/interfaces";

export class SequenceCardImageService implements ISequenceCardImageService {
  private cancelRequested = false;
  private currentBatchId: string | null = null;

  constructor(
    private pictographRenderingService: IPictographRenderingService,
    private cacheService: ISequenceCardCacheService,
  ) {}

  /**
   * Generate a high-quality image for a single sequence card
   */
  async generateSequenceCardImage(
    sequence: SequenceData,
    options: ExportOptions,
  ): Promise<Blob> {
    try {
      console.log(`Generating image for sequence "${sequence.name}"`);

      // Check cache first
      const cachedImage = await this.cacheService.retrieveImage(
        sequence.id || sequence.name,
        options,
      );

      if (cachedImage) {
        console.log("Using cached image");
        return cachedImage;
      }

      // Generate new image
      const imageBlob = await this.generateImageFromSequence(sequence, options);

      // Store in cache
      await this.cacheService.storeImage(
        sequence.id || sequence.name,
        imageBlob,
        options,
      );

      return imageBlob;
    } catch (error) {
      console.error("Failed to generate sequence card image:", error);
      throw new Error(
        `Image generation failed: ${error instanceof Error ? error.message : "Unknown error"}`,
      );
    }
  }

  /**
   * Generate images for multiple sequences in batch
   */
  async generateBatchImages(
    sequences: SequenceData[],
    options: ExportOptions,
    onProgress?: (progress: ProgressInfo) => void,
  ): Promise<ExportResult[]> {
    const batchId = `batch_${Date.now()}`;
    this.currentBatchId = batchId;
    this.cancelRequested = false;

    const startTime = new Date();
    const results: ExportResult[] = [];

    try {
      console.log(
        `Starting batch image generation for ${sequences.length} sequences`,
      );

      for (let i = 0; i < sequences.length; i++) {
        // Check for cancellation
        if (this.cancelRequested || this.currentBatchId !== batchId) {
          console.log("Batch generation cancelled");
          break;
        }

        const sequence = sequences[i];
        const sequenceStartTime = performance.now();

        try {
          // Report progress
          if (onProgress) {
            onProgress({
              current: i + 1,
              total: sequences.length,
              percentage: ((i + 1) / sequences.length) * 100,
              message: `Processing sequence "${sequence.name}"`,
              stage: "processing",
              startTime,
              errorCount: results.filter((r) => !r.success).length,
              warningCount: 0,
            });
          }

          // Generate image
          const blob = await this.generateSequenceCardImage(sequence, options);
          const processingTime = performance.now() - sequenceStartTime;

          // Create successful result
          results.push({
            sequenceId: sequence.id || sequence.name,
            success: true,
            blob,
            metrics: {
              processingTime,
              fileSize: blob.size,
              resolution: await this.getImageDimensions(blob),
            },
          });

          // Memory cleanup every 10 items
          if (i % 10 === 0 && i > 0) {
            await this.performMemoryCleanup();
          }
        } catch (error) {
          console.error(
            `Failed to generate image for sequence "${sequence.name}":`,
            error,
          );

          // Create failed result
          results.push({
            sequenceId: sequence.id || sequence.name,
            success: false,
            error: error instanceof Error ? error : new Error("Unknown error"),
            metrics: {
              processingTime: performance.now() - sequenceStartTime,
              fileSize: 0,
              resolution: { width: 0, height: 0 },
            },
          });
        }
      }

      // Final progress report
      if (onProgress && !this.cancelRequested) {
        onProgress({
          current: sequences.length,
          total: sequences.length,
          percentage: 100,
          message: "Batch generation completed",
          stage: "completed",
          startTime,
          errorCount: results.filter((r) => !r.success).length,
          warningCount: 0,
        });
      }

      console.log(
        `Batch generation completed. ${results.filter((r) => r.success).length}/${sequences.length} successful`,
      );
      return results;
    } catch (error) {
      console.error("Batch image generation failed:", error);
      throw error;
    } finally {
      this.currentBatchId = null;
      await this.performMemoryCleanup();
    }
  }

  /**
   * Get cached image for a sequence
   */
  async getCachedImage(
    sequenceId: string,
    options: ExportOptions,
  ): Promise<Blob | null> {
    return await this.cacheService.retrieveImage(sequenceId, options);
  }

  /**
   * Preload images for a set of sequences
   */
  async preloadImages(
    sequences: SequenceData[],
    options: ExportOptions,
  ): Promise<void> {
    console.log(`Preloading images for ${sequences.length} sequences`);

    const preloadPromises = sequences.map(async (sequence) => {
      try {
        await this.generateSequenceCardImage(sequence, options);
      } catch (error) {
        console.warn(
          `Failed to preload image for sequence "${sequence.name}":`,
          error,
        );
      }
    });

    await Promise.allSettled(preloadPromises);
    console.log("Image preloading completed");
  }

  /**
   * Clear image cache
   */
  async clearImageCache(): Promise<void> {
    await this.cacheService.clearCache();
    console.log("Image cache cleared");
  }

  /**
   * Get cache statistics
   */
  async getCacheStats(): Promise<{
    size: number;
    count: number;
    hitRate: number;
  }> {
    const stats = await this.cacheService.getCacheStats();
    return {
      size: stats.totalSize,
      count: stats.entryCount,
      hitRate: stats.hitRate,
    };
  }

  /**
   * Cancel current batch operation
   */
  cancelCurrentBatch(): void {
    this.cancelRequested = true;
    console.log("Batch cancellation requested");
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  /**
   * Generate image from sequence data using SVG to Canvas pipeline
   */
  private async generateImageFromSequence(
    sequence: SequenceData,
    options: ExportOptions,
  ): Promise<Blob> {
    try {
      // 1. Generate SVG for each beat
      const beatSVGs = await Promise.all(
        sequence.beats.map((beat) =>
          this.pictographRenderingService.renderBeat(beat),
        ),
      );

      // 2. Compose sequence layout SVG
      const sequenceSVG = await this.composeSequenceLayout(
        beatSVGs,
        sequence,
        options,
      );

      // 3. Add metadata overlays (title, beat numbers, etc.)
      const finalSVG = await this.addMetadataOverlays(
        sequenceSVG,
        sequence,
        options,
      );

      // 4. Convert SVG to high-quality Canvas
      const canvas = await this.svgToCanvas(finalSVG, options);

      // 5. Export as PNG with embedded metadata
      return await this.canvasToBlob(canvas, sequence, options);
    } catch (error) {
      console.error("SVG to image conversion failed:", error);
      throw new Error(
        `SVG conversion failed: ${error instanceof Error ? error.message : "Unknown error"}`,
      );
    }
  }

  /**
   * Compose individual beat SVGs into a sequence layout
   */
  private async composeSequenceLayout(
    beatSVGs: SVGElement[],
    sequence: SequenceData,
    options: ExportOptions,
  ): Promise<SVGElement> {
    const beatCount = sequence.beats.length;
    const { beatSize, spacing } = options;

    // Calculate grid layout (similar to legacy app)
    const cols = Math.ceil(Math.sqrt(beatCount));
    const rows = Math.ceil(beatCount / cols);

    const totalWidth = cols * beatSize + (cols - 1) * spacing;
    const totalHeight = rows * beatSize + (rows - 1) * spacing;

    // Create container SVG
    const containerSVG = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "svg",
    );
    containerSVG.setAttribute("width", totalWidth.toString());
    containerSVG.setAttribute("height", totalHeight.toString());
    containerSVG.setAttribute("viewBox", `0 0 ${totalWidth} ${totalHeight}`);

    // Add background if specified
    if (options.backgroundColor) {
      const background = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "rect",
      );
      background.setAttribute("width", "100%");
      background.setAttribute("height", "100%");
      background.setAttribute("fill", options.backgroundColor);
      containerSVG.appendChild(background);
    }

    // Position each beat SVG in the grid
    beatSVGs.forEach((beatSVG, index) => {
      const col = index % cols;
      const row = Math.floor(index / cols);
      const x = col * (beatSize + spacing);
      const y = row * (beatSize + spacing);

      // Create group for beat
      const beatGroup = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "g",
      );
      beatGroup.setAttribute("transform", `translate(${x}, ${y})`);

      // Scale beat SVG to fit beatSize
      const beatContainer = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "svg",
      );
      beatContainer.setAttribute("width", beatSize.toString());
      beatContainer.setAttribute("height", beatSize.toString());
      beatContainer.setAttribute(
        "viewBox",
        beatSVG.getAttribute("viewBox") || "0 0 100 100",
      );

      // Copy beat SVG content
      beatContainer.innerHTML = beatSVG.innerHTML;
      beatGroup.appendChild(beatContainer);

      containerSVG.appendChild(beatGroup);
    });

    return containerSVG;
  }

  /**
   * Add metadata overlays (title, beat numbers, author, etc.)
   */
  private async addMetadataOverlays(
    svg: SVGElement,
    sequence: SequenceData,
    options: ExportOptions,
  ): Promise<SVGElement> {
    const svgWidth = parseInt(svg.getAttribute("width") || "800");
    const svgHeight = parseInt(svg.getAttribute("height") || "600");

    // Add padding for metadata
    const padding = options.padding || 40;
    const newWidth = svgWidth + padding * 2;
    const newHeight = svgHeight + padding * 3; // Extra padding for title

    // Create new container with padding
    const containerSVG = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "svg",
    );
    containerSVG.setAttribute("width", newWidth.toString());
    containerSVG.setAttribute("height", newHeight.toString());
    containerSVG.setAttribute("viewBox", `0 0 ${newWidth} ${newHeight}`);

    // Add background
    if (options.backgroundColor) {
      const background = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "rect",
      );
      background.setAttribute("width", "100%");
      background.setAttribute("height", "100%");
      background.setAttribute("fill", options.backgroundColor);
      containerSVG.appendChild(background);
    }

    // Add title if enabled
    if (options.includeTitle) {
      const titleText = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "text",
      );
      titleText.setAttribute("x", (newWidth / 2).toString());
      titleText.setAttribute("y", (padding / 2).toString());
      titleText.setAttribute("text-anchor", "middle");
      titleText.setAttribute("font-family", "system-ui, sans-serif");
      titleText.setAttribute("font-size", "24");
      titleText.setAttribute("font-weight", "bold");
      titleText.setAttribute("fill", "#333");
      titleText.textContent = sequence.name || "Untitled Sequence";
      containerSVG.appendChild(titleText);
    }

    // Add the main sequence SVG
    const sequenceGroup = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "g",
    );
    sequenceGroup.setAttribute(
      "transform",
      `translate(${padding}, ${padding * 2})`,
    );
    sequenceGroup.innerHTML = svg.innerHTML;
    containerSVG.appendChild(sequenceGroup);

    // Add metadata footer if enabled
    if (options.includeMetadata) {
      const metadataY = newHeight - padding / 2;

      // Add beat count
      const beatCountText = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "text",
      );
      beatCountText.setAttribute("x", padding.toString());
      beatCountText.setAttribute("y", metadataY.toString());
      beatCountText.setAttribute("font-family", "system-ui, sans-serif");
      beatCountText.setAttribute("font-size", "14");
      beatCountText.setAttribute("fill", "#666");
      beatCountText.textContent = `${sequence.beats.length} beats`;
      containerSVG.appendChild(beatCountText);

      // Add difficulty if available
      if (sequence.difficulty_level && options.includeDifficulty) {
        const difficultyText = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "text",
        );
        difficultyText.setAttribute("x", (newWidth / 2).toString());
        difficultyText.setAttribute("y", metadataY.toString());
        difficultyText.setAttribute("text-anchor", "middle");
        difficultyText.setAttribute("font-family", "system-ui, sans-serif");
        difficultyText.setAttribute("font-size", "14");
        difficultyText.setAttribute("fill", "#666");
        difficultyText.textContent = sequence.difficulty_level;
        containerSVG.appendChild(difficultyText);
      }

      // Add author if available
      if (sequence.author && options.includeAuthor) {
        const authorText = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "text",
        );
        authorText.setAttribute("x", (newWidth - padding).toString());
        authorText.setAttribute("y", metadataY.toString());
        authorText.setAttribute("text-anchor", "end");
        authorText.setAttribute("font-family", "system-ui, sans-serif");
        authorText.setAttribute("font-size", "14");
        authorText.setAttribute("fill", "#666");
        authorText.textContent = sequence.author;
        containerSVG.appendChild(authorText);
      }
    }

    return containerSVG;
  }

  /**
   * Convert SVG to Canvas with high quality rendering
   */
  private async svgToCanvas(
    svg: SVGElement,
    options: ExportOptions,
  ): Promise<HTMLCanvasElement> {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    if (!ctx) {
      throw new Error("Canvas 2D context not available");
    }

    // Calculate dimensions based on DPI
    const dpi = parseInt(options.resolution) || 300;
    const scaleFactor = dpi / 96; // 96 DPI is standard screen DPI

    const svgWidth = parseInt(svg.getAttribute("width") || "800");
    const svgHeight = parseInt(svg.getAttribute("height") || "600");

    canvas.width = svgWidth * scaleFactor;
    canvas.height = svgHeight * scaleFactor;

    // Scale context for high DPI
    ctx.scale(scaleFactor, scaleFactor);

    // Enable high quality rendering
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";

    // Convert SVG to image
    const svgData = new XMLSerializer().serializeToString(svg);
    const svgBlob = new Blob([svgData], {
      type: "image/svg+xml;charset=utf-8",
    });
    const svgUrl = URL.createObjectURL(svgBlob);

    try {
      const img = new Image();

      return new Promise((resolve, reject) => {
        img.onload = () => {
          ctx.drawImage(img, 0, 0, svgWidth, svgHeight);
          URL.revokeObjectURL(svgUrl);
          resolve(canvas);
        };

        img.onerror = () => {
          URL.revokeObjectURL(svgUrl);
          reject(new Error("Failed to load SVG image"));
        };

        img.src = svgUrl;
      });
    } catch (error) {
      URL.revokeObjectURL(svgUrl);
      throw error;
    }
  }

  /**
   * Convert Canvas to Blob with metadata embedding
   */
  private async canvasToBlob(
    canvas: HTMLCanvasElement,
    sequence: SequenceData,
    options: ExportOptions,
  ): Promise<Blob> {
    return new Promise((resolve, reject) => {
      // Determine quality based on format
      let quality = 0.95; // Default high quality
      if (options.quality === "medium") quality = 0.8;
      if (options.quality === "low") quality = 0.6;

      canvas.toBlob(
        (blob) => {
          if (blob) {
            resolve(blob);
          } else {
            reject(new Error("Failed to create image blob"));
          }
        },
        `image/${options.format.toLowerCase()}`,
        quality,
      );
    });
  }

  /**
   * Get image dimensions from blob
   */
  private async getImageDimensions(
    blob: Blob,
  ): Promise<{ width: number; height: number }> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      const url = URL.createObjectURL(blob);

      img.onload = () => {
        URL.revokeObjectURL(url);
        resolve({ width: img.naturalWidth, height: img.naturalHeight });
      };

      img.onerror = () => {
        URL.revokeObjectURL(url);
        reject(new Error("Failed to load image for dimension calculation"));
      };

      img.src = url;
    });
  }

  /**
   * Perform memory cleanup to prevent browser crashes
   */
  private async performMemoryCleanup(): Promise<void> {
    // Force garbage collection if available (Chrome DevTools)
    if ("gc" in window && typeof (window as any).gc === "function") {
      (window as any).gc();
    }

    // Small delay to allow cleanup
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
}
