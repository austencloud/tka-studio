/**
 * Rotated Complementary CAP Executor
 *
 * Executes the rotated-complementary CAP (Circular Arrangement Pattern) by combining:
 * 1. ROTATED: Rotate locations based on handpath direction (90°, 180°, or 270°)
 * 2. COMPLEMENTARY: Flip letters (A↔B), flip motion types (PRO↔ANTI), flip prop rotation (CW↔CCW)
 *
 * This creates a sequence where:
 * - Letters are flipped (complementary effect)
 * - Motion types are flipped (PRO ↔ ANTI) (complementary effect)
 * - Prop rotation directions are flipped (CW ↔ CCW) (complementary effect)
 * - Locations are rotated based on the handpath direction
 * - **Colors are NOT swapped** (Blue stays Blue, Red stays Red)
 *
 * IMPORTANT: Supports both quartered and halved slice sizes
 * IMPORTANT: End position is calculated from rotated locations
 */

import type { BeatData } from "$build/workspace-panel";
import { MotionColor, MotionType, type IGridPositionDeriver } from "$shared";
import { TYPES } from "$shared/inversify/types";
import type { GridLocation, GridPosition } from "$shared/pictograph/grid/domain/enums/grid-enums";
import { RotationDirection } from "$shared/pictograph/shared/domain/enums/pictograph-enums";
import { inject, injectable } from "inversify";
import type { IOrientationCalculationService } from "../../../shared/services/contracts";
import { type IComplementaryLetterService } from "../../../shared/services/contracts";
import {
    getHandRotationDirection,
    getLocationMapForHandRotation,
    HALVED_CAPS,
    QUARTERED_CAPS,
} from "../../domain/constants/circular-position-maps";
import type { SliceSize } from "../../domain/models/circular-models";

@injectable()
export class RotatedComplementaryCAPExecutor {
	constructor(
		@inject(TYPES.IOrientationCalculationService)
		private orientationCalculationService: IOrientationCalculationService,
		@inject(TYPES.IGridPositionDeriver)
		private gridPositionDeriver: IGridPositionDeriver,
		@inject(TYPES.IComplementaryLetterService)
		private complementaryLetterService: IComplementaryLetterService
	) {}

	/**
	 * Execute the rotated-complementary CAP
	 *
	 * @param sequence - The partial sequence to complete (must include start position at index 0)
	 * @param sliceSize - Slice size for the CAP (quartered or halved)
	 * @returns The complete circular sequence with all beats
	 */
	executeCAP(sequence: BeatData[], sliceSize: SliceSize): BeatData[] {
		// Validate the sequence
		this._validateSequence(sequence, sliceSize);

		// Remove start position (index 0) for processing
		const startPosition = sequence.shift();
		if (!startPosition) {
			throw new Error("Sequence must have a start position");
		}

		// Calculate how many beats to generate based on slice size
		const sequenceLength = sequence.length;
		let entriesToAdd: number;

		if (sliceSize === "quartered") {
			// Quartered adds 3x the original length
			entriesToAdd = sequenceLength * 3;
		} else {
			// Halved adds 1x the original length (doubles total)
			entriesToAdd = sequenceLength;
		}

		// Generate the new beats
		const generatedBeats: BeatData[] = [];
		let lastBeat = sequence[sequence.length - 1];
		let nextBeatNumber = lastBeat.beatNumber + 1;

		// Generate CAP beats
		const finalIntendedLength = sequenceLength + entriesToAdd;
		for (let i = 0; i < entriesToAdd; i++) {
			const nextBeat = this._createNewCAPEntry(
				sequence,
				lastBeat,
				nextBeatNumber,
				finalIntendedLength,
				sliceSize
			);

			generatedBeats.push(nextBeat);
			sequence.push(nextBeat);
			lastBeat = nextBeat;
			nextBeatNumber++;
		}

		// Re-insert start position at the beginning
		sequence.unshift(startPosition);

		return sequence;
	}

	/**
	 * Validate that the sequence can perform a rotated-complementary CAP
	 */
	private _validateSequence(sequence: BeatData[], sliceSize: SliceSize): void {
		if (sequence.length < 2) {
			throw new Error("Sequence must have at least 2 beats (start position + 1 beat)");
		}

		const startPos = sequence[0].startPosition;
		const endPos = sequence[sequence.length - 1].endPosition;

		if (!startPos || !endPos) {
			throw new Error("Sequence beats must have valid start and end positions");
		}

		// Check if the (start, end) pair is valid for the requested slice size
		const key = `${startPos},${endPos}`;
		const validationSet = sliceSize === "quartered" ? QUARTERED_CAPS : HALVED_CAPS;

		if (!validationSet.has(key)) {
			throw new Error(
				`Invalid position pair for rotated-complementary ${sliceSize} CAP: ${startPos} → ${endPos}. ` +
					`The end position must match the ${sliceSize} rotation requirement.`
			);
		}
	}

