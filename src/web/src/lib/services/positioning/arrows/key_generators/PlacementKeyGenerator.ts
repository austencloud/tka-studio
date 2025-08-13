import type { MotionData, PictographData } from "$lib/domain";
import { ArrowPlacementKeyService } from "../../../implementations/ArrowPlacementKeyService";
import type { IPlacementKeyGenerator } from "../../data-services";

/**
 * PlacementKeyGenerator
 * Adapter around ArrowPlacementKeyService to implement IPlacementKeyGenerator.
 */
export class PlacementKeyGenerator implements IPlacementKeyGenerator {
  private service = new ArrowPlacementKeyService();

  generatePlacementKey(
    motionData: MotionData,
    pictographData: PictographData,
    defaultPlacements: Record<string, unknown>,
    _gridMode?: string,
  ): string {
    // Interpret defaultPlacements as a set of available keys
    const availableKeys = Object.keys(defaultPlacements || {});
    if (availableKeys.length === 0) {
      // Fall back: pick the first candidate from service
      const candidates = this.service.debugCandidateKeys(
        motionData,
        pictographData,
      );
      return (
        candidates[0] ??
        this.service.generateBasicKey(
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          (motionData as any).motion_type || "pro",
        )
      );
    }

    const candidates = this.service.debugCandidateKeys(
      motionData,
      pictographData,
    );
    for (const key of candidates) {
      if (availableKeys.includes(key)) return key;
    }
    // Fallback to basic
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return this.service.generateBasicKey(
      (motionData as any).motion_type || "pro",
    );
  }
}
