import type { BeatData, PictographData } from "$shared";

export interface IPictographFilterService {
  filterByContinuity(options: PictographData[], lastBeat: BeatData | null): PictographData[];
  filterByRotation(
    options: PictographData[],
    blueRotationDirection: string,
    redRotationDirection: string
  ): PictographData[];
  filterByLetterTypes(options: PictographData[], letterTypes: string[]): PictographData[];
  filterStartPositions(options: PictographData[]): PictographData[];
  selectRandom<T>(array: T[]): T;
}

