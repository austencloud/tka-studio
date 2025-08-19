/**
 * Sequence Service - Application Layer
 *
 * Coordinates between domain logic and persistence for sequence operations.
 * This service orchestrates the business workflows for sequence management.
 */

import type { BeatData, SequenceData } from "$lib/domain";
import {
  GridMode,
  MotionType,
  RotationDirection,
  Location,
  Orientation,
} from "$lib/domain/enums";

import { PngMetadataExtractor } from "$lib/utils/png-metadata-extractor";
import type {
  IPersistenceService,
  ISequenceDomainService,
  ISequenceService,
  SequenceCreateRequest,
} from "../interfaces/sequence-interfaces";

export class SequenceService implements ISequenceService {
  constructor(
    private sequenceDomainService: ISequenceDomainService,
    private persistenceService: IPersistenceService
  ) {}

  /**
   * Create a new sequence
   */
  async createSequence(request: SequenceCreateRequest): Promise<SequenceData> {
    try {
      // Use domain service to create the sequence
      const sequence = this.sequenceDomainService.createSequence(request);
      await this.persistenceService.saveSequence(sequence);
      return sequence;
    } catch (error) {
      console.error("Failed to create sequence:", error);
      throw new Error(
        `Failed to create sequence: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Update a beat in a sequence
   */
  async updateBeat(
    sequenceId: string,
    beatIndex: number,
    beatData: BeatData
  ): Promise<void> {
    try {
      // Load the current sequence
      const currentSequence =
        await this.persistenceService.loadSequence(sequenceId);
      if (!currentSequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }

      // Use domain service to update the beat
      const updatedSequence = this.sequenceDomainService.updateBeat(
        currentSequence,
        beatIndex,
        beatData
      );

      await this.persistenceService.saveSequence(updatedSequence);
    } catch (error) {
      console.error("Failed to update beat:", error);
      throw new Error(
        `Failed to update beat: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Set the start position for a sequence
   */
  async setSequenceStartPosition(
    sequenceId: string,
    startPosition: BeatData
  ): Promise<void> {
    try {
      // Load the current sequence
      const currentSequence =
        await this.persistenceService.loadSequence(sequenceId);
      if (!currentSequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }

      // Update the sequence with the start position
      const updatedSequence = {
        ...currentSequence,
        startPosition: startPosition,
      } as SequenceData;

      await this.persistenceService.saveSequence(updatedSequence);
    } catch (error) {
      console.error("Failed to set start position:", error);
      throw new Error(
        `Failed to set start position: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Delete a sequence
   */
  async deleteSequence(id: string): Promise<void> {
    try {
      await this.persistenceService.deleteSequence(id);
    } catch (error) {
      console.error("Failed to delete sequence:", error);
      throw new Error(
        `Failed to delete sequence: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Get a sequence by ID
   */
  async getSequence(id: string): Promise<SequenceData | null> {
    try {
      let sequence = await this.persistenceService.loadSequence(id);

      // If sequence not found, try to load from PNG metadata
      if (!sequence) {
        console.log(
          `🎬 Sequence ${id} not found, attempting to load from PNG metadata`
        );
        try {
          sequence = await this.loadSequenceFromPNG(id);
          // Save it to localStorage for future use
          if (sequence) {
            await this.persistenceService.saveSequence(sequence);
          }
        } catch (error) {
          console.error(`Failed to load sequence ${id} from PNG:`, error);
          return null;
        }
      }

      return sequence;
    } catch (error) {
      console.error(`Failed to get sequence ${id}:`, error);
      return null;
    }
  }

  /**
   * Get all sequences
   */
  async getAllSequences(): Promise<SequenceData[]> {
    try {
      return await this.persistenceService.loadAllSequences();
    } catch (error) {
      console.error("Failed to get all sequences:", error);
      return [];
    }
  }

  /**
   * Add a beat to a sequence
   */
  async addBeat(
    sequenceId: string,
    beatData?: Partial<BeatData>
  ): Promise<void> {
    try {
      const sequence = await this.getSequence(sequenceId);
      if (!sequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }

      // Create new beat with next beat number
      const nextBeatNumber = sequence.beats.length + 1;
      const newBeat: BeatData = {
        id: crypto.randomUUID(),
        beat_number: nextBeatNumber,
        duration: 1.0,
        blue_reversal: false,
        red_reversal: false,
        isBlank: true,
        pictograph_data: null,
        metadata: {},
        ...beatData,
      };
      const updatedSequence = {
        ...sequence,
        beats: [...sequence.beats, newBeat],
      } as SequenceData;
      await this.persistenceService.saveSequence(updatedSequence);
    } catch (error) {
      console.error("Failed to add beat:", error);
      throw new Error(
        `Failed to add beat: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Remove a beat from a sequence
   */
  async removeBeat(sequenceId: string, beatIndex: number): Promise<void> {
    try {
      const sequence = await this.getSequence(sequenceId);
      if (!sequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }

      if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
        throw new Error(`Beat index ${beatIndex} is out of range`);
      }

      // Remove the beat and renumber remaining beats
      const newBeats = sequence.beats
        .filter((_, index) => index !== beatIndex)
        .map((beat, index) => ({ ...beat, beat_number: index + 1 }));
      const updatedSequence = { ...sequence, beats: newBeats } as SequenceData;
      await this.persistenceService.saveSequence(updatedSequence);
    } catch (error) {
      console.error("Failed to remove beat:", error);
      throw new Error(
        `Failed to remove beat: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Load sequence from PNG metadata using the reliable PNG metadata extractor
   */
  private async loadSequenceFromPNG(id: string): Promise<SequenceData | null> {
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
      const sequence = await this.convertPngMetadataToSequence(id, pngMetadata);
      console.log(`✅ Loaded real sequence data from PNG for ${id}`);
      return sequence;
    } catch (error) {
      console.error(`Failed to load PNG metadata for ${id}:`, error);
      // Fallback to test sequence
      return this.createTestSequence(id);
    }
  }

  /**
   * Convert PNG metadata to SequenceData format
   */
  private async convertPngMetadataToSequence(
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
        beat_number: step.beat as number,
        duration: 1,
        blue_reversal: false,
        red_reversal: false,
        isBlank: false,
        pictograph_data: {
          id: `pictograph-${step.beat}`,
          gridData: {
            gridMode: (meta.gridMode as GridMode) || GridMode.DIAMOND,
            center_x: 0,
            center_y: 0,
            radius: 100,
            grid_points: {},
          },
          arrows: {},
          props: {},
          motions: {
            blue: {
              motionType:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.motionType as MotionType) || MotionType.STATIC,
              start_loc:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.start_loc as Location) || Location.SOUTH,
              end_loc:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.end_loc as Location) || Location.SOUTH,
              startOrientation:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.startOrientation as Orientation) || Orientation.IN,
              endOrientation: (step.blueAttributes as Record<string, unknown>)
                ?.endOrientation as Orientation, // Don't set default - let it be undefined
              rotationDirection:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.rotationDirection as RotationDirection) ||
                RotationDirection.NO_ROTATION,
              turns:
                ((step.blueAttributes as Record<string, unknown>)
                  ?.turns as number) || 0,
              is_visible: true,
            },
            red: {
              motionType:
                ((step.redAttributes as Record<string, unknown>)
                  ?.motionType as MotionType) || MotionType.STATIC,
              start_loc:
                ((step.redAttributes as Record<string, unknown>)
                  ?.start_loc as Location) || Location.SOUTH,
              end_loc:
                ((step.redAttributes as Record<string, unknown>)
                  ?.end_loc as Location) || Location.SOUTH,
              startOrientation:
                ((step.redAttributes as Record<string, unknown>)
                  ?.startOrientation as Orientation) || Orientation.IN,
              endOrientation: (step.redAttributes as Record<string, unknown>)
                ?.endOrientation as Orientation, // Don't set default - let it be undefined
              rotationDirection:
                ((step.redAttributes as Record<string, unknown>)
                  ?.rotationDirection as RotationDirection) ||
                RotationDirection.NO_ROTATION,
              turns:
                ((step.redAttributes as Record<string, unknown>)
                  ?.turns as number) || 0,
              is_visible: true,
            },
          },
          letter: (step.letter as string) || "",
          beat: step.beat as number,
          isBlank: false,
          isMirrored: false,
          metadata: {},
        },
        metadata: {},
      }));

    console.log(`✅ Converted to web app format: ${beats.length} beats`);

    return {
      id,
      name: (meta.word as string) || id.toUpperCase(),
      word: (meta.word as string) || id.toUpperCase(),
      beats,
      thumbnails: [`${id.toUpperCase()}_ver1.png`],
      sequence_length: beats.length,
      author: (meta.author as string) || "Unknown",
      level: (meta.level as number) || 1,
      date_added: new Date((meta.date_added as string | number) || Date.now()),
      gridMode: (meta.gridMode as string) || "diamond",
      prop_type: (meta.prop_type as string) || "unknown",
      is_favorite: (meta.is_favorite as boolean) || false,
      is_circular: (meta.is_circular as boolean) || false,
      starting_position: (meta.sequence_start_position as string) || "beta",
      difficulty_level: this.mapLevelToDifficulty((meta.level as number) || 1),
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

  /**
   * Load sequence from PNG metadata or create fallback
   */
  private async createTestSequence(id: string): Promise<SequenceData> {
    console.log(`🎬 Loading sequence from PNG metadata for ID: ${id}`);

    // Try to load from PNG metadata first
    try {
      const sequenceData = await this.loadSequenceFromPNG(id);
      if (sequenceData) {
        console.log(`✅ Loaded real sequence data from PNG for ${id}`);
        return sequenceData;
      }
    } catch (error) {
      console.warn(`⚠️ Failed to load PNG metadata for ${id}:`, error);
    }

    // Fallback: Return error - no fake sequences
    throw new Error(
      `No PNG metadata found for sequence ${id}. Please ensure the sequence has a valid PNG thumbnail with embedded metadata.`
    );
  }
}
