import type { BeatData, PictographData } from "$shared";

export interface IBeatConverterService {
  convertToBeat(pictograph: PictographData, beatNumber: number): BeatData;
}

