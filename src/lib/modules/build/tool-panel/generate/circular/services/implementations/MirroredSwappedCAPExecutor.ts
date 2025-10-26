/**
 * Mirrored Swapped CAP Executor
 *
 * Executes the mirrored-swapped CAP (Circular Arrangement Pattern) by combining:
 * 1. SWAPPED: Blue does what Red did, Red does what Blue did
 * 2. MIRRORED: Mirror locations vertically (E↔W), flip prop rotation (CW↔CCW)
 *
 * This creates a sequence where:
 * - Colors are swapped (Blue performs Red's actions and vice versa)
 * - Locations are mirrored vertically across the north-south axis
 * - Prop rotation directions are flipped
 * - Motion types stay the same
 * - Letters stay the same
 *
 * IMPORTANT: Slice size is ALWAYS halved (no quartering)
 * IMPORTANT: End position must be vertical mirror of start position
 */

import type { BeatData } from "$build/workbench";
import { MotionColor, RotationDirection, type IGridPositionDeriver } from "$shared";
import { TYPES } from "$shared/inversify/types";
import type { GridPosition, GridLocation } from "$shared/pictograph/grid/domain/enums/grid-enums";
import { inject, injectable } from "inversify";
import type { IOrientationCalculationService } from "../../../shared/services/contracts";
import {
	VERTICAL_MIRROR_POSITION_MAP,
	VERTICAL_MIRROR_LOCATION_MAP,
	MIRRORED_SWAPPED_VALIDATION_SET,
} from "../../domain/constants/strict-cap-position-maps";
import type { SliceSize } from "../../domain/models/circular-models";

@injectable()
export class MirroredSwappedCAPExecutor {
	constructor(
		@inject(TYPES.IOrientationCalculationService)
		private orientationCalculationService: IOrientationCalculationService,
		@inject(TYPES.IGridPositionDeriver)
		private gridPositionDeriver: IGridPositionDeriver
	) {}

	/**
	 * Execute the mirrored-swapped CAP
	 *
	 * @param sequence - The partial sequence to complete (must include start position at index 0)
	 * @param sliceSize - Ignored (mirrored-swapped CAP always uses halved)
	 * @returns The complete circular sequence with all beats
	 */
	executeCAP(sequence: BeatData[], sliceSize: SliceSize): BeatData[] {
		console.log("🔄🪞 Executing Mirrored-Swapped CAP (always halved)");
		console.log(`📊 Input sequence length: ${sequence.length} beats`);

		// Validate the sequence
		this._validateSequence(sequence);

		// Remove start position (index 0) for processing
		const startPosition = sequence.shift();
		if (!startPosition) {
			throw new Error("Sequence must have a start position");
		}

		// Calculate how many beats to generate (always doubles for halved)
		const sequenceLength = sequence.length;
		const entriesToAdd = sequenceLength;
		console.log(`➕ Will generate ${entriesToAdd} additional beats (mirrored-swapped)`);

		// Generate the new beats
		const generatedBeats: BeatData[] = [];
		let lastBeat = sequence[sequence.length - 1];
		let nextBeatNumber = lastBeat.beatNumber + 1;

		// Skip first two beats in the loop (start from beat 2)
		for (let i = 2; i < sequenceLength + 2; i++) {
			const finalIntendedLength = sequenceLength + entriesToAdd;
			const nextBeat = this._createNewCAPEntry(
				sequence,
				lastBeat,
				nextBeatNumber + i - 2,
				finalIntendedLength
			);

			generatedBeats.push(nextBeat);
			sequence.push(nextBeat);
			lastBeat = nextBeat;

			console.log(`✅ Generated mirrored-swapped beat ${nextBeat.beatNumber}: ${nextBeat.letter || "unknown"}`);
		}

		// Re-insert start position at the beginning
		sequence.unshift(startPosition);

		console.log(`🎉 Mirrored-Swapped CAP complete! Final sequence length: ${sequence.length} beats`);
		return sequence;
	}

	/**
	 * Validate that the sequence can perform a mirrored-swapped CAP
	 * Requirement: end_position must be vertical mirror of start_position
	 */
	private _validateSequence(sequence: BeatData[]): void {
		if (sequence.length < 2) {
			throw new Error("Sequence must have at least 2 beats (start position + 1 beat)");
		}

		const startPos = sequence[0].startPosition;
		const endPos = sequence[sequence.length - 1].endPosition;

		if (!startPos || !endPos) {
			throw new Error("Sequence beats must have valid start and end positions");
		}

		// Check if the (start, end) pair is valid for mirrored-swapped
		const key = `${startPos},${endPos}`;

		if (!MIRRORED_SWAPPED_VALIDATION_SET.has(key)) {
			throw new Error(
				`Invalid position pair for mirrored-swapped CAP: ${startPos} → ${endPos}. ` +
					`For a mirrored-swapped CAP, the end position must be the vertical mirror of start position.`
			);
		}

		console.log(`✅ Validation passed: ${startPos} → ${endPos} is valid for mirrored-swapped CAP`);
	}

