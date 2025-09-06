/**
 * Text Rendering Utilities
 *
 * Common text measurement and rendering utilities shared across text renderers.
 */

import { injectable } from "inversify";
import type { ITextRenderingUtils } from "../contracts";
import { createFont } from "./TextRenderingTypes";


@injectable()
export class TextRenderingUtils implements ITextRenderingUtils {
  /**
   * Calculate text dimensions for layout planning
   */
  measureText(
    text: string,
    fontFamily: string,
    fontSize: number,
    fontWeight: string = "normal"
  ): { width: number; height: number } {
    // Create temporary canvas for measurement
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    if (!ctx) {
      throw new Error("Failed to get 2D context for text measurement");
    }

    ctx.font = createFont(fontFamily, fontSize, fontWeight);
    const metrics = ctx.measureText(text);

    return {
      width: metrics.width,
      height: fontSize, // Approximation
    };
  }

  /**
   * Apply custom kerning to text
   */
  renderTextWithKerning(
    ctx: CanvasRenderingContext2D,
    text: string,
    x: number,
    y: number,
    kerning: number
  ): void {
    let currentX = x;

    for (const letter of text) {
      ctx.fillText(letter, currentX, y);
      const letterWidth = ctx.measureText(letter).width;
      currentX += letterWidth + kerning;
    }
  }

  /**
   * Validate font loading and availability
   */
  async validateFonts(): Promise<{ available: boolean; missing: string[] }> {
    const requiredFonts = ["Georgia"]; // Common font family used across renderers

    const missing: string[] = [];

    for (const font of requiredFonts) {
      if (!this.isFontAvailable(font)) {
        missing.push(font);
      }
    }

    return {
      available: missing.length === 0,
      missing,
    };
  }

  /**
   * Check if font is available in the browser
   */
  private isFontAvailable(fontFamily: string): boolean {
    // Create a temporary canvas to test font availability
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    if (!ctx) {
      return false; // If we can't get context, assume font is not available
    }

    // Test with fallback font
    ctx.font = `12px ${fontFamily}, monospace`;
    const testWidth1 = ctx.measureText("test").width;

    // Test with just monospace
    ctx.font = "12px monospace";
    const testWidth2 = ctx.measureText("test").width;

    // If widths are different, the font is available
    return testWidth1 !== testWidth2;
  }
}