	/**
	 * Create a new CAP entry by transforming a previous beat with ROTATION + COMPLEMENTARY
	 */
	private _createNewCAPEntry(
		sequence: BeatData[],
		previousBeat: BeatData,
		beatNumber: number,
		finalIntendedLength: number,
		sliceSize: SliceSize
	): BeatData {
		// Get the corresponding beat from the first section using index mapping
		const previousMatchingBeat = this._getPreviousMatchingBeat(
			sequence,
			beatNumber,
			finalIntendedLength,
			sliceSize
		);

		// Get the complementary letter (COMPLEMENTARY effect)
		if (!previousMatchingBeat.letter) {
			throw new Error("Previous matching beat must have a letter");
		}
		const complementaryLetter = this.complementaryLetterService.getComplementaryLetter(
			previousMatchingBeat.letter
		);

		// Calculate the rotated end position
		const rotatedEndPosition = this._getRotatedEndPosition(previousBeat, previousMatchingBeat);

		// Create the new beat with rotated and complementary attributes
		// KEY: No color swapping - Blue stays Blue, Red stays Red
		//      Motion types are flipped (PRO ↔ ANTI)
		//      Prop rotations are flipped (CW ↔ CCW)
		//      Locations are rotated based on handpath direction
		const newBeat: BeatData = {
			...previousMatchingBeat,
			id: `beat-${beatNumber}`,
			beatNumber,
			letter: complementaryLetter, // COMPLEMENTARY: Flip letter
			startPosition: previousBeat.endPosition ?? null,
			endPosition: rotatedEndPosition,
			motions: {
				[MotionColor.BLUE]: this._createRotatedComplementaryMotion(
					MotionColor.BLUE,
					previousBeat,
					previousMatchingBeat
				),
				[MotionColor.RED]: this._createRotatedComplementaryMotion(
					MotionColor.RED,
					previousBeat,
					previousMatchingBeat
				),
			},
		};

		// Update orientations
		const beatWithStartOri = this.orientationCalculationService.updateStartOrientations(
			newBeat,
			previousBeat
		);
		const finalBeat = this.orientationCalculationService.updateEndOrientations(beatWithStartOri);

		return finalBeat;
	}

	/**
	 * Get the previous matching beat using index mapping
	 */
	private _getPreviousMatchingBeat(
		sequence: BeatData[],
		beatNumber: number,
		finalLength: number,
		sliceSize: SliceSize
	): BeatData {
		const indexMap = this._getIndexMap(finalLength, sliceSize);
		const matchingBeatNumber = indexMap[beatNumber];

		if (matchingBeatNumber === undefined) {
			throw new Error(`No index mapping found for beatNumber ${beatNumber}`);
		}

		// Convert 1-based beatNumber to 0-based array index
		const arrayIndex = matchingBeatNumber - 1;

		if (arrayIndex < 0 || arrayIndex >= sequence.length) {
			throw new Error(
				`Invalid index mapping: beatNumber ${beatNumber} → matchingBeatNumber ${matchingBeatNumber} → arrayIndex ${arrayIndex} (sequence length: ${sequence.length})`
			);
		}

		return sequence[arrayIndex];
	}

	/**
	 * Generate index mapping for retrieving corresponding beats
	 * Works for both quartered and halved patterns
	 */
	private _getIndexMap(length: number, sliceSize: SliceSize): Record<number, number> {
		const map: Record<number, number> = {};

		// Edge case handling
		if (sliceSize === "quartered" && length < 4) {
			for (let i = 1; i <= length; i++) {
				map[i] = Math.max(i - 1, 1);
			}
			return map;
		}

		if (sliceSize === "halved" && length < 2) {
			for (let i = 1; i <= length; i++) {
				map[i] = Math.max(i - 1, 1);
			}
			return map;
		}

		if (sliceSize === "quartered") {
			// Quartered: length = base * 4, so base = length / 4
			const baseLength = Math.floor(length / 4);
			for (let i = baseLength + 1; i <= length; i++) {
				map[i] = i - baseLength;
			}
		} else {
			// Halved: length = base * 2, so base = length / 2
			const baseLength = Math.floor(length / 2);
			for (let i = baseLength + 1; i <= length; i++) {
				map[i] = i - baseLength;
			}
		}

		return map;
	}

