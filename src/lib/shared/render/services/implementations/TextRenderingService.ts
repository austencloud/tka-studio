/**
 * Text Rendering Service
 *
 * Handles rendering of sequence titles, user info, and other text overlays
 * on exported images. Matches desktop application text rendering patterns.
 */

import { inject, injectable } from "inversify";
import { TYPES } from "../../../inversify/types";
import type { TextRenderOptions, UserInfo } from "../../domain/models";
import type { ITextRenderingService } from "../contracts";
import type { IDimensionCalculationService } from "../contracts/IDimensionCalculationService";
@injectable()
export class TextRenderingService implements ITextRenderingService {
  // Font configuration matching WordLabel component exactly
  private readonly titleFontFamily = "Georgia, serif"; // Matches WordLabel
  private readonly titleFontWeight = "600"; // Matches WordLabel
  private readonly fallbackFontFamily =
    "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";
  private readonly userInfoFontWeight = "400";

  constructor(
    @inject(TYPES.IDimensionCalculationService)
    private dimensionService: IDimensionCalculationService
  ) {}

  /**
   * Render sequence word/title text at the top center of the canvas
   */
  renderWordText(
    canvas: HTMLCanvasElement,
    word: string,
    options: TextRenderOptions,
    beatCount: number = 3 // Default to 3+ beats scaling
  ): void {
    if (!word || word.trim() === "") {
      console.log("🚫 TextRenderingService: No word to render");
      return;
    }

    const ctx = canvas.getContext("2d");
    if (!ctx) {
      console.log("🚫 TextRenderingService: No canvas context");
      return;
    }

    // Get desktop-compatible font scaling based on beat count
    const scalingFactors =
      this.dimensionService.getTextScalingFactors(beatCount);

    // Calculate title area height (matches ImageCompositionService logic)
    const titleHeight = this.calculateTitleHeight(
      beatCount,
      options.beatScale || 1
    );
    const scaledFontSize = titleHeight * scalingFactors.fontScale;
    const finalFontSize = scaledFontSize * (options.beatScale || 1);

    // Set font properties using Georgia serif font (matches WordLabel)
    ctx.font = `${this.titleFontWeight} ${finalFontSize}px ${this.titleFontFamily}`;
    ctx.fillStyle = "black"; // Matches WordLabel color
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    // Calculate positioning
    const centerX = canvas.width / 2;
    const centerY = titleHeight / 2;

    this.drawTitleBackground(ctx, canvas.width, titleHeight);

    // Set text color to dark gray for visibility
    ctx.fillStyle = "black";

    // Render the text
    ctx.fillText(word, centerX, centerY);
  }

  /**
   * Calculate title height based on beat count (matches desktop logic)
   */
  private calculateTitleHeight(beatCount: number, beatScale: number): number {
    let baseHeight = 0;

    // Match desktop logic exactly based on beat count
    if (beatCount === 0) {
      baseHeight = 0;
    } else if (beatCount === 1) {
      baseHeight = 150;
    } else if (beatCount === 2) {
      baseHeight = 200;
    } else {
      // beatCount >= 3
      baseHeight = 300;
    }

    // Apply beat scale
    return Math.floor(baseHeight * beatScale);
  }

  /**
   * Render user information (name, date, notes) at the bottom of the canvas
   */
  renderUserInfo(
    canvas: HTMLCanvasElement,
    userInfo: UserInfo,
    options: TextRenderOptions
  ): void {
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const fontSize = Math.max(10, Math.min(16, canvas.width / 40));
    ctx.font = `${this.userInfoFontWeight} ${fontSize}px ${this.fallbackFontFamily}`;
    ctx.fillStyle = "#666666";
    ctx.textAlign = "left";
    ctx.textBaseline = "bottom";

    const margin = options.margin || 10;
    let yPosition = canvas.height - margin;

    // Render user name
    if (userInfo.userName && userInfo.userName.trim() !== "") {
      ctx.fillText(`By: ${userInfo.userName}`, margin, yPosition);
      yPosition -= fontSize + 5;
    }

    // Render export date
    if (userInfo.exportDate) {
      const date = new Date(userInfo.exportDate).toLocaleDateString();
      ctx.fillText(`Date: ${date}`, margin, yPosition);
      yPosition -= fontSize + 5;
    }

    // Render notes
    if (userInfo.notes && userInfo.notes.trim() !== "") {
      ctx.fillText(`Notes: ${userInfo.notes}`, margin, yPosition);
    }
  }

