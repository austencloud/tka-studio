/**
 * Sequence Import Service
 *
 * Handles importing sequence data from external sources like PNG metadata.
 * Separate from core sequence CRUD operations and focused on data transformation.
 */

import type { ISequenceImportService } from "$contracts";
import type { BeatData, Letter, SequenceData } from "$domain";
import {
  createMotionData,
  createPictographData,
  GridMode,
  Location,
  MotionColor,
  MotionType,
  Orientation,
  PngMetadataArraySchema,
  PropType,
  RotationDirection,
  SequenceDataSchema,
} from "$domain";
import { PngMetadataExtractor } from "$utils";
import { parseStrict } from "$utils";
import { injectable } from "inversify";

// Constants for PNG metadata conversion
const PNG_MOTION_TYPES = {
  STATIC: "static",
  PRO: "pro",
  ANTI: "anti",
  FLOAT: "float",
  DASH: "dash",
} as const;

@injectable()
export class SequenceImportService implements ISequenceImportService {
  /**
   * Import sequence from PNG metadata
   */
  async importFromPNG(id: string): Promise<SequenceData | null> {
    console.log(`🎬 Loading sequence from PNG metadata for ID: ${id}`);

    try {
      // Extract metadata from PNG file using the reliable extractor
      const pngMetadata = await PngMetadataExtractor.extractSequenceMetadata(
        id.toUpperCase()
      );

      if (!pngMetadata || pngMetadata.length === 0) {
        console.error(`No metadata found in PNG for sequence: ${id}`);
        return null;
      }

      // Convert PNG metadata to web app format
      const sequence = await this.convertPngMetadata(id, pngMetadata);
      console.log(`✅ Loaded real sequence data from PNG for ${id}`);
      return sequence;
    } catch (error) {
      console.error(`Failed to load PNG metadata for ${id}:`, error);
      // No fallback - let the error bubble up
      throw new Error(
        `No PNG metadata found for sequence ${id}. Please ensure the sequence has a valid PNG thumbnail with embedded metadata.`
      );
    }
  }

  /**
   * Convert PNG metadata to SequenceData format - Now with bulletproof Zod validation!
   * Replaces 100+ lines of manual type assertions with validated parsing.
   */
  async convertPngMetadata(
    id: string,
    pngMetadata: unknown[]
  ): Promise<SequenceData> {
    console.log(`🔄 Converting PNG metadata to web app format for ${id}`);

    // Validate PNG structure first - throws if malformed
    const validatedSteps = parseStrict(
      PngMetadataArraySchema,
      pngMetadata.slice(1), // Skip metadata header, validate steps
      `PNG steps for sequence ${id}`
    );

    // Convert validated steps to beats (no more type assertions needed!)
    const beats: BeatData[] = validatedSteps.map((step) => ({
      id: `${step.beat}-${step.letter}`,
      beatNumber: step.beat, // Guaranteed to be positive number
      duration: 1,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
      pictographData: createPictographData({
        id: `pictograph-${step.beat}`,
        motions: {
          blue: createMotionData({
            color: MotionColor.BLUE,
            motionType:
              this.convertMotionType(step.blue_attributes?.motion_type) ||
              MotionType.STATIC,
            startLocation:
              this.convertLocation(step.blue_attributes?.start_loc) ||
              Location.NORTH,
            endLocation:
              this.convertLocation(step.blue_attributes?.end_loc) ||
              Location.NORTH,
            startOrientation:
              this.convertOrientation(step.blue_attributes?.start_ori) ||
              Orientation.IN,
            endOrientation:
              this.convertOrientation(step.blue_attributes?.end_ori) ||
              Orientation.IN,
            rotationDirection:
              this.convertRotationDirection(
                step.blue_attributes?.prop_rot_dir
              ) || RotationDirection.NO_ROTATION,
            turns: step.blue_attributes?.turns || 0,
            isVisible: true,
            propType: PropType.STAFF,
            arrowLocation:
              this.convertLocation(step.blue_attributes?.start_loc) ||
              Location.NORTH,
          }),
          red: createMotionData({
            color: MotionColor.RED,
            motionType:
              this.convertMotionType(step.red_attributes?.motion_type) ||
              MotionType.STATIC,
            startLocation:
              this.convertLocation(step.red_attributes?.start_loc) ||
              Location.SOUTH,
            endLocation:
              this.convertLocation(step.red_attributes?.end_loc) ||
              Location.SOUTH,
            startOrientation:
              this.convertOrientation(step.red_attributes?.start_ori) ||
              Orientation.IN,
            endOrientation:
              this.convertOrientation(step.red_attributes?.end_ori) ||
              Orientation.IN,
            rotationDirection:
              this.convertRotationDirection(
                step.red_attributes?.prop_rot_dir
              ) || RotationDirection.NO_ROTATION,
            turns: step.red_attributes?.turns || 0,
            isVisible: true,
            propType: PropType.STAFF,
            arrowLocation:
              this.convertLocation(step.red_attributes?.start_loc) ||
              Location.SOUTH,
          }),
        },
        letter: step.letter as Letter, // Guaranteed valid string
      }),
    }));

    console.log(`✅ Converted to web app format: ${beats.length} beats`);

    // Create sequence data with validated structure - final validation
    const sequenceData = {
      id: crypto.randomUUID(), // Generate proper UUID for validation
      name: id.toUpperCase(),
      word: id as string, // Ensure word is always a string
      beats,
      thumbnails: [], // Empty array as default - schema requires URLs
      sequenceLength: beats.length,
      author: "PNG Import",
      level: 1,
      dateAdded: new Date(),
      gridMode: GridMode.DIAMOND,
      propType: PropType.FAN,
      isFavorite: false,
      isCircular: false,
      difficultyLevel: "beginner",
      tags: ["imported", "png"],
      metadata: {
        source: "png_metadata",
        extracted_at: new Date().toISOString(),
        original_id: id, // Keep original ID for reference
      },
    };

    // Ensure all required properties are present and properly typed
    const validSequenceData = {
      id: sequenceData.id,
      name: sequenceData.name,
      word: id, // Explicitly ensure word is the id string
      beats: sequenceData.beats,
      thumbnails: sequenceData.thumbnails,
      isFavorite: sequenceData.isFavorite,
      isCircular: sequenceData.isCircular,
      tags: sequenceData.tags,
      metadata: sequenceData.metadata,
      propType: sequenceData.propType,
      gridMode: sequenceData.gridMode,
      difficultyLevel: sequenceData.difficultyLevel,
      author: sequenceData.author,
      level: sequenceData.level,
      dateAdded: sequenceData.dateAdded,
      sequenceLength: sequenceData.sequenceLength,
    };

    // @ts-expect-error - TypeScript is incorrectly inferring word as potentially undefined
    return parseStrict(
      SequenceDataSchema,
      validSequenceData,
      `final sequence validation for ${id}`
    );
  }

