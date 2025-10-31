/**
 * Explore Metadata Extractor Service
 *
 * Extracts metadata from sequence files (PNG, WebP, or JSON sidecars)
 * with proper error handling and type safety.
 */

import type { BeatData } from "$shared";
import { GridMode } from "$shared/pictograph/grid/domain/enums/grid-enums";
import { PropType } from "$shared/pictograph/prop/domain/enums/PropType";
import { injectable } from "inversify";
import { UniversalMetadataExtractor } from "../../../../../shared/services/UniversalMetadataExtractor";
import type {
  IExploreMetadataExtractor,
  SequenceMetadata,
} from "../contracts/IExploreMetadataExtractor";

// Constants for metadata extraction
const DEFAULT_METADATA: SequenceMetadata = {
  beats: [],
  author: "Unknown",
  difficultyLevel: "beginner",
  dateAdded: new Date(),
  gridMode: GridMode.DIAMOND,
  isCircular: false,
  propType: "Staff" as PropType,
  sequenceLength: 0,
  startingPosition: "alpha",
};

const DATE_FIELD_NAMES = [
  "date_added",
  "dateAdded",
  "date",
  "created_date",
  "timestamp",
] as const;

@injectable()
export class ExploreMetadataExtractor implements IExploreMetadataExtractor {
  async extractMetadata(
    sequenceName: string,
    thumbnailPath?: string
  ): Promise<SequenceMetadata> {
    try {
      const sequenceWithVersion = this.determineSequenceVersion(
        sequenceName,
        thumbnailPath
      );

      const result =
        await UniversalMetadataExtractor.extractMetadata(sequenceWithVersion);

      if (!result.success || !result.data) {
        console.warn(
          `⚠️ No metadata found for ${sequenceName}, using defaults`
        );
        return DEFAULT_METADATA;
      }

      this.logExtractionSource(sequenceName, result.source);

      return this.parseMetadataResult(sequenceName, result.data);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : String(error);

      // Only log non-routine errors
      if (!errorMessage.includes("No valid version found")) {
        console.warn(
          `⚠️ Failed to extract metadata for ${sequenceName}:`,
          error
        );
      }

      throw error;
    }
  }

  /**
   * Determine the sequence version from thumbnail path or default to ver1
   */
  private determineSequenceVersion(
    sequenceName: string,
    thumbnailPath?: string
  ): string {
    if (!thumbnailPath) {
      return `${sequenceName}_ver1`;
    }

    const versionMatch = thumbnailPath.match(/_ver(\d+)\.webp$/);
    if (versionMatch) {
      const version = versionMatch[1];
      return `${sequenceName}_ver${version}`;
    }

    return `${sequenceName}_ver1`;
  }

  /**
   * Log the source of metadata extraction for optimization tracking
   */
  private logExtractionSource(sequenceName: string, source?: string): void {
    switch (source) {
      case "sidecar":
        console.log(`⚡ Modern sidecar metadata loaded for ${sequenceName}`);
        break;
      case "fallback-webp":
        console.log(
          `📝 WebP fallback used for ${sequenceName} - consider migrating to sidecar`
        );
        break;
      case "fallback-png":
        console.log(
          `📝 PNG fallback used for ${sequenceName} - consider migrating to sidecar`
        );
        break;
    }
  }

  /**
   * Parse raw metadata into typed SequenceMetadata
   */
  private parseMetadataResult(
    sequenceName: string,
    rawData: Record<string, unknown>
  ): SequenceMetadata {
    const beats = this.parseBeats(sequenceName, rawData.sequence);
    const gridMode = this.parseGridMode(rawData.grid_mode);
    const difficultyLevel = this.parseDifficultyLevel(rawData.level);
    const dateAdded = this.parseDateAdded(rawData);
    const startingPosition = this.parseStartingPosition(beats);

    return {
      beats,
      author: String(rawData.author || "Unknown"),
      difficultyLevel,
      dateAdded,
      gridMode,
      isCircular: Boolean(rawData.is_circular),
      propType: String(rawData.prop_type || "Staff") as PropType,
      sequenceLength: beats.length,
      startingPosition,
    };
  }

  /**
   * Parse beat data from sequence array
   */
  private parseBeats(sequenceName: string, sequence: unknown): BeatData[] {
    if (!Array.isArray(sequence)) {
      return [];
    }

    return sequence.map((step: unknown, index: number) => {
      const stepData = step as Record<string, unknown>;

      return {
        // PictographData properties
        id: `beat-${sequenceName}-${index + 1}`,
        letter: String(stepData.letter || ""),
        startPosition: null,
        endPosition: null,
        motions: {},
        // Beat context properties
        beatNumber: Number(stepData.beat || index + 1),
        duration: 1.0,
        blueReversal: false,
        redReversal: false,
        isBlank: false,
      } as BeatData;
    });
  }

  /**
   * Parse grid mode with fallback
   */
  private parseGridMode(gridModeValue: unknown): GridMode {
    if (gridModeValue === "diamond") {
      return GridMode.DIAMOND;
    }
    if (gridModeValue === "box") {
      return GridMode.BOX;
    }
    return GridMode.DIAMOND;
  }

  /**
   * Parse difficulty level from numeric level
   */
  private parseDifficultyLevel(level: unknown): string {
    const levelNum = Number(level || 1);

    if (levelNum >= 3) {
      return "advanced";
    }
    if (levelNum >= 2) {
      return "intermediate";
    }
    return "beginner";
  }

  /**
   * Parse date from various possible field names
   */
  private parseDateAdded(rawData: Record<string, unknown>): Date {
    for (const fieldName of DATE_FIELD_NAMES) {
      const fieldValue = rawData[fieldName];
      if (fieldValue) {
        try {
          const date = new Date(String(fieldValue));
          if (!isNaN(date.getTime())) {
            return date;
          }
        } catch {
          // Continue to next field
        }
      }
    }

    return new Date();
  }

  /**
   * Extract starting position from first beat
   */
  private parseStartingPosition(beats: BeatData[]): string {
    if (beats.length > 0) {
      const firstLetter = beats[0]?.letter;
      if (firstLetter) {
        return firstLetter;
      }
    }
    return "alpha";
  }
}
