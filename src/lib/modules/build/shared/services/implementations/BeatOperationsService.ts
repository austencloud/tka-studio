/**
 * Beat Operations Service Implementation
 * 
 * Handles all beat manipulation business logic extracted from BuildTab.svelte.
 * Manages beat removal, batch editing, undo snapshots, and beat selection.
 * 
 * Domain: Build Module - Beat Manipulation for Sequence Construction
 * Achieves Single Responsibility Principle by centralizing beat operation logic.
 */

import { injectable } from "inversify";
import { createComponentLogger } from "$shared";
import type { IBeatOperationsService } from "../contracts/IBeatOperationsService";

@injectable()
export class BeatOperationsService implements IBeatOperationsService {
  private logger = createComponentLogger('BeatOperations');

  removeBeat(beatIndex: number, buildTabState: any): void {
    if (!buildTabState) {
      console.warn("BeatOperations: Cannot remove beat - build tab state not initialized");
      return;
    }

    const selectedBeat = buildTabState.sequenceState.selectedBeatData;

    // Special case: Removing start position (beatNumber === 0) clears entire sequence
    if (selectedBeat && selectedBeat.beatNumber === 0) {
      this.logger.log('Removing start position - clearing entire sequence');
      
      buildTabState.pushUndoSnapshot('CLEAR_SEQUENCE', {
        description: 'Clear sequence (removed start position)'
      });
      
      buildTabState.sequenceState.clearSequenceCompletely();
      buildTabState.setactiveToolPanel("construct");
      return;
    }

    // Calculate how many beats will be removed (beat at index + all subsequent)
    const currentSequence = buildTabState.sequenceState.currentSequence;
    const beatsToRemove = currentSequence ? currentSequence.beats.length - beatIndex : 0;

    this.logger.log(`Removing beat ${beatIndex} and ${beatsToRemove - 1} subsequent beats`);

    // Push undo snapshot before removal
    buildTabState.pushUndoSnapshot('REMOVE_BEATS', {
      beatIndex,
      beatsRemoved: beatsToRemove,
      description: `Remove beat ${beatIndex} and ${beatsToRemove - 1} subsequent beats`
    });

    // Remove the beat and all subsequent beats with staggered animation
    buildTabState.sequenceState.removeBeatAndSubsequentWithAnimation(beatIndex, () => {
      // After animation completes, select appropriate beat
      if (beatIndex > 0) {
        // Select the previous beat (array index beatIndex-1 has beatNumber beatIndex)
        buildTabState.sequenceState.selectBeat(beatIndex);
      } else {
        // If removing beat 0 (first beat after start), select start position
        buildTabState.sequenceState.selectStartPositionForEditing();
      }
    });
  }

  applyBatchChanges(changes: any, buildTabState: any): void {
    if (!buildTabState) {
      console.warn("BeatOperations: Cannot apply batch changes - build tab state not initialized");
      return;
    }

    const selectedBeatNumbers = buildTabState.sequenceState.selectedBeatNumbers;
    if (!selectedBeatNumbers || selectedBeatNumbers.size === 0) {
      this.logger.warn('No beats selected for batch edit');
      return;
    }

    this.logger.log(`Applying batch changes to ${selectedBeatNumbers.size} beats`, changes);

    // Push undo snapshot before batch edit
    buildTabState.pushUndoSnapshot('BATCH_EDIT', {
      beatNumbers: Array.from(selectedBeatNumbers),
      changes,
      description: `Batch edit ${selectedBeatNumbers.size} beats`
    });

    // Apply changes via sequence state
    buildTabState.sequenceState.applyBatchChanges(changes);

    this.logger.success(`Applied batch changes to ${selectedBeatNumbers.size} beats`);
  }
}
