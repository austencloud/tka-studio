/**
 * Sequence Domain Service Contract
 *
 * Service for sequence domain operations and business logic
 */

import type { BeatData, SequenceCreateRequest, SequenceData } from "$shared";

export interface ISequenceDomainService {
  /**
   * Validate a sequence according to business rules
   * @param sequence - Sequence to validate
   * @returns Validation result with errors and warnings
   */
  validateSequence(sequence: SequenceData): {
    isValid: boolean;
    errors: string[];
    warnings: string[];
  };

  /**
   * Calculate sequence statistics
   * @param sequence - Target sequence
   * @returns Statistics object
   */
  calculateStatistics(sequence: SequenceData): {
    totalBeats: number;
    filledBeats: number;
    emptyBeats: number;
    duration: number;
  };

  /**
   * Generate a word from sequence pictograph letters
   * @param sequence - Target sequence
   * @returns Generated word string
   */
  generateWord(sequence: SequenceData): string;

  /**
   * Check if a beat is valid for the sequence
   * @param sequence - Target sequence
   * @param beat - Beat to validate
   * @returns True if beat is valid
   */
  isValidBeat(sequence: SequenceData, beat: BeatData): boolean;

  /**
   * Create a new sequence from request
   * @param request - Sequence creation request
   * @returns New sequence data
   */
  createSequence(request: SequenceCreateRequest): SequenceData;

  /**
   * Update a beat in the sequence
   * @param sequence - Target sequence
   * @param beatIndex - Index of beat to update
   * @param beatData - New beat data
   * @returns Updated sequence
   */
  updateBeat(
    sequence: SequenceData,
    beatIndex: number,
    beatData: BeatData
  ): SequenceData;
}
