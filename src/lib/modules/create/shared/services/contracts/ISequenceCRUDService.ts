/**
 * Interface for sequence CRUD operations (Create, Read, Update, Delete)
 */
import type { BeatData, SequenceData } from "$shared";

export interface CreateSequenceRequest {
  name: string;
  length: number;
  word?: string;
}

export interface ISequenceCRUDService {
  /**
   * Create a new sequence
   */
  createSequence(request: CreateSequenceRequest): Promise<SequenceData>;

  /**
   * Update an entire sequence
   */
  updateSequence(sequence: SequenceData): Promise<SequenceData>;

  /**
   * Delete a sequence by ID
   */
  deleteSequence(id: string): Promise<void>;

  /**
   * Update a specific beat in a sequence
   */
  updateBeat(
    sequenceId: string,
    beatIndex: number,
    beat: BeatData
  ): Promise<void>;

  /**
   * Add a beat to a sequence
   */
  addBeat(sequenceId: string, beat: BeatData): Promise<void>;

  /**
   * Remove a beat from a sequence
   */
  removeBeat(sequenceId: string, beatIndex: number): Promise<void>;

  /**
   * Load all sequences
   */
  loadAllSequences(): Promise<SequenceData[]>;

  /**
   * Duplicate a sequence
   */
  duplicateSequence(sequence: SequenceData): Promise<SequenceData>;
}
