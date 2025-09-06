// src/lib/components/objects/Arrow/ArrowPlacementManager/utils/OrientationKeyGenerator.ts
import { RADIAL, NONRADIAL, IN, OUT, CLOCK, COUNTER } from '$lib/types/Constants';
import { LetterConditions } from '$lib/components/Pictograph/constants/LetterConditions';
import type { ArrowData } from '$lib/components/objects/Arrow/ArrowData';
import type { ArrowPlacementConfig } from '../types';

/**
 * Generates orientation keys for arrow placements.
 * Directly matches Python's ori_key_generator behavior.
 */
export class OrientationKeyGenerator {
	private static instance: OrientationKeyGenerator;

	private constructor() {}

	/**
	 * Gets the singleton instance
	 */
	public static getInstance(): OrientationKeyGenerator {
		if (!OrientationKeyGenerator.instance) {
			OrientationKeyGenerator.instance = new OrientationKeyGenerator();
		}
		return OrientationKeyGenerator.instance;
	}

	/**
	 * Generates an orientation key from an arrow and motion
	 * Matches Python's generate_ori_key_from_motion method
	 */
	public generateOriKeyFromMotion(arrow: ArrowData, checker: any): string {
		const endOri = arrow.endOri as string;

		// Determine if the pictograph has different orientation types
		const hasHybridOrientation = checker.endsWithLayer3();
		const hasRadialProps = checker.endsWithRadialOri();
		const hasNonRadialProps = checker.endsWithNonRadialOri();

		// Handle orientation prefix
		let oriPrefix = '';
		if (hasHybridOrientation) {
			if (endOri === IN || endOri === OUT) {
				oriPrefix = `${RADIAL}_`;
			} else if (endOri === CLOCK || endOri === COUNTER) {
				oriPrefix = `${NONRADIAL}_`;
			}
		}

		// Determine the layer
		let layer = '';
		if (hasRadialProps) {
			layer = 'layer1';
		} else if (hasNonRadialProps) {
			layer = 'layer2';
		} else if (hasHybridOrientation) {
			layer = 'layer3';
		}

		// Add prop type suffix
		let propSuffix = '';
		const hasAlphaProps = checker.checkLetterCondition(LetterConditions.ALPHA_ENDING);
		const hasBetaProps = checker.checkLetterCondition(LetterConditions.BETA_ENDING);
		const hasGammaProps = checker.checkLetterCondition(LetterConditions.GAMMA_ENDING);

		if (hasAlphaProps) {
			propSuffix = '_alpha';
		} else if (hasBetaProps) {
			propSuffix = '_beta';
		} else if (hasGammaProps) {
			propSuffix = '_gamma';
		}

		// Combine all parts to create the final folder name
		if (layer) {
			return `${oriPrefix}${layer}${propSuffix}`;
		}

		return '';
	}

	/**
	 * Gets the other layer3 orientation key
	 * Matches Python's get_other_layer3_ori_key method
	 */
	public getOtherLayer3OriKey(oriKey: string): string {
		if (oriKey === 'from_layer3_blue1_red2') {
			return 'from_layer3_blue2_red1';
		} else if (oriKey === 'from_layer3_blue2_red1') {
			return 'from_layer3_blue1_red2';
		}
		return oriKey;
	}
}
