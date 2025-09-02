/**
 * Text Rendering Service
 *
 * Facade service that provides backward compatibility for the original
 * ITextRenderingService interface. This service uses the individual
 * text rendering components via dependency injection.
 *
 * Note: For new development, prefer using the individual components directly:
 * - IWordTextRenderer for word/title text
 * - IUserInfoRenderer for user information
 * - IDifficultyBadgeRenderer for difficulty badges
 * - ITextRenderingUtils for text utilities
 */

import type { ITextRenderingService } from "$contracts";
import type { TextRenderOptions, UserInfo } from "$domain";

import type {
  IDifficultyBadgeRenderer,
  ITextRenderingUtils,
  IUserInfoRenderer,
  IWordTextRenderer,
} from "$contracts/text-rendering-interfaces";
import { inject, injectable } from "inversify";
import { TYPES } from "../../inversify/types";

@injectable()
export class TextRenderingService implements ITextRenderingService {
  constructor(
    @inject(TYPES.IWordTextRenderer) private wordRenderer: IWordTextRenderer,
    @inject(TYPES.IUserInfoRenderer)
    private userInfoRenderer: IUserInfoRenderer,
    @inject(TYPES.IDifficultyBadgeRenderer)
    private difficultyRenderer: IDifficultyBadgeRenderer,
    @inject(TYPES.ITextRenderingUtils) private textUtils: ITextRenderingUtils
  ) {}

  /**
   * Render sequence word/title text
   * Delegates to WordTextRenderer
   */
  renderWordText(
    canvas: HTMLCanvasElement,
    word: string,
    options: TextRenderOptions
  ): void {
    this.wordRenderer.render(canvas, word, options);
  }

  /**
   * Render user information (name, date, notes)
   * Delegates to UserInfoRenderer
   */
  renderUserInfo(
    canvas: HTMLCanvasElement,
    userInfo: UserInfo,
    options: TextRenderOptions
  ): void {
    this.userInfoRenderer.render(canvas, userInfo, options);
  }

  /**
   * Render difficulty level badge
   * Delegates to DifficultyBadgeRenderer
   */
  renderDifficultyBadge(
    canvas: HTMLCanvasElement,
    level: number,
    position: [number, number],
    size: number
  ): void {
    this.difficultyRenderer.render(canvas, level, position, size);
  }

  /**
   * Calculate text dimensions for layout planning
   * Delegates to TextRenderingUtils
   */
  measureText(
    text: string,
    fontFamily: string,
    fontSize: number,
    fontWeight: string = "normal"
  ): { width: number; height: number } {
    return this.textUtils.measureText(text, fontFamily, fontSize, fontWeight);
  }

  /**
   * Apply custom kerning to text
   * Delegates to TextRenderingUtils
   */
  renderTextWithKerning(
    ctx: CanvasRenderingContext2D,
    text: string,
    x: number,
    y: number,
    kerning: number
  ): void {
    this.textUtils.renderTextWithKerning(ctx, text, x, y, kerning);
  }

  // ============================================================================
  // ADDITIONAL UTILITY METHODS (Delegated to components)
  // ============================================================================

  /**
   * Validate font loading and availability
   * Delegates to TextRenderingUtils
   */
  async validateFonts(): Promise<{ available: boolean; missing: string[] }> {
    return this.textUtils.validateFonts();
  }

  /**
   * Get recommended text settings for different contexts
   * Delegates to appropriate renderers
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
      case "word":
        return this.wordRenderer.getRecommendedSettings(beatScale);

      case "userInfo":
        return this.userInfoRenderer.getRecommendedSettings(
          beatCount,
          beatScale
        );

      case "difficulty":
        return this.difficultyRenderer.getRecommendedSettings();

      default:
        throw new Error(`Unknown context: ${context}`);
    }
  }

  /**
   * Debug method to test text rendering
   * Uses individual components for testing
   */
  debugTextRendering(
    canvas: HTMLCanvasElement,
    testText: string = "Test"
  ): void {
    const ctx = canvas.getContext("2d");
    if (!ctx) {
      throw new Error("Failed to get 2D context for font testing");
    }

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
