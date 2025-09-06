import { autoAdjustLayout } from '$lib/components/SequenceWorkbench/BeatFrame/beatFrameHelpers';
import type { CanvasDimensions, EnhancedExportOptions } from './exportTypes';

export function calculateDimensions(options: EnhancedExportOptions): CanvasDimensions {
	const beatSize = 950;
	const hasStartPosition = options.includeStartPosition;
	const beatCount = options.beats.length;

	let columnsForBeats;
	if (options.columns && options.columns > 0) {
		columnsForBeats = options.columns;
	} else {
		if (beatCount <= 1) {
			columnsForBeats = 1;
		} else if (beatCount <= 2) {
			columnsForBeats = 2;
		} else if (beatCount <= 3) {
			columnsForBeats = 3;
		} else {
			const [_, cols] = autoAdjustLayout(beatCount);
			columnsForBeats = cols;
		}
	}

	const rowsForBeats = Math.ceil(beatCount / columnsForBeats);
	const totalColumns = hasStartPosition ? columnsForBeats + 1 : columnsForBeats;
	const width = totalColumns * beatSize;
	const height = rowsForBeats * beatSize;

	// Calculate margins with optimized sizing for better readability
	// Adjust margins based on row count to maintain visual balance

	// Base minimum margins
	// Significantly increase top margin for single-row sequences to properly fit the title
	let MIN_TOP_MARGIN = rowsForBeats === 1 ? 250 : 150; // Significantly increased for single-row sequences
	let MIN_BOTTOM_MARGIN = 110; // Slightly reduced from 120 (by about 10%)

	// Adjust minimum margins based on row count
	// For longer sequences (more rows), we can reduce the margins proportionally
	if (rowsForBeats > 1) {
		// Reduce margins for multi-row layouts
		// For 2 rows: 85% of base, 3 rows: 75% of base, 4 rows: 65% of base
		const marginScaleFactor = Math.max(0.65, 1 - (rowsForBeats - 1) * 0.15);
		MIN_TOP_MARGIN = Math.round(MIN_TOP_MARGIN * marginScaleFactor);
		MIN_BOTTOM_MARGIN = Math.round(MIN_BOTTOM_MARGIN * marginScaleFactor);
	}

	// Calculate percentage-based margins with row-aware scaling
	// For longer sequences, use smaller percentages
	// Significantly increase top margin percentage for single-row sequences
	const topMarginPercentage =
		rowsForBeats === 1
			? 0.25 // 25% for single-row sequences (significantly increased from 18%)
			: Math.max(0.08, 0.15 - (rowsForBeats - 1) * 0.02);

	// Slightly reduce bottom margin percentage
	const bottomMarginPercentage = Math.max(0.05, 0.1 - (rowsForBeats - 1) * 0.02);

	// Calculate margins with adjusted percentages
	const calculatedTopMargin = options.addWord ? Math.round(height * topMarginPercentage) : 0;
	const calculatedBottomMargin = options.addUserInfo
		? Math.round(height * bottomMarginPercentage)
		: 0;

	// Use the larger of the calculated or minimum values
	const topMargin = options.addWord ? Math.max(calculatedTopMargin, MIN_TOP_MARGIN) : 0;
	const bottomMargin = options.addUserInfo
		? Math.max(calculatedBottomMargin, MIN_BOTTOM_MARGIN)
		: 0;

	console.log('EnhancedExporter: Layout calculated', {
		beatCount,
		rowsForBeats,
		columnsForBeats,
		totalColumns,
		hasStartPosition,
		width,
		height,
		topMargin,
		bottomMargin,
		calculatedTopMargin,
		MIN_TOP_MARGIN,
		topMarginPercentage
	});

	return {
		width,
		height,
		topMargin,
		bottomMargin,
		beatSize,
		rows: rowsForBeats,
		columns: totalColumns,
		columnsForBeats
	};
}
