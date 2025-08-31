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
import type { SequenceData } from "$domain";
import type {
  ExportValidationResult,
  MemoryEstimate,
} from "$domain/data-interfaces/image-export-utility-interfaces-data";
import type { TKAImageExportOptions } from "./image-export-core-interfaces";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IExportSettingsService {
  /**
   * Get current export settings
   */
  getCurrentSettings(): TKAImageExportOptions;

  /**
   * Update export settings
   */
  updateSettings(settings: Partial<TKAImageExportOptions>): Promise<void>;

  /**
   * Reset to default settings
   */
  resetToDefaults(): Promise<void>;

  /**
   * Save settings preset
   */
  savePreset(name: string, settings: TKAImageExportOptions): Promise<void>;

  /**
   * Load settings preset
   */
  loadPreset(name: string): Promise<TKAImageExportOptions | null>;

  /**
   * Get available presets
   */
  getPresets(): Promise<string[]>;

  /**
   * Validate settings
   */
  validateSettings(settings: TKAImageExportOptions): boolean;
}

export interface IExportConfigurationManager {
  getDefaultOptions(): TKAImageExportOptions;
  mergeWithDefaults(
    options: Partial<TKAImageExportOptions>
  ): TKAImageExportOptions;
  createPreviewOptions(
    options: Partial<TKAImageExportOptions>
  ): TKAImageExportOptions;
}

export interface IExportMemoryCalculator {
  estimateMemoryUsage(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): MemoryEstimate;
  isWithinMemoryLimits(
    sequence: SequenceData,
    options: TKAImageExportOptions,
    limitMB?: number
  ): boolean;
}

export interface IExportOptionsValidator {
  validateExport(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): ExportValidationResult;
  validateOptions(options: TKAImageExportOptions): ExportValidationResult;
  validateSequence(sequence: SequenceData): ExportValidationResult;
}

export interface IFilenameGeneratorService {
  generateDefaultFilename(
    sequence: SequenceData,
    options: Partial<TKAImageExportOptions>
  ): string;
  generateVersionedFilename(word: string, format: string): string;
  sanitizeFilename(filename: string): string;
}

export interface IImagePreviewGenerator {
  generatePreview(
    sequence: SequenceData,
    options?: Partial<TKAImageExportOptions>
  ): Promise<string>;
  generateThumbnail(sequence: SequenceData, maxSize?: number): Promise<string>;
}

// ============================================================================
// RE-EXPORT TYPES FOR EXTERNAL USE
// ============================================================================

// Re-export types that other modules need to import
export type {
  ExportValidationResult,
  MemoryEstimate,
} from "$domain/data-interfaces/image-export-utility-interfaces-data";
