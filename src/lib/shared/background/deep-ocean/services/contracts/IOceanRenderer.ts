import type { Dimensions } from "$shared";
import type {
  MarineLife,
  Bubble,
  OceanParticle,
} from "../../domain/models/DeepOceanModels";

/**
 * Contract for ocean background rendering
 */
export interface IOceanRenderer {
  /**
   * Draw the ocean gradient background
   */
  drawOceanGradient(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions
  ): void;

  /**
   * Draw light rays from surface
   */
  drawLightRays(
    ctx: CanvasRenderingContext2D,
    dimensions: Dimensions,
    lightRays: Array<{
      x: number;
      opacity: number;
      width: number;
      angle: number;
      phase: number;
      speed: number;
    }>,
    quality: string
  ): void;

  /**
   * Draw bubbles
   */
  drawBubbles(ctx: CanvasRenderingContext2D, bubbles: Bubble[]): void;

  /**
   * Draw marine life
   */
  drawMarineLife(ctx: CanvasRenderingContext2D, marineLife: MarineLife[]): void;

  /**
   * Draw particles
   */
  drawParticles(
    ctx: CanvasRenderingContext2D,
    particles: OceanParticle[]
  ): void;
}
