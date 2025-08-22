/**
 * Sequence Import Service
 *
 * Handles importing sequence data from external sources like PNG metadata.
 * Separate from core sequence CRUD operations and focused on data transformation.
 */

import type { BeatData, SequenceData, Letter } from "$lib/domain";
import { createMotionData, createPictographData } from "$lib/domain";
import {
  GridMode,
  MotionType,
  PropType,
  MotionColor,
  RotationDirection,
  Location,
  Orientation,
} from "$lib/domain/enums";
import { PngMetadataExtractor } from "$lib/utils/png-metadata-extractor";

export interface ISequenceImportService {
  importFromPNG(id: string): Promise<SequenceData | null>;
  convertPngMetadata(id: string, metadata: unknown[]): Promise<SequenceData>;
}

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
   * Convert PNG metadata to SequenceData format
   */
  async convertPngMetadata(
    id: string,
    pngMetadata: unknown[]
  ): Promise<SequenceData> {
    console.log(`🔄 Converting standalone data to web app format for ${id}`);

    // Extract metadata from first element
    const meta = pngMetadata[0] as Record<string, unknown>;
    const steps = pngMetadata.slice(1) as Record<string, unknown>[]; // Skip metadata, get actual steps

    // Convert steps to beats
    const beats: BeatData[] = steps
      .filter((step) => typeof step.beat === "number" && step.beat > 0) // Only actual beats, not start state
      .map((step) => ({
        id: `${step.beat}-${step.letter}`,
        beatNumber: step.beat as number,
        duration: 1,
        blueReversal: false,
        redReversal: false,
        isBlank: false,
        pictographData: createPictographData({
          id: `pictograph-${step.beat}`,
          gridMode: (meta.gridMode as GridMode) || GridMode.DIAMOND,
          motions: {
            blue: createMotionData({
              color: MotionColor.BLUE,
              motionType:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.motionType as MotionType) || MotionType.STATIC,
              startLocation:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.startLocation as Location) || Location.SOUTH,
              endLocation:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.endLocation as Location) || Location.SOUTH,
              startOrientation:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.startOrientation as Orientation) || Orientation.IN,
              endOrientation:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.endOrientation as Orientation) || Orientation.IN,
              rotationDirection:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.rotationDirection as RotationDirection) ||
                RotationDirection.NO_ROTATION,
              turns:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.turns as number) || 0,
              isVisible: true,
              propType: PropType.STAFF,
              arrowLocation:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.startLocation as Location) || Location.SOUTH,
            }),
            red: createMotionData({
              color: MotionColor.RED,
              motionType:
                ((step.redAttributes as Record<string, unknown>)
                  ?.motionType as MotionType) || MotionType.STATIC,
              startLocation:
                ((step.redAttributes as Record<string, unknown>)
                  ?.startLocation as Location) || Location.SOUTH,
              endLocation:
                ((step.redAttributes as Record<string, unknown>)
                  ?.endLocation as Location) || Location.SOUTH,
              startOrientation:
                ((step.redAttributes as Record<string, unknown>)
                  ?.startOrientation as Orientation) || Orientation.IN,
              endOrientation:
                ((step.redAttributes as Record<string, unknown>)
                  ?.endOrientation as Orientation) || Orientation.IN,
              rotationDirection:
                ((step.redAttributes as Record<string, unknown>)
                  ?.rotationDirection as RotationDirection) ||
                RotationDirection.NO_ROTATION,
              turns:
                ((step.redAttributes as Record<string, unknown>)
                  ?.turns as number) || 0,
              isVisible: true,
              propType: PropType.STAFF,
              arrowLocation:
                ((step.redAttributes as Record<string, unknown>)
                  ?.startLocation as Location) || Location.SOUTH,
            }),
          },
          letter: (step.letter as Letter) || null,
          isBlank: false,
          metadata: {},
        }),
        metadata: {},
      }));

    console.log(`✅ Converted to web app format: ${beats.length} beats`);

    return {
      id,
      name: (meta.word as string) || id.toUpperCase(),
      word: (meta.word as string) || id.toUpperCase(),
      beats,
      thumbnails: [`${id.toUpperCase()}_ver1.png`],
      sequenceLength: beats.length,
      author: (meta.author as string) || "Unknown",
      level: (meta.level as number) || 1,
      dateAdded: new Date((meta.dateAdded as string | number) || Date.now()),
      gridMode: ((meta.gridMode as string) || GridMode.DIAMOND) as GridMode,
      propType: ((meta.propType as string) || PropType.FAN) as PropType,
      isFavorite: (meta.isFavorite as boolean) || false,
      isCircular: (meta.isCircular as boolean) || false,
      // startingPosition: TODO - needs to be BeatData, not string
      difficultyLevel: this.mapLevelToDifficulty((meta.level as number) || 1),
      tags: ["flow", "practice"],
      metadata: {
        source: "png_metadata",
        extracted_at: new Date().toISOString(),
        ...meta,
      },
    };
  }

  /**
   * Map numeric level to difficulty string
   */
  private mapLevelToDifficulty(level: number): string {
    if (level <= 1) return "beginner";
    if (level <= 2) return "intermediate";
    return "advanced";
  }
}
