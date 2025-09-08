import type { BeatData } from "../models/BeatData";

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
