/**
 * Title Renderer
 *
 * This module provides functionality to render a title on the canvas.
 */

import type { CanvasDimensions } from './exportTypes';
import {
	calculateOptimalFontSize,
	calculateLayoutAwareFontSize,
	calculateLetterSpacing,
	drawTextWithSpacing,
	type FontOptions
} from './FontSizeHelper';

/**
 * Draws the title on the canvas with responsive sizing
 *
 * @param ctx The canvas rendering context
 * @param title The title to draw
 * @param dimensions Canvas dimensions
 */
export function drawTitle(
	ctx: CanvasRenderingContext2D,
	title: string,
	dimensions: CanvasDimensions
): void {
	if (!title) return;

	const { width, topMargin } = dimensions;

	// Calculate padding (6% of container width to match other elements)
	const padding = Math.round(width * 0.06);

	// Define min/max font sizes - further increased for better readability
	const MIN_FONT_SIZE = 56; // Increased from 48
	const MAX_FONT_SIZE = 200; // Increased from 175 for larger titles

	// Available space is container width minus double padding
	const availableWidth = width - padding * 2;

	// Base font options
	const fontOptions: FontOptions = {
		family: 'Georgia, serif', // Changed from Arial to Georgia to match Python
		size: MAX_FONT_SIZE,
		weight: 'bold',
		style: 'normal'
	};

	// Get the number of rows from dimensions
	const { rows } = dimensions;

	// Calculate optimal font size using layout-aware sizing
	// This ensures consistent visual size across different sequence lengths
	const optimalFontSize = calculateLayoutAwareFontSize(
		ctx,
		title,
		availableWidth,
		fontOptions,
		rows,
		MIN_FONT_SIZE,
		MAX_FONT_SIZE,
		1 // Base row count
	);

	// Update font size
	fontOptions.size = optimalFontSize;

	// Log font size and positioning for debugging
	console.log('TitleRenderer: Font size and positioning calculated', {
		title,
		rows,
		optimalFontSize,
		availableWidth,
		padding,
		topMargin,
		verticalPositionFactor: 0.5,
		centerY: topMargin * 0.5
	});

	// Calculate letter spacing (kerning)
	const letterSpacing = calculateLetterSpacing(
		ctx,
		title,
		availableWidth,
		fontOptions,
		0, // Min spacing
		20 // Max spacing - matches Python implementation
	);

	// Save context for restoration
	ctx.save();

	// Create high-contrast text with shadow for legibility
	// Apply text shadow (2px blur, 50% opacity)
	ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
	ctx.shadowBlur = 2;
	ctx.shadowOffsetX = 1;
	ctx.shadowOffsetY = 1;

	// Position text in the center of the allocated space
	// Adjust vertical position to ensure consistent spacing between title and first row of beats
	const centerX = width / 2;

	// For single-row sequences, position the title properly within the increased top margin
	// This creates more balanced spacing between the title and the first row
	const verticalPositionFactor = dimensions.rows === 1 ? 0.5 : 0.5;
	const centerY = topMargin * verticalPositionFactor;

	// Draw main text with proper color
	ctx.fillStyle = '#000000';

	// If we're using letter spacing, we need to calculate the starting X position
	if (letterSpacing > 0) {
		// Set the font for measurement
		ctx.font = `${fontOptions.style} ${fontOptions.weight} ${fontOptions.size}px ${fontOptions.family}`;

		// Measure the total width with spacing
		const totalWidth = ctx.measureText(title).width + letterSpacing * (title.length - 1);

		// Calculate starting X position to center the text
		const startX = centerX - totalWidth / 2;

		// Draw text with spacing
		drawTextWithSpacing(ctx, title, startX, centerY, fontOptions, letterSpacing);
	} else {
		// Center-align text horizontally for normal drawing
		ctx.textAlign = 'center';
		ctx.textBaseline = 'middle';
		ctx.font = `${fontOptions.style} ${fontOptions.weight} ${fontOptions.size}px ${fontOptions.family}`;
		ctx.fillText(title, centerX, centerY);
	}

	// Restore context
	ctx.restore();
}