  /**
   * Convert PNG motion type string to MotionType enum
   * @param motionType - PNG motion type string ("static", "pro", "anti", "float", "dash")
   * @returns Corresponding MotionType enum value or undefined if invalid
   */
  private convertMotionType(motionType?: string): MotionType | undefined {
    if (!motionType) return undefined;

    switch (motionType.toLowerCase()) {
      case PNG_MOTION_TYPES.STATIC:
        return MotionType.STATIC;
      case PNG_MOTION_TYPES.PRO:
        return MotionType.PRO;
      case PNG_MOTION_TYPES.ANTI:
        return MotionType.ANTI;
      case PNG_MOTION_TYPES.FLOAT:
        return MotionType.FLOAT;
      case PNG_MOTION_TYPES.DASH:
        return MotionType.DASH;
      default:
        return undefined;
    }
  }

  /**
   * Convert PNG location string to Location enum
   */
  private convertLocation(location?: string): Location | undefined {
    if (!location) return undefined;

    switch (location.toLowerCase()) {
      case "n":
        return Location.NORTH;
      case "e":
        return Location.EAST;
      case "s":
        return Location.SOUTH;
      case "w":
        return Location.WEST;
      case "ne":
        return Location.NORTHEAST;
      case "se":
        return Location.SOUTHEAST;
      case "sw":
        return Location.SOUTHWEST;
      case "nw":
        return Location.NORTHWEST;
      default:
        return undefined;
    }
  }

  /**
   * Convert PNG orientation string to Orientation enum
   */
  private convertOrientation(orientation?: string): Orientation | undefined {
    if (!orientation) return undefined;

    switch (orientation.toLowerCase()) {
      case "in":
        return Orientation.IN;
      case "out":
        return Orientation.OUT;
      default:
        return undefined;
    }
  }

  /**
   * Convert PNG rotation direction string to RotationDirection enum
   */
  private convertRotationDirection(
    rotationDir?: string
  ): RotationDirection | undefined {
    if (!rotationDir) return undefined;

    switch (rotationDir.toLowerCase()) {
      case "no_rot":
        return RotationDirection.NO_ROTATION;
      case "cw":
        return RotationDirection.CLOCKWISE;
      case "ccw":
        return RotationDirection.COUNTER_CLOCKWISE;
      default:
        return undefined;
    }
  }
}
