/**
 * Sequence Persistence Service Contract
 * 
 * Service for managing sequence state persistence that survives hot module replacement.
 * This service ensures that sequence state is maintained during development and provides
 * smooth clear sequence functionality.
 */

import type { ActiveBuildTab, PictographData, SequenceData } from "$shared";

export interface ISequencePersistenceService {
  /**
   * Initialize the persistence service and restore any saved state
   */
  initialize(): Promise<void>;

  /**
   * Save the current sequence state for hot module replacement survival
   * @param state - Current sequence state to persist
   */
  saveCurrentState(state: {
    currentSequence: SequenceData | null;
    selectedStartPosition: PictographData | null;
    hasStartPosition: boolean;
    activeBuildSection: ActiveBuildTab;
  }): Promise<void>;

  /**
   * Load the current sequence state after hot module replacement
   * @returns Saved sequence state or null if none exists
   */
  loadCurrentState(): Promise<{
    currentSequence: SequenceData | null;
    selectedStartPosition: PictographData | null;
    hasStartPosition: boolean;
    activeBuildSection: ActiveBuildTab;
  } | null>;

  /**
   * Clear the current sequence state (for clear sequence functionality)
   */
  clearCurrentState(): Promise<void>;

  /**
   * Check if there is a saved sequence state
   * @returns True if there is a saved state that can be restored
   */
  hasSavedState(): Promise<boolean>;

  /**
   * Get the timestamp of the last saved state
   * @returns Timestamp of last save or null if no state exists
   */
  getLastSaveTimestamp(): Promise<number | null>;
}
