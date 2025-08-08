/**
 * Staff orientation mapping system based on manual test data
 * This module handles the conversion from position + orientation to exact rotation angles
 */

import type { Orientation } from '../types/core.js';
import { degreesToRadians } from './manual-rotation.js';

/**
 * Type definition for orientation mapping data
 */
export interface OrientationMappingData {
	[position: string]: {
		[_orientation in Orientation]?: number; // angles in degrees
	};
}

/**
 * Finalized orientation mappings from systematic testing
 * These are the exact rotation angles validated through the test interface
 */
const FINALIZED_ORIENTATION_MAPPINGS: OrientationMappingData = {
	// Hand positions - primary staff positions
	n_hand: {
		in: 90, // pointing down toward center
		out: 270, // pointing up away from center
		clockwise: 90, // clockwise rotation from in
		counter: 180 // counter-clockwise rotation from in
	},
	e_hand: {
		in: 180, // pointing left toward center
		out: 0, // pointing right away from center
		clockwise: 90, // clockwise rotation from in
		counter: 270 // counter-clockwise rotation from in
	},
	s_hand: {
		in: 270, // pointing up toward center
		out: 90, // pointing down away from center
		clockwise: 180, // clockwise rotation from in
		counter: 270 // counter-clockwise rotation from in
	},
	w_hand: {
		in: 0, // pointing right toward center
		out: 180, // pointing left away from center
		clockwise: 270, // clockwise rotation from in
		counter: 90 // counter-clockwise rotation from in
	},
	// Diagonal positions
	ne: {
		in: 135, // pointing southwest toward center
		out: 315, // pointing northeast away from center
		clockwise: 45, // clockwise rotation from in
		counter: 225 // counter-clockwise rotation from in
	},
	se: {
		in: 225, // pointing northwest toward center
		out: 45, // pointing southeast away from center
		clockwise: 135, // clockwise rotation from in
		counter: 315 // counter-clockwise rotation from in
	},
	sw: {
		in: 315, // pointing northeast toward center
		out: 135, // pointing southwest away from center
		clockwise: 225, // clockwise rotation from in
		counter: 45 // counter-clockwise rotation from in
	},
	nw: {
		in: 45, // pointing southeast toward center
		out: 225, // pointing northwest away from center
		clockwise: 315, // clockwise rotation from in
		counter: 135 // counter-clockwise rotation from in
	}
};

/**
 * Current orientation mappings using finalized test data
 */
let currentOrientationMappings: OrientationMappingData = { ...FINALIZED_ORIENTATION_MAPPINGS };

/**
 * Get the rotation angle for a specific position and orientation
 */
export function getOrientationAngle(position: string, orientation: Orientation): number {
	const positionData = currentOrientationMappings[position];
	if (!positionData) {
		// No orientation data found for position
		return 0;
	}

	if (!orientation) {
		return 0;
	}

	const angle = positionData[orientation];
	if (angle === undefined) {
		// No orientation data found for position + orientation
		return 0;
	}

	return angle;
}

/**
 * Get the rotation angle in radians for a specific position and orientation
 */
export function getOrientationAngleRadians(position: string, orientation: Orientation): number {
	const degrees = getOrientationAngle(position, orientation);
	return degreesToRadians(degrees);
}

/**
 * Update orientation mappings with new test data
 */
export function updateOrientationMappings(newMappings: OrientationMappingData): void {
	currentOrientationMappings = { ...currentOrientationMappings, ...newMappings };
}

/**
 * Load orientation mappings from JSON data (from test interface export)
 */
export function loadOrientationMappingsFromJSON(jsonData: string): boolean {
	try {
		const data = JSON.parse(jsonData) as OrientationMappingData;
		updateOrientationMappings(data);
		return true;
	} catch {
		// Error loading orientation mappings from JSON
		return false;
	}
}

/**
 * Reset orientation mappings to finalized values
 */
export function resetOrientationMappings(): void {
	currentOrientationMappings = { ...FINALIZED_ORIENTATION_MAPPINGS };
}

/**
 * Get all current orientation mappings
 */
export function getCurrentOrientationMappings(): OrientationMappingData {
	return { ...currentOrientationMappings };
}

