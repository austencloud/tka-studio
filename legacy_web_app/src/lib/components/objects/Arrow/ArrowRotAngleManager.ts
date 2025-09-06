import {
	PRO,
	ANTI,
	FLOAT,
	DASH,
	STATIC,
	IN,
	OUT,
	CLOCK,
	COUNTER,
	CLOCKWISE,
	COUNTER_CLOCKWISE,
	NO_ROT,
	CW_SHIFT,
	DIAMOND,
	BOX
} from '$lib/types/Constants';
import type {
	Loc,
	PropRotDir,
	Orientation,
	TKATurns,
	HandRotDir,
	GridMode
} from '$lib/types/Types';
import type { Motion } from '../Motion/Motion';
import { Letter } from '$lib/types/Letter';
import { LetterType } from '$lib/types/LetterType';
import { LetterUtils } from '$lib/utils/LetterUtils';

import {
	PRO_ROTATION_MAP,
	ANTI_REGULAR_MAP,
	ANTI_ALT_MAP,
	FLOAT_DIRECTION_MAP,
	DASH_NO_ROTATION_MAP,
	DASH_ORIENTATION_MAP,
	CW_DASH_ANGLE_OVERRIDE_MAP,
	CCW_DASH_ANGLE_OVERRIDE_MAP,
	RADIAL_STATIC_DIRECTION_MAP,
	NONRADIAL_STATIC_DIRECTION_MAP,
	STATIC_FROM_RADIAL_ANGLE_OVERRIDE_MAP,
	STATIC_FROM_NONRADIAL_ANGLE_OVERRIDE_MAP,
	PHI_DASH_PSI_DASH_ANGLE_MAP,
	LAMBDA_ZERO_TURNS_ANGLE_MAP,
	DIAMOND_DASH_ANGLE_MAP,
	BOX_DASH_ANGLE_MAP,
	OPPOSITE_LOCATION_MAP
} from './constants/ArrowRotationConstants';
import type { PictographService } from '$lib/components/Pictograph/PictographService';
import { calculateShiftLocation } from './ArrowLocationManager';
import type { PictographData } from '$lib/types/PictographData';

export default class ArrowRotAngleManager {
	private service?: PictographService;
	private data: PictographData;

	constructor(data: PictographData, service?: PictographService) {
		this.data = data;
		this.service = service;
	}

	/**
	 * Public method to calculate rotation angle with mirroring support
	 * @param motion The motion object
	 * @param arrowLoc The arrow location
	 * @param isMirrored Whether the arrow is mirrored
	 * @returns The calculated rotation angle in degrees
	 */
	calculateRotationAngle(motion: Motion, arrowLoc: Loc, isMirrored: boolean = false): number {
		// Calculate the base rotation angle
		const angle = this.calculateBaseRotationAngle(motion, arrowLoc);

		// Apply mirror effect if needed
		if (isMirrored) {
			// For mirrored arrows, we need to adjust the rotation angle
			return (360 - angle) % 360;
		}

		return angle;
	}

	/**
	 * Calculate the base rotation angle for the given motion and location
	 */
	private calculateBaseRotationAngle(motion: Motion, arrowLoc: Loc): number {
		const { motionType } = motion;

		// Select calculator based on motion type
		switch (motionType) {
			case PRO:
				return this.calculateProRotationAngle(arrowLoc, motion);
			case ANTI:
				return this.calculateAntiRotationAngle(arrowLoc, motion);
			case FLOAT:
				return this.calculateFloatRotationAngle(arrowLoc, motion);
			case DASH:
				return this.calculateDashRotationAngle(arrowLoc, motion);
			case STATIC:
				return this.calculateStaticRotationAngle(arrowLoc, motion);
			default:
				return 0;
		}
	}

	// Pro rotation calculation
	private calculateProRotationAngle(loc: Loc, motion: Motion): number {
		const propRotDir = motion.propRotDir;
		return PRO_ROTATION_MAP[propRotDir]?.[loc] ?? 0;
	}

	// Anti rotation calculation
	private calculateAntiRotationAngle(loc: Loc, motion: Motion): number {
		const { propRotDir, startOri, turns } = motion;

		// Choose map based on orientation and turns
		let directionMap;

		if (
			[CLOCK, COUNTER].includes(startOri) &&
			typeof turns === 'number' &&
			[0.5, 1.5, 2.5].includes(turns)
		) {
			directionMap = ANTI_ALT_MAP;
		} else {
			directionMap = ANTI_REGULAR_MAP;
		}

		return directionMap[propRotDir]?.[loc] ?? 0;
	}

	// Float rotation calculation
	private calculateFloatRotationAngle(loc: Loc, motion: Motion): number {
		const { handRotDir } = motion;

		// Use the specified rotation direction or default
		const activeRotDirection = handRotDir || CW_SHIFT;

		return FLOAT_DIRECTION_MAP[activeRotDirection]?.[loc] ?? 0;
	}

