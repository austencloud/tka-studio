/**
 * Text Rendering Component Interfaces
 *
 * Proper interfaces for individual text rendering components,
 * enabling proper dependency injection and testability.
 */

import type { TextRenderOptions, UserInfo } from "$domain";

/**
 * Word text rendering interface
 * Handles sequence word/title text with font scaling and kerning
 */
export interface IWordTextRenderer {
  /**
   * Render sequence word/title text
   */
  render(
    canvas: HTMLCanvasElement,
    word: string,
    options: TextRenderOptions
  ): void;

  /**
   * Get recommended word text settings
   */
  getRecommendedSettings(beatScale: number): {
    fontFamily: string;
    fontSize: number;
    fontWeight: string;
    italic: boolean;
  };
}

/**
 * User info rendering interface
 * Handles 3-column user information layout
 */
export interface IUserInfoRenderer {
  /**
   * Render user information (name, date, notes)
   */
  render(
    canvas: HTMLCanvasElement,
    userInfo: UserInfo,
    options: TextRenderOptions
  ): void;

  /**
   * Get recommended user info text settings
   */
  getRecommendedSettings(
    beatCount: number,
    beatScale: number
  ): {
    fontFamily: string;
    fontSize: number;
    fontWeight: string;
    italic: boolean;
  };
}

/**
 * Difficulty badge rendering interface
 * Handles difficulty level badges with gradients
 */
export interface IDifficultyBadgeRenderer {
  /**
   * Render difficulty level badge
   */
  render(
    canvas: HTMLCanvasElement,
    level: number,
    position: [number, number],
    size: number
  ): void;

  /**
   * Get recommended difficulty badge settings
   */
  getRecommendedSettings(): {
    fontFamily: string;
    fontSize: number;
    fontWeight: string;
    italic: boolean;
  };
}

/**
 * Text utilities interface
 * Common text measurement and rendering utilities
 */
export interface ITextRenderingUtils {
  /**
   * Calculate text dimensions for layout planning
   */
  measureText(
    text: string,
    fontFamily: string,
    fontSize: number,
    fontWeight?: string
  ): { width: number; height: number };

  /**
   * Apply custom kerning to text
   */
  renderTextWithKerning(
    ctx: CanvasRenderingContext2D,
    text: string,
    x: number,
    y: number,
    kerning: number
  ): void;

  /**
   * Validate font loading and availability
   */
  validateFonts(): Promise<{ available: boolean; missing: string[] }>;
}
