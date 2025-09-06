/**
 * TKA Image Export Orchestrator
 *
 * Main orchestrator for TKA sequence image export. This service provides the
 * top-level API for exporting sequences as images, coordinating all the
 * specialized services to create pixel-perfect images.
 *
 * Refactored from the monolithic TKAImageExportService to focus solely on orchestration.
 */

import type { SequenceData } from "../../../../../shared/domain";
import type { SequenceExportOptions } from "../../domain/models";
import type { IDimensionCalculationService, IExportOptionsValidator, IFilenameGeneratorService, IImageCompositionService, IImagePreviewGenerator, ILayoutCalculationService, ITKAImageExportService } from "../contracts";
import type { IFileExportService } from "../contracts/image-export-file-interfaces";
import type { IExportConfig } from "../contracts/image-export-interfaces";


export class TKAImageExportOrchestrator implements ITKAImageExportService {
  constructor(
    private compositionService: IImageCompositionService,
    private fileService: IFileExportService,
    private layoutService: ILayoutCalculationService,
    private dimensionService: IDimensionCalculationService,
    private configManager: IExportConfig,
    private validator: IExportOptionsValidator,
    private previewGenerator: IImagePreviewGenerator,
    private filenameGenerator: IFilenameGeneratorService
  ) {}

  /**
   * Export a complete sequence as an image blob
   * Main entry point for image export functionality
   */
  async exportSequenceImage(
    sequence: SequenceData,
    options: Partial<SequenceExportOptions> = {}
  ): Promise<Blob> {
    if (!sequence) {
      throw new Error("Sequence data is required for export");
    }

    // Merge with defaults to get complete options
    const fullOptions = this.configManager.mergeWithDefaults(options);

    // Validate export parameters
    const validation = this.validator.validateExport(sequence, fullOptions);
    if (!validation.isValid) {
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
    options: Partial<SequenceExportOptions> = {}
  ): Promise<string> {
    return this.previewGenerator.generatePreview(sequence, options);
  }

  /**
   * Export and download image file directly
   */
  async exportAndDownload(
    sequence: SequenceData,
    filename?: string,
    options: Partial<SequenceExportOptions> = {}
  ): Promise<void> {
    const blob = await this.exportSequenceImage(sequence, options);
    const finalFilename =
      filename ||
      this.filenameGenerator.generateDefaultFilename(sequence, options);

    // Create download link
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = finalFilename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  /**
   * Export multiple sequences as a batch
   */
  async batchExport(
    sequences: SequenceData[],
    options: Partial<SequenceExportOptions> = {},
    progressCallback?: (current: number, total: number) => void
  ): Promise<void> {
    for (let i = 0; i < sequences.length; i++) {
      const sequence = sequences[i];
      progressCallback?.(i, sequences.length);

      await this.exportAndDownload(sequence, undefined, options);

      // Small delay to prevent overwhelming the browser
      await new Promise((resolve) => setTimeout(resolve, 100));
    }

    progressCallback?.(sequences.length, sequences.length);
  }

  /**
   * Validate sequence and options before export
   */
  validateExport(
    sequence: SequenceData,
    options: SequenceExportOptions
  ): { valid: boolean; errors: string[] } {
    const result = this.validator.validateExport(sequence, options);
    return {
      valid: result.isValid,
      errors: result.errors.map((e: any) => (typeof e === "string" ? e : e.message)),
    };
  }

  /**
   * Export with default filename
   */
  async exportSequenceImageWithFilename(
    sequence: SequenceData,
    options: Partial<SequenceExportOptions> = {}
  ): Promise<{ blob: Blob; filename: string }> {
    const blob = await this.exportSequenceImage(sequence, options);
    const filename = this.filenameGenerator.generateDefaultFilename(
      sequence,
      options
    );

    return { blob, filename };
  }

  /**
   * Export with custom canvas size (for special use cases)
   */
  async exportWithCustomSize(
    sequence: SequenceData,
    targetWidth: number,
    targetHeight: number,
    options: Partial<SequenceExportOptions> = {}
  ): Promise<Blob> {
    // Calculate required scale to fit target dimensions
    const beatCount = sequence.beats.length;
    const [columns, rows] = this.layoutService.calculateLayout(
      beatCount,
      options.includeStartPosition ?? true
    );

    const baseOptions = this.configManager.mergeWithDefaults(options);
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
   * Get default export options
   */
  getDefaultOptions(): SequenceExportOptions {
    return this.configManager.getDefaultOptions();
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

      const validation = this.validator.validateExport(testSequence, defaults);
      validationTest = validation.isValid;

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
