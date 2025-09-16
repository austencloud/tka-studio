/**
 * Reversal Detection Service Contract
 * 
 * Detects reversals between beats in sequences based on prop rotation direction changes.
 */

import type { BeatData, SequenceData } from "$shared";

export interface IReversalDetectionService {
  /**
   * Process a sequence and apply reversal detection to all beats
   * @param sequence The sequence to process
   * @returns The sequence with reversal flags applied to beats
   */
  processReversals(sequence: SequenceData): SequenceData;
}
