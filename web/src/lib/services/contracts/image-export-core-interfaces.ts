/**
 * TKA Image Export Core Interfaces
 *
 * Core service contracts and types for the TKA image export system.
 * Contains the main orchestrator service and fundamental configuration types.
 */
// ============================================================================
// EXPORT OPTIONS AND CONFIGURATION
// ============================================================================
import type { SequenceData } from "$domain";
import type { TKAImageExportOptions } from "$domain/data-interfaces/image-export-core-interfaces-data";

// Re-export the imported types so other services can use them
export type {
  BeatRenderOptions,
  CompositionOptions,
  ExportError,
  ExportProgress,
  ExportResult,
  LayoutConstraints,
  LayoutData,
  RenderQualitySettings,
  TextRenderOptions,
  TKAImageExportOptions,
  UserInfo,
} from "$domain/data-interfaces/image-export-core-interfaces-data";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface ITKAImageExportService {
  /**
   * Export a complete sequence as an image blob
   */
  exportSequenceImage(
    sequence: SequenceData,
    options?: Partial<TKAImageExportOptions>
  ): Promise<Blob>;

  /**
   * Generate a preview image (smaller scale for UI)
   */
  generatePreview(
    sequence: SequenceData,
    options?: Partial<TKAImageExportOptions>
  ): Promise<string>; // Returns data URL

  /**
   * Export and download image file directly
   */
  exportAndDownload(
    sequence: SequenceData,
    filename?: string,
    options?: Partial<TKAImageExportOptions>
  ): Promise<void>;

  /**
   * Export multiple sequences as a batch
   */
  batchExport(
    sequences: SequenceData[],
    options?: Partial<TKAImageExportOptions>,
    progressCallback?: (current: number, total: number) => void
  ): Promise<void>;

  /**
   * Validate sequence and options before export
   */
  validateExport(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): { valid: boolean; errors: string[] };

  /**
   * Get default export options
   */
  getDefaultOptions(): TKAImageExportOptions;
}

// Note: Import types directly from $domain/data-interfaces/image-export-core-interfaces-data
// instead of re-exporting them from service contracts
