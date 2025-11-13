/**
 * Sequence Deletion Service
 *
 * Handles all deletion operations for sequences and sequence components.
 * Centralizes deletion logic for better consistency and maintainability.
 */

import type { SequenceData } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { ISequenceDeletionService } from "../contracts";

// Import from build shared contracts
import type {
  IPersistenceService,
  ISequenceService,
} from "../../../../shared/services/contracts";

@injectable()
export class SequenceDeletionService implements ISequenceDeletionService {
  constructor(
    @inject(TYPES.ISequenceService) private sequenceService: ISequenceService,
    @inject(TYPES.IPersistenceService)
    private persistenceService: IPersistenceService
  ) {}

  /**
   * Delete an entire sequence
   */
  async deleteSequence(sequenceId: string): Promise<void> {
    try {
      await this.persistenceService.deleteSequence(sequenceId);
    } catch (error) {
      console.error("Failed to delete sequence:", error);
      throw new Error(
        `Failed to delete sequence: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Remove a specific beat from a sequence and return updated sequence
   */
  async removeBeat(
    sequenceId: string,
    beatIndex: number
  ): Promise<SequenceData> {
    try {
      const sequence = await this.sequenceService.getSequence(sequenceId);
      if (!sequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }

      if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
        throw new Error(`Beat index ${beatIndex} is out of range`);
      }

      // Remove the beat and renumber remaining beats
      const newBeats = sequence.beats
        .filter((_, index) => index !== beatIndex)
        .map((beat, index) => ({ ...beat, beatNumber: index + 1 }));

      const updatedSequence = { ...sequence, beats: newBeats } as SequenceData;
      await this.persistenceService.saveSequence(updatedSequence);
      return updatedSequence;
    } catch (error) {
      console.error("Failed to remove beat:", error);
      throw new Error(
        `Failed to remove beat: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Clear all beats from a sequence, keeping the sequence structure
   */
  async clearSequenceBeats(sequenceId: string): Promise<SequenceData> {
    try {
      const sequence = await this.sequenceService.getSequence(sequenceId);
      if (!sequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }

      const updatedSequence = {
        ...sequence,
        beats: [],
      } as SequenceData;

      await this.persistenceService.saveSequence(updatedSequence);
      return updatedSequence;
    } catch (error) {
      console.error("Failed to clear sequence beats:", error);
      throw new Error(
        `Failed to clear beats: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Remove multiple beats from a sequence by indices
   */
  async removeBeats(
    sequenceId: string,
    beatIndices: number[]
  ): Promise<SequenceData> {
    try {
      const sequence = await this.sequenceService.getSequence(sequenceId);
      if (!sequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }

      // Sort indices in descending order to remove from end to beginning
      const sortedIndices = [...beatIndices].sort((a, b) => b - a);

      // Validate all indices
      for (const index of sortedIndices) {
        if (index < 0 || index >= sequence.beats.length) {
          throw new Error(`Beat index ${index} is out of range`);
        }
      }

      // Remove beats and renumber
      let newBeats = [...sequence.beats];
      for (const index of sortedIndices) {
        newBeats.splice(index, 1);
      }

      // Renumber remaining beats
      newBeats = newBeats.map((beat, index) => ({
        ...beat,
        beatNumber: index + 1,
      }));

      const updatedSequence = { ...sequence, beats: newBeats } as SequenceData;
      await this.persistenceService.saveSequence(updatedSequence);
      return updatedSequence;
    } catch (error) {
      console.error("Failed to remove beats:", error);
      throw new Error(
        `Failed to remove beats: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Remove all beats from a specific index onwards (like desktop app's "delete beat and following")
   */
  async removeBeatAndFollowing(
    sequenceId: string,
    startIndex: number
  ): Promise<SequenceData> {
    try {
      const sequence = await this.sequenceService.getSequence(sequenceId);
      if (!sequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }

      if (startIndex < 0 || startIndex >= sequence.beats.length) {
        throw new Error(`Start index ${startIndex} is out of range`);
      }

      // Keep only beats before the start index
      const newBeats = sequence.beats
        .slice(0, startIndex)
        .map((beat, index) => ({ ...beat, beatNumber: index + 1 }));

      const updatedSequence = { ...sequence, beats: newBeats } as SequenceData;
      await this.persistenceService.saveSequence(updatedSequence);
      return updatedSequence;
    } catch (error) {
      console.error("Failed to remove beat and following:", error);
      throw new Error(
        `Failed to remove beat and following: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
}
