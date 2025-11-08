import type { Dimensions } from "$shared";
import type { FishSprite } from "../../domain/models/DeepOceanModels";

/**
 * Contract for fish sprite management and caching
 */
export interface IFishSpriteManager {
  /**
   * Preload all fish sprites
   */
  preloadSprites(): Promise<void>;

  /**
   * Get a random fish sprite entry
   */
  getRandomSpriteEntry():
    | { sprite: FishSprite; image?: HTMLImageElement }
    | undefined;

  /**
   * Get any loaded sprite entry (for fish created before sprites finished loading)
   */
  getAnyLoadedSpriteEntry():
    | { sprite: FishSprite; image: HTMLImageElement }
    | undefined;

  /**
   * Get marine life color for type
   */
  getMarineLifeColor(type: "fish" | "jellyfish"): string;

  /**
   * Check if sprites are loaded and ready
   */
  isReady(): boolean;
}
