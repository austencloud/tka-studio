import { formatPatternCSV, formatPatternDisplay } from './PatternGenerator';
import type { PatternRow } from './PatternGenerator';

// Import letter generators from all modules
import { generateLetterA, generateLetterB, generateLetterC } from './BasicLetters';

import {
	generateLetterD,
	generateLetterE,
	generateLetterF,
	generateLetterG,
	generateLetterH,
	generateLetterI,
	generateLetterJ,
	generateLetterK,
	generateLetterL,
	generateLetterM
} from './IntermediateLetters';

import {
	generateLetterN,
	generateLetterO,
	generateLetterP,
	generateLetterQ,
	generateLetterR,
	generateLetterS,
	generateLetterT,
	generateLetterU,
	generateLetterV,
	generateLetterW,
	generateLetterX,
	generateLetterY,
	generateLetterZ
} from './AdvancedLetters';

import {
	generateGreekAlpha,
	generateGreekBeta,
	generateGreekGamma,
	generateGreekDelta,
	generateGreekEpsilon,
	generateGreekZeta,
	generateGreekOmega,
	generateGreekPhi,
	generateGreekPi,
	generateGreekSigma,
	generateGreekTheta,
	generateGreekPsi,
	generateGreekLambda
} from './GreekLetters';

// Map of all letter generators
const letterGenerators = {
	// Latin alphabet
	A: generateLetterA,
	B: generateLetterB,
	C: generateLetterC,
	D: generateLetterD,
	E: generateLetterE,
	F: generateLetterF,
	G: generateLetterG,
	H: generateLetterH,
	I: generateLetterI,
	J: generateLetterJ,
	K: generateLetterK,
	L: generateLetterL,
	M: generateLetterM,
	N: generateLetterN,
	O: generateLetterO,
	P: generateLetterP,
	Q: generateLetterQ,
	R: generateLetterR,
	S: generateLetterS,
	T: generateLetterT,
	U: generateLetterU,
	V: generateLetterV,
	W: generateLetterW,
	X: generateLetterX,
	Y: generateLetterY,
	Z: generateLetterZ,

	// Greek alphabet
	Alpha: generateGreekAlpha,
	Beta: generateGreekBeta,
	Gamma: generateGreekGamma,
	Delta: generateGreekDelta,
	Epsilon: generateGreekEpsilon,
	Zeta: generateGreekZeta,
	Omega: generateGreekOmega,
	Phi: generateGreekPhi,
	Pi: generateGreekPi,
	Sigma: generateGreekSigma,
	Theta: generateGreekTheta,
	Psi: generateGreekPsi,
	Lambda: generateGreekLambda
};

// Define a type for the keys of letterGenerators
type LetterGeneratorKey = keyof typeof letterGenerators;

// Generate all patterns from implemented generators
function generateAllPatterns(): PatternRow[] {
	const patterns: PatternRow[] = [];

	// Call all generator functions and collect results
	Object.values(letterGenerators).forEach((generator) => {
		patterns.push(...generator());
	});

	return patterns;
}

// Generate patterns for a specific letter
function generatePatternsForLetter(letter: string): PatternRow[] {
	const key = letter.charAt(0).toUpperCase() + letter.slice(1);

	// Check if the key is a valid key of letterGenerators
	if (key in letterGenerators) {
		// Assert key as a valid LetterGeneratorKey
		const generatorKey = key as LetterGeneratorKey;
		return letterGenerators[generatorKey]();
	}

	return [];
}

export {
	formatPatternCSV,
	formatPatternDisplay,

	// Generator functions
	generateAllPatterns,
	generatePatternsForLetter,
	letterGenerators,

	// Individual letter generators
	generateLetterA,
	generateLetterB,
	generateLetterC,
	generateLetterD,
	generateLetterE,
	generateLetterF,
	generateLetterG,
	generateLetterH,
	generateLetterI,
	generateLetterJ,
	generateLetterK,
	generateLetterL,
	generateLetterM,
	generateLetterN,
	generateLetterO,
	generateLetterP,
	generateLetterQ,
	generateLetterR,
	generateLetterS,
	generateLetterT,
	generateLetterU,
	generateLetterV,
	generateLetterW,
	generateLetterX,
	generateLetterY,
	generateLetterZ,

	// Greek letter generators
	generateGreekAlpha,
	generateGreekBeta,
	generateGreekGamma,
	generateGreekDelta,
	generateGreekEpsilon,
	generateGreekZeta,
	generateGreekOmega,
	generateGreekPhi,
	generateGreekPi,
	generateGreekSigma,
	generateGreekTheta,
	generateGreekPsi,
	generateGreekLambda
};

// Export types correctly
export type {
	// Pattern types and utilities
	PatternRow as Pattern // Alias PatternRow to Pattern for backward compatibility
};
