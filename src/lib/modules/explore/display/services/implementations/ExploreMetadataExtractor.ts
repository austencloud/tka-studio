/**
 * Explore Metadata Extractor Service
 *
 * Extracts metadata from sequence files (PNG, WebP, or JSON sidecars)
 * with proper error handling and type safety.
 */

import type { BeatData } from "$shared";
import {
  createMotionData,
  GridLocation,
  GridMode,
  MotionColor,
  MotionType,
  Orientation,
  RotationDirection,
} from "$shared";
import { PropType } from "$shared/pictograph/prop/domain/enums/PropType";
import { inject, injectable } from "inversify";
import { TYPES } from "../../../../../shared/inversify/types";
import { UniversalMetadataExtractor } from "../../../../../shared/services/UniversalMetadataExtractor";
import type {
  IExploreMetadataExtractor,
  SequenceMetadata,
} from "../contracts/IExploreMetadataExtractor";
import type { ISequenceDifficultyCalculator } from "../contracts/ISequenceDifficultyCalculator";
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
  constructor(
    @inject(TYPES.ISequenceDifficultyCalculator)
    private readonly difficultyCalculator: ISequenceDifficultyCalculator
  ) {}

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
        return DEFAULT_METADATA;
      }

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
   * Parse raw metadata into typed SequenceMetadata
   */
  private parseMetadataResult(
    sequenceName: string,
    rawData: Record<string, unknown>
  ): SequenceMetadata {
    const beats = this.parseBeats(sequenceName, rawData.sequence);
    const gridMode = this.parseGridMode(rawData.grid_mode);

    // Calculate difficulty from actual sequence data instead of stored level
    const difficultyLevel = this.calculateDifficultyLevel(beats);

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
   * Parse beat data from sequence array with full motion parsing
   */
  private parseBeats(sequenceName: string, sequence: unknown): BeatData[] {
    if (!Array.isArray(sequence)) {
      return [];
    }

    return sequence.map((step: unknown, index: number) => {
      const stepData = step as Record<string, unknown>;
      const blueAttrs = stepData.blue_attributes as Record<string, unknown>;
      const redAttrs = stepData.red_attributes as Record<string, unknown>;

      return {
        // PictographData properties
        id: `beat-${sequenceName}-${index + 1}`,
        letter: String(stepData.letter || ""),
        startPosition: null,
        endPosition: null,
        motions: {
          [MotionColor.BLUE]: blueAttrs
            ? createMotionData({
                color: MotionColor.BLUE,
                motionType: this.parseMotionType(blueAttrs.motion_type),
                startLocation: this.parseLocation(blueAttrs.start_loc),
                endLocation: this.parseLocation(blueAttrs.end_loc),
                startOrientation: this.parseOrientation(blueAttrs.start_ori),
                endOrientation: this.parseOrientation(blueAttrs.end_ori),
                rotationDirection: this.parseRotationDirection(
                  blueAttrs.prop_rot_dir
                ),
                turns: this.parseTurns(blueAttrs.turns),
                isVisible: true,
                propType: PropType.STAFF,
                arrowLocation:
                  this.parseLocation(blueAttrs.start_loc) || GridLocation.NORTH,
                gridMode: GridMode.DIAMOND,
              })
            : undefined,
          [MotionColor.RED]: redAttrs
            ? createMotionData({
                color: MotionColor.RED,
                motionType: this.parseMotionType(redAttrs.motion_type),
                startLocation: this.parseLocation(redAttrs.start_loc),
                endLocation: this.parseLocation(redAttrs.end_loc),
                startOrientation: this.parseOrientation(redAttrs.start_ori),
                endOrientation: this.parseOrientation(redAttrs.end_ori),
                rotationDirection: this.parseRotationDirection(
                  redAttrs.prop_rot_dir
                ),
                turns: this.parseTurns(redAttrs.turns),
                isVisible: true,
                propType: PropType.STAFF,
                arrowLocation:
                  this.parseLocation(redAttrs.start_loc) || GridLocation.SOUTH,
                gridMode: GridMode.DIAMOND,
              })
            : undefined,
        },
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
   * Calculate difficulty level from actual beat data
   * Replaces the old parseDifficultyLevel that just read a stored value
   */
  private calculateDifficultyLevel(beats: BeatData[]): string {
    const numericLevel =
      this.difficultyCalculator.calculateDifficultyLevel(beats);
    return this.difficultyCalculator.levelToString(numericLevel);
  }

  /**
   * Parse motion type with fallback
   */
  private parseMotionType(value: unknown): MotionType {
    const str = String(value || "").toLowerCase();
    switch (str) {
      case "pro":
        return MotionType.PRO;
      case "anti":
        return MotionType.ANTI;
      case "float":
        return MotionType.FLOAT;
      case "dash":
        return MotionType.DASH;
      case "static":
        return MotionType.STATIC;
      default:
        return MotionType.STATIC;
    }
  }

  /**
   * Parse grid location with fallback
   */
  private parseLocation(value: unknown): GridLocation {
    const str = String(value || "").toUpperCase();
    // Map common location strings to GridLocation enum values
    const locationMap: Record<string, GridLocation> = {
      N: GridLocation.NORTH,
      NORTH: GridLocation.NORTH,
      E: GridLocation.EAST,
      EAST: GridLocation.EAST,
      S: GridLocation.SOUTH,
      SOUTH: GridLocation.SOUTH,
      W: GridLocation.WEST,
      WEST: GridLocation.WEST,
      NE: GridLocation.NORTHEAST,
      NORTHEAST: GridLocation.NORTHEAST,
      SE: GridLocation.SOUTHEAST,
      SOUTHEAST: GridLocation.SOUTHEAST,
      SW: GridLocation.SOUTHWEST,
      SOUTHWEST: GridLocation.SOUTHWEST,
      NW: GridLocation.NORTHWEST,
      NORTHWEST: GridLocation.NORTHWEST,
    };
    return locationMap[str] || GridLocation.NORTH;
  }

  /**
   * Parse orientation with fallback
   */
  private parseOrientation(value: unknown): Orientation {
    const str = String(value || "").toLowerCase();
    switch (str) {
      case "in":
        return Orientation.IN;
      case "out":
        return Orientation.OUT;
      case "clock":
      case "clockwise":
        return Orientation.CLOCK;
      case "counter":
      case "counterclockwise":
        return Orientation.COUNTER;
      default:
        return Orientation.IN;
    }
  }

  /**
   * Parse rotation direction with fallback
   */
  private parseRotationDirection(value: unknown): RotationDirection {
    const str = String(value || "").toLowerCase();
    switch (str) {
      case "cw":
      case "clockwise":
        return RotationDirection.CLOCKWISE;
      case "ccw":
      case "counterclockwise":
      case "counter_clockwise":
        return RotationDirection.COUNTER_CLOCKWISE;
      case "no_rotation":
      case "norotation":
        return RotationDirection.NO_ROTATION;
      default:
        return RotationDirection.NO_ROTATION;
    }
  }

  /**
   * Parse turns value (can be number or "fl" for float)
   */
  private parseTurns(value: unknown): number | "fl" {
    if (value === "fl" || value === "float") {
      return "fl";
    }
    const num = Number(value);
    return isNaN(num) ? 0 : num;
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
