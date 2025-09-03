import { generatePatternRow } from './PatternGenerator';
import { positionCycles } from './PatternGenerator';
import type { PatternRow } from './PatternGenerator';

// Generate patterns for Letter N (gamma diagonal patterns)
export function generateLetterN(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'N';
	const timing = 'quarter';
	const direction = 'opp';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define N pattern transitions
	const transitions = [
		{ startPos: 'gamma3', endPos: 'gamma13' }, // Diagonal line
		{ startPos: 'gamma13', endPos: 'gamma5' } // Vertical line
	];

	// Generate N patterns with opposite rotations
	transitions.forEach(({ startPos, endPos }) => {
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

	return patterns;
}

// Generate patterns for Letter O (circular beta patterns)
export function generateLetterO(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'O';
	const timing = 'split';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Circular pattern in beta positions
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

	return patterns;
}

// Generate patterns for Letter P (vertical line with clockwise loop)
export function generateLetterP(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'P';
	const timing = 'tog';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';
	const blueRotDir = 'cw';
	const redRotDir = 'cw';

	// Define P shape transitions
	const transitions = [
		{ startPos: 'beta1', endPos: 'beta5' }, // Vertical line
		{ startPos: 'beta5', endPos: 'beta3' }, // Bottom to right
		{ startPos: 'beta3', endPos: 'beta1' } // Right to top
	];

	// Generate P shape patterns
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

// Generate patterns for Letter Q (O with diagonal tail)
export function generateLetterQ(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Q';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// First part: circular pattern (similar to O)
	positionCycles.beta.cw.slice(0, 3).forEach((startPos, i) => {
		const endPos = positionCycles.beta.cw[(i + 1) % 4];

		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing: 'split',
				direction: 'same',
				blueMotion,
				blueRotDir: 'cw',
				redMotion,
				redRotDir: 'cw'
			})
		);
	});

	// Second part: diagonal tail
	patterns.push(
		generatePatternRow({
			letter,
			startPos: 'beta7',
			endPos: 'gamma13',
			timing: 'tog',
			direction: 'opp',
			blueMotion,
			blueRotDir: 'cw',
			redMotion,
			redRotDir: 'ccw'
		})
	);

	return patterns;
}

// Generate patterns for Letter R (P with diagonal leg)
export function generateLetterR(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'R';
	const timing = 'tog';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';
	const blueRotDir = 'cw';
	const redRotDir = 'cw';

	// Define R shape transitions (P with diagonal leg)
	const transitions = [
		{ startPos: 'beta1', endPos: 'beta5' }, // Vertical line
		{ startPos: 'beta5', endPos: 'beta3' }, // Bottom to right
		{ startPos: 'beta3', endPos: 'beta1' }, // Right to top
		{ startPos: 'beta5', endPos: 'alpha7' } // Diagonal leg
	];

	// Generate R shape patterns
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

// Generate patterns for Letter S (serpentine pattern)
export function generateLetterS(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'S';
	const timing = 'tog';
	const direction = 'opp';
	const blueMotion = 'float';
	const redMotion = 'float';

	// Define S shape curved transitions
	const transitions = [
		{ startPos: 'beta3', endPos: 'beta1', blueRotDir: 'ccw', redRotDir: 'cw' },
		{ startPos: 'beta1', endPos: 'beta7', blueRotDir: 'cw', redRotDir: 'ccw' },
		{ startPos: 'beta7', endPos: 'beta5', blueRotDir: 'ccw', redRotDir: 'cw' }
	];

	// Generate S shape patterns
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

// Generate patterns for Letter T (horizontal with vertical stem)
export function generateLetterT(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'T';
	const timing = 'split';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';
	const blueRotDir = 'cw';
	const redRotDir = 'cw';

	// Define T shape transitions
	const transitions = [
		{ startPos: 'beta3', endPos: 'beta1' }, // Horizontal top
		{ startPos: 'beta1', endPos: 'beta5' } // Vertical stem
	];

	// Generate T shape patterns
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

// Generate patterns for Letter U (curved bottom between vertical lines)
export function generateLetterU(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'U';
	const timing = 'tog';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define U shape transitions
	const transitions = [
		{ startPos: 'beta1', endPos: 'beta5', blueRotDir: 'cw', redRotDir: 'cw' }, // Left vertical
		{ startPos: 'beta5', endPos: 'beta7', blueRotDir: 'cw', redRotDir: 'cw' }, // Bottom curve
		{ startPos: 'beta7', endPos: 'beta3', blueRotDir: 'cw', redRotDir: 'cw' } // Right vertical
	];

	// Generate U shape patterns
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

// Generate patterns for Letter V (diagonal lines meeting at bottom)
export function generateLetterV(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'V';
	const timing = 'split';
	const direction = 'opp';
	const blueMotion = 'float';
	const redMotion = 'float';

	// Define V shape transitions
	const transitions = [
		{ startPos: 'alpha3', endPos: 'beta5', blueRotDir: 'cw', redRotDir: 'ccw' },
		{ startPos: 'alpha1', endPos: 'beta5', blueRotDir: 'ccw', redRotDir: 'cw' }
	];

	// Generate V shape patterns
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

// Generate patterns for Letter W (double V pattern)
export function generateLetterW(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'W';
	const timing = 'split';
	const direction = 'opp';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define W shape transitions
	const transitions = [
		{ startPos: 'gamma3', endPos: 'gamma7', blueRotDir: 'ccw', redRotDir: 'cw' },
		{ startPos: 'gamma7', endPos: 'gamma11', blueRotDir: 'cw', redRotDir: 'ccw' },
		{ startPos: 'gamma11', endPos: 'gamma15', blueRotDir: 'ccw', redRotDir: 'cw' }
	];

	// Generate W shape patterns
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

// Generate patterns for Letter X (crossing diagonals)
export function generateLetterX(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'X';
	const timing = 'quarter';
	const direction = 'opp';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define X shape diagonal transitions
	const transitions = [
		{ startPos: 'gamma3', endPos: 'gamma13', blueRotDir: 'ccw', redRotDir: 'cw' }, // Top-left to bottom-right
		{ startPos: 'gamma1', endPos: 'gamma11', blueRotDir: 'cw', redRotDir: 'ccw' } // Top-right to bottom-left
	];

	// Generate X shape patterns
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

// Generate patterns for Letter Y (forked pattern)
export function generateLetterY(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Y';
	const timing = 'tog';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';
	const blueRotDir = 'cw';
	const redRotDir = 'cw';

	// Define Y shape transitions
	const transitions = [
		{ startPos: 'gamma3', endPos: 'gamma7' }, // Top-left to center
		{ startPos: 'gamma11', endPos: 'gamma7' }, // Top-right to center
		{ startPos: 'gamma7', endPos: 'gamma13' } // Center to bottom
	];

	// Generate Y shape patterns
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

// Generate patterns for Letter Z (horizontal lines connected by diagonal)
export function generateLetterZ(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Z';
	const timing = 'split';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';
	const blueRotDir = 'cw';
	const redRotDir = 'cw';

	// Define Z shape transitions
	const transitions = [
		{ startPos: 'beta1', endPos: 'beta3' }, // Top horizontal
		{ startPos: 'beta3', endPos: 'beta7' }, // Diagonal
		{ startPos: 'beta7', endPos: 'beta5' } // Bottom horizontal
	];

	// Generate Z shape patterns
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
