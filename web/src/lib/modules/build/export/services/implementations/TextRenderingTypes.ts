/**
 * Text Rendering Types and Utilities
 *
 * Consolidated text rendering utilities used across text rendering services.
 * Provides font creation, text measurement, kerning functionality, and canvas utilities.
 *
 * This file consolidates functionality from TextRenderingUtils to eliminate redundancy.
 */

export interface FontConfig {
  family: string;
  size: number;
  weight: string;
  style: string;
}

export interface TextMetrics {
  width: number;
  height: number;
  actualBoundingBoxLeft: number;
  actualBoundingBoxRight: number;
  actualBoundingBoxAscent: number;
  actualBoundingBoxDescent: number;
}

/**
 * Create a font string from configuration
 */
export function createFont(config: FontConfig): string;
export function createFont(family: string, size: number, weight?: string, style?: string): string;
export function createFont(
  configOrFamily: FontConfig | string,
  size?: number,
  weight: string = 'normal',
  style: string = 'normal'
): string {
  if (typeof configOrFamily === 'object') {
    const config = configOrFamily;
    return `${config.style} ${config.weight} ${config.size}px ${config.family}`;
  } else {
    const family = configOrFamily;
    return `${style} ${weight} ${size}px ${family}`;
  }
}

/**
 * Measure text with kerning adjustments
 */
export function measureTextWithKerning(
  ctx: CanvasRenderingContext2D,
  text: string,
  kerning?: number
): TextMetrics;
export function measureTextWithKerning(
  text: string,
  fontFamily: string,
  fontSize: number,
  fontWeight?: string
): number;
export function measureTextWithKerning(
  ctxOrText: CanvasRenderingContext2D | string,
  textOrFontFamily?: string,
  kerningOrFontSize?: number,
  fontWeight?: string
): TextMetrics | number {
  if (typeof ctxOrText === 'string') {
    // Legacy signature: measureTextWithKerning(text, fontFamily, fontSize, fontWeight)
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d')!;
    ctx.font = createFont(textOrFontFamily!, kerningOrFontSize!, fontWeight);
    return ctx.measureText(ctxOrText).width;
  } else {
    // New signature: measureTextWithKerning(ctx, text, kerning)
    const ctx = ctxOrText;
    const text = textOrFontFamily!;
    const kerning = kerningOrFontSize || 0;
    const metrics = ctx.measureText(text);

    // Adjust width for kerning
    const adjustedWidth = metrics.width + (kerning * (text.length - 1));

    return {
      width: adjustedWidth,
      height: metrics.actualBoundingBoxAscent + metrics.actualBoundingBoxDescent,
      actualBoundingBoxLeft: metrics.actualBoundingBoxLeft,
      actualBoundingBoxRight: metrics.actualBoundingBoxRight,
      actualBoundingBoxAscent: metrics.actualBoundingBoxAscent,
      actualBoundingBoxDescent: metrics.actualBoundingBoxDescent,
    };
  }
}

/**
 * Render text with custom kerning
 */
export function renderTextWithKerning(
  ctx: CanvasRenderingContext2D,
  text: string,
  x: number,
  y: number,
  kerning: number = 0
): void {
  if (kerning === 0) {
    ctx.fillText(text, x, y);
    return;
  }

  let currentX = x;
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    ctx.fillText(char, currentX, y);
    
    const charWidth = ctx.measureText(char).width;
    currentX += charWidth + kerning;
  }
}

/**
 * Get default font configuration
 */
export function getDefaultFont(): FontConfig {
  return {
    family: 'Arial, sans-serif',
    size: 16,
    weight: 'normal',
    style: 'normal'
  };
}

/**
 * Validate font availability
 */
export function validateFont(fontFamily: string): boolean {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  if (!ctx) return false;

  // Test with a known fallback
  ctx.font = `16px ${fontFamily}, Arial`;
  const testWidth = ctx.measureText('Test').width;

  ctx.font = '16px Arial';
  const fallbackWidth = ctx.measureText('Test').width;

  return testWidth !== fallbackWidth;
}

/**
 * Get canvas context with error handling
 * Consolidated utility to avoid repetitive context retrieval code
 */
export function getCanvasContext(canvas: HTMLCanvasElement): CanvasRenderingContext2D {
  const ctx = canvas.getContext('2d');
  if (!ctx) {
    throw new Error('Canvas context not available');
  }
  return ctx;
}

/**
 * Validate font loading and availability for multiple fonts
 */
export function validateFonts(requiredFonts: string[] = ['Georgia']): { available: boolean; missing: string[] } {
  const missing: string[] = [];

  for (const font of requiredFonts) {
    if (!validateFont(font)) {
      missing.push(font);
    }
  }

  return {
    available: missing.length === 0,
    missing,
  };
}