/**
 * Validate orientation mapping data
 */
export function validateOrientationMappings(data: OrientationMappingData): {
	isValid: boolean;
	errors: string[];
	warnings: string[];
} {
	const errors: string[] = [];
	const warnings: string[] = [];

	for (const [position, orientations] of Object.entries(data)) {
		if (typeof orientations !== 'object' || orientations === null) {
			errors.push(`Position ${position}: orientations must be an object`);
			continue;
		}

		for (const [orientation, angle] of Object.entries(orientations)) {
			if (typeof angle !== 'number' || isNaN(angle)) {
				errors.push(
					`Position ${position}, orientation ${orientation}: angle must be a valid number`
				);
			} else if (angle < 0 || angle >= 360) {
				warnings.push(
					`Position ${position}, orientation ${orientation}: angle ${angle} is outside normal range (0-359)`
				);
			}
		}
	}

	return {
		isValid: errors.length === 0,
		errors,
		warnings
	};
}

/**
 * Generate TypeScript code for the orientation mappings
 */
export function generateOrientationMappingCode(): string {
	return `// Generated orientation mappings from test interface
export const ORIENTATION_MAPPINGS: OrientationMappingData = ${JSON.stringify(currentOrientationMappings, null, 2)};`;
}

/**
 * Get orientation mapping statistics
 */
export function getOrientationMappingStats(): {
	totalPositions: number;
	totalMappings: number;
	completedPositions: number;
	missingMappings: Array<{ position: string; orientation: Orientation }>;
} {
	const allOrientations: Orientation[] = ['in', 'out', 'n', 'e', 's', 'w'];
	const positions = Object.keys(currentOrientationMappings);
	let totalMappings = 0;
	let completedPositions = 0;
	const missingMappings: Array<{ position: string; orientation: Orientation }> = [];

	for (const position of positions) {
		const orientations = currentOrientationMappings[position];
		const definedOrientations = Object.keys(orientations || {});
		totalMappings += definedOrientations.length;

		if (definedOrientations.length === allOrientations.length) {
			completedPositions++;
		}

		// Find missing orientations
		for (const orientation of allOrientations) {
			if (!orientations || orientations[orientation] === undefined) {
				missingMappings.push({ position, orientation });
			}
		}
	}

	return {
		totalPositions: positions.length,
		totalMappings,
		completedPositions,
		missingMappings
	};
}

/**
 * Create a mapping function that can be used in place of the current orientation calculation
 */
export function createOrientationMapper(): (
	_position: string,
	_orientation: Orientation
) => number {
	return (_position: string, _orientation: Orientation) => {
		return getOrientationAngleRadians(_position, _orientation);
	};
}

/**
 * Export orientation mappings in various formats
 */
export const OrientationMappingExporter = {
	/**
	 * Export as JSON string
	 */
	toJSON(): string {
		return JSON.stringify(currentOrientationMappings, null, 2);
	},

	/**
	 * Export as TypeScript constant
	 */
	toTypeScript(): string {
		return generateOrientationMappingCode();
	},

	/**
	 * Export as CSV for spreadsheet analysis
	 */
	toCSV(): string {
		const lines = ['Position,Orientation,Angle'];

		for (const [position, orientations] of Object.entries(currentOrientationMappings)) {
			for (const [orientation, angle] of Object.entries(orientations)) {
				lines.push(`${position},${orientation},${angle}`);
			}
		}

		return lines.join('\n');
	},

	/**
	 * Export as markdown table for documentation
	 */
	toMarkdown(): string {
		const lines = [
			'| Position | in | out | n | e | s | w |',
			'|----------|----|----|---|---|---|---|'
		];

		for (const [position, orientations] of Object.entries(currentOrientationMappings)) {
			const row = [
				position,
				orientations.in?.toString() || '-',
				orientations.out?.toString() || '-',
				orientations.n?.toString() || '-',
				orientations.e?.toString() || '-',
				orientations.s?.toString() || '-',
				orientations.w?.toString() || '-'
			];
			lines.push(`| ${row.join(' | ')} |`);
		}

		return lines.join('\n');
	}
};
