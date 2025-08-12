/**
 * Shift Location Calculator
 *
 * Handles location calculation for pro, anti, and float motions.
 * Based on the legacy desktop ShiftLocationCalculator.
 */

import type { MotionData } from '$lib/domain';

export class ShiftLocationCalculator {
	calculateLocation(motion: MotionData): string {
		const startLoc = motion.start_loc?.toLowerCase();
		const endLoc = motion.end_loc?.toLowerCase();

		if (!startLoc || !endLoc) {
			console.warn('Missing start_loc or end_loc for shift motion');
			return 'center';
		}

		// Direction pairs mapping from the legacy Python code
		const directionPairs: Record<string, string> = {
			// North-East combinations
			'n-e': 'ne',
			'e-n': 'ne',

			// East-South combinations
			'e-s': 'se',
			's-e': 'se',

			// South-West combinations
			's-w': 'sw',
			'w-s': 'sw',

			// West-North combinations
			'w-n': 'nw',
			'n-w': 'nw',

			// Additional cardinal-to-cardinal mappings
			'n-s': 'center', // North to South - typically center
			's-n': 'center', // South to North - typically center
			'e-w': 'center', // East to West - typically center
			'w-e': 'center', // West to East - typically center
		};

		const pairKey = `${startLoc}-${endLoc}`;
		const location = directionPairs[pairKey];

		if (!location) {
			console.warn(`Unknown direction pair: ${startLoc} -> ${endLoc}`);
			return 'center';
		}

		return location;
	}
}
