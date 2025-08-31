/**
 * Shared types and utilities for image composition components
 */

import type { SequenceData } from "$domain";
import type {
  CompositionOptions,
  LayoutData,
  TKAImageExportOptions,
} from "../../../../contracts/image-export-interfaces";

export interface CompositionContext {
  sequence: SequenceData;
  layoutData: LayoutData;
  options: TKAImageExportOptions;
}

export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

export interface MemoryEstimate {
  estimatedMB: number;
  safe: boolean;
}

export interface CompositionStats {
  beatCount: number;
  canvasSize: [number, number];
  layoutDimensions: [number, number];
  memoryEstimate: MemoryEstimate;
}

/**
 * Shared utility functions for composition
 */
export class CompositionUtils {
  /**
   * Convert options to composition options with layout data
   */
  static toCompositionOptions(
    options: TKAImageExportOptions,
    layoutData: LayoutData
  ): CompositionOptions {
    return {
      ...options,
      layout: [layoutData.columns, layoutData.rows],
      additionalHeightTop: layoutData.additionalHeightTop || 0,
      additionalHeightBottom: layoutData.additionalHeightBottom || 0,
    };
  }

  /**
   * Calculate memory usage estimation
   */
  static estimateCanvasMemory(width: number, height: number): number {
    // 4 bytes per pixel (RGBA)
    return (width * height * 4) / (1024 * 1024); // MB
  }

  /**
   * Validate canvas dimensions
   */
  static validateCanvasDimensions(
    width: number,
    height: number
  ): ValidationResult {
    const errors: string[] = [];

    if (width <= 0 || height <= 0) {
      errors.push("Canvas dimensions must be positive");
    }

    // Browser limits - conservative estimate
    const maxDimension = 32767;
    if (width > maxDimension || height > maxDimension) {
      errors.push(
        `Canvas dimensions exceed browser limits (${maxDimension}px)`
      );
    }

    const memoryMB = CompositionUtils.estimateCanvasMemory(width, height);
    if (memoryMB > 100) {
      // 100MB threshold
      errors.push(
        `Canvas would use ${memoryMB.toFixed(1)}MB memory, which may cause performance issues`
      );
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }
}
