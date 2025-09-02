/**
 * TKA Image Export Service
 *
 * Main orchestrator for TKA sequence image export. This service provides the
 * top-level API for exporting sequences as images, coordinating all the
 * specialized services to create pixel-perfect images matching the desktop
 * application's output.
 *
 * Equivalent to desktop ImageExportManager.
 */

import type {
  IDimensionCalculationService,
  IFileExportService,
  IImageCompositionService,
  ILayoutCalculationService,
  ITKAImageExportService,
} from "$contracts/image-export-interfaces";
import type { SequenceData, TKAImageExportOptions } from "$domain";
import { inject, injectable } from "inversify";
import { TYPES } from "../../inversify/types";

@injectable()
export class TKAImageExportService implements ITKAImageExportService {
  constructor(
    @inject(TYPES.IImageCompositionService)
    private compositionService: IImageCompositionService,
    @inject(TYPES.IFileExportService) private fileService: IFileExportService,
    @inject(TYPES.ILayoutCalculationService)
    private layoutService: ILayoutCalculationService,
    @inject(TYPES.IDimensionCalculationService)
    private dimensionService: IDimensionCalculationService
  ) {}

  /**
   * Export a complete sequence as an image blob
   * Main entry point for image export functionality
   */
  async exportSequenceImage(
    sequence: SequenceData,
    options: Partial<TKAImageExportOptions> = {}
  ): Promise<Blob> {
    if (!sequence) {
      throw new Error("Sequence data is required for export");
    }

    // Merge with defaults to get complete options
    const fullOptions = this.mergeWithDefaults(options);

    // Validate export parameters
    const validation = this.validateExport(sequence, fullOptions);
    if (!validation.valid) {
      throw new Error(
        `Export validation failed: ${validation.errors.join(", ")}`
      );
    }

    try {
      // Compose the image
      const canvas = await this.compositionService.composeSequenceImage(
        sequence,
        fullOptions
      );

      // Convert to blob
      const blob = await this.fileService.canvasToBlob(
        canvas,
        fullOptions.format,
        fullOptions.quality
      );

      return blob;
    } catch (error) {
      throw new Error(
        `Image export failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Generate a preview image (smaller scale for UI)
   * Returns data URL for immediate display
   */
  async generatePreview(
    sequence: SequenceData,
    options: Partial<TKAImageExportOptions> = {}
  ): Promise<string> {
    if (!sequence) {
      throw new Error("Sequence data is required for preview");
    }

    try {
      // Create preview options with smaller scale
      const previewOptions = this.createPreviewOptions(options);

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
   * Export and download image file directly
   * Convenience method that handles the complete export-to-download flow
   */
  async exportAndDownload(
    sequence: SequenceData,
    filename?: string,
    options: Partial<TKAImageExportOptions> = {}
  ): Promise<void> {
    if (!sequence) {
      throw new Error("Sequence data is required for export and download");
    }

    try {
      // Generate the image blob
      const blob = await this.exportSequenceImage(sequence, options);

      // Generate filename if not provided
      const finalFilename =
        filename || this.generateDefaultFilename(sequence, options);

      // Download the file
      await this.fileService.downloadBlob(blob, finalFilename);
    } catch (error) {
      throw new Error(
        `Export and download failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Validate sequence and options before export
   */
  validateExport(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    // Validate sequence
    if (!sequence) {
      errors.push("Sequence data is required");
    } else {
      if (!sequence.beats) {
        errors.push("Sequence must have beats array");
      } else if (sequence.beats.length === 0 && !options.includeStartPosition) {
        errors.push("Empty sequence requires start position to be included");
      } else if (sequence.beats.length > 64) {
        errors.push("Sequence has too many beats (maximum 64)");
      }

      if (
        options.addWord &&
        (!sequence.word || sequence.word.trim().length === 0)
      ) {
        errors.push('Sequence word is required when "add word" is enabled');
      }
    }

    // Validate options
    if (!options) {
      errors.push("Export options are required");
    } else {
      if (options.beatScale <= 0 || options.beatScale > 5) {
        errors.push("Beat scale must be between 0.1 and 5");
      }

      if (options.beatSize <= 0 || options.beatSize > 1000) {
        errors.push("Beat size must be between 1 and 1000 pixels");
      }

      if (options.margin < 0 || options.margin > 200) {
        errors.push("Margin must be between 0 and 200 pixels");
      }

      if (options.quality < 0 || options.quality > 1) {
        errors.push("Quality must be between 0 and 1");
      }

      if (!["PNG", "JPEG"].includes(options.format)) {
        errors.push("Format must be PNG or JPEG");
      }

      if (options.addUserInfo && !options.userName) {
        errors.push('User name is required when "add user info" is enabled');
      }
    }

    // Validate memory requirements
    if (sequence && options) {
      const memoryEstimate = this.estimateMemoryUsage(sequence, options);
      if (memoryEstimate.estimatedMB > 200) {
        errors.push(
          `Image would require ${Math.round(memoryEstimate.estimatedMB)}MB memory (limit: 200MB)`
        );
      }
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Get default export options
   * Matches desktop application defaults exactly
   */
  getDefaultOptions(): TKAImageExportOptions {
    return {
      // Core export settings (match desktop defaults)
      includeStartPosition: true,
      addBeatNumbers: true,
      addReversalSymbols: true,
      addUserInfo: true,
      addWord: true,
      combinedGrids: false,

      // Scaling and sizing
      beatScale: 1.0,
      beatSize: 144, // Match desktop base beat size
      margin: 50, // Match desktop base margin

      // Visibility settings
      redVisible: true,
      blueVisible: true,

      // User information
      userName: "TKA User",
      exportDate: new Date()
        .toLocaleDateString("en-US", {
          year: "numeric",
          month: "numeric",
          day: "numeric",
        })
        .replace(/\//g, "-"),
      notes: "Created using The Kinetic Alphabet",

      // Output format
      format: "PNG",
      quality: 1.0, // Maximum quality

      // Additional features
      addDifficultyLevel: false,
    };
  }

  /**
   * Merge provided options with defaults
   */
  private mergeWithDefaults(
    options: Partial<TKAImageExportOptions>
  ): TKAImageExportOptions {
    const defaults = this.getDefaultOptions();
    return { ...defaults, ...options };
  }

  /**
   * Create preview-optimized options
   */
  private createPreviewOptions(
    options: Partial<TKAImageExportOptions>
  ): TKAImageExportOptions {
    const baseOptions = this.mergeWithDefaults(options);

    return {
      ...baseOptions,
      beatScale: baseOptions.beatScale * 0.5, // Smaller scale for preview
      quality: 0.8, // Lower quality for faster generation
      // Disable expensive features for preview
      addReversalSymbols: false,
      combinedGrids: false,
    };
  }

  /**
   * Generate default filename for export
   */
  private generateDefaultFilename(
    sequence: SequenceData,
    options: Partial<TKAImageExportOptions>
  ): string {
    const word = sequence.word || "sequence";
    const format = options.format || "PNG";

    return this.fileService.generateVersionedFilename(word, format);
  }

  /**
   * Estimate memory usage for export
   */
  private estimateMemoryUsage(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): { estimatedMB: number; safe: boolean } {
    const beatCount = sequence.beats.length;

    // Calculate layout and dimensions
    const [columns, rows] = this.layoutService.calculateLayout(
      beatCount,
      options.includeStartPosition
    );

    const [additionalTop, additionalBottom] =
      this.dimensionService.determineAdditionalHeights(
        options,
        beatCount,
        options.beatScale
      );

    const [width, height] = this.layoutService.calculateImageDimensions(
      [columns, rows],
      additionalTop + additionalBottom,
      options.beatScale
    );

    // Estimate memory usage
    const mainCanvasBytes = width * height * 4; // RGBA
    const beatCanvasBytes =
      beatCount * (options.beatSize * options.beatScale) ** 2 * 4;
    const totalBytes = mainCanvasBytes + beatCanvasBytes * 2; // 2x for processing overhead

    const estimatedMB = totalBytes / (1024 * 1024);
    const safe = estimatedMB < 200; // 200MB conservative limit

    return { estimatedMB, safe };
  }

  /**
   * Get export capabilities and limits
   */
  getExportCapabilities(): {
    maxSequenceLength: number;
    supportedFormats: string[];
    maxImageDimensions: { width: number; height: number };
    maxMemoryMB: number;
    supportedFeatures: string[];
  } {
    return {
      maxSequenceLength: 64,
      supportedFormats: ["PNG", "JPEG"],
      maxImageDimensions: { width: 16384, height: 16384 },
      maxMemoryMB: 200,
      supportedFeatures: [
        "includeStartPosition",
        "addBeatNumbers",
        "addReversalSymbols",
        "addUserInfo",
        "addWord",
        "addDifficultyLevel",
        "combinedGrids",
        "customScaling",
        "visibilityControl",
      ],
    };
  }

  /**
   * Batch export multiple sequences
   */
  async batchExport(
    sequences: SequenceData[],
    options: Partial<TKAImageExportOptions> = {},
    progressCallback?: (current: number, total: number) => void
  ): Promise<void> {
    const results: Array<{
      sequence: SequenceData;
      blob: Blob | null;
      error?: string;
    }> = [];

    for (let i = 0; i < sequences.length; i++) {
      const sequence = sequences[i];

      try {
        const blob = await this.exportSequenceImage(sequence, options);
        results.push({ sequence, blob });
      } catch (error) {
        results.push({
          sequence,
          blob: null,
          error: error instanceof Error ? error.message : "Unknown error",
        });
      }

      progressCallback?.(i + 1, sequences.length);
    }

    // Method returns void - results are handled through downloads
  }

  /**
   * Export with custom canvas size (for special use cases)
   */
  async exportWithCustomSize(
    sequence: SequenceData,
    targetWidth: number,
    targetHeight: number,
    options: Partial<TKAImageExportOptions> = {}
  ): Promise<Blob> {
    // Calculate required scale to fit target dimensions
    const beatCount = sequence.beats.length;
    const [columns, rows] = this.layoutService.calculateLayout(
      beatCount,
      options.includeStartPosition ?? true
    );

    const baseOptions = this.mergeWithDefaults(options);
    const [additionalTop, additionalBottom] =
      this.dimensionService.determineAdditionalHeights(
        baseOptions,
        beatCount,
        1.0 // Use scale 1.0 for calculation
      );

    const [baseWidth, baseHeight] = this.layoutService.calculateImageDimensions(
      [columns, rows],
      additionalTop + additionalBottom,
      1.0 // Use scale 1.0 for calculation
    );

    // Calculate scale to fit target dimensions
    const scaleX = targetWidth / baseWidth;
    const scaleY = targetHeight / baseHeight;
    const scale = Math.min(scaleX, scaleY);

    // Export with calculated scale
    const customOptions = {
      ...baseOptions,
      beatScale: scale,
    };

    return await this.exportSequenceImage(sequence, customOptions);
  }

  /**
   * Debug method to test export pipeline
   */
  async debugExport(): Promise<{
    defaultOptionsTest: boolean;
    validationTest: boolean;
    previewTest: boolean;
    exportTest: boolean;
  }> {
    let defaultOptionsTest = false;
    let validationTest = false;
    let previewTest = false;
    let exportTest = false;

    try {
      // Test default options
      const defaults = this.getDefaultOptions();
      defaultOptionsTest =
        defaults.beatScale === 1.0 && defaults.format === "PNG";

      // Test validation
      const testSequence: SequenceData = {
        id: "test",
        name: "Test",
        word: "TEST",
        beats: [],
        thumbnails: [],
        isFavorite: false,
        isCircular: false,
        tags: [],
        metadata: {},
      };

      const validation = this.validateExport(testSequence, defaults);
      validationTest = validation.valid;

      // Test preview generation
      const preview = await this.generatePreview(testSequence);
      previewTest = preview.startsWith("data:image/");

      // Test export
      const blob = await this.exportSequenceImage(testSequence);
      exportTest = blob.size > 0;
    } catch (error) {
      console.error("Export debug failed:", error);
    }

    return {
      defaultOptionsTest,
      validationTest,
      previewTest,
      exportTest,
    };
  }
}
