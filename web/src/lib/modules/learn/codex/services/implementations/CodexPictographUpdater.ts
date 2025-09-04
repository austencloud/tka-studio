import type { PictographData } from "../../../../../shared/domain";
import type { CodexTransformationOperation } from "../../domain";
import type { ICodexPictographUpdater } from "../contracts/ICodexPictographUpdater";

export class CodexPictographUpdater implements ICodexPictographUpdater {
  async rotateAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]> {
    console.log("🔄 Applying rotation to", pictographs.length, "pictographs");

    return [...pictographs];
  }

  async mirrorAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]> {
    console.log("🪞 Applying mirror to", pictographs.length, "pictographs");

    return [...pictographs];
  }

  async colorSwapAllPictographs(
    pictographs: PictographData[]
  ): Promise<PictographData[]> {
    console.log(
      "⚫⚪ Applying color swap to",
      pictographs.length,
      "pictographs"
    );

    return [...pictographs];
  }

  async applyOperation(
    pictographs: PictographData[],
    operation: CodexTransformationOperation
  ): Promise<PictographData[]> {
    switch (operation) {
      case "rotate":
        return this.rotateAllPictographs(pictographs);
      case "mirror":
        return this.mirrorAllPictographs(pictographs);
      case "colorSwap":
        return this.colorSwapAllPictographs(pictographs);
      default:
        console.warn(`Unknown operation: ${operation}`);
        return [...pictographs];
    }
  }
}
