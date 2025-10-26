/**
 * Sequence Transform Service Contract
 * 
 * Defines interface for sequence transformation operations like mirror, rotate, and swap colors.
 * These operations transform sequence data without side effects.
 */

import type { SequenceData } from "$shared";

export interface ISequenceTransformService {
  /**
   * Mirror a sequence by flipping movement and rotation values
   * @param sequence - The sequence to mirror
   * @returns New sequence with mirrored transformations
   */
  mirrorSequence(sequence: SequenceData): SequenceData;

  /**
   * Swap red and blue color reversals in a sequence
   * @param sequence - The sequence to transform
   * @returns New sequence with swapped colors
   */
  swapColors(sequence: SequenceData): SequenceData;

  /**
   * Rotate a sequence clockwise or counterclockwise
   * @param sequence - The sequence to rotate
   * @param direction - Direction of rotation
   * @returns New sequence with rotated transformations
   */
  rotateSequence(
    sequence: SequenceData,
    direction: "clockwise" | "counterclockwise"
  ): SequenceData;

  /**
   * Clear all beats in a sequence, making them blank
   * @param sequence - The sequence to clear
   * @returns New sequence with all beats cleared
   */
  clearSequence(sequence: SequenceData): SequenceData;

  /**
   * Duplicate a sequence with a new ID and optional new name
   * @param sequence - The sequence to duplicate
   * @param newName - Optional new name for the duplicated sequence
   * @returns New sequence that is a copy of the original
   */
  duplicateSequence(sequence: SequenceData, newName?: string): SequenceData;
}
