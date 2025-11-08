import type { Dimensions } from "$shared";
import type { OceanParticle } from "../../domain/models/DeepOceanModels";

/**
 * Contract for particle system management
 */
export interface IParticleSystem {
  /**
   * Initialize particles for the given dimensions
   */
  initializeParticles(dimensions: Dimensions, count: number): OceanParticle[];

  /**
   * Create a single particle
   */
  createParticle(dimensions: Dimensions): OceanParticle;

  /**
   * Update particle positions and lifecycle
   */
  updateParticles(
    particles: OceanParticle[],
    dimensions: Dimensions,
    frameMultiplier: number
  ): OceanParticle[];

  /**
   * Get optimal particle count for quality level
   */
  getParticleCount(quality: string): number;

  /**
   * Get particle color palette
   */
  getParticleColor(): string;
}