	/**
	 * Create a new CAP entry by transforming a previous beat with SWAP + MIRROR
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
			`🔍 Creating mirrored-swapped beat ${beatNumber} from beat ${previousMatchingBeat.beatNumber} (letter: ${previousMatchingBeat.letter})`
		);

		// Get the mirrored end position
		const mirroredEndPosition = this._getMirroredPosition(previousMatchingBeat);

		// Create the new beat with swapped and mirrored attributes
		// KEY: Blue gets attributes from Red's matching beat (SWAP)
		//      Red gets attributes from Blue's matching beat (SWAP)
		//      Then locations and rotations are mirrored
		const newBeat: BeatData = {
			...previousMatchingBeat,
			id: `beat-${beatNumber}`,
			beatNumber,
			letter: previousMatchingBeat.letter, // Same letter
			startPosition: previousBeat.endPosition ?? null,
			endPosition: mirroredEndPosition,
			motions: {
				// SWAP: Blue does what Red did, but with mirrored transformation
				[MotionColor.BLUE]: this._createMirroredSwappedMotion(
					MotionColor.BLUE,
					previousBeat,
					previousMatchingBeat,
					true // isSwapped = true (use opposite color's data)
				),
				// SWAP: Red does what Blue did, but with mirrored transformation
				[MotionColor.RED]: this._createMirroredSwappedMotion(
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
	 * Get the previous matching beat using index mapping (halved pattern)
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
	 * Generate index mapping for retrieving corresponding beats (halved pattern only)
	 * Maps second half beats to first half beats
	 */
	private _getIndexMap(length: number): Record<number, number> {
		const map: Record<number, number> = {};
		const halfLength = Math.floor(length / 2);

		// Map beats in second half to their corresponding beats in first half
		for (let i = halfLength + 1; i <= length; i++) {
			map[i] = i - halfLength;
		}

		return map;
	}

	/**
	 * Get the vertical mirrored position
	 */
	private _getMirroredPosition(previousMatchingBeat: BeatData): GridPosition | null {
		const endPos = previousMatchingBeat.endPosition;

		if (!endPos) {
			throw new Error("Previous matching beat must have an end position");
		}

		const mirroredPosition = VERTICAL_MIRROR_POSITION_MAP[endPos as GridPosition];

		if (!mirroredPosition) {
			throw new Error(`No mirrored position found for ${endPos}`);
		}

		console.log(`📍 Mirrored position: ${endPos} → ${mirroredPosition}`);

		return mirroredPosition;
	}

	/**
	 * Create mirrored-swapped motion data for the new beat
	 * Combines color swapping with location mirroring and rotation flipping
	 */
	private _createMirroredSwappedMotion(
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

		// Mirror the end location vertically
		const mirroredEndLocation = this._getMirroredLocation(matchingMotion.endLocation as GridLocation);

		// Flip the prop rotation direction (mirroring effect)
		const originalPropRotDir = matchingMotion.rotationDirection;
		const mirroredPropRotDir = this._getMirroredPropRotDir(matchingMotion.rotationDirection);

		console.log(
			`🔄🪞 [${color}] Mirrored-Swapped: motionType=${matchingMotion.motionType}, ` +
			`${originalPropRotDir} → ${mirroredPropRotDir}, ` +
			`${matchingMotion.endLocation} → ${mirroredEndLocation}`
		);

		// Create mirrored-swapped motion
		const mirroredSwappedMotion = {
			...matchingMotion,
			color, // IMPORTANT: Preserve the color (Blue stays Blue, Red stays Red)
			motionType: matchingMotion.motionType, // Same motion type (no complementary flip)
			startLocation: previousMotion.endLocation,
			endLocation: mirroredEndLocation,
			rotationDirection: mirroredPropRotDir,
			// Start orientation will be set by orientationCalculationService
			// End orientation will be calculated by orientationCalculationService
		};

		return mirroredSwappedMotion;
	}

	/**
	 * Mirror a location vertically (flip east/west)
	 */
	private _getMirroredLocation(location: GridLocation): GridLocation {
		const mirrored = VERTICAL_MIRROR_LOCATION_MAP[location];

		if (!mirrored) {
			throw new Error(`No mirrored location found for ${location}`);
		}

		return mirrored;
	}

	/**
	 * Mirror prop rotation direction (flip CLOCKWISE ↔ COUNTER_CLOCKWISE)
	 * NO_ROTATION stays NO_ROTATION
	 */
	private _getMirroredPropRotDir(propRotDir: RotationDirection): RotationDirection {
		if (propRotDir === RotationDirection.CLOCKWISE) {
			return RotationDirection.COUNTER_CLOCKWISE;
		} else if (propRotDir === RotationDirection.COUNTER_CLOCKWISE) {
			return RotationDirection.CLOCKWISE;
		}

		// NO_ROTATION stays NO_ROTATION
		return propRotDir;
	}
}
