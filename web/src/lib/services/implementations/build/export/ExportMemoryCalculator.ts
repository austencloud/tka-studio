/**
 * Export Memory Calculator
 *
 * Handles memory estimation calculations for TKA image exports.
 * Extracted from the monolithic TKAImageExportService to focus solely on memory calculations.
 */

import type { IExportMemoryCalculator } from "$contracts";
import type {
  ImageExportOptions,
  MemoryEstimate,
  SequenceData,
} from "$domain";
import { injectable } from "inversify";

@injectable()
export class ExportMemoryCalculator implements IExportMemoryCalculator {
  private readonly DEFAULT_MEMORY_LIMIT_MB = 200;

  /**
   * Estimate memory usage for export
   */
  estimateMemoryUsage(
    sequence: SequenceData,
    options: ImageExportOptions
  ): MemoryEstimate {
    const beatCount = sequence.beats.length;
    const beatSize = options.beatSize * options.beatScale;

    // Estimate layout dimensions
    const columns = Math.ceil(
      Math.sqrt(beatCount + (options.includeStartPosition ? 1 : 0))
    );
    const rows = Math.ceil(
      (beatCount + (options.includeStartPosition ? 1 : 0)) / columns
    );

    const width = Math.round(columns * beatSize + options.margin * 2);
    const height = Math.round(rows * beatSize + options.margin * 2);

    // Add text overlay space
    const textHeightEstimate =
      options.addUserInfo || options.addWord ? 100 * options.beatScale : 0;
    const finalHeight = height + textHeightEstimate;

    const pixelCount = width * finalHeight;

    // Estimate color depth and compression
    const colorDepth = 4; // RGBA = 4 bytes per pixel
    const compressionFactor = options.format === "PNG" ? 0.6 : 0.3; // PNG ~60%, JPEG ~30%

    const estimatedBytes = pixelCount * colorDepth * compressionFactor;
    const estimatedMB = estimatedBytes / (1024 * 1024);

    return {
      estimatedMB,
      safe: estimatedMB < 100, // Consider safe if under 100MB
    };
  }

  /**
   * Check if export would exceed memory limits
   */
  isWithinMemoryLimits(
    sequence: SequenceData,
    options: ImageExportOptions,
    limitMB: number = this.DEFAULT_MEMORY_LIMIT_MB
  ): boolean {
    const estimate = this.estimateMemoryUsage(sequence, options);
    return estimate.estimatedMB <= limitMB;
  }
}
