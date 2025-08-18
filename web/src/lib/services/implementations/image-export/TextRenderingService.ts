/**
 * Text Rendering Service
 *
 * Handles all text rendering for TKA image export, providing pixel-perfect
 * compatibility with desktop typography. This service implements the exact
 * font scaling, kerning, and positioning logic from the desktop WordDrawer,
 * UserInfoDrawer, and ImageExportDifficultyLevelDrawer.
 *
 * Critical: Font sizes, kerning, and positioning must match desktop exactly.
 */

import type {
  ITextRenderingService,
  TextRenderOptions,
  UserInfo,
} from "../../interfaces/image-export-interfaces";

export class TextRenderingService implements ITextRenderingService {
  // Font constants matching desktop application
  private static readonly WORD_FONT_FAMILY = "Georgia";
  private static readonly WORD_BASE_FONT_SIZE = 175;
  private static readonly WORD_FONT_WEIGHT = "600"; // DemiBold

  private static readonly USER_INFO_FONT_FAMILY = "Georgia";
  private static readonly USER_INFO_BASE_FONT_SIZE = 50;

  private static readonly DIFFICULTY_FONT_FAMILY = "Georgia";

  // Kerning constant matching desktop
  private static readonly WORD_KERNING_BASE = 20;

  /**
   * Render sequence word/title text
   * Matches desktop WordDrawer exactly
   */
  renderWordText(
    canvas: HTMLCanvasElement,
    word: string,
    options: TextRenderOptions
  ): void {
    if (!word || !word.trim()) {
      return; // No word to render
    }

    const ctx = canvas.getContext("2d")!;
    if (!ctx) {
      throw new Error("Canvas context not available");
    }

    // Calculate initial font size and kerning with scaling
    let fontSize = Math.floor(
      TextRenderingService.WORD_BASE_FONT_SIZE * options.beatScale
    );
    const kerning = Math.floor(
      TextRenderingService.WORD_KERNING_BASE * options.beatScale
    );

    // Create initial font
    let font = this.createFont(
      TextRenderingService.WORD_FONT_FAMILY,
      fontSize,
      TextRenderingService.WORD_FONT_WEIGHT
    );

    ctx.font = font;

    // Calculate text width with kerning
    let textWidth = this.measureTextWithKerning(ctx, word, kerning);

    // Auto-scale font to fit width (match desktop logic exactly)
    const maxWidth = canvas.width - canvas.width / 4; // Same as desktop
    const margin = options.margin;

    while (textWidth + 2 * margin > maxWidth && fontSize > 10) {
      fontSize--;
      font = this.createFont(
        TextRenderingService.WORD_FONT_FAMILY,
        fontSize,
        TextRenderingService.WORD_FONT_WEIGHT
      );
      ctx.font = font;
      textWidth = this.measureTextWithKerning(ctx, word, kerning);
    }

    // Position text in top margin area (match desktop)
    const additionalHeightTop = options.additionalHeightTop || 0;
    const textHeight = fontSize;

    // Center vertically in the additional height area
    const y = additionalHeightTop / 2 + textHeight / 2 - textHeight / 10;

    // Center horizontally with kerning consideration
    const totalTextWidth = textWidth + kerning * (word.length - 1);
    const x = (canvas.width - totalTextWidth) / 2;

    // Render text with custom kerning
    ctx.fillStyle = "black";
    ctx.textBaseline = "middle";
    ctx.textAlign = "left";

    this.renderTextWithKerning(ctx, word, x, y, kerning);
  }

  /**
   * Render user information (name, date, notes)
   * Matches desktop UserInfoDrawer exactly with 3-column layout
   */
  renderUserInfo(
    canvas: HTMLCanvasElement,
    userInfo: UserInfo,
    options: TextRenderOptions
  ): void {
    const ctx = canvas.getContext("2d")!;
    if (!ctx) {
      throw new Error("Canvas context not available");
    }

    const margin = options.margin;
    const bottomY = canvas.height - margin;

    // Calculate scaled font sizes
    const baseFontSize = TextRenderingService.USER_INFO_BASE_FONT_SIZE;
    const { fontSize } = this.adjustFontAndMargin(
      baseFontSize,
      margin,
      3,
      options.beatScale
    );

    // Format export date (match desktop formatting)
    const formattedDate = this.formatExportDate(userInfo.exportDate);
    const notes = userInfo.notes || "Created using The Kinetic Alphabet";

    // Left: User name (bold italic)
    ctx.font = this.createFont(
      TextRenderingService.USER_INFO_FONT_FAMILY,
      fontSize,
      "bold",
      true // italic
    );
    ctx.fillStyle = "black";
    ctx.textAlign = "left";
    ctx.textBaseline = "bottom";
    ctx.fillText(userInfo.userName, margin, bottomY);

    // Center: Notes (italic)
    ctx.font = this.createFont(
      TextRenderingService.USER_INFO_FONT_FAMILY,
      fontSize,
      "normal",
      true // italic
    );
    ctx.textAlign = "center";
    ctx.fillText(notes, canvas.width / 2, bottomY);

    // Right: Export date (italic)
    ctx.textAlign = "right";
    ctx.fillText(formattedDate, canvas.width - margin, bottomY);
  }

