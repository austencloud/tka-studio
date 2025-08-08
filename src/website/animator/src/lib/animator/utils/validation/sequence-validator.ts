/**
 * Sequence data validation utilities
 */

// import type { SequenceData } from '../../types/core.js'; // Not used currently

export interface ValidationResult {
	isValid: boolean;
	error?: string;
}

export function validateSequenceData(data: unknown): ValidationResult {
	if (!Array.isArray(data)) {
		return {
			isValid: false,
			error: 'Sequence data must be an array'
		};
	}

	if (data.length < 2) {
		return {
			isValid: false,
			error: 'Invalid sequence format: Expected an array with metadata and steps'
		};
	}

	// Validate metadata (first element)
	const metadata = data[0];
	if (!metadata || typeof metadata !== 'object') {
		return {
			isValid: false,
			error: 'First element must be metadata object'
		};
	}

	// Validate steps (remaining elements)
	for (let i = 1; i < data.length; i++) {
		const step = data[i];
		if (!step || typeof step !== 'object') {
			return {
				isValid: false,
				error: `Step ${i} must be an object`
			};
		}

		if (typeof step.beat !== 'number') {
			return {
				isValid: false,
				error: `Step ${i} must have a numeric beat property`
			};
		}

		if (!step.blue_attributes || !step.red_attributes) {
			return {
				isValid: false,
				error: `Step ${i} must have blue_attributes and red_attributes`
			};
		}
	}

	return { isValid: true };
}

export function validateFileType(file: File): ValidationResult {
	if (!file.type.includes('png') && !file.name.toLowerCase().endsWith('.png')) {
		return {
			isValid: false,
			error:
				'Please select a PNG image file. Only PNG files with embedded sequence metadata are supported.'
		};
	}

	return { isValid: true };
}

export function validateJSONInput(input: string): ValidationResult {
	if (!input.trim()) {
		return {
			isValid: false,
			error: 'Please enter sequence data'
		};
	}

	try {
		const parsed = JSON.parse(input);
		return validateSequenceData(parsed);
	} catch (err) {
		return {
			isValid: false,
			error: `Parse error: ${err instanceof Error ? err.message : String(err)}`
		};
	}
}
