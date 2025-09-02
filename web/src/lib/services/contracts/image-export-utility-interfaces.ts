/**
 * TKA Image Export Utility Interfaces
 *
 * Service contracts for configuration management, memory calculation,
 * validation, and utility functions in the TKA image export system.
 */
// ============================================================================
// UTILITY AND HELPER SERVICES
// ============================================================================
/**
 * Export settings management service
 */
import type {
  ImageExportOptions,
  MemoryEstimate,
  SequenceData,
  ValidationResult,
} from "$domain";

// Export validation result for image export operations
export interface ExportValidationResult extends ValidationResult {
  memoryEstimate?: MemoryEstimate;
  recommendedOptions?: Partial<ImageExportOptions>;
}

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IExportSettingsService {
  /**
   * Get current export settings
   */
  getCurrentSettings(): ImageExportOptions;

  /**
   * Update export settings
   */
  updateSettings(settings: Partial<ImageExportOptions>): Promise<void>;

  /**
   * Reset to default settings
   */
  resetToDefaults(): Promise<void>;

  /**
   * Save settings preset
   */
  savePreset(name: string, settings: ImageExportOptions): Promise<void>;

  /**
   * Load settings preset
   */
  loadPreset(name: string): Promise<ImageExportOptions | null>;

  /**
   * Get available presets
   */
  getPresets(): Promise<string[]>;

  /**
   * Validate settings
   */
  validateSettings(settings: ImageExportOptions): boolean;
}

export interface IExportConfigurationManager {
  getDefaultOptions(): ImageExportOptions;
  mergeWithDefaults(options: Partial<ImageExportOptions>): ImageExportOptions;
  createPreviewOptions(
    options: Partial<ImageExportOptions>
  ): ImageExportOptions;
}

export interface IExportMemoryCalculator {
  estimateMemoryUsage(
    sequence: SequenceData,
    options: ImageExportOptions
  ): MemoryEstimate;
  isWithinMemoryLimits(
    sequence: SequenceData,
    options: ImageExportOptions,
    limitMB?: number
  ): boolean;
}

export interface IExportOptionsValidator {
  validateExport(
    sequence: SequenceData,
    options: ImageExportOptions
  ): ExportValidationResult;
  validateOptions(options: ImageExportOptions): ExportValidationResult;
  validateSequence(sequence: SequenceData): ExportValidationResult;
}

export interface IFilenameGeneratorService {
  generateDefaultFilename(
    sequence: SequenceData,
    options: Partial<ImageExportOptions>
  ): string;
  generateVersionedFilename(word: string, format: string): string;
  sanitizeFilename(filename: string): string;
}

export interface IImagePreviewGenerator {
  generatePreview(
    sequence: SequenceData,
    options?: Partial<ImageExportOptions>
  ): Promise<string>;
  generateThumbnail(sequence: SequenceData, maxSize?: number): Promise<string>;
}
