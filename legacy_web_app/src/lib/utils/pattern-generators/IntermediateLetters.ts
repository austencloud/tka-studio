import { generatePatternRow } from './PatternGenerator';
import { positionCycles } from './PatternGenerator';
import type { PatternRow } from './PatternGenerator';

// Generate patterns for Letter D (beta to alpha transitions with alternating timing)
export function generateLetterD(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'D';
	const direction = 'opp';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define specific transitions
	const transitions = [
		{ startPos: 'beta3', endPos: 'alpha5', timing: 'split' },
		{ startPos: 'beta5', endPos: 'alpha7', timing: 'tog' },
		{ startPos: 'beta7', endPos: 'alpha1', timing: 'split' },
		{ startPos: 'beta1', endPos: 'alpha3', timing: 'tog' },
		{ startPos: 'beta7', endPos: 'alpha5', timing: 'split' },
		{ startPos: 'beta1', endPos: 'alpha7', timing: 'tog' },
		{ startPos: 'beta5', endPos: 'alpha3', timing: 'tog' },
		{ startPos: 'beta3', endPos: 'alpha1', timing: 'split' }
	];

	// Generate first set with ccw/cw rotation
	transitions.slice(0, 4).forEach(({ startPos, endPos, timing }) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing,
				direction,
				blueMotion,
				blueRotDir: 'ccw',
				redMotion,
				redRotDir: 'cw'
			})
		);
	});

	// Generate second set with cw/ccw rotation
	transitions.slice(4).forEach(({ startPos, endPos, timing }) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing,
				direction,
				blueMotion,
				blueRotDir: 'cw',
				redMotion,
				redRotDir: 'ccw'
			})
		);
	});

	return patterns;
}

// Generate patterns for Letter E (dash motions in alpha system)
export function generateLetterE(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'E';
	const timing = 'tog';
	const direction = 'opp';
	const blueMotion = 'dash';
	const redMotion = 'dash';
	const blueRotDir = 'no_rot';
	const redRotDir = 'no_rot';

	// Generate dash patterns for all alpha positions
	positionCycles.alpha.cw.forEach((startPos) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos: startPos, // Same position for dash motion
				timing,
				direction,
				blueMotion,
				blueRotDir,
				redMotion,
				redRotDir
			})
		);
	});

	return patterns;
}

// Generate patterns for Letter F (float motions in beta system)
export function generateLetterF(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'F';
	const timing = 'split';
	const direction = 'same';
	const blueMotion = 'float';
	const redMotion = 'float';

	// First set: Clockwise float
	positionCycles.beta.cw.forEach((startPos, i) => {
		const endPos = positionCycles.beta.cw[(i + 1) % 4];

		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing,
				direction,
				blueMotion,
				blueRotDir: 'cw',
				redMotion,
				redRotDir: 'cw'
			})
		);
	});

	// Second set: Counterclockwise float
	positionCycles.beta.ccw.forEach((startPos, i) => {
		const endPos = positionCycles.beta.ccw[(i + 1) % 4];

		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing,
				direction,
				blueMotion,
				blueRotDir: 'ccw',
				redMotion,
				redRotDir: 'ccw'
			})
		);
	});

	return patterns;
}

// Generate patterns for Letter G (gamma with mixed motions)
export function generateLetterG(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'G';
	const timing = 'tog';
	const direction = 'opp';

	// Define mixed motion patterns
	const motionPatterns = [
		{ startPos: 'gamma3', endPos: 'gamma7', blueMotion: 'pro', redMotion: 'float' },
		{ startPos: 'gamma7', endPos: 'gamma11', blueMotion: 'float', redMotion: 'pro' },
		{ startPos: 'gamma11', endPos: 'gamma15', blueMotion: 'pro', redMotion: 'float' },
		{ startPos: 'gamma15', endPos: 'gamma3', blueMotion: 'float', redMotion: 'pro' }
	];

	// Generate mixed motion patterns
	motionPatterns.forEach(({ startPos, endPos, blueMotion, redMotion }) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing,
				direction,
				blueMotion,
				blueRotDir: 'cw',
				redMotion,
				redRotDir: 'ccw'
			})
		);
	});

	return patterns;
}

