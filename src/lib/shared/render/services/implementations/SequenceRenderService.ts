/**
 * Main Sequence Render Service
 *
 * Pure image generation service - orchestrates all rendering operations.
 * No download/sharing logic - only creates images from sequence data.
 */

import type { SequenceData } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { SequenceExportOptions } from "../../domain/models";
import type { IDimensionCalculationService, IImageCompositionService, IImageFormatConverterService, ILayoutCalculationService } from "../contracts";
import {  } from "../contracts";
import {} from "../contracts";
import type { ISequenceRenderService } from "../contracts/ISequenceRenderService";
import { LayoutCalculationService } from "./LayoutCalculationService";

@injectable()
export class SequenceRenderService implements ISequenceRenderService {
  constructor(
    @inject(TYPES.IImageCompositionService)
    private compositionService: IImageCompositionService,
    @inject(TYPES.IImageFormatConverterService)
    private formatService: IImageFormatConverterService,
    @inject(TYPES.ILayoutCalculationService)
    private layoutService: ILayoutCalculationService,
    @inject(TYPES.IDimensionCalculationService)
    private dimensionService: IDimensionCalculationService
  ) {}

  /**
   * Render a complete sequence as a canvas
   * Pure rendering - returns canvas for further processing
   */
  async renderSequenceToCanvas(
    sequence: SequenceData,
    options: Partial<SequenceExportOptions> = {}
  ): Promise<HTMLCanvasElement> {
    if (!sequence) {
      throw new Error("Sequence data is required for rendering");
    }

    try {
      // Get full options with defaults
      const fullOptions = this.mergeWithDefaults(options);

      // Validate before rendering
      const validation = this.validateRender(sequence, fullOptions);
      if (!validation.valid) {
        throw new Error(
          `Render validation failed: ${validation.errors.join(", ")}`
        );
      }

      // Render the sequence using composition service
      const canvas = await this.compositionService.composeSequenceImage(
        sequence,
        fullOptions
      );

      return canvas;
    } catch (error) {
      throw new Error(
        `Sequence rendering failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Render a sequence as an image blob
   * For use by sharing/export modules
   */
  async renderSequenceToBlob(
    sequence: SequenceData,
    options: Partial<SequenceExportOptions> = {}
  ): Promise<Blob> {
    if (!sequence) {
      throw new Error("Sequence data is required for rendering");
    }

    try {
      // Get full options with defaults
      const fullOptions = this.mergeWithDefaults(options);

      // Render to canvas first
      const canvas = await this.renderSequenceToCanvas(sequence, fullOptions);

      // Convert to blob using format service
      const blob = await this.formatService.canvasToBlob(canvas, {
        format: fullOptions.format.toLowerCase() as "png" | "jpeg" | "webp",
        quality: fullOptions.quality,
        ...(fullOptions.width !== undefined
          ? { width: fullOptions.width }
          : {}),
        ...(fullOptions.height !== undefined
          ? { height: fullOptions.height }
          : {}),
      });

      return blob;
    } catch (error) {
      throw new Error(
        `Blob rendering failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Generate a preview image (smaller scale for UI)
   * Returns data URL for immediate display in components
   */
  async generatePreview(
    sequence: SequenceData,
    options: Partial<SequenceExportOptions> = {}
  ): Promise<string> {
    if (!sequence) {
      throw new Error("Sequence data is required for preview generation");
    }

    try {
      // Create preview options (smaller scale for faster rendering)
      const previewOptions = this.mergeWithDefaults({
        ...options,
        beatScale: 0.5, // Smaller scale for preview instead of fixed dimensions
        quality: 0.8,
      });

      // Render to canvas
      const canvas = await this.renderSequenceToCanvas(
        sequence,
        previewOptions
      );

      // Convert to data URL for immediate display
      return this.formatService.canvasToDataURL(canvas, {
        format: previewOptions.format.toLowerCase() as "png" | "jpeg" | "webp",
        quality: previewOptions.quality,
        ...(previewOptions.width !== undefined
          ? { width: previewOptions.width }
          : {}),
        ...(previewOptions.height !== undefined
          ? { height: previewOptions.height }
          : {}),
      });
    } catch (error) {
      throw new Error(
        `Preview generation failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Validate sequence and options before rendering
   * Returns validation result with specific error messages
   */
  validateRender(
    sequence: SequenceData,
    options: SequenceExportOptions
  ): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    // Validate sequence
    if (!sequence) {
      errors.push("Sequence data is required");
    } else {
      if (!sequence.beats || sequence.beats.length === 0) {
        errors.push("Sequence must contain at least one beat");
      }
      // Word validation disabled - not required for grid-only exports
      // Sequences can be exported without words for minimal visualization
    }

    // Validate options
    if (options.width && options.width <= 0) {
      errors.push("Width must be positive");
    }
    if (options.height && options.height <= 0) {
      errors.push("Height must be positive");
    }
    if (options.quality && (options.quality < 0 || options.quality > 1)) {
      errors.push("Quality must be between 0 and 1");
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Get default render options
   * Returns desktop-compatible default settings
   */
  getDefaultOptions(): SequenceExportOptions {
    return {
      // Core export settings
      includeStartPosition: true,
      addBeatNumbers: true,
      addReversalSymbols: true,
      addUserInfo: true,
      addWord: true,
      combinedGrids: false,
      addDifficultyLevel: true,

      // Scaling and sizing
      beatScale: 1.0,
      beatSize: LayoutCalculationService.getBaseBeatSize(), // Use desktop-compatible BASE_BEAT_SIZE (144px)
      margin: 0, // No margin - beats are directly adjacent like BeatGrid

      // Visibility settings
      redVisible: true,
      blueVisible: true,

      // User information
      userName: "",
      exportDate: new Date().toISOString(),
      notes: "",

      // Output format
      format: "PNG",
      quality: 1.0,
      scale: 1.0,
      // width and height are calculated dynamically based on content
      backgroundColor: "#FFFFFF",
    };
  }

  /**
   * Batch render multiple sequences
   * Returns array of canvases for further processing
   */
  async batchRender(
    sequences: SequenceData[],
    options: SequenceExportOptions
  ): Promise<HTMLCanvasElement[]> {
    if (!sequences || sequences.length === 0) {
      throw new Error("At least one sequence is required for batch rendering");
    }

    try {
      const canvases: HTMLCanvasElement[] = [];

      for (const sequence of sequences) {
        const canvas = await this.renderSequenceToCanvas(sequence, options);
        canvases.push(canvas);
      }

      return canvases;
    } catch (error) {
      throw new Error(
        `Batch rendering failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Merge provided options with defaults
   */
  private mergeWithDefaults(
    options: Partial<SequenceExportOptions>
  ): SequenceExportOptions {
    const defaults = this.getDefaultOptions();
    return { ...defaults, ...options };
  }
}
