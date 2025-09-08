/**
 * Sequence Transform Service
 *
 * Handles sequence transformation operations like mirror, rotate, and swap colors.
 * Pure business logic with no side effects - transforms sequence data only.
 */

import type { SequenceData } from "$shared";
import {
  createSequenceData,
  updateSequenceData,
} from "$shared";
import { injectable } from "inversify";
import type { ISequenceTransformService } from "../contracts";
import { createBeatData } from "../../../shared";

@injectable()
export class SequenceTransformService implements ISequenceTransformService {
  /**
   * Mirror a sequence by flipping movement and rotation values
   */
  mirrorSequence(sequence: SequenceData): SequenceData {
    // Mirror the sequence by flipping movement and rotation values
    const mirroredBeats = sequence.beats.map((beat) => {
      if (beat.isBlank || !beat.pictographData) {
        return beat;
      }

      // Create mirrored pictograph data
      // This is a simplified implementation - full mirroring would need
      // to reverse specific movement and rotation patterns
      const mirroredPictographData = {
        ...beat.pictographData,
        // TODO: Implement specific mirroring transformations based on movement types
        // For now, we'll just mark it as mirrored
      };

      return createBeatData({
        ...beat,
        pictographData: mirroredPictographData,
      });
    });

    return {
      ...sequence,
      beats: mirroredBeats,
      name: `${sequence.name} (Mirrored)`,
    };
  }

  /**
   * Swap red and blue color reversals in a sequence
   */
  swapColors(sequence: SequenceData): SequenceData {
    const swappedBeats = sequence.beats.map((beat) => ({
      ...beat,
      blueReversal: beat.redReversal,
      redReversal: beat.blueReversal,
    }));

    return updateSequenceData(sequence, {
      beats: swappedBeats,
    });
  }

  /**
   * Rotate a sequence clockwise or counterclockwise
   */
  rotateSequence(
    sequence: SequenceData,
    _direction: "clockwise" | "counterclockwise"
  ): SequenceData {
    // TODO: Implement rotation logic based on pictograph data
    console.warn("rotateSequence not yet implemented");
    return sequence;
  }

  /**
   * Clear all beats in a sequence, making them blank
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
      startingPositionBeat: undefined,
    });
  }

  /**
   * Duplicate a sequence with a new ID and optional new name
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
}
