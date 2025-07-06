/**
 * Sequence Domain Models for TKA
 *
 * Pure business data for beats and sequences.
 * No UI dependencies, completely immutable.
 *
 * Source: src/desktop/modern/src/domain/models/core_models.py (BeatData, SequenceData)
 */

import type { MotionData, GlyphData } from "./core.js";

// ============================================================================
// INTERFACES
// ============================================================================

/**
 * Pure business data for a single beat in a sequence.
 * Replaces Beat class with UI coupling.
 * No UI dependencies, completely immutable.
 */
export interface BeatData {
  // Core identity
  id: string;
  beat_number: number;

  // Business data
  letter?: string | null;
  duration: number;

  // Motion data (replaces complex dictionaries)
  blue_motion?: MotionData | null;
  red_motion?: MotionData | null;

  // Glyph data
  glyph_data?: GlyphData | null;

  // State flags
  blue_reversal: boolean;
  red_reversal: boolean;
  is_blank: boolean;

  // Metadata
  metadata: Record<string, any>;
}

/**
 * Pure business data for a complete kinetic sequence.
 * Replaces complex sequence management with UI coupling.
 * No UI dependencies, completely immutable.
 */
export interface SequenceData {
  // Core identity
  id: string;
  name: string;
  word: string; // Generated word from sequence

  // Business data
  beats: BeatData[];
  start_position?: string | null; // Simplified for now

  // Metadata
  metadata: Record<string, any>;
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Generate a simple UUID-like string for testing/development.
 */
function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36);
}

/**
 * Create a default beat data object.
 */
export function createDefaultBeatData(beatNumber: number = 1): BeatData {
  return {
    id: generateId(),
    beat_number: beatNumber,
    letter: null,
    duration: 1.0,
    blue_motion: null,
    red_motion: null,
    glyph_data: null,
    blue_reversal: false,
    red_reversal: false,
    is_blank: false,
    metadata: {},
  };
}

/**
 * Create an empty beat data object.
 */
export function createEmptyBeatData(): BeatData {
  return {
    ...createDefaultBeatData(),
    is_blank: true,
  };
}

/**
 * Create a default sequence data object.
 */
export function createDefaultSequenceData(): SequenceData {
  return {
    id: generateId(),
    name: "",
    word: "",
    beats: [],
    start_position: null,
    metadata: {},
  };
}

/**
 * Create an empty sequence data object.
 */
export function createEmptySequenceData(): SequenceData {
  return {
    ...createDefaultSequenceData(),
    name: "",
    beats: [],
  };
}

/**
 * Check if beat has valid data for sequence inclusion.
 */
export function isBeatValid(beat: BeatData): boolean {
  if (beat.is_blank) {
    return true;
  }
  return (
    beat.letter !== null &&
    beat.blue_motion !== null &&
    beat.red_motion !== null
  );
}

/**
 * Check if sequence is valid.
 */
export function isSequenceValid(sequence: SequenceData): boolean {
  if (sequence.beats.length === 0) {
    return false;
  }
  return sequence.beats.every((beat) => isBeatValid(beat));
}

/**
 * Get the total duration of a sequence.
 */
export function getSequenceTotalDuration(sequence: SequenceData): number {
  return sequence.beats.reduce((total, beat) => total + beat.duration, 0);
}

/**
 * Get a beat by its number from a sequence.
 */
export function getBeatByNumber(
  sequence: SequenceData,
  beatNumber: number
): BeatData | null {
  return sequence.beats.find((beat) => beat.beat_number === beatNumber) || null;
}

/**
 * Add a beat to a sequence (returns new sequence).
 */
export function addBeatToSequence(
  sequence: SequenceData,
  beatData: BeatData
): SequenceData {
  const newBeat = {
    ...beatData,
    beat_number: sequence.beats.length + 1,
  };

  return {
    ...sequence,
    beats: [...sequence.beats, newBeat],
  };
}

/**
 * Remove a beat from a sequence (returns new sequence).
 */
export function removeBeatFromSequence(
  sequence: SequenceData,
  beatNumber: number
): SequenceData {
  const newBeats = sequence.beats
    .filter((beat) => beat.beat_number !== beatNumber)
    .map((beat, index) => ({
      ...beat,
      beat_number: index + 1,
    }));

  return {
    ...sequence,
    beats: newBeats,
  };
}

/**
 * Update a beat in a sequence (returns new sequence).
 */
export function updateBeatInSequence(
  sequence: SequenceData,
  beatNumber: number,
  updates: Partial<BeatData>
): SequenceData {
  const newBeats = sequence.beats.map((beat) =>
    beat.beat_number === beatNumber ? { ...beat, ...updates } : beat
  );

  return {
    ...sequence,
    beats: newBeats,
  };
}
