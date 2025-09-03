/**
 * Font Size Helper
 *
 * This module provides utilities for dynamically sizing text to fit available space
 * similar to the Python implementation.
 */

/**
 * Font options for text rendering
 */
export interface FontOptions {
	family: string;
	size: number;
	weight: string;
	style?: string;
}

/**
 * Creates a CSS font string from font options
 *
 * @param options Font options
 * @returns CSS font string
 */
export function createFontString(options: FontOptions): string {
	const { family, size, weight, style = 'normal' } = options;
	return `${style} ${weight} ${size}px ${family}`;
}

/**
 * Measures text width using the canvas context
 *
 * @param ctx Canvas context
 * @param text Text to measure
 * @param font Font options or CSS font string
 * @returns Text width in pixels
 */
export function measureTextWidth(
	ctx: CanvasRenderingContext2D,
	text: string,
	font: FontOptions | string
): number {
	// Save current font
	const currentFont = ctx.font;

	// Set font for measurement
	if (typeof font === 'string') {
		ctx.font = font;
	} else {
		ctx.font = createFontString(font);
	}

	// Measure text
	const metrics = ctx.measureText(text);
	const width = metrics.width;

	// Restore original font
	ctx.font = currentFont;

	return width;
}

/**
 * Calculates the optimal font size to fit text within available width
 *
 * @param ctx Canvas context
 * @param text Text to fit
 * @param maxWidth Maximum available width
 * @param fontOptions Base font options
 * @param minSize Minimum font size (default: 12)
 * @param maxSize Maximum font size (default: 200)
 * @returns Optimal font size
 */
export function calculateOptimalFontSize(
	ctx: CanvasRenderingContext2D,
	text: string,
	maxWidth: number,
	fontOptions: FontOptions,
	minSize: number = 12,
	maxSize: number = 200
): number {
	// Start with the maximum size
	let size = maxSize;
	let currentOptions = { ...fontOptions, size };

	// Binary search for optimal size
	let low = minSize;
	let high = maxSize;

	while (low <= high) {
		const mid = Math.floor((low + high) / 2);
		currentOptions.size = mid;

		const width = measureTextWidth(ctx, text, currentOptions);

		if (width <= maxWidth) {
			// This size fits, try a larger one
			low = mid + 1;
			size = mid; // Update the current best size
		} else {
			// This size is too large
			high = mid - 1;
		}
	}

	// Return the optimal size
	return size;
}

/**
 * Calculates font size based on sequence layout to ensure consistent sizing
 * across different sequence lengths
 *
 * @param ctx Canvas context
 * @param text Text to fit
 * @param maxWidth Maximum available width
 * @param fontOptions Base font options
 * @param rows Number of rows in the sequence layout
 * @param minSize Minimum font size
 * @param maxSize Maximum font size
 * @param baseRowCount Base row count for scaling (default: 1)
 * @returns Optimal font size adjusted for sequence layout
 */
export function calculateLayoutAwareFontSize(
	ctx: CanvasRenderingContext2D,
	text: string,
	maxWidth: number,
	fontOptions: FontOptions,
	rows: number,
	minSize: number = 12,
	maxSize: number = 200,
	baseRowCount: number = 1
): number {
	// Calculate the base optimal font size
	const optimalSize = calculateOptimalFontSize(ctx, text, maxWidth, fontOptions, minSize, maxSize);

	// For single row layouts, use the optimal size directly
	if (rows <= baseRowCount) {
		return optimalSize;
	}

	// For multi-row layouts, apply a scaling factor to maintain visual consistency
	// The scaling factor increases as the number of rows increases
	// This ensures text doesn't appear too small on larger layouts

	// Calculate scaling factor based on row count
	// For 2 rows: 1.25x, 3 rows: 1.5x, 4 rows: 1.75x
	// Increased from previous values (1.2x, 1.4x, 1.6x) for better consistency
	const scalingFactor = 1 + (rows - baseRowCount) * 0.25;

	// Apply scaling factor to the optimal size
	const scaledSize = Math.round(optimalSize * scalingFactor);

	// Ensure the scaled size doesn't exceed the maximum
	return Math.min(scaledSize, maxSize);
}

/**
 * Calculates letter spacing (kerning) based on text length and available width
 *
 * @param ctx Canvas context
 * @param text Text to space
 * @param maxWidth Maximum available width
 * @param fontOptions Font options
 * @param minSpacing Minimum spacing (default: 0)
 * @param maxSpacing Maximum spacing (default: 20)
 * @returns Optimal letter spacing in pixels
 */
export function calculateLetterSpacing(
	ctx: CanvasRenderingContext2D,
	text: string,
	maxWidth: number,
	fontOptions: FontOptions,
	minSpacing: number = 0,
	maxSpacing: number = 20
): number {
	// If text is empty or single character, no spacing needed
	if (!text || text.length <= 1) return 0;

	// Measure text width without spacing
	const textWidth = measureTextWidth(ctx, text, fontOptions);

	// If text already fits with no spacing, return minimum
	if (textWidth <= maxWidth) return minSpacing;

	// Calculate available space for spacing
	const availableSpace = maxWidth - textWidth;
	const charCount = text.length - 1; // Spaces between characters

	// Calculate spacing per character
	const spacing = Math.min(maxSpacing, availableSpace / charCount);

	// Return spacing (minimum 0)
	return Math.max(minSpacing, spacing);
}

/**
 * Draws text with custom letter spacing
 *
 * @param ctx Canvas context
 * @param text Text to draw
 * @param x Starting X position
 * @param y Y position
 * @param fontOptions Font options
 * @param letterSpacing Letter spacing in pixels
 */
export function drawTextWithSpacing(
	ctx: CanvasRenderingContext2D,
	text: string,
	x: number,
	y: number,
	fontOptions: FontOptions,
	letterSpacing: number = 0
): void {
	// Set font
	ctx.font = createFontString(fontOptions);

	// If no spacing, draw normally
	if (letterSpacing <= 0) {
		ctx.fillText(text, x, y);
		return;
	}

	// Draw each character with spacing
	let currentX = x;
	for (let i = 0; i < text.length; i++) {
		const char = text[i];
		ctx.fillText(char, currentX, y);
		currentX += measureTextWidth(ctx, char, fontOptions) + letterSpacing;
	}
}
