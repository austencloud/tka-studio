import { generatePatternRow } from './PatternGenerator';
import { positionCycles } from './PatternGenerator';
import type { PatternRow } from './PatternGenerator';

// Generate patterns for Greek Alpha (triangle shape)
export function generateGreekAlpha(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Alpha';
	const timing = 'tog';
	const direction = 'opp';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define Alpha shape transitions (triangle with crossbar)
	const transitions = [
		{ startPos: 'beta7', endPos: 'beta1', blueRotDir: 'ccw', redRotDir: 'cw' }, // Left diagonal
		{ startPos: 'beta1', endPos: 'beta3', blueRotDir: 'cw', redRotDir: 'ccw' }, // Right diagonal
		{ startPos: 'beta3', endPos: 'beta7', blueRotDir: 'cw', redRotDir: 'ccw' }, // Base
		{ startPos: 'gamma5', endPos: 'gamma15', blueRotDir: 'ccw', redRotDir: 'cw' } // Crossbar
	];

	// Generate Alpha shape patterns
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

// Generate patterns for Greek Beta (double curve)
export function generateGreekBeta(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Beta';
	const timing = 'split';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';
	const blueRotDir = 'cw';
	const redRotDir = 'cw';

	// Define Beta shape transitions (vertical with two curves)
	const transitions = [
		{ startPos: 'beta1', endPos: 'beta5' }, // Vertical line
		{ startPos: 'beta5', endPos: 'beta3' }, // Bottom curve
		{ startPos: 'beta3', endPos: 'gamma9' }, // Middle transition
		{ startPos: 'gamma9', endPos: 'beta1' } // Top curve
	];

	// Generate Beta shape patterns
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

// Generate patterns for Greek Gamma (right angle)
export function generateGreekGamma(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Gamma';
	const timing = 'tog';
	const direction = 'same';
	const blueMotion = 'float';
	const redMotion = 'float';
	const blueRotDir = 'cw';
	const redRotDir = 'cw';

	// Define Gamma shape transitions (vertical with top horizontal)
	const transitions = [
		{ startPos: 'beta1', endPos: 'beta3' }, // Top horizontal
		{ startPos: 'beta3', endPos: 'beta5' } // Vertical
	];

	// Generate Gamma shape patterns
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

// Generate patterns for Greek Delta (triangle)
export function generateGreekDelta(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Delta';
	const timing = 'split';
	const direction = 'opp';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define Delta shape transitions (triangle)
	const transitions = [
		{ startPos: 'beta1', endPos: 'alpha7', blueRotDir: 'cw', redRotDir: 'ccw' }, // Right diagonal
		{ startPos: 'alpha7', endPos: 'alpha3', blueRotDir: 'cw', redRotDir: 'ccw' }, // Base
		{ startPos: 'alpha3', endPos: 'beta1', blueRotDir: 'cw', redRotDir: 'ccw' } // Left diagonal
	];

	// Generate Delta shape patterns
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

// Generate patterns for Greek Epsilon (E with curved edges)
export function generateGreekEpsilon(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Epsilon';
	const timing = 'tog';
	const direction = 'same';
	const blueMotion = 'float';
	const redMotion = 'float';

	// Define Epsilon shape transitions (C with middle bar)
	const transitions = [
		{ startPos: 'beta3', endPos: 'beta1', blueRotDir: 'ccw', redRotDir: 'ccw' }, // Top curve
		{ startPos: 'beta1', endPos: 'beta7', blueRotDir: 'ccw', redRotDir: 'ccw' }, // Vertical
		{ startPos: 'beta7', endPos: 'beta5', blueRotDir: 'ccw', redRotDir: 'ccw' }, // Bottom curve
		{ startPos: 'gamma1', endPos: 'gamma7', blueRotDir: 'cw', redRotDir: 'cw' } // Middle bar
	];

	// Generate Epsilon shape patterns
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

// Generate patterns for Greek Zeta (Z with curved edges)
export function generateGreekZeta(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Zeta';
	const timing = 'split';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define Zeta shape transitions (Z with curved edges)
	const transitions = [
		{ startPos: 'beta1', endPos: 'beta3', blueRotDir: 'cw', redRotDir: 'cw' }, // Top horizontal
		{ startPos: 'beta3', endPos: 'beta7', blueRotDir: 'ccw', redRotDir: 'ccw' }, // Diagonal
		{ startPos: 'beta7', endPos: 'beta5', blueRotDir: 'cw', redRotDir: 'cw' } // Bottom horizontal
	];

	// Generate Zeta shape patterns
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

// Generate patterns for Greek Omega (curved bottom with tails)
export function generateGreekOmega(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Omega';
	const timing = 'tog';
	const direction = 'opp';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define Omega shape transitions
	const transitions = [
		{ startPos: 'beta1', endPos: 'beta5', blueRotDir: 'ccw', redRotDir: 'cw' }, // Left vertical
		{ startPos: 'beta5', endPos: 'beta7', blueRotDir: 'cw', redRotDir: 'ccw' }, // Bottom curve
		{ startPos: 'beta7', endPos: 'beta3', blueRotDir: 'cw', redRotDir: 'ccw' }, // Right vertical
		{ startPos: 'beta3', endPos: 'gamma3', blueRotDir: 'cw', redRotDir: 'ccw' }, // Right tail
		{ startPos: 'beta1', endPos: 'gamma1', blueRotDir: 'ccw', redRotDir: 'cw' } // Left tail
	];

	// Generate Omega shape patterns
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

// Generate patterns for Greek Phi (circle with vertical line)
export function generateGreekPhi(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Phi';
	const timing = 'quarter';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define Phi shape transitions
	const circleTransitions = positionCycles.beta.cw.map((startPos, i) => {
		return {
			startPos,
			endPos: positionCycles.beta.cw[(i + 1) % 4],
			blueRotDir: 'cw',
			redRotDir: 'cw'
		};
	});

	const verticalTransitions = [
		{ startPos: 'beta1', endPos: 'beta5', blueRotDir: 'ccw', redRotDir: 'ccw' } // Vertical line through circle
	];

	// Generate Phi circle patterns
	circleTransitions.forEach(({ startPos, endPos, blueRotDir, redRotDir }) => {
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

	// Generate Phi vertical line pattern
	verticalTransitions.forEach(({ startPos, endPos, blueRotDir, redRotDir }) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing: 'split', // Different timing for the vertical line
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

// Generate patterns for Greek Pi (horizontal with two verticals)
export function generateGreekPi(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Pi';
	const timing = 'split';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';
	const blueRotDir = 'cw';
	const redRotDir = 'cw';

	// Define Pi shape transitions
	const transitions = [
		{ startPos: 'beta1', endPos: 'beta3' }, // Top horizontal
		{ startPos: 'beta1', endPos: 'beta5' }, // Left vertical
		{ startPos: 'beta3', endPos: 'beta7' } // Right vertical
	];

	// Generate Pi shape patterns
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

// Generate patterns for Greek Sigma (E without middle horizontal)
export function generateGreekSigma(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Sigma';
	const timing = 'tog';
	const direction = 'opp';
	const blueMotion = 'dash';
	const redMotion = 'dash';
	const blueRotDir = 'no_rot';
	const redRotDir = 'no_rot';

	// Define Sigma shape transitions
	const transitions = [
		{ startPos: 'beta1', endPos: 'beta3' }, // Top horizontal
		{ startPos: 'beta3', endPos: 'beta7' }, // Diagonal
		{ startPos: 'beta7', endPos: 'beta5' } // Bottom horizontal
	];

	// Generate Sigma shape patterns
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

// Generate patterns for Greek Theta (circle with horizontal line)
export function generateGreekTheta(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Theta';
	const timing = 'quarter';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';

	// Define Theta shape transitions
	const circleTransitions = positionCycles.beta.cw.map((startPos, i) => {
		return {
			startPos,
			endPos: positionCycles.beta.cw[(i + 1) % 4],
			blueRotDir: 'cw',
			redRotDir: 'cw'
		};
	});

	const horizontalTransitions = [
		{ startPos: 'beta3', endPos: 'beta7', blueRotDir: 'ccw', redRotDir: 'ccw' } // Horizontal line through circle
	];

	// Generate Theta circle patterns
	circleTransitions.forEach(({ startPos, endPos, blueRotDir, redRotDir }) => {
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

	// Generate Theta horizontal line pattern
	horizontalTransitions.forEach(({ startPos, endPos, blueRotDir, redRotDir }) => {
		patterns.push(
			generatePatternRow({
				letter,
				startPos,
				endPos,
				timing: 'split', // Different timing for the horizontal line
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

// Generate patterns for Greek Psi (trident shape)
export function generateGreekPsi(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Psi';
	const timing = 'tog';
	const direction = 'same';
	const blueMotion = 'pro';
	const redMotion = 'pro';
	const blueRotDir = 'cw';
	const redRotDir = 'cw';

	// Define Psi shape transitions
	const transitions = [
		{ startPos: 'gamma3', endPos: 'gamma7' }, // Left prong
		{ startPos: 'gamma7', endPos: 'beta5' }, // Center stem
		{ startPos: 'gamma7', endPos: 'gamma11' } // Right prong
	];

	// Generate Psi shape patterns
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

// Generate patterns for Greek Lambda (inverted V)
export function generateGreekLambda(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Common properties
	const letter = 'Lambda';
	const timing = 'split';
	const direction = 'opp';
	const blueMotion = 'float';
	const redMotion = 'float';

	// Define Lambda shape transitions (inverted V)
	const transitions = [
		{ startPos: 'beta5', endPos: 'beta1', blueRotDir: 'ccw', redRotDir: 'cw' }, // Left diagonal
		{ startPos: 'beta5', endPos: 'beta3', blueRotDir: 'cw', redRotDir: 'ccw' } // Right diagonal
	];

	// Generate Lambda shape patterns
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
