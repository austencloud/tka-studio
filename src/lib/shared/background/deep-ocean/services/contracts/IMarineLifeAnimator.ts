import type { Dimensions } from "$shared";
import type {
  MarineLife,
  MarineLifeType,
} from "../../domain/models/DeepOceanModels";

/**
 * Contract for marine life animation and movement
 */
export interface IMarineLifeAnimator {
  /**
   * Initialize marine life for the given dimensions
   * Preloads sprites before creating fish
   */
  initializeMarineLife(
    dimensions: Dimensions,
    fishCount: number,
    jellyfishCount: number
  ): Promise<MarineLife[]>;

  /**
   * Create fish with animation properties
   */
  createFish(dimensions: Dimensions): MarineLife;

  /**
   * Create jellyfish with animation properties
   */
  createJellyfish(dimensions: Dimensions): MarineLife;

  /**
   * Update marine life positions and animations
   */
  updateMarineLife(
    marineLife: MarineLife[],
    dimensions: Dimensions,
    frameMultiplier: number,
    animationTime: number
  ): MarineLife[];

  /**
   * Get optimal marine life count for quality level
   */
  getMarineLifeCount(quality: string): number;

  /**
   * Schedule new marine life to spawn
   */
  scheduleSpawn(type: MarineLifeType, spawnTime: number): void;

  /**
   * Process pending spawns and create new marine life
   */
  processPendingSpawns(
    dimensions: Dimensions,
    currentTime: number
  ): MarineLife[];
}
