/**
 * Options Service for OptionPicker using ONLY Svelte 5 Runes
 *
 * Provides functionality for generating, filtering, sorting, and grouping pictograph options.
 * Complete port from legacy system without any stores - pure runes and functions.
 */

import type { PictographData } from '$lib/domain/PictographData';
import type { ReversalFilter, SortMethod } from '../config';

/**
 * Determine reversal category for an option
 */
export function determineReversalCategory(
	sequence: PictographData[],
	option: PictographData
): ReversalFilter {
	// Simplified reversal detection
	if (!sequence || sequence.length === 0) {
		return 'all';
	}

	const lastBeat = sequence[sequence.length - 1];
	if (!lastBeat?.motions?.red || !lastBeat?.motions?.blue) {
		return 'all';
	}

	if (!option?.motions?.red || !option?.motions?.blue) {
		return 'all';
	}

	// Check if rotation directions continue or reverse
	const redContinuous = lastBeat.motions.red.prop_rot_dir === option.motions.red.prop_rot_dir;
	const blueContinuous = lastBeat.motions.blue.prop_rot_dir === option.motions.blue.prop_rot_dir;

	if (redContinuous && blueContinuous) {
		return 'continuous';
	} else if (redContinuous || blueContinuous) {
		return 'oneReversal';
	} else {
		return 'twoReversals';
	}
}

/**
 * Determine group key for an option based on sort method
 */
export function determineGroupKey(
	option: PictographData,
	sortMethod: SortMethod,
	sequence: PictographData[]
): string {
	switch (sortMethod) {
		case 'type':
			return getLetterType(option.letter || null);
		case 'endPosition': {
			const endPos = option.end_position;
			if (typeof endPos === 'string') {
				return endPos;
			}
			const metaEndPos = option.metadata?.endPosition;
			if (typeof metaEndPos === 'string') {
				return metaEndPos;
			}
			return 'Unknown';
		}
		case 'reversals':
			return determineReversalCategory(sequence, option);
		default:
			return 'all';
	}
}

/**
 * Get letter type for grouping - matches legacy system exactly
 */
function getLetterType(letter: string | null): string {
	if (!letter) return 'Unknown';

	// Type 1: Dual-Shift letters
	const type1Letters = [
		'A',
		'B',
		'C',
		'D',
		'E',
		'F',
		'G',
		'H',
		'I',
		'J',
		'K',
		'L',
		'M',
		'N',
		'O',
		'P',
		'Q',
		'R',
		'S',
		'T',
		'U',
		'V',
	];

	// Type 2: Shift letters
	const type2Letters = ['W', 'X', 'Y', 'Z', 'Σ', 'Δ', 'θ', 'Ω'];

	// Type 3: Dash letters
	const type3Letters = ['W-', 'X-', 'Y-', 'Z-', 'Σ-', 'Δ-', 'θ-', 'Ω-'];

	// Type 4: Static letters
	const type4Letters = ['Φ', 'Ψ', 'Λ'];

	// Type 5: Dash Static letters
	const type5Letters = ['Φ-', 'Ψ-', 'Λ-'];

	// Type 6: Flip letters
	const type6Letters = ['α', 'β', 'Γ'];

	if (type1Letters.includes(letter)) return 'Type1';
	if (type2Letters.includes(letter)) return 'Type2';
	if (type3Letters.includes(letter)) return 'Type3';
	if (type4Letters.includes(letter)) return 'Type4';
	if (type5Letters.includes(letter)) return 'Type5';
	if (type6Letters.includes(letter)) return 'Type6';

	return 'Unknown';
}

/**
 * Get sorted group keys based on sort method
 */
export function getSortedGroupKeys(keys: string[], sortMethod: SortMethod): string[] {
	switch (sortMethod) {
		case 'type':
			return keys.sort((a, b) => {
				const order = ['Type1', 'Type2', 'Type3', 'Type4', 'Type5', 'Type6', 'Unknown'];
				return order.indexOf(a) - order.indexOf(b);
			});
		case 'endPosition':
			return keys.sort((a, b) => {
				// Sort positions in TKA order: alpha1-8, beta1-8, gamma1-16
				const getPositionOrder = (pos: string): number => {
					if (pos.startsWith('alpha')) {
						const num = parseInt(pos.replace('alpha', ''), 10);
						return num || 0;
					} else if (pos.startsWith('beta')) {
						const num = parseInt(pos.replace('beta', ''), 10);
						return 8 + (num || 0);
					} else if (pos.startsWith('gamma')) {
						const num = parseInt(pos.replace('gamma', ''), 10);
						return 16 + (num || 0);
					}
					return 999; // Unknown positions last
				};

				return getPositionOrder(a) - getPositionOrder(b);
			});
		case 'reversals':
			return keys.sort((a, b) => {
				const order = ['continuous', 'oneReversal', 'twoReversals', 'all'];
				return order.indexOf(a) - order.indexOf(b);
			});
		default:
			return keys.sort();
	}
}

