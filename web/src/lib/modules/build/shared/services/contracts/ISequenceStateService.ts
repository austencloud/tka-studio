/**
 * Sequence State Service Contract
 * 
 * Service for sequence state management and transformations
 */

import type { BeatData, SequenceData, ValidationResult } from "$shared";

export interface ISequenceStateService {
  // ============================================================================
  // SEQUENCE MANAGEMENT
  // ============================================================================

  /**
   * Create a new sequence with the specified name and length
   * @param name - Sequence name
   * @param length - Number of beats (default: 16)
   * @returns New sequence data
   */
  createNewSequence(name: string, length?: number): SequenceData;

  /**
   * Validate a sequence and return validation results
   * @param sequence - Sequence to validate
   * @returns Validation result with errors and warnings
   */
  validateSequence(sequence: SequenceData): ValidationResult;

  // ============================================================================
  // BEAT OPERATIONS
  // ============================================================================

  /**
   * Add a beat to the sequence
   * @param sequence - Target sequence
   * @param beatData - Optional beat data (defaults will be used if not provided)
   * @returns Updated sequence
   */
  addBeat(sequence: SequenceData, beatData?: Partial<BeatData>): SequenceData;

  /**
   * Remove a beat from the sequence
   * @param sequence - Target sequence
   * @param beatIndex - Index of beat to remove
   * @returns Updated sequence
   */
  removeBeat(sequence: SequenceData, beatIndex: number): SequenceData;

  // ============================================================================
  // BEAT SELECTION HELPERS
  // ============================================================================

  /**
   * Check if a beat index is valid for the sequence
   * @param sequence - Target sequence
   * @param beatIndex - Beat index to check
   * @returns True if index is valid
   */
  isValidBeatIndex(sequence: SequenceData | null, beatIndex: number): boolean;

  // ============================================================================
  // SEQUENCE TRANSFORMATIONS
  // ============================================================================

  /**
   * Clear all beats in the sequence
   * @param sequence - Target sequence
   * @returns Sequence with all beats cleared
   */
  clearSequence(sequence: SequenceData): SequenceData;

  /**
   * Duplicate a sequence with optional new name
   * @param sequence - Source sequence
   * @param newName - Optional new name (defaults to "Name (Copy)")
   * @returns Duplicated sequence
   */
  duplicateSequence(sequence: SequenceData, newName?: string): SequenceData;

  /**
   * Mirror the sequence by flipping movements
   * @param sequence - Target sequence
   * @returns Mirrored sequence
   */
  mirrorSequence(sequence: SequenceData): SequenceData;

  /**
   * Swap blue and red colors in the sequence
   * @param sequence - Target sequence
   * @returns Sequence with swapped colors
   */
  swapColors(sequence: SequenceData): SequenceData;

  // ============================================================================
  // VALIDATION AND UTILITIES
  // ============================================================================

  /**
   * Generate a word from the sequence's pictograph letters
   * @param sequence - Target sequence
   * @returns Generated word string
   */
  generateSequenceWord(sequence: SequenceData): string;

  /**
   * Calculate the total duration of the sequence
   * @param sequence - Target sequence
   * @returns Total duration in beats
   */
  calculateSequenceDuration(sequence: SequenceData): number;

  // ============================================================================
  // BEAT SELECTION AND RETRIEVAL
  // ============================================================================

  /**
   * Get the selected beat from a sequence
   * @param sequence - Target sequence
   * @param index - Beat index
   * @returns Selected beat data or null if not found
   */
  getSelectedBeat(sequence: SequenceData | null, index: number): BeatData | null;

  /**
   * Get sequence statistics
   * @param sequence - Target sequence
   * @returns Statistics object
   */
  getSequenceStatistics(sequence: SequenceData): {
    totalBeats: number;
    filledBeats: number;
    emptyBeats: number;
    duration: number;
  };

  /**
   * Apply reversal detection to an existing sequence
   * @param sequence - Target sequence
   * @returns Sequence with reversal data applied
   */
  applyReversalDetection(sequence: SequenceData): SequenceData;

  // ============================================================================
  // BEAT MANIPULATION
  // ============================================================================

  /**
   * Update a beat in the sequence
   * @param sequence - Target sequence
   * @param beatIndex - Index of beat to update
   * @param beatData - New beat data
   * @returns Updated sequence
   */
  updateBeat(sequence: SequenceData, beatIndex: number, beatData: BeatData): SequenceData;

  /**
   * Insert a beat at the specified position
   * @param sequence - Target sequence
   * @param beatIndex - Index where to insert the beat
   * @param beatData - Beat data to insert
   * @returns Updated sequence
   */
  insertBeat(sequence: SequenceData, beatIndex: number, beatData: BeatData): SequenceData;

  /**
   * Set the start position for the sequence
   * @param sequence - Target sequence
   * @param startPosition - Start position beat data
   * @returns Updated sequence
   */
  setStartPosition(sequence: SequenceData, startPosition: BeatData): SequenceData;

  /**
   * Rotate the sequence by the specified number of beats
   * @param sequence - Target sequence
   * @param rotationAmount - Number of beats to rotate (positive = right, negative = left)
   * @returns Rotated sequence
   */
  rotateSequence(sequence: SequenceData, rotationAmount: number): SequenceData;
}
