import { injectable } from "inversify";
import { BackgroundFactory } from "./BackgroundFactory";
import { detectAppropriateQuality } from "$lib/domain/background/configs/config";
import type {
  BackgroundType,
  QualityLevel,
  BackgroundSystem,
  PerformanceMetrics,
} from "$lib/domain/background/BackgroundTypes";
import type { IBackgroundService } from "../../interfaces/background-interfaces";

@injectable()
export class BackgroundService implements IBackgroundService {
  async createSystem(
    type: BackgroundType,
    quality: QualityLevel
  ): Promise<BackgroundSystem> {
    return BackgroundFactory.createBackgroundSystem({
      type,
      initialQuality: quality,
    });
  }

  getSupportedTypes(): BackgroundType[] {
    return BackgroundFactory.getSupportedBackgroundTypes();
  }

  detectOptimalQuality(): QualityLevel {
    return detectAppropriateQuality();
  }

  getSystemMetrics(system: BackgroundSystem): PerformanceMetrics | null {
    if (system.getMetrics) {
      return system.getMetrics();
    }
    return null;
  }
}
