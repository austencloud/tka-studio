import { inject, injectable } from "inversify";
import type { Dimensions } from "$shared";
import { TYPES } from "$shared/inversify/types";
import type { MarineLife, MarineLifeType, FishMarineLife, JellyfishMarineLife } from "../../domain/models/DeepOceanModels";
import type { IMarineLifeAnimator, IFishSpriteManager } from "../contracts";

@injectable()
export class MarineLifeAnimator implements IMarineLifeAnimator {
  private pendingSpawns: Array<{ type: MarineLifeType; spawnTime: number }> = [];

  constructor(
    @inject(TYPES.IFishSpriteManager)
    private fishSpriteManager: IFishSpriteManager
  ) {}

  async initializeMarineLife(dimensions: Dimensions, fishCount: number, jellyfishCount: number): Promise<MarineLife[]> {
    // Preload sprites FIRST to ensure fish get actual sprites
    await this.fishSpriteManager.preloadSprites();

    const marineLife: MarineLife[] = [];

    // Create fish (now sprites are loaded)
    for (let i = 0; i < fishCount; i++) {
      marineLife.push(this.createFish(dimensions));
    }

    // Create jellyfish
    for (let i = 0; i < jellyfishCount; i++) {
      marineLife.push(this.createJellyfish(dimensions));
    }

    return marineLife;
  }

  createFish(dimensions: Dimensions): FishMarineLife {
    const entry = this.fishSpriteManager.getRandomSpriteEntry();
    const sprite = entry?.sprite ?? { name: "Default", path: "" };
    const image = entry?.image;

    const direction: 1 | -1 = Math.random() > 0.5 ? 1 : -1;
    const baseWidth = image?.naturalWidth ?? 96;
    const baseHeight = image?.naturalHeight ?? 64;
    const scale = 0.35 + Math.random() * 0.25; // Moderately smaller: 35-60% instead of 55-90%
    const width = baseWidth * scale;
    const height = baseHeight * scale;
    const depthBand = {
      min: 90,
      max: Math.max(240, dimensions.height - 180),
    };
    const maxOffset = Math.max(140, dimensions.width * 0.2);

    const startX =
      direction === 1
        ? -width - Math.random() * maxOffset
        : dimensions.width + width + Math.random() * maxOffset;
    const baseY =
      depthBand.min +
      Math.random() * Math.max(60, depthBand.max - depthBand.min);

    const fish: FishMarineLife = {
      type: "fish",
      sprite,
      image,
      width,
      height,
      direction,
      speed: 12 + Math.random() * 15, // Much slower: 12-27 instead of 35-80
      verticalDrift: (Math.random() - 0.5) * 6, // Gentler drift: ±3 instead of ±9
      bobAmplitude: 3 + Math.random() * 4, // Subtler bob: 3-7 instead of 6-15
      bobSpeed: 0.01 + Math.random() * 0.015, // Slower bob: 0.01-0.025 instead of 0.02-0.05
      depthBand,
      x: startX,
      baseY,
      y: baseY,
      opacity: 0.35 + Math.random() * 0.15,
      animationPhase: Math.random() * Math.PI * 2,
    };

    // Mark fish that need sprite update (created before sprites loaded)
    if (!image || sprite.name === "Default") {
      (fish as any)._needsSpriteUpdate = true;
    }

    return fish;
  }

  createJellyfish(dimensions: Dimensions): JellyfishMarineLife {
    const size = 18 + Math.random() * 15; // Moderately smaller: 18-33px instead of 28-52px
    const baseY =
      dimensions.height * 0.25 + Math.random() * (dimensions.height * 0.45);
    const tentacleSeeds = Array.from(
      { length: 5 + Math.floor(Math.random() * 3) },
      () => Math.random() * Math.PI * 2
    );

    return {
      type: "jellyfish",
      size,
      color: this.fishSpriteManager.getMarineLifeColor("jellyfish"),
      horizontalSpeed: (Math.random() - 0.5) * 8, // Slower: ±4 instead of ±10
      verticalSpeed: -6 - Math.random() * 6, // Slower upward: -6 to -12 instead of -18 to -32
      waveAmplitude: 4 + Math.random() * 4, // Gentler wave: 4-8 instead of 10-18
      waveFrequency: 0.008 + Math.random() * 0.012, // Slower wave: 0.008-0.02 instead of 0.015-0.04
      glowIntensity: 0.15 + Math.random() * 0.15, // Subtler glow: 0.15-0.3 instead of 0.35-0.65
      tentacleSeeds,
      baseY,
      x: 60 + Math.random() * (dimensions.width - 120),
      y: baseY,
      opacity: 0.45 + Math.random() * 0.35,
      animationPhase: Math.random() * Math.PI * 2,
    };
  }

