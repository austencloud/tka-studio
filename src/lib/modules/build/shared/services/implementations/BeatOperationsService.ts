/**
 * Beat Operations Service Implementation
 *
 * Handles all beat manipulation business logic extracted from BuildTab.svelte.
 * Manages beat removal, batch editing, individual beat mutations, undo snapshots, and beat selection.
 *
 * Domain: Build Module - Beat Manipulation for Sequence Construction
 * Achieves Single Responsibility Principle by centralizing beat operation logic.
 */

import { createComponentLogger, resolve, TYPES, createMotionData, MotionColor } from "$shared";
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
    console.log(`🎨 BeatOperationsService.updateBeatOrientation called:`, {
      beatNumber,
      color,
      orientation,
      hasBuildTabState: !!buildTabState,
      hasPanelState: !!panelState
    });

    if (!buildTabState) {
      this.logger.warn("Cannot update orientation - state not initialized");
      return;
    }

    // Get beat data from LIVE sequence state, not the snapshot!
    let beatData;
    if (beatNumber === START_POSITION_BEAT_NUMBER) {
      beatData = buildTabState.sequenceState.selectedStartPosition;
    } else {
      const arrayIndex = beatNumber - 1;
      const sequence = buildTabState.sequenceState.currentSequence;
      beatData = sequence?.beats?.[arrayIndex];
    }

    console.log(`  Beat data from live state:`, beatData);

    if (!beatData) {
      this.logger.warn("Cannot update orientation - no beat data available");
      return;
    }

    // Get current motion data for the color
    const currentMotion = beatData.motions?.[color] || {};

    // Create updated beat data with new startOrientation
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

    // Recalculate endOrientation for this beat based on its turns/motion type
    const orientationCalculator = resolve<IOrientationCalculator>(TYPES.IOrientationCalculationService);
    const updatedMotion = updatedBeatData.motions[color];

    if (updatedMotion) {
      const tempMotionData = createMotionData({
        ...updatedMotion,
        startOrientation: orientation,  // Use the new orientation
      });

      const newEndOrientation = orientationCalculator.calculateEndOrientation(
        tempMotionData,
        color as MotionColor
      );

      // Update the endOrientation
      updatedBeatData.motions[color] = {
        ...updatedMotion,
        endOrientation: newEndOrientation,
      };
    }

    // Apply update based on beat number
    if (beatNumber === START_POSITION_BEAT_NUMBER) {
      buildTabState.sequenceState.setStartPosition(updatedBeatData);
      this.logger.log(`Updated start position ${color} orientation to ${orientation}, endOrientation to ${updatedBeatData.motions[color]?.endOrientation}`);

      // Propagate orientation changes through the entire sequence
      this.propagateOrientationsThroughSequence(beatNumber, color, buildTabState);
    } else {
      const arrayIndex = beatNumber - 1; // Beat numbers 1, 2, 3... map to array indices 0, 1, 2...
      buildTabState.sequenceState.updateBeat(arrayIndex, updatedBeatData);
      this.logger.log(`Updated beat ${beatNumber} ${color} orientation to ${orientation}, endOrientation to ${updatedBeatData.motions[color]?.endOrientation}`);

      // Propagate orientation changes through the subsequent beats
      this.propagateOrientationsThroughSequence(beatNumber, color, buildTabState);
    }
  }

  /**
   * Propagates orientation changes through the entire sequence
   * Each beat's startOrientation becomes the previous beat's endOrientation
   * Each beat's endOrientation is recalculated based on its motion properties
   */
  private propagateOrientationsThroughSequence(
    startingBeatNumber: number,
    color: string,
    buildTabState: any
  ): void {
    const currentSequence = buildTabState.sequenceState.currentSequence;
    const startPosition = buildTabState.sequenceState.selectedStartPosition;

    if (!currentSequence || !currentSequence.beats || currentSequence.beats.length === 0) {
      this.logger.log("No sequence beats to propagate through");
      return;
    }

    const orientationCalculator = resolve<IOrientationCalculator>(TYPES.IOrientationCalculationService);

    // Get the starting beat's endOrientation
    let previousEndOrientation: string | undefined;

    if (startingBeatNumber === START_POSITION_BEAT_NUMBER) {
      // Starting from beat 0 (start position)
      previousEndOrientation = startPosition?.motions?.[color]?.endOrientation;
    } else {
      // Starting from a regular beat
      const arrayIndex = startingBeatNumber - 1;
      const startingBeat = currentSequence.beats[arrayIndex];
      previousEndOrientation = startingBeat?.motions?.[color]?.endOrientation;
    }

    if (!previousEndOrientation) {
      this.logger.warn(`Cannot propagate - no endOrientation found for beat ${startingBeatNumber} ${color}`);
      return;
    }

    // Propagate through subsequent beats
    const updatedBeats = [...currentSequence.beats];
    let propagationStartIndex = startingBeatNumber === START_POSITION_BEAT_NUMBER ? 0 : startingBeatNumber;

    this.logger.log(`🔄 Propagating ${color} orientations starting from beat ${startingBeatNumber} (endOrientation: ${previousEndOrientation})`);

    for (let i = propagationStartIndex; i < updatedBeats.length; i++) {
      const beat = updatedBeats[i];
      const beatMotion = beat.motions?.[color];

      if (!beatMotion) {
        this.logger.warn(`No motion data for ${color} at beat ${i + 1}, stopping propagation`);
        break;
      }

      // Update this beat's startOrientation from previous beat's endOrientation
      const updatedMotion = {
        ...beatMotion,
        startOrientation: previousEndOrientation,
      };

      // Recalculate this beat's endOrientation
      const tempMotionData = createMotionData({
        ...updatedMotion,
      });

      const newEndOrientation = orientationCalculator.calculateEndOrientation(
        tempMotionData,
        color as MotionColor
      );

      updatedMotion.endOrientation = newEndOrientation;

      // Update the beat
      updatedBeats[i] = {
        ...beat,
        motions: {
          ...beat.motions,
          [color]: updatedMotion,
        }
      };

      this.logger.log(`  ✓ Beat ${i + 1}: startOri=${previousEndOrientation} → endOri=${newEndOrientation}`);

      // This beat's endOrientation becomes the next beat's startOrientation
      previousEndOrientation = newEndOrientation;
    }

    // Update the sequence with all propagated beats
    const updatedSequence = {
      ...currentSequence,
      beats: updatedBeats,
    };

    buildTabState.sequenceState.setCurrentSequence(updatedSequence);
    this.logger.success(`✅ Propagated ${color} orientations through ${updatedBeats.length - propagationStartIndex} beats`);
  }

  updateBeatTurns(
    beatNumber: number,
    color: string,
    turnAmount: number,
    buildTabState: any,
    panelState: any
  ): void {
    if (!buildTabState) {
      this.logger.warn("Cannot update turns - state not initialized");
      return;
    }

    // Get beat data from LIVE sequence state, not the snapshot!
    let beatData;
    if (beatNumber === START_POSITION_BEAT_NUMBER) {
      beatData = buildTabState.sequenceState.selectedStartPosition;
    } else {
      const arrayIndex = beatNumber - 1;
      const sequence = buildTabState.sequenceState.currentSequence;
      beatData = sequence?.beats?.[arrayIndex];
    }

    if (!beatData) {
      this.logger.warn("Cannot update turns - no beat data available");
      return;
    }

    // Get current motion data for the color
    const currentMotion = beatData.motions?.[color] || {};

    // CRITICAL: Auto-assign rotation direction for DASH/STATIC motions (legacy behavior)
    // This matches legacy json_turns_updater.py lines 43-47 and 67-70
    let updatedRotationDirection = currentMotion.rotationDirection;
    const motionType = currentMotion.motionType;
    const isDashOrStatic = motionType === 'dash' || motionType === 'static';

    if (isDashOrStatic) {
      if (turnAmount > 0 && currentMotion.rotationDirection === 'noRotation') {
        // Auto-assign CLOCKWISE when applying non-zero turns to dash/static with no rotation
        updatedRotationDirection = 'cw';
        this.logger.log(`Auto-assigned CLOCKWISE rotation to ${motionType} motion with ${turnAmount} turns`);
      } else if (turnAmount === 0) {
        // Reset to NO_ROTATION when turns are set to 0
        updatedRotationDirection = 'noRotation';
      }
    }

    // Recalculate endOrientation based on new turn amount and updated rotation direction
    const orientationCalculator = resolve<IOrientationCalculator>(TYPES.IOrientationCalculationService);
    const tempMotionData = createMotionData({
      ...currentMotion,
      turns: turnAmount,  // Use new turn value for calculation
      rotationDirection: updatedRotationDirection,  // Use updated rotation direction
    });
    const newEndOrientation = orientationCalculator.calculateEndOrientation(
      tempMotionData,
      color as MotionColor
    );

    // Create updated beat data with new turn amount, rotation direction, AND recalculated endOrientation
    const updatedBeatData = {
      ...beatData,
      motions: {
        ...beatData.motions,
        [color]: {
          ...currentMotion,
          turns: turnAmount,
          rotationDirection: updatedRotationDirection,  // Include updated rotation direction
          endOrientation: newEndOrientation,  // Update endOrientation so prop rotates correctly
        }
      }
    };

    // Apply update based on beat number
    if (beatNumber === START_POSITION_BEAT_NUMBER) {
      buildTabState.sequenceState.setStartPosition(updatedBeatData);
      this.logger.log(`Updated start position ${color} turns to ${turnAmount} (rotationDirection: ${updatedRotationDirection}, endOrientation: ${newEndOrientation})`);

      // Propagate orientation changes through the entire sequence
      this.propagateOrientationsThroughSequence(beatNumber, color, buildTabState);
    } else {
      const arrayIndex = beatNumber - 1; // Beat numbers 1, 2, 3... map to array indices 0, 1, 2...
      buildTabState.sequenceState.updateBeat(arrayIndex, updatedBeatData);
      this.logger.log(`Updated beat ${beatNumber} ${color} turns to ${turnAmount} (rotationDirection: ${updatedRotationDirection}, endOrientation: ${newEndOrientation})`);

      // Propagate orientation changes through the subsequent beats
      this.propagateOrientationsThroughSequence(beatNumber, color, buildTabState);
    }
  }
}
