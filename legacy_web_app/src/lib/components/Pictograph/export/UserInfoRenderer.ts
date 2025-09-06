/**
 * User Info Renderer
 *
 * This module provides functionality to render user information on the canvas.
 */

import type { CanvasDimensions, EnhancedExportOptions } from './exportTypes';
import {
	calculateOptimalFontSize,
	calculateLayoutAwareFontSize,
	type FontOptions
} from './FontSizeHelper';

/**
 * Draws user info at the bottom of the canvas with responsive sizing
 *
 * @param ctx The canvas rendering context
 * @param options Export options
 * @param dimensions Canvas dimensions
 * @param adjustedSpacing The spacing used for the difficulty circle (for visual consistency)
 */
export function drawUserInfo(
	ctx: CanvasRenderingContext2D,
	options: EnhancedExportOptions,
	dimensions: CanvasDimensions,
	adjustedSpacing?: number
): void {
	const { width, height, topMargin, bottomMargin } = dimensions;

	// Get user info text
	const userName = options.userName || 'User';
	const notes = options.notes || 'Created using The Kinetic Alphabet';
	const exportDate = options.exportDate || new Date().toLocaleDateString();

	// Get the number of rows from dimensions
	const { rows } = dimensions;

	// Calculate consistent spacing for all user info elements
	// If adjustedSpacing is provided, use it for visual consistency with the difficulty circle
	// Otherwise, calculate a default spacing based on the bottom margin
	const spacingPercentage = 0.15; // 15% of bottom margin for spacing (matching difficulty circle)
	const defaultSpacing = Math.round(bottomMargin * spacingPercentage);
	const spacing = adjustedSpacing !== undefined ? adjustedSpacing : defaultSpacing;

	// Use the spacing as the margin for consistent visual appearance
	// This ensures the same spacing is used for all elements throughout the image
	const margin = spacing;

	// Define min/max font sizes with row-based adjustments
	// Increase minimum font size for longer sequences to maintain readability
	const MIN_FONT_SIZE = Math.max(24, 24 + (rows - 1) * 4); // Increase by 4px per row
	const MAX_FONT_SIZE = 60; // Increased from 50 for better readability

	// Calculate base Y position for text - center in the bottom margin
	const baseY = height + topMargin + bottomMargin / 2;

	// Available width for each text element
	const centerTextWidth = width * 0.6; // 60% of width for center text
	const sideTextWidth = width * 0.25; // 25% of width for side texts

	// Base font options for notes (center text)
	const notesFontOptions: FontOptions = {
		family: 'Georgia, serif',
		size: MAX_FONT_SIZE,
		weight: 'normal',
		style: 'italic' // Use italic for notes
	};

	// Calculate optimal font size for notes using layout-aware sizing
	const notesOptimalSize = calculateLayoutAwareFontSize(
		ctx,
		notes,
		centerTextWidth,
		notesFontOptions,
		rows,
		MIN_FONT_SIZE,
		MAX_FONT_SIZE,
		1 // Base row count
	);

	// Update font size
	notesFontOptions.size = notesOptimalSize;

	// Base font options for username (left text) - bold italic
	const userNameFontOptions: FontOptions = {
		family: 'Georgia, serif',
		size: MAX_FONT_SIZE,
		weight: 'bold',
		style: 'italic' // Use bold italic for username
	};

	// Calculate optimal font size for username using layout-aware sizing
	const userNameOptimalSize = calculateLayoutAwareFontSize(
		ctx,
		userName,
		sideTextWidth,
		userNameFontOptions,
		rows,
		MIN_FONT_SIZE,
		MAX_FONT_SIZE,
		1 // Base row count
	);

	// Update font size
	userNameFontOptions.size = userNameOptimalSize;

	// Base font options for date (right text) - italic
	const dateFontOptions: FontOptions = {
		family: 'Georgia, serif',
		size: MAX_FONT_SIZE,
		weight: 'normal',
		style: 'italic' // Use italic for date
	};

	// Calculate optimal font size for date using layout-aware sizing
	const dateOptimalSize = calculateLayoutAwareFontSize(
		ctx,
		exportDate,
		sideTextWidth,
		dateFontOptions,
		rows,
		MIN_FONT_SIZE,
		MAX_FONT_SIZE,
		1 // Base row count
	);

	// Update font size
	dateFontOptions.size = dateOptimalSize;

	// Log font sizes for debugging
	console.log('UserInfoRenderer: Font sizes calculated', {
		rows,
		notesOptimalSize,
		userNameOptimalSize,
		dateOptimalSize,
		MIN_FONT_SIZE
	});

	// Save context for restoration
	ctx.save();

	// Apply subtle text shadow for better legibility
	ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
	ctx.shadowBlur = 2;
	ctx.shadowOffsetX = 1;
	ctx.shadowOffsetY = 1;

	// Calculate vertical position with consistent spacing
	// Position the text with the same spacing from the bottom of the last row of beats
	// as the difficulty circle has from the top and left edges

	// The bottom of the last row of beats is at y = height + topMargin
	// We want to position the text below this with consistent spacing

	// Position the text directly in the vertical center of the bottom margin area
	// This ensures proper vertical centering without the separator line
	const textY = height + topMargin + bottomMargin / 2;

	// Log positioning information
	console.log('UserInfoRenderer: Text positioning', {
		margin,
		spacing,
		textY,
		bottomMargin,
		bottomOfBeats: height + topMargin,
		canvasHeight: height + topMargin + bottomMargin
	});

	// Separator line removed to prevent text overflow issues

	// Draw notes text (center)
	ctx.textAlign = 'center';
	ctx.textBaseline = 'middle';
	ctx.fillStyle = '#000000';
	ctx.font = `${notesFontOptions.style} ${notesFontOptions.weight} ${notesFontOptions.size}px ${notesFontOptions.family}`;
	ctx.fillText(notes, width / 2, textY);

	// Draw username text (left)
	ctx.textAlign = 'left';
	ctx.fillStyle = '#000000';
	ctx.font = `${userNameFontOptions.style} ${userNameFontOptions.weight} ${userNameFontOptions.size}px ${userNameFontOptions.family}`;
	ctx.fillText(userName, margin, textY);

	// Draw export date text (right)
	ctx.textAlign = 'right';
	ctx.fillStyle = '#000000';
	ctx.font = `${dateFontOptions.style} ${dateFontOptions.weight} ${dateFontOptions.size}px ${dateFontOptions.family}`;
	ctx.fillText(exportDate, width - margin, textY);

	// Restore context
	ctx.restore();
}
