/**
 * Sequence Service - Application Layer
 *
 * Coordinates between domain logic and persistence for sequence operations.
 * This service orchestrates the business workflows for sequence management.
 */

import type { BeatData, SequenceData } from "$lib/domain";
import {
  Location,
  MotionType,
  Orientation,
  RotationDirection,
} from "$lib/domain/enums";
import { extractSequenceFromPNG } from "$lib/utils/png-parser.js";
import type {
  IBrowseService,
  IPersistenceService,
  ISequenceDomainService,
  ISequenceService,
  SequenceCreateRequest,
} from "../interfaces";

export class SequenceService implements ISequenceService {
  constructor(
    private sequenceDomainService: ISequenceDomainService,
    private persistenceService: IPersistenceService,
    private browseService: IBrowseService
  ) {}

  /**
   * Create a new sequence
   */
  async createSequence(request: SequenceCreateRequest): Promise<SequenceData> {
    try {
      console.log("Creating sequence:", request);

      // Use domain service to create the sequence
      const sequence = this.sequenceDomainService.createSequence(request);
      await this.persistenceService.saveSequence(sequence);
      console.log("Sequence created successfully:", sequence.id);
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
      console.log(`Updating beat ${beatIndex} in sequence ${sequenceId}`);

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

      console.log("Beat updated successfully");
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
      console.log(`Setting start position for sequence ${sequenceId}`);

      // Load the current sequence
      const currentSequence =
        await this.persistenceService.loadSequence(sequenceId);
      if (!currentSequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }

      // Update the sequence with the start position
      const updatedSequence = {
        ...currentSequence,
        start_position: startPosition,
      } as SequenceData;

      await this.persistenceService.saveSequence(updatedSequence);

      console.log("Start position set successfully");
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
      console.log(`Deleting sequence ${id}`);
      await this.persistenceService.deleteSequence(id);
      console.log("Sequence deleted successfully");
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
          sequence = await this.createTestSequence(id);
          // Save it to localStorage for future use
          await this.persistenceService.saveSequence(sequence);
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
        is_blank: true,
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

  /**
   * Load sequence data from PNG metadata
   */
  private async loadSequenceFromPNG(
    sequenceId: string
  ): Promise<SequenceData | null> {
    try {
      // Get the PNG file for this sequence
      const pngFile = await this.getPNGFileForSequence(sequenceId);
      if (!pngFile) {
        console.log(`No PNG file found for sequence ${sequenceId}`);
        return null;
      }

      // Extract sequence data from PNG metadata
      console.log(`🔍 Extracting metadata from PNG file for ${sequenceId}`);
      const result = await extractSequenceFromPNG(pngFile);
      if (result.success && result.data) {
        console.log(`✅ Successfully extracted PNG metadata for ${sequenceId}`);
        // Convert standalone format to web app format
        const webAppSequence = this.convertStandaloneToWebApp(
          result.data,
          sequenceId
        );
        return webAppSequence;
      } else {
        console.warn(`Failed to extract PNG metadata: ${result.error}`);
        return null;
      }
    } catch (error) {
      console.error(`Error loading PNG metadata for ${sequenceId}:`, error);
      return null;
    }
  }

  /**
   * Get PNG file for a sequence from thumbnail URL
   */
  private async getPNGFileForSequence(
    sequenceId: string
  ): Promise<File | null> {
    try {
      // First, get the sequence metadata to find the correct thumbnail path
      const allSequences = await this.browseService.loadSequenceMetadata();
      const sequenceMetadata = allSequences.find(
        (seq) => seq.id === sequenceId
      );

      if (!sequenceMetadata) {
        console.warn(`⚠️ Sequence ${sequenceId} not found in metadata index`);
        return null;
      }

      if (
        !sequenceMetadata.thumbnails ||
        sequenceMetadata.thumbnails.length === 0
      ) {
        console.warn(
          `⚠️ No thumbnail metadata found for sequence ${sequenceId}. Available metadata:`,
          sequenceMetadata
        );
        return null;
      }

      // Try each thumbnail URL from the metadata
      for (const thumbnailUrl of sequenceMetadata.thumbnails) {
        try {
          console.log(
            `🖼️ Trying to fetch PNG file from metadata: ${thumbnailUrl}`
          );

          // Fetch the PNG file
          const response = await fetch(thumbnailUrl);
          if (response.ok) {
            // Convert to File object
            const blob = await response.blob();
            const file = new File([blob], `${sequenceId}.png`, {
              type: "image/png",
            });

            console.log(
              `✅ Successfully loaded PNG file for ${sequenceId} from ${thumbnailUrl}, size: ${file.size} bytes`
            );
            return file;
          } else {
            console.log(
              `❌ Failed to fetch from ${thumbnailUrl}: ${response.status}`
            );
          }
        } catch (error) {
          console.log(`❌ Error fetching from ${thumbnailUrl}:`, error);

          // Provide specific error messages for different failure types
          if (
            error instanceof TypeError &&
            error.message.includes("Failed to fetch")
          ) {
            console.warn(
              `❌ Network error: PNG file may not exist at ${thumbnailUrl}`
            );
          } else {
            console.warn(`❌ Unknown error fetching PNG: ${error}`);
          }

          continue;
        }
      }

      console.warn(
        `⚠️ No PNG file found for sequence ${sequenceId} using metadata thumbnail paths`
      );
      return null;
    } catch (error) {
      console.error(`Error fetching PNG file for ${sequenceId}:`, error);
      return null;
    }
  }

  /**
   * Convert standalone format to web app format
   */
  private convertStandaloneToWebApp(
    standaloneData: any[],
    sequenceId: string
  ): SequenceData {
    console.log(
      `🔄 Converting standalone data to web app format for ${sequenceId}`
    );

    if (!Array.isArray(standaloneData) || standaloneData.length < 2) {
      throw new Error(
        "Invalid standalone data: must be array with metadata + beats"
      );
    }

    // First element is metadata
    const metadata = standaloneData[0];
    const word = metadata.word || sequenceId.toUpperCase();

    // Remaining elements are beats
    const beatElements = standaloneData.slice(1);
    const beats: BeatData[] = [];

    beatElements.forEach((beatData, index) => {
      // Skip start position elements
      if (beatData.sequence_start_position !== undefined) {
        return;
      }

      const beat: BeatData = {
        id: crypto.randomUUID(),
        beat_number: beatData.beat || index + 1,
        duration: 1.0,
        blue_reversal: false,
        red_reversal: false,
        is_blank: false,
        pictograph_data: {
          id: crypto.randomUUID(),
          letter: beatData.letter || "",
          end_pos: beatData.end_pos || "",
          timing: null,
          direction: null,
          grid_data: {} as any,
          arrows: {},
          props: {},
          beat: beatData.beat || index + 1,
          is_blank: false,
          is_mirrored: false,
          metadata: {},
          motions: {
            blue: this.convertMotionAttributes(beatData.blue_attributes),
            red: this.convertMotionAttributes(beatData.red_attributes),
          },
        },
        metadata: {},
      };

      beats.push(beat);
    });

    const sequence: SequenceData = {
      id: sequenceId,
      name: word,
      word: word,
      beats,
      thumbnails: [],
      is_favorite: false,
      is_circular: false,
      tags: ["imported", "animation"],
      metadata: {
        length: beats.length,
        author: metadata.author || "Unknown",
        level: metadata.level || 1,
        imported_from_png: true,
        created_at: new Date().toISOString(),
      },
    };

    console.log(`✅ Converted to web app format: ${beats.length} beats`);
    return sequence;
  }

  /**
   * Convert standalone motion attributes to web app motion format
   */
  private convertMotionAttributes(attributes: any): any {
    if (!attributes) {
      return {
        start_loc: Location.SOUTH,
        end_loc: Location.SOUTH,
        start_ori: Orientation.IN,
        end_ori: Orientation.IN,
        prop_rot_dir: RotationDirection.NO_ROTATION,
        turns: 0,
        motion_type: MotionType.STATIC,
        is_visible: true,
      };
    }

    return {
      start_loc: this.convertLocation(attributes.start_loc),
      end_loc: this.convertLocation(attributes.end_loc),
      start_ori: this.convertOrientation(attributes.start_ori),
      end_ori: this.convertOrientation(attributes.end_ori),
      prop_rot_dir: this.convertRotationDirection(attributes.prop_rot_dir),
      turns: attributes.turns || 0,
      motion_type: this.convertMotionType(attributes.motion_type),
      is_visible: true,
    };
  }

  private convertLocation(loc: string): Location {
    const locationMap: Record<string, Location> = {
      s: Location.SOUTH,
      n: Location.NORTH,
      e: Location.EAST,
      w: Location.WEST,
      center: Location.SOUTH, // Use SOUTH as default for center
      top: Location.NORTH,
      bottom: Location.SOUTH,
      left: Location.WEST,
      right: Location.EAST,
    };
    return locationMap[loc] || Location.SOUTH;
  }

  private convertOrientation(ori: string): Orientation {
    const orientationMap: Record<string, Orientation> = {
      in: Orientation.IN,
      out: Orientation.OUT,
    };
    return orientationMap[ori] || Orientation.IN;
  }

  private convertRotationDirection(dir: string): RotationDirection {
    const rotationMap: Record<string, RotationDirection> = {
      cw: RotationDirection.CLOCKWISE,
      ccw: RotationDirection.COUNTER_CLOCKWISE,
      no_rot: RotationDirection.NO_ROTATION,
    };
    return rotationMap[dir] || RotationDirection.NO_ROTATION;
  }

  private convertMotionType(type: string): MotionType {
    const motionMap: Record<string, MotionType> = {
      pro: MotionType.PRO,
      anti: MotionType.ANTI,
      static: MotionType.STATIC,
    };
    return motionMap[type] || MotionType.STATIC;
  }
}
