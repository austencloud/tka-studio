import { injectable } from "inversify";
import type { SequenceExportOptions } from "../../domain/models";
import type { IExportConfig } from "../contracts/image-export-interfaces";

/**
 * Export Config Manager
 *
 * Handles default options, configuration management, and option merging for TKA image exports.
 * Extracted from the monolithic TKAImageExportService to focus solely on configuration concerns.
 */


@injectable()
export class ExportConfig implements IExportConfig {
  /**
   * Get default export options
   * Matches desktop application defaults exactly
   */
  getDefaultOptions(): SequenceExportOptions {
    return {
      // Core export settings (match desktop defaults)
      includeStartPosition: true,
      addBeatNumbers: true,
      addReversalSymbols: true,
      addUserInfo: true,
      addWord: true,
      combinedGrids: false,
      addDifficultyLevel: false,

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
      scale: 1.0, // Default scale
    };
  }

  /**
   * Merge provided options with defaults
   */
  mergeWithDefaults(
    options: Partial<SequenceExportOptions>
  ): SequenceExportOptions {
    const defaults = this.getDefaultOptions();
    return { ...defaults, ...options };
  }

  /**
   * Create preview-optimized options
   */
  createPreviewOptions(
    options: Partial<SequenceExportOptions>
  ): SequenceExportOptions {
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
}
