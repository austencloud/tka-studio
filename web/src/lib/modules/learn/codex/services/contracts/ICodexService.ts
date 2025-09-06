import type { PictographData } from "$shared/domain";

export interface ICodexService {
  loadAllPictographs(): Promise<PictographData[]>;

  searchPictographs(searchTerm: string): Promise<PictographData[]>;

  getPictographByLetter(letter: string): Promise<PictographData | null>;

  getPictographsForLesson(lessonType: string): Promise<PictographData[]>;

  getLettersByRow(): Promise<string[][]>;

  rotateAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]>;

  mirrorAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]>;

  colorSwapAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]>;

  getAllPictographData(): Promise<Record<string, PictographData | null>>;
}
