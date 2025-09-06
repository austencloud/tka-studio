/**
 * Metadata Extraction Service Interface
 *
 * Interface for extracting metadata from sequence files.
 * Essential for Browse tab functionality.
 */

import type { SequenceMetadata } from "$shared/domain";
import type {
    GalleryThumbnailFile,
    MetadataAnalysisResult,
} from "../../domain/models/metadata-models";

export interface IMetadataExtractionService {
  /**
   * Extract metadata from a thumbnail file
   */
  extractMetadata(thumbnail: GalleryThumbnailFile): Promise<SequenceMetadata>;

  /**
   * Extract metadata from multiple files
   */
  extractMetadataFromFiles(
    files: GalleryThumbnailFile[]
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
