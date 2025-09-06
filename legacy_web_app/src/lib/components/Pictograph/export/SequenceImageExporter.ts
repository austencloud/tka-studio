/**
 * Enhanced Image Exporter
 *
 * This module provides functionality to export images with additional elements
 * like title, user info, and difficulty label.
 */

import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';
import { drawDifficultyCircle } from './difficultyCircleDrawer';
import { calculateDimensions } from './CanvasDimensionsCalculator';
import { drawTitle } from './TitleRenderer';
import { drawUserInfo } from './UserInfoRenderer';
import { renderSvgElements } from './SvgElementRenderer';
import type {
	EnhancedExportOptions,
	EnhancedExportResult,
	RequiredExportOptions
} from './exportTypes';

/**
 * Exports a sequence with enhanced features
 *
 * @param containerElement The container element with SVG elements
 * @param options Export options
 * @returns Promise resolving to the export result
 */
export async function exportSequenceImage(
	containerElement: HTMLElement,
	options: EnhancedExportOptions
): Promise<EnhancedExportResult> {
	// Validate environment
	if (!browser) {
		return Promise.reject(new Error('Cannot export: not in browser environment'));
	}

	// Validate element
	if (!containerElement) {
		return Promise.reject(new Error('Cannot export: no container element provided'));
	}

	try {
		console.log('EnhancedExporter: Starting export process');

		// Default options with required fields
		const defaultOptions: Required<Omit<EnhancedExportOptions, 'beats' | 'startPosition'>> = {
			backgroundColor: 'white',
			scale: 2,
			quality: 0.92,
			format: 'png',
			columns: 0, // Value will be ignored, autoAdjustLayout will determine columns
			spacing: 0, // No spacing between cells, consistent with BeatFrame
			includeStartPosition: true, // Always include start position if it exists
			// Enable all enhancement features by default
			addWord: true, // Add sequence title at the top
			addUserInfo: true, // Add user info at the bottom
			addDifficultyLevel: true, // Add difficulty level indicator in top-left
			addBeatNumbers: true, // Add beat numbers
			addReversalSymbols: true, // Add reversal symbols
			title: '',
			userName: 'User',
			notes: 'Created using The Kinetic Alphabet',
			exportDate: new Date().toLocaleDateString(),
			difficultyLevel: 1
		};

		// Merge options with type safety
		const mergedOptions: RequiredExportOptions = {
			...defaultOptions,
			...options,
			beats: options.beats,
			startPosition: options.startPosition || null
		};

		// Find all SVG elements in the container
		const svgElements = Array.from(containerElement.querySelectorAll('svg'));

		if (svgElements.length === 0) {
			throw new Error('No SVG elements found in container');
		}

		console.log(`EnhancedExporter: Found ${svgElements.length} SVG elements`);

		// Find all reversal indicators
		const reversalIndicators = Array.from(containerElement.querySelectorAll('.reversal-indicator'));
		console.log(`EnhancedExporter: Found ${reversalIndicators.length} reversal indicators`);

		// Log detailed information about the start position
		console.log('EnhancedExporter: Start position details', {
			// Start position is now always included if available
			hasStartPosition:
				mergedOptions.startPosition !== null && mergedOptions.startPosition !== undefined,
			startPositionData: mergedOptions.startPosition,
			firstBeatMetadata: mergedOptions.beats[0]?.metadata,
			totalBeats: mergedOptions.beats.length
		});

		// Calculate dimensions
		const dimensions = calculateDimensions(mergedOptions);

		// Create a canvas
		const canvas = document.createElement('canvas');
		const { width, height, topMargin, bottomMargin } = dimensions;
		canvas.width = width;
		canvas.height = height + topMargin + bottomMargin;

		// Get canvas context
		const ctx = canvas.getContext('2d');
		if (!ctx) {
			throw new Error('Failed to get canvas context');
		}

		// Fill background with white to ensure consistent background
		ctx.fillStyle = '#FFFFFF';
		ctx.fillRect(0, 0, canvas.width, canvas.height);

		// Draw title if needed
		if (mergedOptions.addWord && mergedOptions.title) {
			drawTitle(ctx, mergedOptions.title, dimensions);
		}

		// Calculate consistent spacing for visual elements
		// This spacing will be used for both the difficulty circle and user info
		// to ensure visual consistency throughout the image
		const spacingPercentage = 0.15; // 15% of top margin for spacing
		const desiredSpacing = Math.round(topMargin * spacingPercentage);

		// Default adjusted spacing (will be refined for difficulty circle if needed)
		let adjustedSpacing = desiredSpacing;

		// Draw difficulty circle if needed
		if (mergedOptions.addDifficultyLevel) {
			// Calculate the circle size based on the top margin height
			// Make the circle diameter 80-90% of the top margin height
			// For single-row sequences with larger top margins, use a smaller percentage
			const isOneRow = dimensions.rows === 1;
			const circleSizePercentage = 0.35; // 35% of top margin height for radius
			const radius = Math.round(topMargin * circleSizePercentage);

			// Calculate the vertical space between the bottom of the circle and the first beat
			// This is the key calculation for visual consistency
			// The first beat starts at y = topMargin, and the bottom of the circle is at y = circleY + radius

			// Verify that the circle will fit within the top margin with this spacing
			// We need: 2*radius + 2*desiredSpacing <= topMargin
			// If not, adjust the spacing to ensure the circle fits
			const requiredSpace = 2 * radius + 2 * desiredSpacing;
			adjustedSpacing =
				requiredSpace > topMargin
					? Math.max(Math.floor((topMargin - 2 * radius) / 2), Math.floor(radius * 0.1)) // Ensure at least 10% of radius as spacing
					: desiredSpacing;

			// Now calculate the y-position of the circle center such that:
			// (circleY + radius + adjustedSpacing = topMargin)
			// Solving for circleY: circleY = topMargin - radius - adjustedSpacing
			// But we also want to ensure the circle has the same spacing from the top edge
			// So we'll use: circleY = radius + adjustedSpacing
			const circleY = radius + adjustedSpacing;

			// Use the same spacing for the left margin to ensure visual consistency
			// This makes the distance from the left edge to the circle the same as
			// the distance from the bottom of the circle to the first beat
			const circleX = radius + adjustedSpacing;

			// The actual spacing values will be:
			// - Space between top edge and circle: circleY - radius
			// - Space between left edge and circle: circleX - radius
			// - Space between circle and first beat: topMargin - (circleY + radius)
			// These values are logged below for debugging

			// Draw circular difficulty indicator in the top-left corner
			// with appropriate size and position
			drawDifficultyCircle(
				ctx,
				mergedOptions.difficultyLevel,
				circleX, // x position with margin
				circleY, // y position with margin
				radius // radius based on top margin height
			);

			console.log('EnhancedExporter: Positioned difficulty circle', {
				circleX,
				circleY,
				radius,
				diameter: radius * 2,
				topMargin,
				desiredSpacing,
				adjustedSpacing,
				requiredSpace,
				spacingPercentage,
				actualTopSpacing: circleY - radius,
				actualLeftSpacing: circleX - radius,
				actualBottomSpacing: topMargin - (circleY + radius),
				topMarginPercentage: (radius * 2) / topMargin,
				canvasWidth: width,
				rows: dimensions.rows,
				isOneRow,
				circleSizePercentage
			});
		}

		// Process each SVG element
		await renderSvgElements(ctx, svgElements, mergedOptions, dimensions, containerElement);

		// Draw user info if needed
		if (mergedOptions.addUserInfo) {
			// Pass the adjustedSpacing from the difficulty circle to ensure visual consistency
			// This ensures the same spacing is used throughout the image
			drawUserInfo(ctx, mergedOptions, dimensions, adjustedSpacing);
		}

		// Convert canvas to data URL
		const format = mergedOptions.format === 'jpeg' ? 'image/jpeg' : 'image/png';
		const dataUrl = canvas.toDataURL(format, mergedOptions.quality);

		console.log('EnhancedExporter: Export completed successfully', {
			width: canvas.width,
			height: canvas.height,
			dataUrlLength: dataUrl.length
		});

		// Return the result
		return {
			dataUrl,
			width: canvas.width,
			height: canvas.height,
			format: mergedOptions.format
		};
	} catch (error) {
		// Log detailed error information
		logger.error('Error exporting enhanced image', {
			error: error instanceof Error ? error : new Error(String(error))
		});

		// Re-throw the error
		throw new Error(
			`Failed to export enhanced image: ${error instanceof Error ? error.message : String(error)}`
		);
	}
}
