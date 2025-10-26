/**
 * Strict Mirrored CAP Executor
 *
 * Executes the strict mirrored CAP (Circular Arrangement Pattern) by:
 * 1. Taking a partial sequence (always first half - no quartering)
 * 2. Applying vertical mirroring transformations to each beat
 * 3. Generating the remaining beats to complete the circular pattern
 *
 * The mirroring works by:
 * - Flipping positions vertically across the center horizontal axis
 * - Mirroring hand locations (east ↔ west, northeast ↔ northwest, etc.)
 * - Flipping prop rotation directions (clockwise ↔ counter-clockwise)
 * - Maintaining the same letters and motion types
 *
 * IMPORTANT: Slice size is ALWAYS halved (no user choice like STRICT_ROTATED)
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
	MIRRORED_CAP_VALIDATION_SET,
} from "../../domain/constants/strict-cap-position-maps";
import type { SliceSize } from "../../domain/models/circular-models";

@injectable()
export class StrictMirroredCAPExecutor {
	constructor(
		@inject(TYPES.IOrientationCalculationService)
		private orientationCalculationService: IOrientationCalculationService,
		@inject(TYPES.IGridPositionDeriver)
		private gridPositionDeriver: IGridPositionDeriver
	) {}

	/**
	 * Execute the strict mirrored CAP
	 *
	 * @param sequence - The partial sequence to complete (must include start position at index 0)
	 * @param sliceSize - Ignored (mirrored CAP always uses halved)
	 * @returns The complete circular sequence with all beats
	 */
	executeCAP(sequence: BeatData[], sliceSize: SliceSize): BeatData[] {
		console.log("🪞 Executing Strict Mirrored CAP (always halved)");
		console.log(`📊 Input sequence length: ${sequence.length} beats`);

		// Validate the sequence
		this._validateSequence(sequence);

		// Remove start position (index 0) for processing
		const startPosition = sequence.shift();
		if (!startPosition) {
			throw new Error("Sequence must have a start position");
		}

		// Calculate how many beats to generate (always doubles for mirrored)
		const sequenceLength = sequence.length;
		const entriesToAdd = sequenceLength; // Always halved = doubles the sequence
		console.log(`➕ Will generate ${entriesToAdd} additional beats (mirrored)`);

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

			console.log(`✅ Generated mirrored beat ${nextBeat.beatNumber}: ${nextBeat.letter || "unknown"}`);
		}

		// Re-insert start position at the beginning
		sequence.unshift(startPosition);

		console.log(`🎉 Mirrored CAP complete! Final sequence length: ${sequence.length} beats`);
		return sequence;
	}

	/**
	 * Validate that the sequence can perform a mirrored CAP
	 * Requirement: vertical_mirror(start_position) === end_position
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

		// Check if the (start, end) pair is valid for mirroring
		const key = `${startPos},${endPos}`;

		if (!MIRRORED_CAP_VALIDATION_SET.has(key)) {
			const expectedEnd = VERTICAL_MIRROR_POSITION_MAP[startPos as GridPosition];
			throw new Error(
				`Invalid position pair for mirrored CAP: ${startPos} → ${endPos}. ` +
					`For a mirrored CAP from ${startPos}, the sequence must end at ${expectedEnd}.`
			);
		}

		console.log(`✅ Validation passed: ${startPos} → ${endPos} is valid for mirrored CAP`);
	}

	/**
	 * Create a new CAP entry by transforming a previous beat
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
			`🔍 Mirroring beat ${beatNumber} with beat ${previousMatchingBeat.beatNumber} (letter: ${previousMatchingBeat.letter})`
		);

		// Calculate new end position (vertical mirror)
		const newEndPosition = this._getMirroredPosition(previousMatchingBeat);

		// Create the new beat with mirrored attributes
		const newBeat: BeatData = {
			...previousMatchingBeat,
			id: `beat-${beatNumber}`,
			beatNumber,
			startPosition: previousBeat.endPosition ?? null,
			endPosition: newEndPosition,
			motions: {
				[MotionColor.BLUE]: this._createMirroredMotion(
					MotionColor.BLUE,
					previousBeat,
					previousMatchingBeat
				),
				[MotionColor.RED]: this._createMirroredMotion(
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

		// Debug: Verify prop rotation is still correct after orientation calculations
		console.log(
			`✅ Beat ${beatNumber} final prop rotations:`,
			{
				blue: finalBeat.motions[MotionColor.BLUE]?.rotationDirection,
				red: finalBeat.motions[MotionColor.RED]?.rotationDirection,
			}
		);

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
	 * Create mirrored motion data for the new beat
	 * Mirrors locations vertically and flips prop rotation direction
	 */
	private _createMirroredMotion(
		color: MotionColor,
		previousBeat: BeatData,
		previousMatchingBeat: BeatData
	): any {
		const previousMotion = previousBeat.motions[color];
		const matchingMotion = previousMatchingBeat.motions[color];

		if (!previousMotion || !matchingMotion) {
			throw new Error(`Missing motion data for ${color}`);
		}

		// Mirror the end location vertically
		const mirroredEndLocation = this._getMirroredLocation(matchingMotion.endLocation as GridLocation);

		// Flip the prop rotation direction
		const originalPropRotDir = matchingMotion.rotationDirection;
		const mirroredPropRotDir = this._getMirroredPropRotDir(matchingMotion.rotationDirection);

		console.log(
			`🔄 [${color}] Prop rotation mirroring: ${originalPropRotDir} → ${mirroredPropRotDir}`
		);

		// Create mirrored motion
		const mirroredMotion = {
			...matchingMotion,
			startLocation: previousMotion.endLocation,
			endLocation: mirroredEndLocation,
			rotationDirection: mirroredPropRotDir,
			// Start orientation will be set by orientationCalculationService
			// End orientation will be calculated by orientationCalculationService
		};

		console.log(
			`📦 [${color}] Mirrored motion created:`,
			{
				motionType: mirroredMotion.motionType,
				startLoc: mirroredMotion.startLocation,
				endLoc: mirroredMotion.endLocation,
				rotationDir: mirroredMotion.rotationDirection,
			}
		);

		return mirroredMotion;
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
	 * Mirror prop rotation direction (flip clockwise/counter-clockwise)
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
