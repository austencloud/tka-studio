import type { ArrowData } from '$lib/components/objects/Arrow/ArrowData';
import type { PictographData } from '$lib/types/PictographData';
import { LetterUtils } from '$lib/utils/LetterUtils';
import { LetterConditions } from '$lib/components/Pictograph/constants/LetterConditions';
import { CLOCK, COUNTER, IN, OUT } from '$lib/types/Constants';
import type { PictographChecker } from '$lib/components/Pictograph/services/PictographChecker';

export class AttrKeyGenerator {
	private static instance: AttrKeyGenerator;

	private constructor() {}

	public static getInstance(): AttrKeyGenerator {
		if (!this.instance) {
			this.instance = new AttrKeyGenerator();
		}
		return this.instance;
	}

	/**
	 * Generates a key for an arrow based on multiple conditions
	 * @param arrow The arrow data
	 * @param checker The PictographChecker instance
	 * @param pictographData The full pictograph data
	 * @returns The generated key string
	 */
	public getKeyFromArrow(
		arrow: ArrowData,
		checker: PictographChecker,
		pictographData: PictographData
	): string {
		const letter = pictographData.letter;
		if (!letter) return arrow.color;

		const letterEnum = LetterUtils.fromString(letter);
		const hasHybridMotions = this.hasHybridMotions(pictographData);

		// Use helper method to determine starts from orientation
		const startsFromMixedOrientation = this.startsFromMixedOrientation(pictographData);
		const startsFromStandardOrientation = !startsFromMixedOrientation;

		const startOri = this.getStartOrientation(arrow, pictographData);
		const leadState = this.getLeadState(pictographData);

		// Key generation logic matching Python implementation
		if (startsFromMixedOrientation) {
			if (['S', 'T'].includes(letter)) {
				return leadState || '';
			}

			if (hasHybridMotions) {
				if ([IN, OUT].includes(startOri)) {
					return `${arrow.motionType}_from_layer1`;
				} else if ([CLOCK, COUNTER].includes(startOri)) {
					return `${arrow.motionType}_from_layer2`;
				} else {
					return arrow.color;
				}
			}

			if (LetterUtils.getLettersByCondition(LetterConditions.NON_HYBRID).includes(letterEnum)) {
				return arrow.color;
			}

			return arrow.motionType;
		}

		if (startsFromStandardOrientation) {
			if (['S', 'T'].includes(letter)) {
				return `${arrow.color}${leadState}`;
			}

			if (hasHybridMotions) {
				return arrow.motionType;
			}

			return arrow.color;
		}

		return arrow.motionType; // Default fallback
	}

	private getStartOrientation(arrow: ArrowData, pictographData: PictographData): string {
		// Determine start orientation based on motion color
		const motionData =
			arrow.color === 'red' ? pictographData.redMotionData : pictographData.blueMotionData;

		return motionData?.startOri || '';
	}

	private getLeadState(pictographData: PictographData): string | null {
		// Determine lead state, prioritizing float motions
		const redMotion = pictographData.redMotionData;
		const blueMotion = pictographData.blueMotionData;

		if (redMotion?.motionType === 'float') return 'red_float';
		if (blueMotion?.motionType === 'float') return 'blue_float';

		return null;
	}

	private hasHybridMotions(pictographData: PictographData): boolean {
		// Check if pictograph has hybrid motions
		const letter = pictographData.letter;
		if (!letter) return false;

		const letterEnum = LetterUtils.fromString(letter);
		return LetterUtils.getLettersByCondition(LetterConditions.HYBRID).includes(letterEnum);
	}

	private startsFromMixedOrientation(pictographData: PictographData): boolean {
		const redMotion = pictographData.redMotionData;
		const blueMotion = pictographData.blueMotionData;

		if (!redMotion || !blueMotion) return false;

		const redStartOri = redMotion.startOri;
		const blueStartOri = blueMotion.startOri;

		// Check for different orientation types
		const radialOrientations = [IN, OUT];
		const nonradialOrientations = [CLOCK, COUNTER];

		const redIsRadial = radialOrientations.includes(redStartOri);
		const redIsNonRadial = nonradialOrientations.includes(redStartOri);
		const blueIsRadial = radialOrientations.includes(blueStartOri);
		const blueIsNonRadial = nonradialOrientations.includes(blueStartOri);

		return (redIsRadial && blueIsNonRadial) || (redIsNonRadial && blueIsRadial);
	}
}