  /**
   * Render difficulty level badge with beautiful gradients
   */
  renderDifficultyBadge(
    canvas: HTMLCanvasElement,
    level: number,
    position: [number, number],
    size: number
  ): void {
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const [x, y] = position;
    const radius = size / 2;
    const centerX = x + radius;
    const centerY = y + radius;

    // Create gradient based on difficulty level
    const gradient = this.createDifficultyGradient(
      ctx,
      centerX,
      centerY,
      radius,
      level
    );

    // Draw badge background with gradient
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.fillStyle = gradient;
    ctx.fill();

    // Draw badge border
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw level text
    ctx.fillStyle = "#000000"; // Black text for better contrast on gradients
    ctx.font = `bold ${size * 0.6}px ${this.fallbackFontFamily}`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(level.toString(), centerX, centerY);
  }

  /**
   * Calculate text dimensions for layout planning
   */
  measureText(
    text: string,
    fontFamily: string,
    fontSize: number,
    fontWeight?: string
  ): { width: number; height: number } {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    if (!ctx) return { width: 0, height: 0 };

    ctx.font = `${fontWeight || "normal"} ${fontSize}px ${fontFamily}`;
    const metrics = ctx.measureText(text);

    return {
      width: metrics.width,
      height: fontSize, // Approximate height
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
    if (kerning === 0) {
      ctx.fillText(text, x, y);
      return;
    }

    let currentX = x;
    for (let i = 0; i < text.length; i++) {
      const char = text[i]!;
      ctx.fillText(char, currentX, y);

      const charWidth = ctx.measureText(char).width;
      currentX += charWidth + kerning;
    }
  }

  /**
   * Draw subtle background behind title text
   */
  private drawTitleBackground(
    ctx: CanvasRenderingContext2D,
    width: number,
    height: number
  ): void {
    // Very subtle white background
    ctx.fillStyle = "rgba(235, 235, 235, 0.98)";
    ctx.fillRect(0, 0, width, height);

    // Very subtle bottom border
    ctx.strokeStyle = "rgba(0, 0, 0, 0.05)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, height - 1);
    ctx.lineTo(width, height - 1);
    ctx.stroke();
  }

  /**
   * Create beautiful gradient for difficulty level badge
   * Based on legacy desktop gradient definitions
   */
  private createDifficultyGradient(
    ctx: CanvasRenderingContext2D,
    centerX: number,
    centerY: number,
    radius: number,
    level: number
  ): CanvasGradient {
    // Create radial gradient from center to edge
    const gradient = ctx.createRadialGradient(
      centerX,
      centerY,
      0,
      centerX,
      centerY,
      radius
    );

    if (level <= 2) {
      // Beginner - Light gray (solid color, matches desktop)
      gradient.addColorStop(0, "rgb(245, 245, 245)");
      gradient.addColorStop(1, "rgb(225, 225, 225)");
    } else if (level <= 4) {
      // Intermediate - Gray gradient (matches desktop)
      gradient.addColorStop(0, "rgb(180, 180, 180)");
      gradient.addColorStop(0.3, "rgb(170, 170, 170)");
      gradient.addColorStop(0.6, "rgb(120, 120, 120)");
      gradient.addColorStop(1, "rgb(110, 110, 110)");
    } else {
      // Advanced - Gold/brown gradient (matches desktop)
      gradient.addColorStop(0, "rgb(255, 215, 0)");
      gradient.addColorStop(0.2, "rgb(238, 201, 0)");
      gradient.addColorStop(0.4, "rgb(218, 165, 32)");
      gradient.addColorStop(0.6, "rgb(184, 134, 11)");
      gradient.addColorStop(0.8, "rgb(139, 69, 19)");
      gradient.addColorStop(1, "rgb(85, 107, 47)");
    }

    return gradient;
  }
}
