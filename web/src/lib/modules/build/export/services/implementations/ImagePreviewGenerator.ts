/**
 * Image Preview Generator
 *
 * Handles preview image generation for TKA image exports.
 * Extracted from the monolithic TKAImageExportService to focus solely on preview generation.
 */

import { inject, injectable } from "inversify";
import type { SequenceData } from "../../../../../shared/domain";
import { TYPES } from "../../../../../shared/inversify";
import type { SequenceExportOptions } from "../../domain/models";
import type { IImageCompositionService, IImagePreviewGenerator } from "../contracts";
import type { IFileExportService } from "../contracts/image-export-file-interfaces";
import type { IExportConfig } from "../contracts/image-export-interfaces";



@injectable()
export class ImagePreviewGenerator implements IImagePreviewGenerator {
  constructor(
    @inject(TYPES.IImageCompositionService)
    private compositionService: IImageCompositionService,
    @inject(TYPES.IFileExportService) private fileService: IFileExportService,
    @inject(TYPES.IExportConfigManager)
    private configManager: IExportConfig
  ) {}

  /**
   * Generate a preview image (smaller scale for UI)
   * Returns data URL for immediate display
   */
  async generatePreview(
    sequence: SequenceData,
    options: Partial<SequenceExportOptions> = {}
  ): Promise<string> {
    if (!sequence) {
      throw new Error("Sequence data is required for preview");
    }

    try {
      // Create preview options with smaller scale
      const previewOptions = this.configManager.createPreviewOptions(options);

      // Compose preview image
      const canvas = await this.compositionService.composeSequenceImage(
        sequence,
        previewOptions
      );

      // Convert to data URL for immediate display
      return this.fileService.canvasToDataURL(
        canvas,
        previewOptions.format,
        previewOptions.quality
      );
    } catch (error) {
      throw new Error(
        `Preview generation failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Generate a thumbnail image (very small scale for lists/grids)
   * Returns data URL optimized for small display
   */
  async generateThumbnail(
    sequence: SequenceData,
    maxSize: number = 128
  ): Promise<string> {
    if (!sequence) {
      throw new Error("Sequence data is required for thumbnail");
    }

    try {
      // Create thumbnail options with very small scale
      const baseOptions = this.configManager.getDefaultOptions();
      const thumbnailOptions: SequenceExportOptions = {
        ...baseOptions,
        beatScale: 0.25, // Very small scale for thumbnail
        quality: 0.6, // Lower quality for faster generation
        margin: 10, // Smaller margin
        // Disable all text overlays for clean thumbnail
        addBeatNumbers: false,
        addReversalSymbols: false,
        addUserInfo: false,
        addWord: false,
        addDifficultyLevel: false,
        format: "PNG", // PNG for better small-scale quality
      };

      // Compose thumbnail image
      const canvas = await this.compositionService.composeSequenceImage(
        sequence,
        thumbnailOptions
      );

      // Scale canvas to fit within maxSize while maintaining aspect ratio
      const scaledCanvas = this.scaleCanvasToFit(canvas, maxSize);

      // Convert to data URL
      return this.fileService.canvasToDataURL(scaledCanvas, "PNG", 0.8);
    } catch (error) {
      throw new Error(
        `Thumbnail generation failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Scale canvas to fit within maximum size while maintaining aspect ratio
   */
  private scaleCanvasToFit(
    sourceCanvas: HTMLCanvasElement,
    maxSize: number
  ): HTMLCanvasElement {
    const { width, height } = sourceCanvas;

    // Calculate scale to fit within maxSize
    const scale = Math.min(maxSize / width, maxSize / height);

    if (scale >= 1) {
      return sourceCanvas; // No scaling needed
    }

    // Create new canvas with scaled dimensions
    const scaledCanvas = document.createElement("canvas");
    const ctx = scaledCanvas.getContext("2d");

    if (!ctx) {
      throw new Error("Failed to get 2D context for scaled canvas");
    }

    scaledCanvas.width = Math.round(width * scale);
    scaledCanvas.height = Math.round(height * scale);

    // Draw scaled image
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(sourceCanvas, 0, 0, scaledCanvas.width, scaledCanvas.height);

    return scaledCanvas;
  }
}
