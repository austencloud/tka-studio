/**
 * Beat Domain Model
 *
 */

import type { PictographData } from "./PictographData";

export interface BeatData {
  readonly id: string;
  readonly beatNumber: number;
  readonly duration: number;
  readonly blueReversal: boolean;
  readonly redReversal: boolean;
  readonly isBlank: boolean;
  readonly pictographData: PictographData | null;
}

export function createBeatData(data: Partial<BeatData> = {}): BeatData {
  return {
    id: data.id ?? crypto.randomUUID(),
    beatNumber: data.beatNumber ?? 1,
    duration: data.duration ?? 1.0,
    blueReversal: data.blueReversal ?? false,
    redReversal: data.redReversal ?? false,
    isBlank: data.isBlank ?? false,
    pictographData: data.pictographData ?? null,
  };
}
