import type { PictographData } from "../models";

export function createPictographData(
  data: Partial<PictographData> = {}
): PictographData {
  return {
    id: data.id || crypto.randomUUID(),
    motions: data.motions || {},
    letter: data.letter || null,
    startPosition: data.startPosition ?? null,
    endPosition: data.endPosition ?? null,
  };
}
