/**
 * Pure Sequence State Service Implementation
 *
 * Extracted business logic from SequenceStateService.svelte.ts
 * Contains only pure functions with no reactive state.
 */

import type { ISequenceStateService } from "$contracts";
import type {
  BeatData,
  Letter,
  SequenceData,
  SequenceStatistics,
  ValidationResult,
} from "$domain";
import {
  addBeatToSequence,
  createSequenceData,
  removeBeatFromSequence,
  updateSequenceData,
} from "$domain";
import { injectable } from "inversify";
@injectable()
export class SequenceStateService implements ISequenceStateService {
  // ============================================================================
  // SEQUENCE MANAGEMENT
  // ============================================================================

  createNewSequence(name: string, length: number = 16): SequenceData {
    if (!name.trim()) {
      throw new Error("Sequence name is required");
    }

    if (length < 1 || length > 64) {
      throw new Error("Sequence length must be between 1 and 64 beats");
    }

    const beats: BeatData[] = Array.from({ length }, (_, i) => ({
      id: crypto.randomUUID(),
      beatNumber: i + 1,
      duration: 1.0,
      blueReversal: false,
      redReversal: false,
      isBlank: true,
      pictographData: null,
    }));

    return createSequenceData({
      name: name.trim(),
      beats,
    });
  }

  validateSequence(sequence: SequenceData): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Basic validation
    if (!sequence.name.trim()) {
      errors.push("Sequence name is required");
    }

    if (sequence.beats.length === 0) {
      warnings.push("Sequence has no beats");
    }

    if (sequence.beats.length > 64) {
      errors.push("Sequence cannot have more than 64 beats");
    }

    // Beat validation
    sequence.beats.forEach((beat, index) => {
      if (beat.beatNumber !== index + 1) {
        errors.push(
          `Beat ${index + 1} has incorrect beat number: ${beat.beatNumber}`
        );
      }

      if (beat.duration <= 0) {
        errors.push(`Beat ${index + 1} has invalid duration: ${beat.duration}`);
      }
    });

