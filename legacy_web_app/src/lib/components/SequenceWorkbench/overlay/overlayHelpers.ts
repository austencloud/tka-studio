/**
 * Sequence Overlay Helpers
 *
 * This module provides utility functions for the sequence overlay component.
 * It uses the same layout algorithm as the BeatFrame component to ensure
 * consistent behavior between the two components.
 */

import { autoAdjustLayout } from '../BeatFrame/beatFrameHelpers';

/**
 * Calculate the optimal cell size for the overlay grid
 * @param beatCount Number of beats in the sequence
 * @param containerWidth Width of the container
 * @param containerHeight Height of the container
 * @param totalRows Number of rows in the grid
 * @param totalCols Number of columns in the grid
 * @returns Optimal cell size in pixels
 */
export function calculateOverlayCellSize(
	beatCount: number,
	containerWidth: number,
	containerHeight: number,
	totalRows: number,
	totalCols: number
): number {
	// Ensure we have valid dimensions
	if (containerWidth <= 0 || containerHeight <= 0 || totalRows <= 0 || totalCols <= 0) {
		return 120; // Default fallback size
	}

	// No gaps between cells in the overlay
	const gap = 0;

	// Calculate total space needed for gaps
	const totalGapWidth = gap * (totalCols - 1);
	const totalGapHeight = gap * (totalRows - 1);

	// Calculate available space after accounting for gaps and padding
	// Use minimal padding to maximize space usage
	const padding = 0;
	const availableWidth = Math.max(0, containerWidth - totalGapWidth - padding * 2);
	const availableHeight = Math.max(0, containerHeight - totalGapHeight - padding * 2);

	// Calculate cell size based on available space in both dimensions
	const cellWidthByContainer = Math.floor(availableWidth / totalCols);
	const cellHeightByContainer = Math.floor(availableHeight / totalRows);

	// Use the smaller dimension to maintain square cells and prevent overflow
	const baseSize = Math.min(cellWidthByContainer, cellHeightByContainer);

	// Apply constraints to ensure cells are not too small or too large
	return Math.min(Math.max(baseSize, 80), 300); // Min 80px, Max 300px
}

/**
 * Calculate the grid layout for the overlay
 * @param beatCount Number of beats in the sequence
 * @param containerWidth Width of the container
 * @param containerHeight Height of the container
 * @param hasStartPosition Whether the sequence has a start position
 * @returns Object with grid layout information
 */
export function calculateOverlayLayout(
	beatCount: number,
	containerWidth: number,
	containerHeight: number,
	hasStartPosition: boolean = true
): {
	rows: number;
	cols: number;
	cellSize: number;
	gridWidth: number;
	gridHeight: number;
	totalCells: number;
} {
	// Use the same layout algorithm as BeatFrame
	const [baseRows, baseCols] = autoAdjustLayout(beatCount);

	// When we have a start position, we need to adjust the layout
	// The first column is reserved for the start position
	let rows, cols;

	// Special case: If we have only a start position with no beats, use a 1x1 grid
	if (hasStartPosition && beatCount === 0) {
		rows = 1;
		cols = 1;
	}
	// Adjust layout for start position if needed for sequences with beats
	else if (hasStartPosition) {
		// Add one column for the start position
		cols = baseCols + 1;

		// Calculate how many rows we need when beats are arranged in columns 2 and onwards
		// We need to ensure we have enough rows for all beats
		const beatsPerRow = baseCols;
		rows = Math.ceil(beatCount / beatsPerRow);
	} else {
		rows = baseRows;
		cols = baseCols;
	}

	// Total columns in the grid
	const totalCols = cols;

	// Calculate cell size
	const cellSize = calculateOverlayCellSize(
		beatCount,
		containerWidth,
		containerHeight,
		rows,
		totalCols
	);

	// Calculate grid dimensions
	const gridWidth = totalCols * cellSize;
	const gridHeight = rows * cellSize;

	// Calculate total number of cells
	const totalCells = hasStartPosition ? beatCount + 1 : beatCount;

	return {
		rows,
		cols: totalCols,
		cellSize,
		gridWidth,
		gridHeight,
		totalCells
	};
}

/**
 * Get the position of a beat in the grid
 * @param index Index of the beat
 * @param cols Number of columns in the grid
 * @param hasStartPosition Whether the grid has a start position in the top-left
 * @param beatCount Number of beats in the sequence (used for special case handling)
 * @returns Object with row and column indices
 */
export function getBeatPosition(
	index: number,
	cols: number,
	hasStartPosition: boolean = true,
	beatCount: number = -1
): { row: number; col: number } {
	// Special case: If we have only a start position with no beats (1x1 grid)
	if (hasStartPosition && beatCount === 0) {
		// In this case, there are no beats to position, but we'll return a default
		return { row: 0, col: 1 };
	} else if (hasStartPosition) {
		// When there's a start position, we need to adjust the layout
		// Beats should be arranged in columns 2 and onwards
		const beatsPerRow = cols - 1; // One less column for beats since column 1 is reserved
		const row = Math.floor(index / beatsPerRow);
		const col = (index % beatsPerRow) + 2; // +2 because column 1 is reserved for start position
		return { row, col };
	} else {
		// Standard layout without start position - use all columns
		const row = Math.floor(index / cols);
		const col = (index % cols) + 1; // +1 for 1-based column index
		return { row, col };
	}
}

/**
 * Calculate the CSS grid template for the overlay
 * @param rows Number of rows in the grid
 * @param cols Number of columns in the grid
 * @param cellSize Size of each cell in pixels
 * @returns CSS grid template string
 */
export function getGridTemplate(rows: number, cols: number, cellSize: number): string {
	return `repeat(${rows}, ${cellSize}px) / repeat(${cols}, ${cellSize}px)`;
}
