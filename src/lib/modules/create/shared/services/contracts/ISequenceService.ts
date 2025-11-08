/**
 * Sequence Service Contract
 *
 * Core service for sequence CRUD operations
 */

import type { BeatData, SequenceData, SequenceCreateRequest } from "$shared";

export interface ISequenceService {
  /**
   * Create a new sequence
   * @param request - Sequence creation request
   * @returns Promise resolving to created sequence data
   */
  createSequence(request: SequenceCreateRequest): Promise<SequenceData>;

  /**
   * Update a beat in a sequence
   * @param sequenceId - Sequence identifier
   * @param beatIndex - Beat index to update
   * @param beatData - New beat data
   * @returns Promise that resolves when update is complete
   */
  updateBeat(
    sequenceId: string,
    beatIndex: number,
    beatData: BeatData
  ): Promise<void>;

  /**
   * Get a sequence by ID
   * @param id - Sequence identifier
   * @returns Promise resolving to sequence data or null if not found
   */
  getSequence(id: string): Promise<SequenceData | null>;

  /**
   * Get all sequences
   * @returns Promise resolving to array of all sequences
   */
  getAllSequences(): Promise<SequenceData[]>;
}