    return {
      isValid: errors.length === 0,
      errors: errors.map((err) => ({
        code: "VALIDATION_ERROR",
        message: err,
        severity: "error" as const,
      })),
      warnings: warnings.map((warn) => ({
        code: "VALIDATION_WARNING",
        message: warn,
      })),
    };
  }

  // ============================================================================
  // BEAT OPERATIONS
  // ============================================================================

  addBeat(sequence: SequenceData, beatData?: Partial<BeatData>): SequenceData {
    const nextBeatNumber = sequence.beats.length + 1;

    const newBeat: BeatData = {
      id: crypto.randomUUID(),
      beatNumber: nextBeatNumber,
      duration: 1.0,
      blueReversal: false,
      redReversal: false,
      isBlank: true,
      pictographData: null,
      ...beatData,
    };

    return addBeatToSequence(sequence, newBeat);
  }

  removeBeat(sequence: SequenceData, beatIndex: number): SequenceData {
    if (!this.isValidBeatIndex(sequence, beatIndex)) {
      return sequence;
    }

    const updatedSequence = removeBeatFromSequence(sequence, beatIndex);

    // Renumber remaining beats
    const renumberedBeats = updatedSequence.beats.map(
      (beat: any, index: number) => ({
        ...beat,
        beatNumber: index + 1,
      })
    );

    return updateSequenceData(updatedSequence, {
      beats: renumberedBeats,
    });
  }

  updateBeat(
    sequence: SequenceData,
    beatIndex: number,
    beatData: Partial<BeatData>
  ): SequenceData {
    if (!this.isValidBeatIndex(sequence, beatIndex)) {
      return sequence;
    }

    const updatedBeats = sequence.beats.map((beat, index) =>
      index === beatIndex ? { ...beat, ...beatData } : beat
    );

    return updateSequenceData(sequence, {
      beats: updatedBeats,
    });
  }

  insertBeat(
    sequence: SequenceData,
    beatIndex: number,
    beatData?: Partial<BeatData>
  ): SequenceData {
    if (beatIndex < 0 || beatIndex > sequence.beats.length) {
      return sequence;
    }

    const newBeat: BeatData = {
      id: crypto.randomUUID(),
      beatNumber: beatIndex + 1,
      duration: 1.0,
      blueReversal: false,
      redReversal: false,
      isBlank: true,
      pictographData: null,
      ...beatData,
    };

    const newBeats = [
      ...sequence.beats.slice(0, beatIndex),
      newBeat,
      ...sequence.beats.slice(beatIndex),
    ];

    // Renumber all beats
    const renumberedBeats = newBeats.map((beat, index) => ({
      ...beat,
      beatNumber: index + 1,
    }));

    return updateSequenceData(sequence, {
      beats: renumberedBeats,
    });
  }

  // ============================================================================
  // BEAT SELECTION HELPERS
  // ============================================================================

  isValidBeatIndex(sequence: SequenceData | null, beatIndex: number): boolean {
    if (!sequence) return false;
    return beatIndex >= 0 && beatIndex < sequence.beats.length;
  }

  getSelectedBeat(
    sequence: SequenceData | null,
    beatIndex: number
  ): BeatData | null {
    if (!this.isValidBeatIndex(sequence, beatIndex) || !sequence) {
      return null;
    }
    return sequence.beats[beatIndex];
  }

  // ============================================================================
  // SEQUENCE TRANSFORMATIONS
  // ============================================================================

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

  setStartPosition(
    sequence: SequenceData,
    startPosition: BeatData
  ): SequenceData {
    return updateSequenceData(sequence, {
      startingPositionBeat: startPosition,
    });
  }

  // ============================================================================
  // SEQUENCE OPERATIONS (Placeholder implementations)
  // ============================================================================

  mirrorSequence(sequence: SequenceData): SequenceData {
    // TODO: Implement mirroring logic based on pictograph data
    console.warn("mirrorSequence not yet implemented");
    return sequence;
  }

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

  rotateSequence(
    sequence: SequenceData,
    _direction: "clockwise" | "counterclockwise"
  ): SequenceData {
    // TODO: Implement rotation logic based on pictograph data
    console.warn("rotateSequence not yet implemented");
    return sequence;
  }

  // ============================================================================
  // VALIDATION AND UTILITIES
  // ============================================================================

  generateSequenceWord(sequence: SequenceData): string {
    // Extract letters from pictograph data
    const letters = sequence.beats
      .filter((beat) => beat.pictographData?.letter)
      .map((beat) => beat.pictographData?.letter)
      .filter((letter): letter is Letter => letter !== undefined)
      .join("");

    return letters || sequence.name;
  }

  calculateSequenceDuration(sequence: SequenceData): number {
    return sequence.beats.reduce((total, beat) => total + beat.duration, 0);
  }

  getSequenceStatistics(sequence: SequenceData): SequenceStatistics {
    const totalBeats = sequence.beats.length;
    const blankBeats = sequence.beats.filter((beat) => beat.isBlank).length;
    const filledBeats = totalBeats - blankBeats;
    const totalDuration = this.calculateSequenceDuration(sequence);
    const averageBeatDuration = totalBeats > 0 ? totalDuration / totalBeats : 0;

    const reversalCount = sequence.beats.reduce(
      (acc, beat) => ({
        blue: acc.blue + (beat.blueReversal ? 1 : 0),
        red: acc.red + (beat.redReversal ? 1 : 0),
      }),
      { blue: 0, red: 0 }
    );

    return {
      totalBeats,
      blankBeats,
      filledBeats,
      totalDuration,
      averageBeatDuration,
      hasStartPosition: !!sequence.startingPositionBeat,
      reversalCount,
    };
  }
}
