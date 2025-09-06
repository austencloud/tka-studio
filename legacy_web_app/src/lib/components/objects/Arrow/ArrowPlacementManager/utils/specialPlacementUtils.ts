import type { ArrowData } from '$lib/components/objects/Arrow/ArrowData';
import type { ArrowPlacementConfig } from '../types';
import { SpecialPlacementLoader } from './SpecialPlacementLoader';
import { OrientationKeyGenerator } from './OrientationKeyGenerator';
import { AttrKeyGenerator } from './AttrKeyGenerator';

/**
 * Gets a special placement adjustment for an arrow if available.
 * This implementation precisely matches Python's behavior.
 */
export function getSpecialAdjustment(
	arrow: ArrowData,
	config: ArrowPlacementConfig
): [number, number] | null {
	const { pictographData, checker } = config;
	if (!pictographData.letter) return null;

	try {
		// 1. Generate orientation key - EXACTLY like Python does
		const oriKeyGenerator = OrientationKeyGenerator.getInstance();
		const oriKey = oriKeyGenerator.generateOriKeyFromMotion(arrow, checker);

		// 2. Format turns tuple string - EXACTLY like Python does
		const turnsTuple = formatTurnsTuple(pictographData);

		// 3. Get arrow key - EXACTLY like Python's attr_key_generator
		const attrKeyGenerator = AttrKeyGenerator.getInstance();
		let arrowKey = attrKeyGenerator.getKeyFromArrow(arrow, checker, pictographData);

		// 4. Get special placement loader
		const loader = SpecialPlacementLoader.getInstance();
		const gridMode = pictographData.gridMode || 'diamond';
		const letterValue = pictographData.letter as string;

		// 5. Get special adjustment
		const adjustment = loader.getAdjustmentForLetter(
			gridMode,
			oriKey,
			letterValue,
			turnsTuple,
			arrowKey
		);

		return adjustment;
	} catch (error) {
		console.error('Error getting special adjustment:', error);
		return null;
	}
}

/**
 * Formats the turns tuple string EXACTLY like the Python TurnsTupleGenerator
 */
function formatTurnsTuple(pictographData: any): string {
	const redMotion = pictographData.redMotion;
	const blueMotion = pictographData.blueMotion;

	// Always prefer the data from motion first
	const redTurns =
		redMotion?.motionType === 'float'
			? 'fl'
			: redMotion?.turns !== undefined && redMotion.turns !== null
				? redMotion.turns
				: 0;

	const blueTurns =
		blueMotion?.motionType === 'float'
			? 'fl'
			: blueMotion?.turns !== undefined && blueMotion.turns !== null
				? blueMotion.turns
				: 0;

	// Fallback to '(0, 0)' if both are undefined or null
	return `(${redTurns}, ${blueTurns})`;
}
