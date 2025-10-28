/**
 * Beat Operations Service Contract
 *
 * Handles all beat manipulation business logic for BuildTab sequence construction.
 * Manages beat removal, batch editing, individual beat mutations, undo snapshots, and beat selection logic.
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

  /**
   * Update orientation for a specific prop color in a beat
   * Handles both start position (beat 0) and sequence beats
   *
   * @param beatNumber Beat number (0 = start position, 1+ = sequence beats)
   * @param color Prop color ('blue' or 'red')
   * @param orientation New orientation value
   * @param buildTabState Build tab state for sequence operations
   * @param panelState Panel state for current beat data
   */
  updateBeatOrientation(
    beatNumber: number,
    color: string,
    orientation: string,
    buildTabState: any,
    panelState: any
  ): void;

  /**
   * Update turn amount for a specific prop color in a beat
   * Handles both start position (beat 0) and sequence beats
   *
   * @param beatNumber Beat number (0 = start position, 1+ = sequence beats)
   * @param color Prop color ('blue' or 'red')
   * @param turnAmount New turn amount value
   * @param buildTabState Build tab state for sequence operations
   * @param panelState Panel state for current beat data
   */
  updateBeatTurns(
    beatNumber: number,
    color: string,
    turnAmount: number,
    buildTabState: any,
    panelState: any
  ): void;
}
