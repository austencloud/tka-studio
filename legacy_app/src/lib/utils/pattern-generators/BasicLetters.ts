import { generatePatternRow } from './PatternGenerator';
import { positionCycles } from './PatternGenerator';
import type { PatternRow } from './PatternGenerator';

// Generate patterns for Letter A (alpha system, clockwise and counterclockwise)
export function generateLetterA(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'A';
	const timing = 'split';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// First set: Clockwise rotation
	positionCycles.alpha.cw.forEach((startPos, i) => {
		const endPos = positionCycles.alpha.cw[(i + 1) % 4];

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

	// Second set: Counterclockwise rotation
	positionCycles.alpha.ccw.forEach((startPos, i) => {
		const endPos = positionCycles.alpha.ccw[(i + 1) % 4];

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

// Generate patterns for Letter B (beta system, static to clockwise/counterclockwise)
export function generateLetterB(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'B';
	const timing = 'split';
	const direction = 'same';

	// First set: Static blue, clockwise red
	positionCycles.beta.cw.forEach((startPos) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos: startPos, // Same position for static motion
				timing,
				direction,
				blueMotion: 'static',
				blueRotDir: 'no_rot',
				redMotion: 'pro',
				redRotDir: 'cw'
			})
		);
	});

	// Second set: Clockwise blue, static red
	positionCycles.beta.cw.forEach((startPos) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos: startPos, // Same position for static motion
				timing,
				direction,
				blueMotion: 'pro',
				blueRotDir: 'cw',
				redMotion: 'static',
				redRotDir: 'no_rot'
			})
		);
	});

	return patterns;
}

// Generate patterns for Letter C (clockwise alpha to beta transitions)
export function generateLetterC(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'C';
	const timing = 'tog';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';
	const blueRotDir = 'cw';
	const redRotDir = 'cw';

	// Define transitions from alpha to beta
	const transitions = [
		{ startPos: 'alpha3', endPos: 'beta5' },
		{ startPos: 'alpha5', endPos: 'beta7' },
		{ startPos: 'alpha7', endPos: 'beta1' },
		{ startPos: 'alpha1', endPos: 'beta3' }
	];

	// Generate transitions
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
