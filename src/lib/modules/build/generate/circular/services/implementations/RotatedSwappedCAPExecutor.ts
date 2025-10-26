/**
 * Rotated Swapped CAP Executor
 *
 * Executes the rotated-swapped CAP (Circular Arrangement Pattern) by combining:
 * 1. SWAPPED: Blue does what Red did, Red does what Blue did
 * 2. ROTATED: Rotate locations based on handpath direction (90°, 180°, or 270°)
 *
 * This creates a sequence where:
 * - Colors are swapped (Blue performs Red's actions and vice versa)
 * - Locations are rotated based on the handpath direction of each color's motion
 * - Motion types stay the same (from opposite color due to swap)
 * - Prop rotation directions stay the same (from opposite color due to swap)
 * - Letters stay the same
 *
 * IMPORTANT: Supports both quartered and halved slice sizes
 * IMPORTANT: End position is calculated from rotated locations
 */

import type { BeatData } from "$build/workspace-panel";
import { MotionColor, type IGridPositionDeriver } from "$shared";
import { TYPES } from "$shared/inversify/types";
import type { GridLocation, GridPosition } from "$shared/pictograph/grid/domain/enums/grid-enums";
import { inject, injectable } from "inversify";
import type { IOrientationCalculationService } from "../../../shared/services/contracts";
import {
    getHandRotationDirection,
    getLocationMapForHandRotation,
    HALVED_CAPS,
    QUARTERED_CAPS,
} from "../../domain/constants/circular-position-maps";
import type { SliceSize } from "../../domain/models/circular-models";

@injectable()
export class RotatedSwappedCAPExecutor {
	constructor(
		@inject(TYPES.IOrientationCalculationService)
		private orientationCalculationService: IOrientationCalculationService,
		@inject(TYPES.IGridPositionDeriver)
		private gridPositionDeriver: IGridPositionDeriver
	) {}

	/**
	 * Execute the rotated-swapped CAP
	 *
	 * @param sequence - The partial sequence to complete (must include start position at index 0)
	 * @param sliceSize - Slice size for the CAP (quartered or halved)
	 * @returns The complete circular sequence with all beats
	 */
	executeCAP(sequence: BeatData[], sliceSize: SliceSize): BeatData[] {
		console.log(`🔄🔁 Executing Rotated-Swapped CAP (${sliceSize})`);
		console.log(`📊 Input sequence length: ${sequence.length} beats`);

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

		console.log(`➕ Will generate ${entriesToAdd} additional beats (rotated-swapped ${sliceSize})`);

		// Generate the new beats
		const generatedBeats: BeatData[] = [];
		let lastBeat = sequence[sequence.length - 1];
		let nextBeatNumber = lastBeat.beatNumber + 1;

		// Skip first two beats in the loop (start from beat 2)
		const finalIntendedLength = sequenceLength + entriesToAdd;
		for (let i = 0; i < entriesToAdd; i++) {
			const nextBeat = this._createNewCAPEntry(
				sequence,
				lastBeat,
				nextBeatNumber,
				finalIntendedLength
			);

			generatedBeats.push(nextBeat);
			sequence.push(nextBeat);
			lastBeat = nextBeat;
			nextBeatNumber++;

			console.log(`✅ Generated rotated-swapped beat ${nextBeat.beatNumber}: ${nextBeat.letter || "unknown"}`);
		}

		// Re-insert start position at the beginning
		sequence.unshift(startPosition);

		console.log(`🎉 Rotated-Swapped CAP complete! Final sequence length: ${sequence.length} beats`);
		return sequence;
	}

