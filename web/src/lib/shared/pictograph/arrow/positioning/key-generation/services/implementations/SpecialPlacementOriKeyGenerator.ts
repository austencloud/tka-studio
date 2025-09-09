import type {
  ISpecialPlacementOriKeyGenerator,
  MotionData,
  PictographData,
} from "$shared";
import { injectable } from "inversify";

/**
 * SpecialPlacementOriKeyGenerator
 * Generates ori_key matching SpecialPlacementService's internal logic.
 */
@injectable()
export class SpecialPlacementOriKeyGenerator
  implements ISpecialPlacementOriKeyGenerator
{
  generateOrientationKey(
    _motionData: MotionData,
    pictographData: PictographData
  ): string {
    try {
      const blueMotion = pictographData.motions?.blue;
      const redMotion = pictographData.motions?.red;
      if (blueMotion && redMotion) {
        const blueEndOri = blueMotion.endOrientation || "in";
        const redEndOri = redMotion.endOrientation || "in";
        const blueLayer = ["in", "out"].includes(blueEndOri) ? 1 : 2;
        const redLayer = ["in", "out"].includes(redEndOri) ? 1 : 2;
        if (blueLayer === 1 && redLayer === 1) return "from_layer1";
        if (blueLayer === 2 && redLayer === 2) return "from_layer2";
        if (blueLayer === 1 && redLayer === 2) return "from_layer3_blue1_red2";
        if (blueLayer === 2 && redLayer === 1) return "from_layer3_blue2_red1";
        return "from_layer1";
      }
    } catch {
      // fallthrough
    }
    return "from_layer1";
  }
}
