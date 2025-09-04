/**
 * Difficulty Badge Renderer
 *
 * Handles rendering of difficulty level badges with gradients.
 * Matches desktop ImageExportDifficultyLevelDrawer exactly.
 */

import type { IDifficultyBadgeRenderer } from "$services";
import { injectable } from "inversify";
import { createFont } from "./TextRenderingTypes";

@injectable()
export class DifficultyBadgeRenderer implements IDifficultyBadgeRenderer {
  // Font constants matching desktop application
  private static readonly DIFFICULTY_FONT_FAMILY = "Georgia";

  /**
   * Render difficulty level badge
   * Matches desktop ImageExportDifficultyLevelDrawer exactly
   */
  render(
    canvas: HTMLCanvasElement,
    level: number,
    position: [number, number],
    size: number
  ): void {
    const ctx = canvas.getContext("2d");
    if (!ctx) {
      throw new Error("Canvas context not available");
    }

    if (level < 1 || level > 5) {
      throw new Error(`Invalid difficulty level: ${level}`);
    }

    const [x, y] = position;

    // Create gradient background (match desktop gradients)
    const gradient = this.createDifficultyGradient(ctx, level, x, y, size);

    // Draw circle with gradient
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(x + size / 2, y + size / 2, size / 2, 0, 2 * Math.PI);
    ctx.fill();

    // Draw border
    ctx.strokeStyle = "black";
    ctx.lineWidth = Math.max(1, size / 50); // Match desktop border calculation
    ctx.stroke();

    // Draw level number
    const fontSize = Math.floor(size / 1.75); // Match desktop font calculation
    ctx.font = createFont(
      DifficultyBadgeRenderer.DIFFICULTY_FONT_FAMILY,
      fontSize,
      "bold"
    );
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    // Apply Y offset for positioning (match desktop)
    const yOffset = level === 3 ? -25 : -15;
    const textY = y + size / 2 + yOffset;

    ctx.fillText(level.toString(), x + size / 2, textY);
  }

  /**
   * Create difficulty level gradient
   * Matches desktop DifficultyLevelGradients exactly
   */
  private createDifficultyGradient(
    ctx: CanvasRenderingContext2D,
    level: number,
    x: number,
    y: number,
    size: number
  ): CanvasGradient {
    const gradient = ctx.createLinearGradient(x, y, x + size, y + size);

    // Match desktop gradient definitions exactly
    switch (level) {
      case 1:
        gradient.addColorStop(0, "#f5f5f5"); // Light gray
        break;

      case 2:
        gradient.addColorStop(0, "#aaaaaa");
        gradient.addColorStop(0.15, "#d2d2d2");
        gradient.addColorStop(0.3, "#787878");
        gradient.addColorStop(0.4, "#b4b4b4");
        gradient.addColorStop(0.55, "#bebebe");
        gradient.addColorStop(0.75, "#828282");
        gradient.addColorStop(1, "#6e6e6e");
        break;

      case 3:
        gradient.addColorStop(0, "#ffd700"); // Gold
        gradient.addColorStop(0.2, "#eec900"); // Goldenrod
        gradient.addColorStop(0.4, "#daa520"); // Goldenrod darker
        gradient.addColorStop(0.6, "#b8860b"); // Dark goldenrod
        gradient.addColorStop(0.8, "#8b4513"); // Saddle brown
        gradient.addColorStop(1, "#556b2f"); // Dark olive green
        break;

      case 4:
        gradient.addColorStop(0, "#c8a2c8");
        gradient.addColorStop(0.3, "#aa84aa");
        gradient.addColorStop(0.6, "#9400d3");
        gradient.addColorStop(1, "#640096");
        break;

      case 5:
        gradient.addColorStop(0, "#ff4500");
        gradient.addColorStop(0.4, "#ff0000");
        gradient.addColorStop(0.8, "#8b0000");
        gradient.addColorStop(1, "#640000");
        break;

      default:
        gradient.addColorStop(0, "white");
        gradient.addColorStop(1, "white");
        break;
    }

    return gradient;
  }

  /**
   * Get recommended difficulty badge settings
   */
  getRecommendedSettings(): {
    fontFamily: string;
    fontSize: number;
    fontWeight: string;
    italic: boolean;
  } {
    return {
      fontFamily: DifficultyBadgeRenderer.DIFFICULTY_FONT_FAMILY,
      fontSize: 24, // Will be calculated based on badge size
      fontWeight: "bold",
      italic: false,
    };
  }
}
