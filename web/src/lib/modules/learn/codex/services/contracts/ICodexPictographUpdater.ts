import type { PictographData } from "$shared/domain";
import type { CodexTransformationOperation } from "../../domain";

export interface ICodexPictographUpdater {
  rotateAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]>;
  mirrorAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]>;
  colorSwapAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]>;
  applyOperation(
    pictographs: PictographData[],
    operation: CodexTransformationOperation
  ): Promise<PictographData[]>;
}
