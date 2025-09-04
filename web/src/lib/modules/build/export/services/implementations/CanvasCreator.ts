/**
 * Canvas Creator
 *
 * Handles canvas creation, sizing, and background management for image composition.
 * Provides centralized canvas management functionality.
 */

import type {
  IDimensionCalculationService,
  ILayoutCalculationService,
} from "$services";
import type { LayoutData, SequenceData, SequenceExportOptions } from "$shared/domain";
import { CompositionUtils, type ValidationResult } from "./CompositionTypes";

export class CanvasCreator {
  constructor(
    private layoutService: ILayoutCalculationService,
    private dimensionService: IDimensionCalculationService
  ) {}

  /**
   * Calculate layout data for composition
   */
  calculateLayoutData(
    sequence: SequenceData,
    options: SequenceExportOptions
  ): LayoutData {
    const beatCount = sequence.beats.length;

    // Calculate layout using exact desktop algorithms
    const [columns, rows] = this.layoutService.calculateLayout(
      beatCount,
      options.includeStartPosition
    );

    // Calculate additional heights for text areas
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
   * Create main canvas with calculated dimensions
   */
  createMainCanvas(
    layoutData: LayoutData,
    options: SequenceExportOptions
  ): HTMLCanvasElement {
    const totalAdditionalHeight =
      layoutData.additionalHeightTop + layoutData.additionalHeightBottom;

    const [width, height] = this.layoutService.calculateImageDimensions(
      [layoutData.columns, layoutData.rows],
      totalAdditionalHeight,
      options.beatScale
    );

    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;

    return canvas;
  }

  /**
   * Apply background to canvas
   */
  applyBackground(
    canvas: HTMLCanvasElement,
    backgroundColor?: string
  ): HTMLCanvasElement {
    const ctx = canvas.getContext("2d");
    if (!ctx) {
      throw new Error("Failed to get 2D context for background application");
    }

    this.fillBackground(ctx, canvas.width, canvas.height, backgroundColor);
    return canvas;
  }

  /**
   * Fill canvas background
   */
  private fillBackground(
    ctx: CanvasRenderingContext2D,
    width: number,
    height: number,
    backgroundColor: string = "white"
  ): void {
    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, width, height);
  }

  /**
   * Validate canvas creation parameters
   */
  validateCanvasParameters(
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

  /**
   * Estimate memory usage for canvas creation
   */
  estimateMemoryUsage(
    layoutData: LayoutData,
    options: SequenceExportOptions
  ): { estimatedMB: number; safe: boolean } {
    const totalAdditionalHeight =
      layoutData.additionalHeightTop + layoutData.additionalHeightBottom;

    const [width, height] = this.layoutService.calculateImageDimensions(
      [layoutData.columns, layoutData.rows],
      totalAdditionalHeight,
      options.beatScale
    );

    const estimatedMB = CompositionUtils.estimateCanvasMemory(width, height);
    return {
      estimatedMB,
      safe: estimatedMB <= 50, // 50MB threshold for safety
    };
  }
}
