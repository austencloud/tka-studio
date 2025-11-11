/**
 * Sequence Transformation Service Interface
 *
 * Pure transformation functions for sequences.
 */

import type { SequenceData } from "$shared";

export interface ISequenceTransformationService {
  /**
   * Clear all beats in a sequence (make them blank)
   */
  clearSequence(sequence: SequenceData): SequenceData;

  /**
   * Duplicate a sequence with new IDs
   */
  duplicateSequence(sequence: SequenceData, newName?: string): SequenceData;

  /**
   * Mirror sequence (reverse movement and rotation patterns)
   */
  mirrorSequence(sequence: SequenceData): SequenceData;

  /**
   * Swap blue and red colors (reversal flags)
   */
  swapColors(sequence: SequenceData): SequenceData;

  /**
   * Rotate sequence positions
   */
  rotateSequence(sequence: SequenceData, rotationAmount: number): SequenceData;

  /**
   * Reverse sequence (play backwards)
   * - Creates new start position from final beat's end state
   * - Reverses beat order and transforms each beat
   * - Swaps positions, locations, orientations; flips rotation direction
   * - Looks up correct letters from pictograph dataset based on reversed motion configuration
   */
  reverseSequence(sequence: SequenceData): Promise<SequenceData>;
}