  updateMarineLife(
    marineLife: MarineLife[],
    dimensions: Dimensions,
    frameMultiplier: number,
    animationTime: number
  ): MarineLife[] {
    const updatedMarineLife: MarineLife[] = [];
    const deltaSeconds = 0.016 * frameMultiplier;

    for (let i = marineLife.length - 1; i >= 0; i--) {
      const marine = marineLife[i];

      switch (marine.type) {
        case "fish": {
          const fish = marine as FishMarineLife;

          // Update sprite if it wasn't loaded when fish was created
          if ((fish as any)._needsSpriteUpdate) {
            const entry = this.fishSpriteManager.getAnyLoadedSpriteEntry();
            if (entry) {
              fish.image = entry.image;
              fish.sprite = entry.sprite;
              // Recalculate size based on actual sprite dimensions
              const baseWidth = entry.image.naturalWidth ?? 96;
              const baseHeight = entry.image.naturalHeight ?? 64;
              const scale = 0.35 + Math.random() * 0.25;
              fish.width = baseWidth * scale;
              fish.height = baseHeight * scale;
              delete (fish as any)._needsSpriteUpdate;
            }
          }

          // Update fish animation phase and movement (matching monolith exactly)
          fish.animationPhase += fish.bobSpeed * frameMultiplier;
          fish.x += fish.direction * fish.speed * deltaSeconds;
          fish.baseY += fish.verticalDrift * deltaSeconds;
          fish.baseY = Math.max(
            fish.depthBand.min,
            Math.min(fish.depthBand.max, fish.baseY)
          );
          const bob = Math.sin(fish.animationPhase) * fish.bobAmplitude;
          fish.y = fish.baseY + bob;

          // Check boundaries
          const offRight = fish.x > dimensions.width + fish.width + 100;
          const offLeft = fish.x < -fish.width - 100;

          if (offRight || offLeft) {
            // Schedule new fish spawn with delay (2-10 seconds)
            this.scheduleSpawn("fish", animationTime + 2 + Math.random() * 8);
          } else {
            updatedMarineLife.push(fish);
          }
          break;
        }
        case "jellyfish": {
          const jellyfish = marine as JellyfishMarineLife;
          // Update jellyfish animation phase and movement (matching monolith exactly)
          jellyfish.animationPhase += jellyfish.waveFrequency * frameMultiplier;
          jellyfish.x += jellyfish.horizontalSpeed * deltaSeconds;
          jellyfish.baseY += jellyfish.verticalSpeed * deltaSeconds;
          jellyfish.y =
            jellyfish.baseY + Math.sin(jellyfish.animationPhase) * jellyfish.waveAmplitude;

          // Wrap around boundaries
          const wrappedLeft = jellyfish.x < -jellyfish.size;
          const wrappedRight = jellyfish.x > dimensions.width + jellyfish.size;
          const wrappedTop = jellyfish.y < -jellyfish.size;
          const wrappedBottom = jellyfish.y > dimensions.height + jellyfish.size;

          if (wrappedLeft || wrappedRight || wrappedTop || wrappedBottom) {
            // Replace with new jellyfish
            updatedMarineLife.push(this.createJellyfish(dimensions));
          } else {
            updatedMarineLife.push(jellyfish);
          }
          break;
        }
      }
    }

    return updatedMarineLife;
  }

  getMarineLifeCount(quality: string): number {
    switch (quality) {
      case "minimal":
        return 2; // Reduced from 3
      case "low":
        return 4; // Reduced from 6
      case "medium":
        return 6; // Reduced from 9
      case "high":
        return 8; // Reduced from 12
      default:
        return 6;
    }
  }

  scheduleSpawn(type: MarineLifeType, spawnTime: number): void {
    this.pendingSpawns.push({ type, spawnTime });
  }

  processPendingSpawns(dimensions: Dimensions, currentTime: number): MarineLife[] {
    const newMarineLife: MarineLife[] = [];

    for (let i = this.pendingSpawns.length - 1; i >= 0; i--) {
      const spawn = this.pendingSpawns[i];
      if (currentTime >= spawn.spawnTime) {
        // Create new marine life
        if (spawn.type === "fish") {
          newMarineLife.push(this.createFish(dimensions));
        } else if (spawn.type === "jellyfish") {
          newMarineLife.push(this.createJellyfish(dimensions));
        }
        // Remove processed spawn
        this.pendingSpawns.splice(i, 1);
      }
    }

    return newMarineLife;
  }
}