/**
 * Get sorter function for options based on sort method
 */
export function getSorter(
	sortMethod: SortMethod,
	sequence: PictographData[]
): (a: PictographData, b: PictographData) => number {
	switch (sortMethod) {
		case 'type':
			return (a, b) => {
				const typeA = getLetterType(a.letter || null);
				const typeB = getLetterType(b.letter || null);
				if (typeA !== typeB) {
					return typeA.localeCompare(typeB);
				}
				// Within same type, sort by letter
				const letterA = a.letter || '';
				const letterB = b.letter || '';
				return letterA.localeCompare(letterB);
			};
		case 'endPosition':
			return (a, b) => {
				const posA =
					typeof a.end_position === 'string'
						? a.end_position
						: typeof a.metadata?.endPosition === 'string'
							? a.metadata.endPosition
							: '';
				const posB =
					typeof b.end_position === 'string'
						? b.end_position
						: typeof b.metadata?.endPosition === 'string'
							? b.metadata.endPosition
							: '';
				return posA.localeCompare(posB);
			};
		case 'reversals':
			return (a, b) => {
				const reversalA = determineReversalCategory(sequence, a);
				const reversalB = determineReversalCategory(sequence, b);
				if (reversalA !== reversalB) {
					return reversalA.localeCompare(reversalB);
				}
				// Within same reversal category, sort by letter
				const letterA = a.letter || '';
				const letterB = b.letter || '';
				return letterA.localeCompare(letterB);
			};
		default:
			// Default sort by letter
			return (a, b) => {
				const letterA = a.letter || '';
				const letterB = b.letter || '';
				return letterA.localeCompare(letterB);
			};
	}
}

/**
 * Filter options based on reversal filter
 */
export function filterByReversals(
	options: PictographData[],
	sequence: PictographData[],
	filter: ReversalFilter
): PictographData[] {
	if (filter === 'all') {
		return options;
	}

	return options.filter((option) => {
		const category = determineReversalCategory(sequence, option);
		return category === filter;
	});
}

/**
 * Get display name for a group key
 */
export function getGroupDisplayName(groupKey: string, sortMethod: SortMethod): string {
	switch (sortMethod) {
		case 'type':
			switch (groupKey) {
				case 'Type1':
					return 'Type 1: Dual-Shift';
				case 'Type2':
					return 'Type 2: Shift';
				case 'Type3':
					return 'Type 3: Dash';
				case 'Type4':
					return 'Type 4: Static';
				case 'Type5':
					return 'Type 5: Dash Static';
				case 'Type6':
					return 'Type 6: Flip';
				default:
					return groupKey;
			}
		case 'endPosition':
			return `End Position: ${groupKey}`;
		case 'reversals':
			switch (groupKey) {
				case 'continuous':
					return 'Continuous';
				case 'oneReversal':
					return 'One Reversal';
				case 'twoReversals':
					return 'Two Reversals';
				default:
					return groupKey;
			}
		default:
			return groupKey;
	}
}

/**
 * Get summary statistics for options
 */
export function getOptionsSummary(options: PictographData[]): {
	total: number;
	byType: Record<string, number>;
	byEndPosition: Record<string, number>;
} {
	const summary = {
		total: options.length,
		byType: {} as Record<string, number>,
		byEndPosition: {} as Record<string, number>,
	};

	options.forEach((option) => {
		// Count by type
		const type = getLetterType(option.letter || null);
		summary.byType[type] = (summary.byType[type] || 0) + 1;

		// Count by end position
		const endPos =
			typeof option.end_position === 'string'
				? option.end_position
				: typeof option.metadata?.endPosition === 'string'
					? option.metadata.endPosition
					: 'Unknown';
		summary.byEndPosition[endPos] = (summary.byEndPosition[endPos] || 0) + 1;
	});

	return summary;
}
