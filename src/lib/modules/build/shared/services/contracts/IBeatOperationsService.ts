/**
 * Beat Operations Service Contract
 * 
 * Handles all beat manipulation business logic for BuildTab sequence construction.
 * Manages beat removal, batch editing, undo snapshot creation, and beat selection logic.
 * 
 * Domain: Build Module - Beat Manipulation within Sequence Construction
 * Extracted from BuildTab.svelte to achieve Single Responsibility Principle.
 */

export interface IBeatOperationsService {
  /**
   * Remove a beat and all subsequent beats from the sequence
   * Handles special case of removing start position (clears entire sequence)
   * Creates undo snapshot and manages beat selection after removal
   * 
   * @param beatIndex Index of beat to remove (0 = start position)
   * @param buildTabState Build tab state for sequence and undo operations
   */
  removeBeat(beatIndex: number, buildTabState: any): void;

  /**
   * Apply batch changes to multiple selected beats
   * Creates undo snapshot before applying changes
   * 
   * @param changes Partial beat data to apply to all selected beats
   * @param buildTabState Build tab state for sequence operations
   */
  applyBatchChanges(changes: any, buildTabState: any): void;
}
