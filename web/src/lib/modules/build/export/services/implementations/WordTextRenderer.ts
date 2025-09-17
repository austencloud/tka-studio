/**
 * Word Text Renderer
 *
 * Handles rendering of sequence word/title text with font scaling and kerning.
 * Matches desktop WordDrawer exactly.
 */

import { injectable } from "inversify";
import type { TextRenderOptions } from "../../domain/models";
import type { IWordTextRenderer } from "../contracts";
import { createFont, getCanvasContext, measureTextWithKerning, renderTextWithKerning } from "./TextRenderingTypes";


@injectable()
export class WordTextRenderer implements IWordTextRenderer {
  // Font constants matching desktop application
  private static readonly WORD_FONT_FAMILY = "Georgia";
  private static readonly WORD_BASE_FONT_SIZE = 175;
  private static readonly WORD_FONT_WEIGHT = "600"; // DemiBold
  private static readonly WORD_KERNING_BASE = 20;

  /**
   * Render sequence word/title text
   * Matches desktop WordDrawer exactly
   */
  render(
    canvas: HTMLCanvasElement,
    word: string,
    options: TextRenderOptions
  ): void {
    if (!word || !word.trim()) {
      return; // No word to render
    }

    const ctx = getCanvasContext(canvas);

    // Calculate initial font size and kerning with scaling
    let fontSize = Math.floor(
      WordTextRenderer.WORD_BASE_FONT_SIZE * options.beatScale
    );
    const kerning = Math.floor(
      WordTextRenderer.WORD_KERNING_BASE * options.beatScale
    );

    // Create initial font
    let font = createFont(
      WordTextRenderer.WORD_FONT_FAMILY,
      fontSize,
      WordTextRenderer.WORD_FONT_WEIGHT
    );

    ctx.font = font;

    // Calculate text width with kerning
    let textMetrics = measureTextWithKerning(ctx, word, kerning);
    let textWidth = typeof textMetrics === 'number' ? textMetrics : textMetrics.width;

    // Auto-scale font to fit width (match desktop logic exactly)
    const maxWidth = canvas.width - canvas.width / 4; // Same as desktop
    const margin = options.margin;

    while (textWidth + 2 * margin > maxWidth && fontSize > 10) {
      fontSize--;
      font = createFont(
        WordTextRenderer.WORD_FONT_FAMILY,
        fontSize,
        WordTextRenderer.WORD_FONT_WEIGHT
      );
      ctx.font = font;
      const newTextMetrics = measureTextWithKerning(ctx, word, kerning);
      textWidth = typeof newTextMetrics === 'number' ? newTextMetrics : newTextMetrics.width;
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

    renderTextWithKerning(ctx, word, x, y, kerning);
  }

  /**
   * Get recommended word text settings
   */
  getRecommendedSettings(beatScale: number): {
    fontFamily: string;
    fontSize: number;
    fontWeight: string;
    italic: boolean;
  } {
    const wordFontSize = Math.floor(
      WordTextRenderer.WORD_BASE_FONT_SIZE * beatScale
    );
    return {
      fontFamily: WordTextRenderer.WORD_FONT_FAMILY,
      fontSize: wordFontSize,
      fontWeight: WordTextRenderer.WORD_FONT_WEIGHT,
      italic: false,
    };
  }
}