	/**
	 * Validate that the sequence can perform a rotated-swapped CAP
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
				`Invalid position pair for rotated-swapped ${sliceSize} CAP: ${startPos} → ${endPos}. ` +
					`The end position must match the ${sliceSize} rotation requirement.`
			);
		}

		console.log(`✅ Validation passed: ${startPos} → ${endPos} is valid for rotated-swapped ${sliceSize} CAP`);
	}

	/**
	 * Create a new CAP entry by transforming a previous beat with SWAP + ROTATION
	 */
	private _createNewCAPEntry(
		sequence: BeatData[],
		previousBeat: BeatData,
		beatNumber: number,
		finalIntendedLength: number
	): BeatData {
		// Get the corresponding beat from the first section using index mapping
		const previousMatchingBeat = this._getPreviousMatchingBeat(
			sequence,
			beatNumber,
			finalIntendedLength
		);

		console.log(
			`🔍 Creating rotated-swapped beat ${beatNumber} from beat ${previousMatchingBeat.beatNumber} (letter: ${previousMatchingBeat.letter})`
		);

		// Calculate the rotated end position
		const rotatedEndPosition = this._getRotatedEndPosition(previousBeat, previousMatchingBeat);

		// Create the new beat with swapped and rotated attributes
		// KEY: Blue gets attributes from Red's matching beat (SWAP)
		//      Red gets attributes from Blue's matching beat (SWAP)
		//      Then locations are rotated based on handpath direction
		const newBeat: BeatData = {
			...previousMatchingBeat,
			id: `beat-${beatNumber}`,
			beatNumber,
			letter: previousMatchingBeat.letter, // Same letter
			startPosition: previousBeat.endPosition ?? null,
			endPosition: rotatedEndPosition,
			motions: {
				// SWAP: Blue does what Red did, but with rotated transformation
				[MotionColor.BLUE]: this._createRotatedSwappedMotion(
					MotionColor.BLUE,
					previousBeat,
					previousMatchingBeat,
					true // isSwapped = true (use opposite color's data)
				),
				// SWAP: Red does what Blue did, but with rotated transformation
				[MotionColor.RED]: this._createRotatedSwappedMotion(
					MotionColor.RED,
					previousBeat,
					previousMatchingBeat,
					true // isSwapped = true (use opposite color's data)
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
		finalLength: number
	): BeatData {
		const indexMap = this._getIndexMap(finalLength);
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
	private _getIndexMap(length: number): Record<number, number> {
		const map: Record<number, number> = {};

		if (length < 2) {
			// Edge case: very short sequences
			for (let i = 1; i <= length; i++) {
				map[i] = Math.max(i - 1, 1);
			}
			return map;
		}

		// For both quartered and halved, we calculate the base length
		// Quartered: length = base * 4, so base = length / 4
		// Halved: length = base * 2, so base = length / 2
		// The mapping is: beats beyond the base length map back to beats within the base
		const baseLength = Math.floor(length / 2); // Works for both cases due to how they're structured

		for (let i = baseLength + 1; i <= length; i++) {
			map[i] = i - baseLength;
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
		// Get hand rotation directions from the matching beat (before swap)
		// Blue will use Red's handpath (due to swap)
		// Red will use Blue's handpath (due to swap)
		const blueHandRotDir = getHandRotationDirection(
			previousMatchingBeat.motions[MotionColor.RED]!.startLocation as GridLocation,
			previousMatchingBeat.motions[MotionColor.RED]!.endLocation as GridLocation
		);
		const redHandRotDir = getHandRotationDirection(
			previousMatchingBeat.motions[MotionColor.BLUE]!.startLocation as GridLocation,
			previousMatchingBeat.motions[MotionColor.BLUE]!.endLocation as GridLocation
		);

		// Get the location maps for rotation
		const blueLocationMap = getLocationMapForHandRotation(blueHandRotDir);
		const redLocationMap = getLocationMapForHandRotation(redHandRotDir);

		// Rotate the locations from the previous beat
		const newBlueEndLoc = blueLocationMap[previousBeat.motions[MotionColor.BLUE]!.endLocation as GridLocation];
		const newRedEndLoc = redLocationMap[previousBeat.motions[MotionColor.RED]!.endLocation as GridLocation];

		console.log(
			`📍 Rotating locations: Blue ${previousBeat.motions[MotionColor.BLUE]!.endLocation} → ${newBlueEndLoc}, ` +
			`Red ${previousBeat.motions[MotionColor.RED]!.endLocation} → ${newRedEndLoc}`
		);

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
	 * Create rotated-swapped motion data for the new beat
	 * Combines color swapping with location rotation
	 */
	private _createRotatedSwappedMotion(
		color: MotionColor,
		previousBeat: BeatData,
		previousMatchingBeat: BeatData,
		isSwapped: boolean
	): any {
		const previousMotion = previousBeat.motions[color];

		// SWAP: Get the opposite color's motion data
		const oppositeColor = color === MotionColor.BLUE ? MotionColor.RED : MotionColor.BLUE;
		const matchingMotion = isSwapped
			? previousMatchingBeat.motions[oppositeColor]
			: previousMatchingBeat.motions[color];

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

		// Rotate the end location
		const rotatedEndLocation = locationMap[previousMotion.endLocation as GridLocation];

		console.log(
			`🔄🔁 [${color}] Rotated-Swapped: motionType=${matchingMotion.motionType}, ` +
			`rotation=${matchingMotion.rotationDirection}, ` +
			`handRotDir=${handRotDir}, ` +
			`${previousMotion.endLocation} → ${rotatedEndLocation}`
		);

		// Create rotated-swapped motion
		const rotatedSwappedMotion = {
			...matchingMotion,
			color, // IMPORTANT: Preserve the color (Blue stays Blue, Red stays Red)
			motionType: matchingMotion.motionType, // Same motion type (from opposite color due to swap)
			startLocation: previousMotion.endLocation,
			endLocation: rotatedEndLocation,
			rotationDirection: matchingMotion.rotationDirection, // Same rotation direction (from opposite color due to swap)
			// Start orientation will be set by orientationCalculationService
			// End orientation will be calculated by orientationCalculationService
		};

		return rotatedSwappedMotion;
	}
}