// Generate patterns for Letter H (alpha-beta alternations)
export function generateLetterH(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'H';
	const timing = 'split';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define alpha-beta transitions
	const transitions = [
		{ startPos: 'alpha3', endPos: 'beta3' },
		{ startPos: 'beta3', endPos: 'alpha5' },
		{ startPos: 'alpha5', endPos: 'beta5' },
		{ startPos: 'beta5', endPos: 'alpha7' },
		{ startPos: 'alpha7', endPos: 'beta7' },
		{ startPos: 'beta7', endPos: 'alpha1' },
		{ startPos: 'alpha1', endPos: 'beta1' },
		{ startPos: 'beta1', endPos: 'alpha3' }
	];

	// Generate with clockwise rotation for both props
	transitions.forEach(({ startPos, endPos }) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing,
				direction,
				blueMotion,
				blueRotDir: 'cw',
				redMotion,
				redRotDir: 'cw'
			})
		);
	});

	return patterns;
}

// Generate patterns for Letter I (vertical static motions in beta positions)
export function generateLetterI(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'I';
	const timing = 'split';
	const direction = 'same';
	const blueMotion = 'static';
	const redMotion = 'static';
	const blueRotDir = 'no_rot';
	const redRotDir = 'no_rot';

	// Only use beta1 and beta5 (north and south positions)
	const verticalPositions = ['beta1', 'beta5'];

	// Generate static patterns for vertical positions
	verticalPositions.forEach((startPos) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos: startPos, // Same position for static motion
				timing,
				direction,
				blueMotion,
				blueRotDir,
				redMotion,
				redRotDir
			})
		);
	});

	return patterns;
}

// Generate patterns for Letter J (counterclockwise hook pattern)
export function generateLetterJ(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'J';
	const timing = 'tog';
	const direction = 'opp';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define hook pattern (vertical line with curve at bottom)
	const transitions = [
		{ startPos: 'beta1', endPos: 'beta5', blueRotDir: 'ccw', redRotDir: 'cw' },
		{ startPos: 'beta5', endPos: 'alpha7', blueRotDir: 'ccw', redRotDir: 'cw' }
	];

	// Generate J hook pattern
	transitions.forEach(({ startPos, endPos, blueRotDir, redRotDir }) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing,
				direction,
				blueMotion,
				blueRotDir,
				redMotion,
				redRotDir
			})
		);
	});

	return patterns;
}

// Generate patterns for Letter K (gamma diagonal transitions)
export function generateLetterK(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'K';
	const timing = 'tog';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define diagonal transitions for K shape
	const transitions = [
		{ startPos: 'gamma3', endPos: 'gamma13', blueRotDir: 'ccw', redRotDir: 'ccw' },
		{ startPos: 'gamma3', endPos: 'gamma11', blueRotDir: 'cw', redRotDir: 'cw' }
	];

	// Generate K diagonal patterns
	transitions.forEach(({ startPos, endPos, blueRotDir, redRotDir }) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing,
				direction,
				blueMotion,
				blueRotDir,
				redMotion,
				redRotDir
			})
		);
	});

	return patterns;
}

// Generate patterns for Letter L (right angle in beta system)
export function generateLetterL(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'L';
	const timing = 'split';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';
	const blueRotDir = 'cw';
	const redRotDir = 'cw';

	// Define L shape pattern (vertical line with horizontal at bottom)
	const transitions = [
		{ startPos: 'beta1', endPos: 'beta5' }, // Vertical line
		{ startPos: 'beta5', endPos: 'beta7' } // Horizontal line at bottom
	];

	// Generate L shape pattern
	transitions.forEach(({ startPos, endPos }) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing,
				direction,
				blueMotion,
				blueRotDir,
				redMotion,
				redRotDir
			})
		);
	});

	return patterns;
}

// Generate patterns for Letter M (gamma quarter transitions)
export function generateLetterM(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'M';
	const timing = 'quarter';
	const direction = 'opp';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Process quarter1 cycle with ccw/cw rotation
	positionCycles.gamma.quarter1.forEach(([startPos, endPos]) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing,
				direction,
				blueMotion,
				blueRotDir: 'ccw',
				redMotion,
				redRotDir: 'cw'
			})
		);
	});

	// Process reverse quarter1 cycle with cw/ccw rotation
	positionCycles.gamma.quarter1.forEach(([endPos, startPos]) => {
		// Note the swap
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing,
				direction,
				blueMotion,
				blueRotDir: 'cw',
				redMotion,
				redRotDir: 'ccw'
			})
		);
	});

	return patterns;
}
