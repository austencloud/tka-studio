/**
 * Metadata Extraction Service
 *
 * Handles extraction of metadata from PNG files using the PNG metadata extractor.
 * Provides a clean interface for metadata extraction operations.
 */

import { PngMetadataExtractor, type SequenceMetadata } from "$shared";
import type {
  GalleryThumbnailFile,
  MetadataAnalysisResult,
} from "../../domain/models/metadata-models";
import type { IMetadataExtractionService } from "../contracts";

export class MetadataExtractionService implements IMetadataExtractionService {
  async extractMetadataFromFiles(
    _files: GalleryThumbnailFile[]
  ): Promise<MetadataAnalysisResult[]> {
    // Placeholder implementation - extract metadata from multiple files
    return [];
  }

  validateMetadata(_metadata: Record<string, unknown>): boolean {
    // Placeholder implementation - validate metadata structure
    return true;
  }

  getSupportedFields(): string[] {
    // Return supported metadata fields
    return ["word", "beats", "startPosition", "difficulty"];
  }
  async extractMetadata(
    thumbnail: GalleryThumbnailFile
  ): Promise<SequenceMetadata> {
    console.log(
      `🔍 Extracting metadata for: ${thumbnail.metadata?.word || thumbnail.name}`
    );

    try {
      const rawMetadata = await this.extractRawMetadata(thumbnail.path);
      const extractedMetadata = this.processRawMetadata(rawMetadata);

      return {
        word: String(extractedMetadata.word || "Unknown"),
        author: String(extractedMetadata.author || "Unknown"),
        totalBeats: Number(
          extractedMetadata.totalBeats || extractedMetadata.beats || 0
        ),
      };
    } catch (error) {
      console.error(
        `❌ Failed to extract metadata for ${thumbnail.metadata?.word || thumbnail.name}:`,
        error
      );
      throw new Error(`Failed to extract metadata: ${error}`);
    }
  }

  async extractMetadataFromFile(
    file: File
  ): Promise<Record<string, unknown>[]> {
    console.log(`🔍 Extracting metadata from file: ${file.name}`);

    try {
      // Convert File to a temporary path for extraction
      // Note: This would need proper file handling in a real implementation
      // For now, we'll create a temporary URL
      const tempUrl = URL.createObjectURL(file);

      try {
        const metadata = await PngMetadataExtractor.extractMetadata(tempUrl);

        if (!Array.isArray(metadata)) {
          throw new Error("Metadata is not in expected array format");
        }

        return metadata;
      } finally {
        URL.revokeObjectURL(tempUrl);
      }
    } catch (error) {
      console.error(
        `❌ Failed to extract metadata from file ${file.name}:`,
        error
      );
      throw new Error(`Failed to extract metadata: ${error}`);
    }
  }

  async extractRawMetadata(
    filePath: string
  ): Promise<Record<string, unknown>[]> {
    try {
      const metadata = await PngMetadataExtractor.extractMetadata(filePath);

      if (!Array.isArray(metadata)) {
        throw new Error("Metadata is not in expected array format");
      }

      return metadata;
    } catch (error) {
      console.error(
        `❌ Raw metadata extraction failed for ${filePath}:`,
        error
      );
      throw error;
    }
  }

  private processRawMetadata(
    rawMetadata: Record<string, unknown>[]
  ): Record<string, unknown> {
    if (!rawMetadata || rawMetadata.length === 0) {
      return {};
    }

    // Extract common metadata from the first entry
    const firstEntry = rawMetadata[0] || {};

    return {
      totalEntries: rawMetadata.length,
      author: firstEntry.author || null,
      level: firstEntry.level || null,
      sequence_start_position: this.findStartPosition(rawMetadata),
      beat_count: this.countRealBeats(rawMetadata),
      sequenceLength: rawMetadata.length,
      extracted_at: new Date().toISOString(),
      source: "png_metadata",
    };
  }

  private findStartPosition(
    metadata: Record<string, unknown>[]
  ): string | null {
    const startPositionEntry = metadata.find(
      (entry: Record<string, unknown>) => entry.sequence_start_position
    );

    return (startPositionEntry?.sequence_start_position as string) || null;
  }

  private countRealBeats(metadata: Record<string, unknown>[]): number {
    return metadata.filter(
      (entry: Record<string, unknown>) =>
        entry.letter && !entry.sequence_start_position
    ).length;
  }
}
