/**
 * Sequence Domain Model
 *
 * Immutable data structure for complete kinetic sequences.
 * Based on the modern desktop app's SequenceData but adapted for TypeScript.
 */

import type { BeatData, GridMode, GridPositionGroup, PropType } from "$domain";

export interface SequenceData {
  readonly id: string;
  readonly name: string;
  readonly word: string;
  readonly beats: readonly BeatData[];

  // Starting position clarification:
  readonly startingPositionBeat?: BeatData; // The actual visual beat (beat 0)
  readonly startingPositionGroup?: GridPositionGroup; // Position group: "alpha", "beta", "gamma"
  readonly startPosition?: BeatData; // Start position beat data

  readonly thumbnails: readonly string[];
  readonly sequenceLength?: number;
  readonly author?: string;
  readonly level?: number;
  readonly dateAdded?: Date;
  readonly gridMode?: GridMode;
  readonly propType?: PropType;
  readonly isFavorite: boolean;
  readonly isCircular: boolean;
  readonly difficultyLevel?: string;
  readonly tags: readonly string[];
  readonly metadata: Record<string, unknown>;
}

export function createSequenceData(
  data: Partial<SequenceData> = {}
): SequenceData {
  const result: SequenceData = {
    id: data.id ?? crypto.randomUUID(),
    name: data.name ?? "",
    word: data.word ?? "",
    beats: data.beats ?? [],
    thumbnails: data.thumbnails ?? [],
    isFavorite: data.isFavorite ?? false,
    isCircular: data.isCircular ?? false,
    tags: data.tags ?? [],
    metadata: data.metadata ?? {},
    ...(data.sequenceLength !== undefined && {
      sequenceLength: data.sequenceLength,
    }),
    ...(data.author !== undefined && { author: data.author }),
    ...(data.level !== undefined && { level: data.level }),
    ...(data.dateAdded !== undefined && { dateAdded: data.dateAdded }),
    ...(data.gridMode !== undefined && { gridMode: data.gridMode }),
    ...(data.propType !== undefined && { propType: data.propType }),
    ...(data.startingPositionBeat !== undefined && {
      startingPositionBeat: data.startingPositionBeat,
    }),
    ...(data.startingPositionGroup !== undefined && {
      startingPositionGroup: data.startingPositionGroup,
    }),
    ...(data.difficultyLevel !== undefined && {
      difficultyLevel: data.difficultyLevel,
    }),
  };
  return result;
}

export function updateSequenceData(
  sequence: SequenceData,
  updates: Partial<SequenceData>
): SequenceData {
  return {
    ...sequence,
    ...updates,
  };
}

export function addBeatToSequence(
  sequence: SequenceData,
  beat: BeatData
): SequenceData {
  return updateSequenceData(sequence, {
    beats: [...sequence.beats, beat],
  });
}

export function removeBeatFromSequence(
  sequence: SequenceData,
  beatIndex: number
): SequenceData {
  if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
    return sequence;
  }

  const newBeats = sequence.beats.filter((_, index) => index !== beatIndex);
  return updateSequenceData(sequence, {
    beats: newBeats,
  });
}
