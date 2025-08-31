import type {
  BackgroundSystem,
  BackgroundType,
  QualityLevel,
} from "$domain/core/ui/backgrounds/BackgroundTypes";
import type { IBackgroundService } from "$lib/services/contracts/background/IBackgroundService";
import { injectable } from "inversify";
import { BackgroundFactory } from "./BackgroundFactory";

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
}
