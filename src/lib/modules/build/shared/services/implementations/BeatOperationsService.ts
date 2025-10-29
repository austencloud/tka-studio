/**
 * Beat Operations Service Implementation
 *
 * Handles all beat manipulation business logic extracted from BuildTab.svelte.
 * Manages beat removal, batch editing, individual beat mutations, undo snapshots, and beat selection.
 *
 * Domain: Build Module - Beat Manipulation for Sequence Construction
 * Achieves Single Responsibility Principle by centralizing beat operation logic.
 */

import { createComponentLogger, resolve, TYPES, createMotionData } from "$shared";
import { injectable } from "inversify";
import type { IBeatOperationsService } from "../contracts/IBeatOperationsService";
import type { IOrientationCalculator } from "$shared/pictograph/prop/services/contracts/IOrientationCalculationService";

const START_POSITION_BEAT_NUMBER = 0; // Beat 0 = start position, beats 1+ are in the sequence

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

  updateBeatOrientation(
    beatNumber: number,
    color: string,
    orientation: string,
    buildTabState: any,
    panelState: any
  ): void {
    if (!buildTabState || !panelState) {
      this.logger.warn("Cannot update orientation - state not initialized");
      return;
    }

    const beatData = panelState.editPanelBeatData;

    if (!beatData) {
      this.logger.warn("Cannot update orientation - no beat data available");
      return;
    }

    // Get current motion data for the color
    const currentMotion = beatData.motions?.[color] || {};

    // Create updated beat data with new orientation
    const updatedBeatData = {
      ...beatData,
      motions: {
        ...beatData.motions,
        [color]: {
          ...currentMotion,
          startOrientation: orientation,
        }
      }
    };

    // Apply update based on beat number
    if (beatNumber === START_POSITION_BEAT_NUMBER) {
      buildTabState.sequenceState.setStartPosition(updatedBeatData);
      this.logger.log(`Updated start position ${color} orientation to ${orientation}`);
    } else {
      const arrayIndex = beatNumber - 1; // Beat numbers 1, 2, 3... map to array indices 0, 1, 2...
      buildTabState.sequenceState.updateBeat(arrayIndex, updatedBeatData);
      this.logger.log(`Updated beat ${beatNumber} ${color} orientation to ${orientation}`);
    }
  }

  updateBeatTurns(
    beatNumber: number,
    color: string,
    turnAmount: number,
    buildTabState: any,
    panelState: any
  ): void {
    if (!buildTabState || !panelState) {
      this.logger.warn("Cannot update turns - state not initialized");
      return;
    }

    const beatData = panelState.editPanelBeatData;

    if (!beatData) {
      this.logger.warn("Cannot update turns - no beat data available");
      return;
    }

    // Get current motion data for the color
    const currentMotion = beatData.motions?.[color] || {};

    // Recalculate endOrientation based on new turn amount
    const orientationCalculator = resolve<IOrientationCalculator>(TYPES.IOrientationCalculationService);
    const tempMotionData = createMotionData({
      ...currentMotion,
      turns: turnAmount,  // Use new turn value for calculation
    });
    const newEndOrientation = orientationCalculator.calculateEndOrientation(
      tempMotionData,
      currentMotion.startOrientation
    );

    // Create updated beat data with new turn amount AND recalculated endOrientation
    const updatedBeatData = {
      ...beatData,
      motions: {
        ...beatData.motions,
        [color]: {
          ...currentMotion,
          turns: turnAmount,
          endOrientation: newEndOrientation,  // Update endOrientation so prop rotates correctly
        }
      }
    };

    // Apply update based on beat number
    if (beatNumber === START_POSITION_BEAT_NUMBER) {
      buildTabState.sequenceState.setStartPosition(updatedBeatData);
      this.logger.log(`Updated start position ${color} turns to ${turnAmount} (endOrientation: ${newEndOrientation})`);
    } else {
      const arrayIndex = beatNumber - 1; // Beat numbers 1, 2, 3... map to array indices 0, 1, 2...
      buildTabState.sequenceState.updateBeat(arrayIndex, updatedBeatData);
      this.logger.log(`Updated beat ${beatNumber} ${color} turns to ${turnAmount} (endOrientation: ${newEndOrientation})`);
    }
  }
}
