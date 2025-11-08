import { injectable } from "inversify";
import type { Dimensions } from "$shared";
import type { FishSprite } from "../../domain/models/DeepOceanModels";
import type { IFishSpriteManager } from "../contracts";

@injectable()
export class FishSpriteManager implements IFishSpriteManager {
  private readonly fishSprites: FishSprite[] = [
    { name: "Blue", path: "/assets/background/fish/kenney/fish_blue.png" },
    { name: "Orange", path: "/assets/background/fish/kenney/fish_orange.png" },
    { name: "Green", path: "/assets/background/fish/kenney/fish_green.png" },
    {
      name: "Grey Long",
      path: "/assets/background/fish/kenney/fish_grey_long_a.png",
    },
  ];

  private fishSpriteCache = new Map<
    string,
    { sprite: FishSprite; image: HTMLImageElement; ready: boolean }
  >();

  preloadSprites(): Promise<void> {
    if (typeof window === "undefined") {
      return Promise.resolve();
    }

    const loadPromises = this.fishSprites.map((sprite) => {
      if (this.fishSpriteCache.has(sprite.path)) {
        return Promise.resolve();
      }

      return new Promise<void>((resolve, reject) => {
        const image = new Image();
        // CRITICAL: Create cache entry with ready based on image.complete (matching monolith)
        const cacheEntry = { sprite, image, ready: image.complete };

        image.onload = () => {
          // Overwrite cache entry with ready=true (matching monolith)
          this.fishSpriteCache.set(sprite.path, {
            sprite,
            image,
            ready: true,
          });
          resolve();
        };

        image.onerror = (error) => {
          console.warn(`Failed to load fish sprite: ${sprite.path}`);
          this.fishSpriteCache.delete(sprite.path);
          reject(error);
        };

        // Set src BEFORE setting cache entry (images might load synchronously from browser cache!)
        image.src = sprite.path;

        // Set cache entry AFTER src (matching monolith pattern)
        this.fishSpriteCache.set(sprite.path, cacheEntry);
      });
    });

    return Promise.all(loadPromises).then(() => {});
  }

  getRandomSpriteEntry():
    | { sprite: FishSprite; image?: HTMLImageElement }
    | undefined {
    if (this.fishSprites.length === 0) {
      return undefined;
    }

    const sprite =
      this.fishSprites[Math.floor(Math.random() * this.fishSprites.length)];
    if (!sprite) return undefined;
    const entry = this.fishSpriteCache.get(sprite.path);

    return entry ?? undefined;
  }

  getAnyLoadedSpriteEntry():
    | { sprite: FishSprite; image: HTMLImageElement }
    | undefined {
    // Find any loaded sprite to use
    for (const entry of this.fishSpriteCache.values()) {
      if (entry.image && entry.image.complete && entry.ready) {
        return entry;
      }
    }
    return undefined;
  }

  getMarineLifeColor(type: "fish" | "jellyfish"): string {
    if (type === "fish") {
      // Ocean fish in nice teals and blues
      const colors = ["#3d7a8c", "#4a8fa3", "#548da0", "#4b8599"];
      return colors[Math.floor(Math.random() * 4)] || "#3d7a8c";
    }

    // Jellyfish in soft purples and pinks
    const colors = ["#7d5a7a", "#8b6d88", "#946f91", "#866783"];
    return colors[Math.floor(Math.random() * 4)] || "#7d5a7a";
  }

  isReady(): boolean {
    if (this.fishSpriteCache.size === 0) return false;

    for (const entry of this.fishSpriteCache.values()) {
      if (!entry.ready) return false;
    }

    return true;
  }
}
