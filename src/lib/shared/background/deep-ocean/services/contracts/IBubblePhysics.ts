import type { Bubble, Dimensions } from "$shared";

/**
 * Contract for bubble physics calculations and management
 */
export interface IBubblePhysics {
  /**
   * Initialize bubbles for the given dimensions and quality
   */
  initializeBubbles(dimensions: Dimensions, count: number): Bubble[];

  /**
   * Create a single bubble with physics properties
   */
  createBubble(dimensions: Dimensions): Bubble;

  /**
   * Update bubble positions and physics
   */
  updateBubbles(
    bubbles: Bubble[],
    dimensions: Dimensions,
    frameMultiplier: number,
    animationTime: number
  ): Bubble[];

  /**
   * Get optimal bubble count for quality level
   */
  getBubbleCount(quality: string): number;
}
