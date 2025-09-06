/**
 * SVG Element Renderer
 *
 * This module provides functionality to render SVG elements on the canvas.
 */

import type { EnhancedExportOptions, CanvasDimensions } from './exportTypes';
import { renderSvgToImage } from './svgRenderer';
import { drawReversalIndicators } from './ReversalIndicatorRenderer';

/**
 * Renders SVG elements to the canvas
 *
 * @param ctx The canvas rendering context
 * @param svgElements The SVG elements to render
 * @param options Export options
 * @param dimensions Canvas dimensions
 * @param containerElement The container element
 * @returns Promise resolving when rendering is complete
 */
export async function renderSvgElements(
	ctx: CanvasRenderingContext2D,
	svgElements: SVGElement[],
	options: EnhancedExportOptions,
	dimensions: CanvasDimensions,
	containerElement: HTMLElement
): Promise<void> {
	const { beatSize, topMargin = 20, columnsForBeats } = dimensions;

	// Get the beat count
	const beatCount = options.beats.length;

	// Find the start position element index and determine if we have a start position
	// In BeatFrame.svelte, the start position is always in the first cell (top-left)
	let startPositionIndex = -1;

	// Try to find the start position element directly from the container
	const startPositionContainer = containerElement.querySelector('.start-position');

	// Always include the start position if it exists
	// This is a temporary fix until the grid layout issues are resolved
	let hasStartPosition = !!options.startPosition || !!startPositionContainer;

	if (startPositionContainer) {
		console.log('EnhancedExporter: Found start position container in DOM, including it in export');

		const startPositionSvg = startPositionContainer.querySelector('svg');
		if (startPositionSvg) {
			// Find the index of this SVG in our svgElements array
			startPositionIndex = svgElements.findIndex((svg) => svg === startPositionSvg);
			console.log(
				'EnhancedExporter: Found start position element directly at index',
				startPositionIndex
			);
		}
	}

	// If we couldn't find it directly, try looking at parent elements of each SVG
	if (startPositionIndex === -1) {
		for (let i = 0; i < svgElements.length; i++) {
			const element = svgElements[i];
			const parent = element.parentElement;
			const grandparent = parent?.parentElement;

			// Check if this is the start position element
			// The start position is in a container with class "start-position"
			if (grandparent?.classList.contains('start-position')) {
				startPositionIndex = i;
				console.log('EnhancedExporter: Found start position element at index', i);
				break;
			}
		}
	}

	console.log('EnhancedExporter: Rendering SVG elements', {
		svgCount: svgElements.length,
		hasStartPosition,
		startPositionIndex,
		columnsForBeats,
		beatCount
	});

	// Process each SVG element
	for (let i = 0; i < svgElements.length; i++) {
		// Skip rendering the start position element if hasStartPosition is false
		if (!hasStartPosition && i === startPositionIndex) {
			console.log(
				'EnhancedExporter: Skipping start position element because hasStartPosition is false'
			);
			continue;
		}

		let x, y;

		if (hasStartPosition && i === startPositionIndex) {
			// This is the start position - place it in its own column on the left (column 1)
			x = 0;
			y = topMargin;
			console.log('EnhancedExporter: Positioning start position at', { x, y });
		} else {
			// This is a regular beat - calculate position in the main grid
			// We need to map the SVG index to the correct beat index
			// If we have a start position, we need to adjust the index
			let beatIndex = i;

			// If we have a start position and this element comes after it in the DOM,
			// we need to subtract 1 to get the correct beat index
			if (hasStartPosition && startPositionIndex >= 0) {
				if (i > startPositionIndex) {
					beatIndex = i - 1;
				} else if (i < startPositionIndex) {
					// This element comes before the start position in the DOM
					// We need to adjust the index accordingly
					beatIndex = i;
				}
			}

			// IMPORTANT: For a 4x4 grid with start position, we need 5 columns total
			// Column 0 is reserved for start position only
			// Regular beats must be in columns 1-4
			// Each row after the first must start at column 1, not column 0

			// Calculate row and column indices
			const rowIndex = Math.floor(beatIndex / columnsForBeats);
			const colIndex = beatIndex % columnsForBeats;

			// ALWAYS add 1 to column index when we have a start position
			// This ensures beats start from column 1, not column 0
			const col = hasStartPosition ? colIndex + 1 : colIndex;
			const row = rowIndex;

			// Calculate x and y coordinates
			x = col * beatSize; // Column 0 is empty except for start position
			y = row * beatSize + topMargin;

			console.log('EnhancedExporter: Positioning beat', beatIndex, 'at', {
				x,
				y,
				row,
				col,
				svgIndex: i
			});
		}

		// Render the SVG to an image
		const result = await renderSvgToImage({
			element: svgElements[i],
			backgroundColor: 'transparent', // Use transparent for individual beats
			scale: 1, // We'll handle scaling at the canvas level
			quality: options.quality || 0.92,
			format: options.format || 'png'
		});

		// Create an image from the data URL
		const img = new Image();
		img.src = result.dataUrl;

		// Wait for the image to load
		await new Promise<void>((resolve, reject) => {
			img.onload = () => resolve();
			img.onerror = () => reject(new Error('Failed to load image'));
		});

		// Draw a black border around the pictograph
		ctx.strokeStyle = 'black';
		ctx.lineWidth = 2;
		ctx.strokeRect(x, y, beatSize, beatSize);

		// Draw the image on the canvas
		ctx.drawImage(img, x, y, beatSize, beatSize);

		console.log(`EnhancedExporter: Processed SVG element ${i + 1}/${svgElements.length}`);

		// If this is a regular beat (not start position), check if it has reversal indicators
		if (!(hasStartPosition && i === startPositionIndex) && options.addReversalSymbols) {
			// Calculate the beat index using the same logic as for positioning
			let beatIndex = i;
			if (hasStartPosition && startPositionIndex >= 0) {
				if (i > startPositionIndex) {
					beatIndex = i - 1;
				}
			}
			const beat = options.beats[beatIndex];

			// Draw reversal indicators if needed
			if (beat) {
				drawReversalIndicators(ctx, beat, x, y, beatSize);
			}
		}
	}
}
