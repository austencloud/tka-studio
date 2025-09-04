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
    SequenceData,
    ValidationResult,
} from "$shared/domain";
import type { MemoryEstimate, SequenceExportOptions } from "../../domain";

// Export validation result for image export operations
export interface ExportValidationResult extends ValidationResult {
  memoryEstimate?: MemoryEstimate;
  recommendedOptions?: Partial<SequenceExportOptions>;
}

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IExportSettingsService {
  /**
   * Get current export settings
   */
  getCurrentSettings(): SequenceExportOptions;

  /**
   * Update export settings
   */
  updateSettings(settings: Partial<SequenceExportOptions>): Promise<void>;

  /**
   * Reset to default settings
   */
  resetToDefaults(): Promise<void>;

  /**
   * Save settings preset
   */
  savePreset(name: string, settings: SequenceExportOptions): Promise<void>;

  /**
   * Load settings preset
   */
  loadPreset(name: string): Promise<SequenceExportOptions | null>;

  /**
   * Get available presets
   */
  getPresets(): Promise<string[]>;

  /**
   * Validate settings
   */
  validateSettings(settings: SequenceExportOptions): boolean;
}

export interface IExportConfigManager {
  getDefaultOptions(): SequenceExportOptions;
  mergeWithDefaults(options: Partial<SequenceExportOptions>): SequenceExportOptions;
  createPreviewOptions(
    options: Partial<SequenceExportOptions>
  ): SequenceExportOptions;
}

export interface IExportMemoryCalculator {
  estimateMemoryUsage(
    sequence: SequenceData,
    options: SequenceExportOptions
  ): MemoryEstimate;
  isWithinMemoryLimits(
    sequence: SequenceData,
    options: SequenceExportOptions,
    limitMB?: number
  ): boolean;
}

export interface IExportOptionsValidator {
  validateExport(
    sequence: SequenceData,
    options: SequenceExportOptions
  ): ExportValidationResult;
  validateOptions(options: SequenceExportOptions): ExportValidationResult;
  validateSequence(sequence: SequenceData): ExportValidationResult;
}

export interface IFilenameGeneratorService {
  generateDefaultFilename(
    sequence: SequenceData,
    options: Partial<SequenceExportOptions>
  ): string;
  generateVersionedFilename(word: string, format: string): string;
  sanitizeFilename(filename: string): string;
}

export interface IImagePreviewGenerator {
  generatePreview(
    sequence: SequenceData,
    options?: Partial<SequenceExportOptions>
  ): Promise<string>;
  generateThumbnail(sequence: SequenceData, maxSize?: number): Promise<string>;
}