  /**
   * Render difficulty level badge
   * Matches desktop ImageExportDifficultyLevelDrawer exactly
   */
  renderDifficultyBadge(
    canvas: HTMLCanvasElement,
    level: number,
    position: [number, number],
    size: number
  ): void {
    const ctx = canvas.getContext("2d")!;
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
    ctx.font = this.createFont(
      TextRenderingService.DIFFICULTY_FONT_FAMILY,
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
    const ctx = canvas.getContext("2d")!;

    ctx.font = this.createFont(fontFamily, fontSize, fontWeight);
    const metrics = ctx.measureText(text);

    return {
      width: metrics.width,
      height: fontSize, // Approximation
    };
  }

  /**
   * Apply custom kerning to text
   * Matches desktop kerning implementation exactly
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
   * Create font string for canvas context
   */
  private createFont(
    family: string,
    size: number,
    weight: string = "normal",
    italic: boolean = false
  ): string {
    const style = italic ? "italic" : "normal";
    return `${style} ${weight} ${size}px ${family}`;
  }

  /**
   * Measure text width including kerning
   */
  private measureTextWithKerning(
    ctx: CanvasRenderingContext2D,
    text: string,
    kerning: number
  ): number {
    let totalWidth = 0;

    for (const letter of text) {
      totalWidth += ctx.measureText(letter).width;
    }

    // Add kerning for spaces between letters
    totalWidth += kerning * (text.length - 1);

    return totalWidth;
  }

  /**
   * Adjust font size and margin based on beat count
   * Matches desktop FontMarginHelper.adjust_font_and_margin exactly
   */
  private adjustFontAndMargin(
    baseFontSize: number,
    baseMargin: number,
    beatCount: number,
    beatScale: number
  ): { fontSize: number; margin: number } {
    let fontScale: number;
    let marginScale: number;

    // Match desktop scaling logic exactly
    if (beatCount <= 1) {
      fontScale = 1 / 2.3;
      marginScale = 1 / 3;
    } else if (beatCount === 2) {
      fontScale = 1 / 1.5;
      marginScale = 1 / 2;
    } else {
      fontScale = 1.0;
      marginScale = 1.0;
    }

    const fontSize = Math.max(
      1,
      Math.floor(baseFontSize * fontScale * beatScale)
    );
    const margin = Math.max(
      1,
      Math.floor(baseMargin * marginScale * beatScale)
    );

    return { fontSize, margin };
  }

  /**
   * Format export date to match desktop formatting
   * Matches desktop _format_export_date exactly
   */
  private formatExportDate(dateStr: string): string {
    // Convert "MM-DD-YYYY" to "M-D-YYYY" (remove leading zeros)
    return dateStr
      .split("-")
      .map((part) => parseInt(part).toString())
      .join("-");
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
   * Validate font loading and availability
   * Ensures fonts are ready for rendering
   */
  async validateFonts(): Promise<{ available: boolean; missing: string[] }> {
    const requiredFonts = [
      TextRenderingService.WORD_FONT_FAMILY,
      TextRenderingService.USER_INFO_FONT_FAMILY,
      TextRenderingService.DIFFICULTY_FONT_FAMILY,
    ];

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
    const ctx = canvas.getContext("2d")!;

    // Test with fallback font
    ctx.font = `12px ${fontFamily}, monospace`;
    const testWidth1 = ctx.measureText("test").width;

    // Test with just monospace
    ctx.font = "12px monospace";
    const testWidth2 = ctx.measureText("test").width;

    // If widths are different, the font is available
    return testWidth1 !== testWidth2;
  }

  /**
   * Get recommended text settings for different contexts
   */
  getRecommendedTextSettings(
    context: "word" | "userInfo" | "difficulty",
    beatCount: number,
    beatScale: number
  ): {
    fontFamily: string;
    fontSize: number;
    fontWeight: string;
    italic: boolean;
  } {
    switch (context) {
      case "word": {
        const wordFontSize = Math.floor(
          TextRenderingService.WORD_BASE_FONT_SIZE * beatScale
        );
        return {
          fontFamily: TextRenderingService.WORD_FONT_FAMILY,
          fontSize: wordFontSize,
          fontWeight: TextRenderingService.WORD_FONT_WEIGHT,
          italic: false,
        };
      }

      case "userInfo": {
        const { fontSize } = this.adjustFontAndMargin(
          TextRenderingService.USER_INFO_BASE_FONT_SIZE,
          50,
          beatCount,
          beatScale
        );
        return {
          fontFamily: TextRenderingService.USER_INFO_FONT_FAMILY,
          fontSize,
          fontWeight: "normal",
          italic: true,
        };
      }

      case "difficulty":
        return {
          fontFamily: TextRenderingService.DIFFICULTY_FONT_FAMILY,
          fontSize: 24, // Will be calculated based on badge size
          fontWeight: "bold",
          italic: false,
        };

      default:
        throw new Error(`Unknown context: ${context}`);
    }
  }

  /**
   * Debug method to test text rendering
   */
  debugTextRendering(
    canvas: HTMLCanvasElement,
    testText: string = "Test"
  ): void {
    const ctx = canvas.getContext("2d")!;

    // Clear canvas
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Test word rendering
    this.renderWordText(canvas, testText, {
      margin: 50,
      beatScale: 1,
      additionalHeightTop: 300,
    });

    // Test user info rendering
    this.renderUserInfo(
      canvas,
      {
        userName: "Test User",
        notes: "Test Notes",
        exportDate: "1-1-2024",
      },
      {
        margin: 50,
        beatScale: 1,
      }
    );

    // Test difficulty badge
    this.renderDifficultyBadge(canvas, 3, [50, 50], 100);
  }
}
