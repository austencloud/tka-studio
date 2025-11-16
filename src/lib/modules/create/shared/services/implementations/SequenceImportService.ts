/**
 * Sequence Import Service
 *
 * Handles importing sequence data from external sources like PNG metadata.
 * Separate from core sequence CRUD operations and focused on data transformation.
 */

import { PngMetadataExtractor } from "$lib/shared/pictograph/shared/utils/png-metadata-extractor";
import type { BeatData, Letter, SequenceData } from "$shared";
import type { IEnumMapper } from "$shared";
import {
  createMotionData,
  createPictographData,
  createSequenceData,
  GridLocation,
  GridMode,
  MotionColor,
  MotionType,
  Orientation,
  parseStrict,
  PngMetadataArraySchema,
  PropType,
  RotationDirection,
} from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { ISequenceImportService } from "../contracts";

@injectable()
export class SequenceImportService implements ISequenceImportService {
  constructor(
    @inject(TYPES.IEnumMapper) private readonly enumMapper: IEnumMapper
  ) {}
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
    const beats: BeatData[] = validatedSteps.map((step: any) => {
      // Create the pictograph data first
      const pictographData = createPictographData({
        id: `pictograph-${step.beat}`,
        motions: {
          blue: createMotionData({
            color: MotionColor.BLUE,
            motionType:
              this.enumMapper.mapMotionType(
                step.blue_attributes?.motion_type
              ) || MotionType.STATIC,
            startLocation:
              this.enumMapper.mapLocation(step.blue_attributes?.start_loc) ||
              GridLocation.NORTH,
            endLocation:
              this.enumMapper.mapLocation(step.blue_attributes?.end_loc) ||
              GridLocation.NORTH,
            startOrientation:
              this.enumMapper.mapOrientation(step.blue_attributes?.start_ori) ||
              Orientation.IN,
            endOrientation:
              this.enumMapper.mapOrientation(step.blue_attributes?.end_ori) ||
              Orientation.IN,
            rotationDirection:
              this.enumMapper.mapRotationDirection(
                step.blue_attributes?.prop_rot_dir
              ) || RotationDirection.NO_ROTATION,
            turns: step.blue_attributes?.turns || 0,
            isVisible: true,
            propType: PropType.STAFF,
            arrowLocation:
              this.enumMapper.mapLocation(step.blue_attributes?.start_loc) ||
              GridLocation.NORTH,
          }),
          red: createMotionData({
            color: MotionColor.RED,
            motionType:
              this.enumMapper.mapMotionType(step.red_attributes?.motion_type) ||
              MotionType.STATIC,
            startLocation:
              this.enumMapper.mapLocation(step.red_attributes?.start_loc) ||
              GridLocation.SOUTH,
            endLocation:
              this.enumMapper.mapLocation(step.red_attributes?.end_loc) ||
              GridLocation.SOUTH,
            startOrientation:
              this.enumMapper.mapOrientation(step.red_attributes?.start_ori) ||
              Orientation.IN,
            endOrientation:
              this.enumMapper.mapOrientation(step.red_attributes?.end_ori) ||
              Orientation.IN,
            rotationDirection:
              this.enumMapper.mapRotationDirection(
                step.red_attributes?.prop_rot_dir
              ) || RotationDirection.NO_ROTATION,
            turns: step.red_attributes?.turns || 0,
            isVisible: true,
            propType: PropType.STAFF,
            arrowLocation:
              this.enumMapper.mapLocation(step.red_attributes?.start_loc) ||
              GridLocation.SOUTH,
          }),
        },
        letter: step.letter as Letter, // Guaranteed valid string
      });

      // Return BeatData that extends PictographData
      return {
        ...pictographData, // Spread PictographData properties
        id: `${step.beat}-${step.letter}`,
        beatNumber: step.beat, // Guaranteed to be positive number
        duration: 1,
        blueReversal: false,
        redReversal: false,
        isBlank: false,
      };
    });

    console.log(`✅ Converted to web app format: ${beats.length} beats`);

    // Create sequence data with validated structure - final validation
    const sequenceData: Partial<SequenceData> = {
      id: crypto.randomUUID(), // Generate proper UUID for validation
      name: id.toUpperCase(),
      word: id, // Ensure word is always a string
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
      word: id, // Use id directly to ensure it's always a string
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

    // Use createSequenceData to ensure all required properties are properly set
    const finalSequenceData = createSequenceData({
      id: validSequenceData.id || crypto.randomUUID(),
      name: validSequenceData.name || id.toUpperCase(),
      word: id, // Guarantee word is a string
      beats: validSequenceData.beats || [],
      thumbnails: validSequenceData.thumbnails || [],
      isFavorite: validSequenceData.isFavorite ?? false,
      isCircular: validSequenceData.isCircular ?? false,
      tags: validSequenceData.tags || [],
      ...(validSequenceData.metadata
        ? { metadata: validSequenceData.metadata }
        : {}),
      propType: validSequenceData.propType || PropType.FAN,
      gridMode: validSequenceData.gridMode || GridMode.DIAMOND,
      difficultyLevel: validSequenceData.difficultyLevel || "beginner",
      author: validSequenceData.author || "PNG Import",
      level: validSequenceData.level ?? 1,
      dateAdded: validSequenceData.dateAdded || new Date(),
      sequenceLength: validSequenceData.sequenceLength ?? beats.length,
    });

    // The createSequenceData function already ensures proper typing, so return directly
    return finalSequenceData;
  }
}
