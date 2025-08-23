/**
 * Shared types and utilities for text rendering components
 */

export interface FontSettings {
  family: string;
  size: number;
  weight: string;
  italic: boolean;
}

export interface TextMeasurement {
  width: number;
  height: number;
}

export interface GradientStop {
  position: number;
  color: string;
}

/**
 * Create font string for canvas context
 */
export function createFont(
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
export function measureTextWithKerning(
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
 * Apply custom kerning to text
 */
export function renderTextWithKerning(
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
