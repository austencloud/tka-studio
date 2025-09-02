/**
 * Metadata Extraction Service Interface
 *
 * Interface for extracting metadata from sequence files.
 * Essential for Browse tab functionality.
 */

import type {
  MetadataAnalysisResult,
  SequenceMetadata,
  ThumbnailFile,
} from "$domain";

export interface IMetadataExtractionService {
  /**
   * Extract metadata from a thumbnail file
   */
  extractMetadata(thumbnail: ThumbnailFile): Promise<SequenceMetadata>;

  /**
   * Extract metadata from multiple files
   */
  extractMetadataFromFiles(
    files: ThumbnailFile[]
  ): Promise<MetadataAnalysisResult[]>;

  /**
   * Validate metadata format
   */
  validateMetadata(metadata: Record<string, unknown>): boolean;

  /**
   * Get supported metadata fields
   */
  getSupportedFields(): string[];
}
