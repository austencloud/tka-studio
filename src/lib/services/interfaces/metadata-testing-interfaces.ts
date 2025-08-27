/**
 * Metadata Testing Service Interfaces
 *
 * Interfaces for metadata extraction, analysis, and testing services.
 */

import type {
  ThumbnailFile,
  SequenceMetadata,
  MetadataAnalysisResult,
  BatchAnalysisResult,
  BatchAnalysisConfig,
} from "../../domain/metadata-testing/types";

// ============================================================================
// METADATA EXTRACTION SERVICE
// ============================================================================

/**
 * Metadata Extraction Service Interface
 */
export interface IMetadataExtractionService {
  extractMetadata(thumbnail: ThumbnailFile): Promise<SequenceMetadata>;
  extractMetadataFromFile(file: File): Promise<Record<string, unknown>[]>;
  extractRawMetadata(filePath: string): Promise<Record<string, unknown>[]>;
}

// ============================================================================
// METADATA ANALYSIS SERVICE
// ============================================================================

/**
 * Metadata Analysis Service Interface
 */
export interface IMetadataAnalysisService {
  analyzeMetadata(metadata: SequenceMetadata): MetadataAnalysisResult;
  validateMetadata(metadata: SequenceMetadata): boolean;
  getValidationErrors(metadata: SequenceMetadata): string[];
}

// ============================================================================
// SEQUENCE DISCOVERY SERVICE
// ============================================================================

/**
 * Sequence Discovery Service Interface
 */
export interface ISequenceDiscoveryService {
  discoverSequences(directory: string): Promise<ThumbnailFile[]>;
  filterValidSequences(files: ThumbnailFile[]): Promise<ThumbnailFile[]>;
}

// ============================================================================
// BATCH ANALYSIS SERVICE
// ============================================================================

/**
 * Batch Analysis Service Interface
 */
export interface IBatchAnalysisService {
  analyzeBatch(
    thumbnails: ThumbnailFile[],
    config: BatchAnalysisConfig
  ): Promise<BatchAnalysisResult>;
  exportResults(results: BatchAnalysisResult, format: "json" | "csv"): Promise<void>;
}
