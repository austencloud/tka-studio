/**
 * Sequence Transformation Service
 *
 * Pure transformation functions for sequences.
 * All functions return new sequences without mutating inputs.
 *
 * Based on legacy desktop app implementation with modern TypeScript patterns.
 */

import type { BeatData, SequenceData } from "$shared";
import {
  createSequenceData,
  updateSequenceData,
  GridMode,
  MotionColor,
  RotationDirection,
} from "$shared";
import { injectable } from "inversify";
import { createBeatData } from "../../domain/factories/createBeatData";
import type { ISequenceTransformationService } from "../contracts/ISequenceTransformationService";
import {
  QUARTER_POSITION_MAP_CW,
  LOCATION_MAP_CLOCKWISE,
  VERTICAL_MIRROR_POSITION_MAP,
  VERTICAL_MIRROR_LOCATION_MAP,
  SWAPPED_POSITION_MAP,
} from "$create/generate/circular/domain/constants";

@injectable()
export class SequenceTransformationService implements ISequenceTransformationService {
  /**
   * Clear all beats in a sequence (make them blank)
   */
  clearSequence(sequence: SequenceData): SequenceData {
    const clearedBeats = sequence.beats.map((beat) => ({
      ...beat,
      isBlank: true,
      pictographData: null,
      blueReversal: false,
      redReversal: false,
    }));

    return updateSequenceData(sequence, {
      beats: clearedBeats,
    });
  }

  /**
   * Duplicate a sequence with new IDs
   */
  duplicateSequence(sequence: SequenceData, newName?: string): SequenceData {
    return createSequenceData({
      ...sequence,
      id: crypto.randomUUID(),
      name: newName || `${sequence.name} (Copy)`,
      beats: sequence.beats.map((beat) => ({
        ...beat,
        id: crypto.randomUUID(),
      })),
    });
  }

  /**
   * Mirror sequence vertically
   * - Mirrors all positions using vertical mirror map
   * - Mirrors all locations (flips east/west)
   * - Reverses rotation directions (cw ↔ ccw)
   * - Grid mode stays the same
   */
  mirrorSequence(sequence: SequenceData): SequenceData {
    const mirroredBeats = sequence.beats.map((beat) => this.mirrorBeat(beat));

    // Also mirror the start position if it exists
    const mirroredStartPosition = sequence.startPosition
      ? this.mirrorBeat(sequence.startPosition)
      : undefined;

    return updateSequenceData(sequence, {
      beats: mirroredBeats,
      ...(mirroredStartPosition && { startPosition: mirroredStartPosition }),
    });
  }

  /**
   * Mirror a single beat vertically
   */
  private mirrorBeat(beat: BeatData): BeatData {
    if (beat.isBlank || !beat) {
      return beat;
    }

    // Mirror positions (handle undefined as null)
    const mirroredStartPosition = beat.startPosition
      ? VERTICAL_MIRROR_POSITION_MAP[beat.startPosition]
      : (beat.startPosition ?? null);
    const mirroredEndPosition = beat.endPosition
      ? VERTICAL_MIRROR_POSITION_MAP[beat.endPosition]
      : (beat.endPosition ?? null);

    // Mirror motions
    const mirroredMotions = { ...beat.motions };

    // Mirror blue motion
    if (beat.motions[MotionColor.BLUE]) {
      const blueMotion = beat.motions[MotionColor.BLUE]!;
      mirroredMotions[MotionColor.BLUE] = {
        ...blueMotion,
        startLocation: VERTICAL_MIRROR_LOCATION_MAP[blueMotion.startLocation],
        endLocation: VERTICAL_MIRROR_LOCATION_MAP[blueMotion.endLocation],
        arrowLocation: VERTICAL_MIRROR_LOCATION_MAP[blueMotion.arrowLocation],
        rotationDirection: this.reverseRotationDirection(
          blueMotion.rotationDirection
        ),
      };
    }

    // Mirror red motion
    if (beat.motions[MotionColor.RED]) {
      const redMotion = beat.motions[MotionColor.RED]!;
      mirroredMotions[MotionColor.RED] = {
        ...redMotion,
        startLocation: VERTICAL_MIRROR_LOCATION_MAP[redMotion.startLocation],
        endLocation: VERTICAL_MIRROR_LOCATION_MAP[redMotion.endLocation],
        arrowLocation: VERTICAL_MIRROR_LOCATION_MAP[redMotion.arrowLocation],
        rotationDirection: this.reverseRotationDirection(
          redMotion.rotationDirection
        ),
      };
    }

    return createBeatData({
      ...beat,
      startPosition: mirroredStartPosition,
      endPosition: mirroredEndPosition,
      motions: mirroredMotions,
    });
  }

  /**
   * Reverse rotation direction (cw ↔ ccw, others stay same)
   */
  private reverseRotationDirection(
    direction: RotationDirection
  ): RotationDirection {
    if (direction === RotationDirection.CLOCKWISE) {
      return RotationDirection.COUNTER_CLOCKWISE;
    } else if (direction === RotationDirection.COUNTER_CLOCKWISE) {
      return RotationDirection.CLOCKWISE;
    }
    return direction; // NO_ROTATION stays the same
  }

