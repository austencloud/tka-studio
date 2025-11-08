import { injectable } from "inversify";
import type { Bubble, Dimensions } from "$shared";
import type { IBubblePhysics } from "../contracts";

@injectable()
export class BubblePhysics implements IBubblePhysics {
  initializeBubbles(dimensions: Dimensions, count: number): Bubble[] {
    const bubbles: Bubble[] = [];
    for (let i = 0; i < count; i++) {
      bubbles.push(this.createBubble(dimensions));
    }
    return bubbles;
  }

  createBubble(dimensions: Dimensions): Bubble {
    return {
      x: Math.random() * dimensions.width,
      y: dimensions.height + 50, // Start below visible area
      radius: 2 + Math.random() * 6, // Smaller: 2-8px instead of 3-12px
      speed: 0.5 + Math.random() * 1.8, // Match snowfall magnitude: 0.5-2.3 instead of 12-27
      sway: 0.2 + Math.random() * 0.6, // Gentler sway: 0.2-0.8 instead of 0.5-2
      opacity: 0.15 + Math.random() * 0.25, // More subtle: 0.15-0.4 instead of 0.3-0.7
      swayOffset: Math.random() * Math.PI * 2,
      startY: dimensions.height + 50,
    };
  }

  updateBubbles(
    bubbles: Bubble[],
    dimensions: Dimensions,
    frameMultiplier: number,
    animationTime: number
  ): Bubble[] {
    const updatedBubbles: Bubble[] = [];

    for (let i = bubbles.length - 1; i >= 0; i--) {
      const bubble = bubbles[i];
      if (!bubble) continue;

      // Update position
      bubble.y -= bubble.speed * frameMultiplier;
      bubble.x +=
        Math.sin(animationTime * bubble.sway + bubble.swayOffset) *
        0.5 *
        frameMultiplier;

      // Remove if off-screen, otherwise keep
      if (bubble.y < -bubble.radius * 2) {
        // Replace with new bubble
        updatedBubbles.push(this.createBubble(dimensions));
      } else {
        updatedBubbles.push(bubble);
      }
    }

    return updatedBubbles;
  }

  getBubbleCount(quality: string): number {
    switch (quality) {
      case "minimal":
        return 8; // Reduced from 12
      case "low":
        return 14; // Reduced from 20
      case "medium":
        return 22; // Reduced from 32
      case "high":
        return 30; // Reduced from 45
      default:
        return 22;
    }
  }
}
