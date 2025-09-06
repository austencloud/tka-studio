/**
 * Canvas Dimensions Calculator Tests
 *
 * This module tests the canvas dimensions calculator to ensure it correctly
 * calculates dimensions for various scenarios.
 */

import { describe, it, expect } from 'vitest';
import { calculateDimensions } from './CanvasDimensionsCalculator';
import type { EnhancedExportOptions } from './exportTypes';
import type { Beat } from '$lib/types/Beat';

// Create a mock beat for testing
function createMockBeat(beatNumber: number): Beat {
	return {
		id: `beat-${beatNumber}`,
		beatNumber,
		filled: true,
		pictographData: {
			letter: 'A',
			startPos: null,
			endPos: null,
			timing: null,
			direction: null,
			gridMode: 'diamond',
			gridData: null,
			blueMotionData: null,
			redMotionData: null,
			redPropData: null,
			bluePropData: null,
			redArrowData: null,
			blueArrowData: null,
			grid: 'diamond'
		}
	};
}

// Create a mock start position beat
function createMockStartPosition(): Beat {
	return {
		id: 'start-position',
		beatNumber: 0,
		filled: true,
		pictographData: {
			letter: 'S',
			startPos: 'start',
			endPos: null,
			timing: null,
			direction: null,
			gridMode: 'diamond',
			gridData: null,
			blueMotionData: null,
			redMotionData: null,
			redPropData: null,
			bluePropData: null,
			redArrowData: null,
			blueArrowData: null,
			grid: 'diamond'
		}
	};
}

// Create mock export options
function createMockOptions(
	beatCount: number,
	includeStartPosition: boolean
): EnhancedExportOptions {
	const beats = Array.from({ length: beatCount }, (_, i) => createMockBeat(i + 1));
	return {
		beats,
		startPosition: includeStartPosition ? createMockStartPosition() : null,
		includeStartPosition,
		addWord: false,
		addUserInfo: false
	};
}

describe('CanvasDimensionsCalculator', () => {
	// Test with 1 beat with start position
	it('should calculate correct dimensions for 1 beat with start position', () => {
		const options = createMockOptions(1, true);
		const dimensions = calculateDimensions(options);

		// For 1 beat with start position, we expect 2 columns total (1 for start + 1 for beat)
		expect(dimensions.columns).toBe(2);
		expect(dimensions.columnsForBeats).toBe(1);
		expect(dimensions.rows).toBe(1);
	});

	// Test with 2 beats with start position
	it('should calculate correct dimensions for 2 beats with start position', () => {
		const options = createMockOptions(2, true);
		const dimensions = calculateDimensions(options);

		// For 2 beats with start position, we expect 3 columns total (1 for start + 2 for beats)
		expect(dimensions.columns).toBe(3);
		expect(dimensions.columnsForBeats).toBe(2);
		expect(dimensions.rows).toBe(1);
	});

	// Test with 3 beats with start position
	it('should calculate correct dimensions for 3 beats with start position', () => {
		const options = createMockOptions(3, true);
		const dimensions = calculateDimensions(options);

		// For 3 beats with start position, we expect 4 columns total (1 for start + 3 for beats)
		expect(dimensions.columns).toBe(4);
		expect(dimensions.columnsForBeats).toBe(3);
		expect(dimensions.rows).toBe(1);
	});

	// Test with 4 beats with start position
	it('should calculate correct dimensions for 4 beats with start position', () => {
		const options = createMockOptions(4, true);
		const dimensions = calculateDimensions(options);

		// For 4 beats with start position, we expect 5 columns total (1 for start + 4 for beats)
		expect(dimensions.columns).toBe(5);
		expect(dimensions.columnsForBeats).toBe(4);
		expect(dimensions.rows).toBe(1);
	});

	// Test with 5 beats with start position
	it('should calculate correct dimensions for 5 beats with start position', () => {
		const options = createMockOptions(5, true);
		const dimensions = calculateDimensions(options);

		// For 5 beats with start position, we expect 5 columns total (1 for start + 4 for beats)
		// and 2 rows (first row has start + 4 beats, second row has 1 beat)
		expect(dimensions.columns).toBe(5);
		expect(dimensions.columnsForBeats).toBe(4);
		expect(dimensions.rows).toBe(2);
	});

	// Test with 6 beats with start position
	it('should calculate correct dimensions for 6 beats with start position', () => {
		const options = createMockOptions(6, true);
		const dimensions = calculateDimensions(options);

		// For 6 beats with start position, we expect 5 columns total (1 for start + 4 for beats)
		// and 2 rows (first row has start + 4 beats, second row has 2 beats)
		expect(dimensions.columns).toBe(5);
		expect(dimensions.columnsForBeats).toBe(4);
		expect(dimensions.rows).toBe(2);
	});

	// Test without start position
	it('should calculate correct dimensions without start position', () => {
		const options = createMockOptions(4, false);
		const dimensions = calculateDimensions(options);

		// For 4 beats without start position, we expect 4 columns total
		expect(dimensions.columns).toBe(4);
		expect(dimensions.columnsForBeats).toBe(4);
		expect(dimensions.rows).toBe(1);
	});

	// Test with custom columns
	it('should respect custom column count', () => {
		const options = createMockOptions(4, true);
		options.columns = 2; // Override to use 2 columns for beats
		const dimensions = calculateDimensions(options);

		// For 4 beats with start position and 2 columns for beats, we expect 3 columns total (1 for start + 2 for beats)
		// and 2 rows (2 beats per row)
		expect(dimensions.columns).toBe(3);
		expect(dimensions.columnsForBeats).toBe(2);
		expect(dimensions.rows).toBe(2);
	});
});