	/**
	 * Get the rotated end position by rotating both colors' locations
	 */
	private _getRotatedEndPosition(
		previousBeat: BeatData,
		previousMatchingBeat: BeatData
	): GridPosition | null {
		// Get hand rotation directions from the matching beat (same color)
		const blueHandRotDir = getHandRotationDirection(
			previousMatchingBeat.motions[MotionColor.BLUE]!.startLocation as GridLocation,
			previousMatchingBeat.motions[MotionColor.BLUE]!.endLocation as GridLocation
		);
		const redHandRotDir = getHandRotationDirection(
			previousMatchingBeat.motions[MotionColor.RED]!.startLocation as GridLocation,
			previousMatchingBeat.motions[MotionColor.RED]!.endLocation as GridLocation
		);

		// Get the location maps for rotation
		const blueLocationMap = getLocationMapForHandRotation(blueHandRotDir);
		const redLocationMap = getLocationMapForHandRotation(redHandRotDir);

		// Rotate the locations from the previous beat
		const newBlueEndLoc = blueLocationMap[previousBeat.motions[MotionColor.BLUE]!.endLocation as GridLocation];
		const newRedEndLoc = redLocationMap[previousBeat.motions[MotionColor.RED]!.endLocation as GridLocation];

		// Derive position from both locations
		const newEndPosition = this.gridPositionDeriver.getGridPositionFromLocations(newBlueEndLoc, newRedEndLoc);

		if (!newEndPosition) {
			throw new Error(
				`Could not derive position from locations: Blue=${newBlueEndLoc}, Red=${newRedEndLoc}`
			);
		}

		return newEndPosition;
	}

	/**
	 * Create rotated-complementary motion data for the new beat
	 * Combines location rotation with motion type and prop rotation flipping
	 */
	private _createRotatedComplementaryMotion(
		color: MotionColor,
		previousBeat: BeatData,
		previousMatchingBeat: BeatData
	): any {
		const previousMotion = previousBeat.motions[color];
		const matchingMotion = previousMatchingBeat.motions[color]; // Same color (no swap)

		if (!previousMotion || !matchingMotion) {
			throw new Error(`Missing motion data for ${color}`);
		}

		// Get hand rotation direction from the matching motion
		const handRotDir = getHandRotationDirection(
			matchingMotion.startLocation as GridLocation,
			matchingMotion.endLocation as GridLocation
		);

		// Get location map for this rotation direction
		const locationMap = getLocationMapForHandRotation(handRotDir);

		// Rotate the end location (ROTATED effect)
		const rotatedEndLocation = locationMap[previousMotion.endLocation as GridLocation];

		// Flip the motion type (COMPLEMENTARY effect)
		const originalMotionType = matchingMotion.motionType;
		const complementaryMotionType = this._getComplementaryMotionType(matchingMotion.motionType);

		// Flip the prop rotation direction (COMPLEMENTARY effect)
		const complementaryPropRotDir = this._getComplementaryPropRotDir(matchingMotion.rotationDirection);

		// Create rotated-complementary motion
		const rotatedComplementaryMotion = {
			...matchingMotion,
			color, // Preserve the color (no swap)
			motionType: complementaryMotionType, // COMPLEMENTARY: Flip motion type
			startLocation: previousMotion.endLocation,
			endLocation: rotatedEndLocation, // ROTATED: Rotate location
			rotationDirection: complementaryPropRotDir, // COMPLEMENTARY: Flip prop rotation
			// Start orientation will be set by orientationCalculationService
			// End orientation will be calculated by orientationCalculationService
		};

		return rotatedComplementaryMotion;
	}

	/**
	 * Get the complementary motion type (flip PRO ↔ ANTI)
	 * STATIC and DASH stay the same
	 */
	private _getComplementaryMotionType(motionType: MotionType): MotionType {
		if (motionType === MotionType.PRO) {
			return MotionType.ANTI;
		} else if (motionType === MotionType.ANTI) {
			return MotionType.PRO;
		}

		// STATIC and DASH stay the same
		return motionType;
	}

	/**
	 * Get the complementary prop rotation direction (flip CW ↔ CCW)
	 * NO_ROTATION stays NO_ROTATION
	 */
	private _getComplementaryPropRotDir(propRotDir: RotationDirection): RotationDirection {
		if (propRotDir === RotationDirection.CLOCKWISE) {
			return RotationDirection.COUNTER_CLOCKWISE;
		} else if (propRotDir === RotationDirection.COUNTER_CLOCKWISE) {
			return RotationDirection.CLOCKWISE;
		}

		// NO_ROTATION stays NO_ROTATION
		return propRotDir;
	}
}
