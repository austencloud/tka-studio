/**
 * Beat Domain Model
 *
 * Immutable data structure for individual beats in kinetic sequences.
 * Based on the modern desktop app's BeatData adapted for TypeScript.
 */

import type { MotionData } from "./MotionData";
import type { PictographData } from "./PictographData";

export interface BeatData {
  readonly id: string;
  readonly beat_number: number;
  readonly duration: number;
  readonly blue_reversal: boolean;
  readonly red_reversal: boolean;
  readonly is_blank: boolean;
  readonly pictograph_data?: PictographData | null;
  readonly metadata: Record<string, unknown>;
}

export function createBeatData(data: Partial<BeatData> = {}): BeatData {
  return {
    id: data.id ?? crypto.randomUUID(),
    beat_number: data.beat_number ?? 1,
    duration: data.duration ?? 1.0,
    blue_reversal: data.blue_reversal ?? false,
    red_reversal: data.red_reversal ?? false,
    is_blank: data.is_blank ?? false,
    pictograph_data: data.pictograph_data ?? null,
    metadata: data.metadata ?? {},
  };
}

export function updateBeatData(
  beat: BeatData,
  updates: Partial<BeatData>,
): BeatData {
  return {
    ...beat,
    ...updates,
  };
}

export function isValidBeat(beat: BeatData): boolean {
  return beat.duration >= 0 && beat.beat_number >= 0;
}

export function getBeatLetter(beat: BeatData): string | undefined {
  return (
    beat.pictograph_data?.letter ??
    (typeof beat.metadata.letter === "string"
      ? beat.metadata.letter
      : undefined)
  );
}

export function hasPictograph(beat: BeatData): boolean {
  return beat.pictograph_data != null;
}

export function getBlueMotion(beat: BeatData): MotionData | null {
  if (beat.pictograph_data?.motions) {
    return beat.pictograph_data.motions.blue ?? null;
  }
  return null;
}

export function getRedMotion(beat: BeatData): MotionData | null {
  if (beat.pictograph_data?.motions) {
    return beat.pictograph_data.motions.red ?? null;
  }
  return null;
}

export function createBeatFromPictograph(
  pictograph_data: PictographData,
  beat_number: number,
): BeatData {
  return createBeatData({
    beat_number,
    pictograph_data,
    metadata: {
      letter: pictograph_data.letter,
      created_from_pictograph: true,
    },
  });
}

export function beatDataToObject(beat: BeatData): Record<string, unknown> {
  return {
    id: beat.id,
    beat_number: beat.beat_number,
    duration: beat.duration,
    blue_reversal: beat.blue_reversal,
    red_reversal: beat.red_reversal,
    is_blank: beat.is_blank,
    pictograph_data: beat.pictograph_data,
    metadata: beat.metadata,
  };
}

export function beatDataFromObject(data: Record<string, unknown>): BeatData {
  const partialData: Record<string, unknown> = {};

  if (typeof data.id === "string") partialData.id = data.id;
  if (typeof data.beat_number === "number")
    partialData.beat_number = data.beat_number;
  if (typeof data.duration === "number") partialData.duration = data.duration;
  if (typeof data.blue_reversal === "boolean")
    partialData.blue_reversal = data.blue_reversal;
  if (typeof data.red_reversal === "boolean")
    partialData.red_reversal = data.red_reversal;
  if (typeof data.is_blank === "boolean") partialData.is_blank = data.is_blank;
  if (data.pictograph_data)
    partialData.pictograph_data = data.pictograph_data as PictographData;
  if (typeof data.metadata === "object" && data.metadata !== null)
    partialData.metadata = data.metadata as Record<string, unknown>;

  return createBeatData(partialData as Partial<BeatData>);
}
