/**
 * Sequence Deletion Service Contract
 * 
 * Defines interface for sequence and beat deletion operations.
 * These operations handle removing sequences and beats with proper cleanup.
 */

import type { SequenceData } from "$shared";

export interface ISequenceDeletionService {
  /**
   * Delete an entire sequence
   * @param sequenceId - ID of the sequence to delete
   */
  deleteSequence(sequenceId: string): Promise<void>;

  /**
   * Remove a specific beat from a sequence
   * @param sequenceId - ID of the sequence
   * @param beatIndex - Index of the beat to remove
   * @returns Updated sequence data
   */
  removeBeat(sequenceId: string, beatIndex: number): Promise<SequenceData>;

  /**
   * Clear all beats in a sequence (make them blank)
   * @param sequenceId - ID of the sequence
   * @returns Updated sequence data with cleared beats
   */
  clearSequenceBeats(sequenceId: string): Promise<SequenceData>;

  /**
   * Remove multiple beats from a sequence
   * @param sequenceId - ID of the sequence
   * @param beatIndices - Array of beat indices to remove
   * @returns Updated sequence data
   */
  removeBeats(sequenceId: string, beatIndices: number[]): Promise<SequenceData>;

  /**
   * Remove a beat and all following beats
   * @param sequenceId - ID of the sequence
   * @param startIndex - Index to start removing from
   * @returns Updated sequence data
   */
  removeBeatAndFollowing(
    sequenceId: string,
    startIndex: number
  ): Promise<SequenceData>;
}
