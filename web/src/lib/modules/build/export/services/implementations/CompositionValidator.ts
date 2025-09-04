/**
 * Composition Validator
 *
 * Handles validation, debugging, and utility methods for image composition.
 * Provides memory estimation, parameter validation, and test composition capabilities.
 */

import type {
  IDimensionCalculationService,
  ILayoutCalculationService,
} from "$services";
import type { LayoutData, SequenceData, SequenceExportOptions } from "$shared/domain";
import {
  CompositionUtils,
  type CompositionStats,
  type MemoryEstimate,
  type ValidationResult,
} from "./CompositionTypes";

export class CompositionValidator {
  constructor(
    private layoutService: ILayoutCalculationService,
    private dimensionService: IDimensionCalculationService
  ) {}

  /**
   * Validate composition parameters
   */
  validateCompositionParameters(
    sequence: SequenceData,
    options: SequenceExportOptions
  ): ValidationResult {
    const errors: string[] = [];

    if (!sequence) {
      errors.push("Sequence data is required");
    }

    if (!options) {
      errors.push("Export options are required");
    }

    if (options && options.beatScale <= 0) {
      errors.push("Beat scale must be positive");
    }

    if (options && options.beatSize <= 0) {
      errors.push("Beat size must be positive");
    }

    if (sequence && sequence.beats && sequence.beats.length > 1000) {
      errors.push("Too many beats - maximum 1000 supported");
    }

    // Additional canvas dimension validation
    if (sequence && options) {
      const layoutData = this.calculateLayoutData(sequence, options);
      const canvasValidation = this.validateCanvasDimensions(
        layoutData,
        options
      );
      if (!canvasValidation.valid) {
        errors.push(...canvasValidation.errors);
      }
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Calculate memory usage estimate
   */
  estimateMemoryUsage(
    sequence: SequenceData,
    options: SequenceExportOptions
  ): MemoryEstimate {
    const layoutData = this.calculateLayoutData(sequence, options);
    const totalAdditionalHeight =
      layoutData.additionalHeightTop + layoutData.additionalHeightBottom;

    const [width, height] = this.layoutService.calculateImageDimensions(
      [layoutData.columns, layoutData.rows],
      totalAdditionalHeight,
      options.beatScale
    );

    // Estimate memory for main canvas + beat canvases
    const mainCanvasBytes = width * height * 4; // RGBA
    const beatCanvasBytes =
      sequence.beats.length * layoutData.beatSize * layoutData.beatSize * 4;
    const totalBytes = mainCanvasBytes + beatCanvasBytes;

    const estimatedMB = totalBytes / (1024 * 1024);
    const safe = estimatedMB < 100; // Conservative 100MB limit

    return { estimatedMB, safe };
  }

  /**
   * Get comprehensive composition statistics
   */
  getCompositionStats(
    sequence: SequenceData,
    options: SequenceExportOptions
  ): CompositionStats {
    const layoutData = this.calculateLayoutData(sequence, options);
    const totalAdditionalHeight =
      layoutData.additionalHeightTop + layoutData.additionalHeightBottom;

    const [width, height] = this.layoutService.calculateImageDimensions(
      [layoutData.columns, layoutData.rows],
      totalAdditionalHeight,
      options.beatScale
    );

    const memoryEstimate = this.estimateMemoryUsage(sequence, options);

    return {
      beatCount: sequence.beats ? sequence.beats.length : 0,
      canvasSize: [width, height],
      layoutDimensions: [layoutData.columns, layoutData.rows],
      memoryEstimate,
    };
  }

  /**
   * Create test composition for debugging
   */
  createTestSequence(): SequenceData {
    return {
      id: "test",
      name: "Test Sequence",
      word: "TEST",
      beats: [
        {
          id: "beat1",
          beatNumber: 1,
          duration: 1,
          blueReversal: false,
          redReversal: false,
          isBlank: true,
          pictographData: null,
        },
      ],
      thumbnails: [],
      isFavorite: false,
      isCircular: false,
      tags: [],
      metadata: {},
      level: 3,
    };
  }

  /**
   * Create test export options
   */
  createTestOptions(): SequenceExportOptions {
    return {
      includeStartPosition: true,
      addBeatNumbers: true,
      addReversalSymbols: true,
      addUserInfo: true,
      addWord: true,
      combinedGrids: false,
      beatScale: 1,
      beatSize: 144,
      margin: 50,
      redVisible: true,
      blueVisible: true,
      userName: "Test User",
      exportDate: "1-1-2024",
      notes: "Test composition",
      format: "PNG",
      quality: 1.0,
      scale: 1.0,
      addDifficultyLevel: true,
    };
  }

  /**
   * Helper method to calculate layout data
   */
  private calculateLayoutData(
    sequence: SequenceData,
    options: SequenceExportOptions
  ): LayoutData {
    const beatCount = sequence.beats.length;

    const [columns, rows] = this.layoutService.calculateLayout(
      beatCount,
      options.includeStartPosition
    );

    const [additionalHeightTop, additionalHeightBottom] =
      this.dimensionService.determineAdditionalHeights(
        options,
        beatCount,
        options.beatScale
      );

    return {
      columns,
      rows,
      beatSize: Math.floor(options.beatSize * options.beatScale),
      includeStartPosition: options.includeStartPosition,
      additionalHeightTop,
      additionalHeightBottom,
    };
  }

  /**
   * Validate canvas dimensions
   */
  private validateCanvasDimensions(
    layoutData: LayoutData,
    options: SequenceExportOptions
  ): ValidationResult {
    const totalAdditionalHeight =
      layoutData.additionalHeightTop + layoutData.additionalHeightBottom;

    const [width, height] = this.layoutService.calculateImageDimensions(
      [layoutData.columns, layoutData.rows],
      totalAdditionalHeight,
      options.beatScale
    );

    return CompositionUtils.validateCanvasDimensions(width, height);
  }
}
