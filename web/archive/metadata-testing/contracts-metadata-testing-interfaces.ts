// @ts-nocheck
/**
 * Metadata Testing Service Interfaces
 *
 * Interfaces for metadata extraction, analysis, and testing services.
 * These services handle CSV metadata processing and validation.
 */

import type { 
  ThumbnailFile, 
  SequenceFile, 
  MetadataAnalysisResult, 
  BatchAnalysisResult 
} from "$lib/domain/data-interfaces/metadata-testing-interfaces-data";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IMetadataExtractionService {
  /**
   * Extract metadata from sequence files
   */
  extractMetadata(files: SequenceFile[]): Promise<MetadataAnalysisResult[]>;

  /**
   * Validate metadata format
   */
  validateMetadata(metadata: Record<string, unknown>): boolean;

  /**
   * Get supported metadata fields
   */
  getSupportedFields(): string[];
}

export interface IMetadataAnalysisService {
  /**
   * Analyze extracted metadata
   */
  analyzeMetadata(results: MetadataAnalysisResult[]): Promise<BatchAnalysisResult>;

  /**
   * Generate analysis report
   */
  generateReport(analysis: BatchAnalysisResult): string;

  /**
   * Validate analysis results
   */
  validateAnalysis(analysis: BatchAnalysisResult): boolean;
}

export interface ISequenceDiscoveryService {
  /**
   * Discover available sequences
   */
  discoverSequences(): Promise<ThumbnailFile[]>;

  /**
   * Filter sequences by criteria
   */
  filterSequences(sequences: ThumbnailFile[], criteria: Record<string, unknown>): ThumbnailFile[];

  /**
   * Validate sequence files
   */
  validateSequenceFiles(files: ThumbnailFile[]): boolean;
}

export interface IMetadataTestingStateManager {
  /**
   * Initialize testing state
   */
  initialize(): Promise<void>;

  /**
   * Run metadata tests
   */
  runTests(): Promise<BatchAnalysisResult>;

  /**
   * Get current testing state
   */
  getCurrentState(): Record<string, unknown>;

  /**
   * Reset testing state
   */
  reset(): void;
}