  /**
   * Swap colors (blue ↔ red)
   * - Swaps entire blue and red motion data
   * - Swaps blue and red reversal states
   * - Updates positions based on swapped locations
   */
  swapColors(sequence: SequenceData): SequenceData {
    const swappedBeats = sequence.beats.map((beat) => this.colorSwapBeat(beat));

    // Also swap colors for the start position if it exists
    const swappedStartPosition = sequence.startPosition
      ? this.colorSwapBeat(sequence.startPosition)
      : undefined;

    return updateSequenceData(sequence, {
      beats: swappedBeats,
      ...(swappedStartPosition && { startPosition: swappedStartPosition }),
    });
  }

  /**
   * Color swap a single beat
   */
  private colorSwapBeat(beat: BeatData): BeatData {
    if (beat.isBlank || !beat) {
      return beat;
    }

    // Swap positions using swap position map (handle undefined as null)
    const swappedStartPosition = beat.startPosition
      ? SWAPPED_POSITION_MAP[beat.startPosition]
      : (beat.startPosition ?? null);
    const swappedEndPosition = beat.endPosition
      ? SWAPPED_POSITION_MAP[beat.endPosition]
      : (beat.endPosition ?? null);

    // Swap the motions
    const swappedMotions = {
      [MotionColor.BLUE]: beat.motions[MotionColor.RED],
      [MotionColor.RED]: beat.motions[MotionColor.BLUE],
    };

    // Update the color property in each motion to match the new color
    if (swappedMotions[MotionColor.BLUE]) {
      swappedMotions[MotionColor.BLUE] = {
        ...swappedMotions[MotionColor.BLUE]!,
        color: MotionColor.BLUE,
      };
    }
    if (swappedMotions[MotionColor.RED]) {
      swappedMotions[MotionColor.RED] = {
        ...swappedMotions[MotionColor.RED]!,
        color: MotionColor.RED,
      };
    }

    return createBeatData({
      ...beat,
      startPosition: swappedStartPosition,
      endPosition: swappedEndPosition,
      motions: swappedMotions,
      blueReversal: beat.redReversal,
      redReversal: beat.blueReversal,
    });
  }

  /**
   * Rotate sequence 90° clockwise
   * - Rotates all positions using quarter rotation map
   * - Rotates all locations clockwise
   * - Toggles grid mode (DIAMOND ↔ BOX)
   */
  rotateSequence(sequence: SequenceData, _rotationAmount: number): SequenceData {
    const rotatedBeats = sequence.beats.map((beat) => this.rotateBeat(beat));

    // Also rotate the start position if it exists
    const rotatedStartPosition = sequence.startPosition
      ? this.rotateBeat(sequence.startPosition)
      : undefined;

    // Toggle grid mode
    const newGridMode =
      sequence.gridMode === GridMode.DIAMOND ? GridMode.BOX : GridMode.DIAMOND;

    return updateSequenceData(sequence, {
      beats: rotatedBeats,
      ...(rotatedStartPosition && { startPosition: rotatedStartPosition }),
      gridMode: newGridMode,
    });
  }

  /**
   * Rotate a single beat 90° clockwise
   */
  private rotateBeat(beat: BeatData): BeatData {
    if (beat.isBlank || !beat) {
      return beat;
    }

    // Rotate positions (handle undefined as null)
    const rotatedStartPosition = beat.startPosition
      ? QUARTER_POSITION_MAP_CW[beat.startPosition]
      : (beat.startPosition ?? null);
    const rotatedEndPosition = beat.endPosition
      ? QUARTER_POSITION_MAP_CW[beat.endPosition]
      : (beat.endPosition ?? null);

    // Rotate motions
    const rotatedMotions = { ...beat.motions };

    // Rotate blue motion
    if (beat.motions[MotionColor.BLUE]) {
      const blueMotion = beat.motions[MotionColor.BLUE]!;
      rotatedMotions[MotionColor.BLUE] = {
        ...blueMotion,
        startLocation: LOCATION_MAP_CLOCKWISE[blueMotion.startLocation],
        endLocation: LOCATION_MAP_CLOCKWISE[blueMotion.endLocation],
        arrowLocation: LOCATION_MAP_CLOCKWISE[blueMotion.arrowLocation],
      };
    }

    // Rotate red motion
    if (beat.motions[MotionColor.RED]) {
      const redMotion = beat.motions[MotionColor.RED]!;
      rotatedMotions[MotionColor.RED] = {
        ...redMotion,
        startLocation: LOCATION_MAP_CLOCKWISE[redMotion.startLocation],
        endLocation: LOCATION_MAP_CLOCKWISE[redMotion.endLocation],
        arrowLocation: LOCATION_MAP_CLOCKWISE[redMotion.arrowLocation],
      };
    }

    return createBeatData({
      ...beat,
      startPosition: rotatedStartPosition,
      endPosition: rotatedEndPosition,
      motions: rotatedMotions,
    });
  }

  /**
   * Reverse beat order
   */
  reverseSequence(sequence: SequenceData): SequenceData {
    const reversedBeats = [...sequence.beats].reverse();
    
    // Renumber beats after reversing
    const renumberedBeats = reversedBeats.map((beat, index) => ({
      ...beat,
      beatNumber: index + 1,
    }));

    return updateSequenceData(sequence, {
      beats: renumberedBeats,
      name: `${sequence.name} (Reversed)`,
    });
  }
}