	// Dash rotation calculation
	private calculateDashRotationAngle(loc: Loc, motion: Motion): number {
		const { startOri, propRotDir, startLoc, endLoc, turns, gridMode, color, letter } = motion;

		// First check if there's a rotation angle override
		if (this.hasRotationAngleOverride(motion)) {
			return this.getDashRotAngleOverride(loc, motion);
		}

		// Then handle NO_ROT case
		if (propRotDir === NO_ROT) {
			const key = `${startLoc}-${endLoc}`;
			return DASH_NO_ROTATION_MAP[key] ?? 0;
		}

		// Special letter handling
		if (letter && this.service) {
			const letterValue = LetterUtils.getLetter(letter);

			// Handle Phi Dash and Psi Dash special cases
			if ([Letter.Φ_DASH, Letter.Ψ_DASH].includes(letterValue) && turns === 0) {
				const key = `${color}_${startLoc}_${endLoc}`;
				if (PHI_DASH_PSI_DASH_ANGLE_MAP[key] !== undefined) {
					return PHI_DASH_PSI_DASH_ANGLE_MAP[key];
				}

				const otherMotion = this.service.getOtherMotion(motion);
				if (otherMotion && otherMotion.turns !== 0) {
					const otherAngle = this.calculateDashRotationAngle(loc, otherMotion);
					return (otherAngle + 180) % 360;
				}
			}

			// Handle Lambda and Lambda Dash special cases
			if ([Letter.Λ, Letter.Λ_DASH].includes(letterValue) && turns === 0) {
				const otherMotion = this.service.getOtherMotion(motion);
				if (otherMotion) {
					const key = `${startLoc}_${endLoc}_${otherMotion.endLoc}`;
					if (LAMBDA_ZERO_TURNS_ANGLE_MAP[key] !== undefined) {
						return LAMBDA_ZERO_TURNS_ANGLE_MAP[key];
					}
				}
			}

			// Handle Type3 letters in various grid modes
			const letterType = LetterType.getLetterType(letter);
			if (letterType === LetterType.Type3 && turns === 0) {
				const shiftMotion = this.service.getShiftMotion();
				if (shiftMotion) {
					const shiftLoc = calculateShiftLocation(shiftMotion.startLoc, shiftMotion.endLoc);

					if (gridMode === DIAMOND) {
						const key = `${startLoc}_${shiftLoc}`;
						if (DIAMOND_DASH_ANGLE_MAP[key] !== undefined) {
							return DIAMOND_DASH_ANGLE_MAP[key];
						}
					} else if (gridMode === BOX) {
						const key = `${startLoc}_${shiftLoc}`;
						if (BOX_DASH_ANGLE_MAP[key] !== undefined) {
							return BOX_DASH_ANGLE_MAP[key];
						}
					}
				}
			}
		}

		// Default to orientation-based rotation
		return DASH_ORIENTATION_MAP[startOri]?.[propRotDir]?.[loc] ?? 0;
	}

	// Get dash rotation angle override
	private getDashRotAngleOverride(loc: Loc, motion: Motion): number {
		const { propRotDir } = motion;

		if (propRotDir === CLOCKWISE) {
			const locAngle = CW_DASH_ANGLE_OVERRIDE_MAP[loc];
			if (typeof locAngle === 'object') {
				return locAngle[propRotDir] ?? 0;
			}
			return locAngle ?? 0;
		}

		if (propRotDir === COUNTER_CLOCKWISE) {
			const locAngle = CCW_DASH_ANGLE_OVERRIDE_MAP[loc];
			if (typeof locAngle === 'object') {
				return locAngle[propRotDir] ?? 0;
			}
			return locAngle ?? 0;
		}

		if (propRotDir === NO_ROT) {
			// Handle no rotation case
			const key = `${motion.startLoc}-${motion.endLoc}`;
			return DASH_NO_ROTATION_MAP[key] ?? 0;
		}

		return 0;
	}

	// Static rotation calculation
	private calculateStaticRotationAngle(loc: Loc, motion: Motion): number {
		const { startOri, propRotDir } = motion;

		// Check for rotation angle override first
		if (this.hasRotationAngleOverride(motion)) {
			return this.getStaticRotAngleOverride(loc, propRotDir, startOri);
		}

		// Choose direction map based on orientation
		const isRadialOrientation = [IN, OUT].includes(startOri);
		const directionMap = isRadialOrientation
			? RADIAL_STATIC_DIRECTION_MAP
			: NONRADIAL_STATIC_DIRECTION_MAP;

		return directionMap[propRotDir]?.[loc] ?? 0;
	}

	// Get static rotation angle override
	private getStaticRotAngleOverride(
		loc: Loc,
		propRotDir: PropRotDir,
		startOri: Orientation
	): number {
		const isRadialOrientation = [IN, OUT].includes(startOri);
		const overrideMap = isRadialOrientation
			? STATIC_FROM_RADIAL_ANGLE_OVERRIDE_MAP
			: STATIC_FROM_NONRADIAL_ANGLE_OVERRIDE_MAP;

		const locAngle = overrideMap[loc];
		if (typeof locAngle === 'object') {
			return locAngle[propRotDir] ?? 0;
		}
		return locAngle ?? 0;
	}

	// Check if the motion has a rotation angle override
	private hasRotationAngleOverride(motion: Motion): boolean {
		const { motionType, letter } = motion;

		// Skip certain motion types
		if (![DASH, STATIC].includes(motionType)) {
			return false;
		}

		// Check for special letters first
		if (letter) {
			const letterValue = LetterUtils.getLetter(letter);
			const isSpecialLetter = [Letter.Φ_DASH, Letter.Ψ_DASH, Letter.Λ, Letter.Λ_DASH].includes(
				letterValue
			);

			if (isSpecialLetter) {
				return true;
			}
		}

		// Fallback to basic check for zero turns
		return (
			(motionType === DASH && motion.turns === 0) || (motionType === STATIC && motion.turns === 0)
		);
	}
}

// Export common constants for testing
export { OPPOSITE_LOCATION_MAP, PRO_ROTATION_MAP, ANTI_REGULAR_MAP, ANTI_ALT_MAP };