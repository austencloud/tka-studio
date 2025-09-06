import type {
  BackgroundSystem,
  BackgroundType,
  QualityLevel,
} from "$shared/domain";
import { injectable } from "inversify";
import type { IBackgroundService } from "../../contracts/background/IBackgroundService";
import { BackgroundFactory } from "./BackgroundFactory";

@injectable()
export class BackgroundService implements IBackgroundService {
  async createSystem(
    type: BackgroundType,
    quality: QualityLevel
  ): Promise<BackgroundSystem> {
    return BackgroundFactory.createBackgroundSystem({
      type,
      quality,
      initialQuality: quality,
    });
  }
}
