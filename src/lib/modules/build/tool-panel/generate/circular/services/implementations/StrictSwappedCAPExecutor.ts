/**
 * Strict Swapped CAP Executor
 *
 * Executes the strict swapped CAP (Circular Arrangement Pattern) by:
 * 1. Taking a partial sequence (always first half - no quartering)
 * 2. Swapping blue and red attributes between beats
 * 3. Generating the remaining beats to complete the circular pattern
 *
 * The swapping works by:
 * - Swapping blue ↔ red motion attributes entirely
 * - Transforming positions according to the swap map
 * - Maintaining the same letters, motion types, and prop rotation directions
 * - Only the color assignment changes
 *
 * IMPORTANT: Slice size is ALWAYS halved (no user choice like STRICT_ROTATED)
 */

import type { BeatData } from "$build/workbench";
import { MotionColor, type IGridPositionDeriver } from "$shared";
import { TYPES } from "$shared/inversify/types";
import type { GridPosition } from "$shared/pictograph/grid/domain/enums/grid-enums";
import { inject, injectable } from "inversify";
import type { IOrientationCalculationService } from "../../../shared/services/contracts";
import {
	SWAPPED_POSITION_MAP,
	SWAPPED_CAP_VALIDATION_SET,
} from "../../domain/constants/strict-cap-position-maps";
import type { SliceSize } from "../../domain/models/circular-models";

@injectable()
export class StrictSwappedCAPExecutor {
	constructor(
		@inject(TYPES.IOrientationCalculationService)
		private orientationCalculationService: IOrientationCalculationService,
		@inject(TYPES.IGridPositionDeriver)
		private gridPositionDeriver: IGridPositionDeriver
	) {}

	/**
	 * Execute the strict swapped CAP
	 *
	 * @param sequence - The partial sequence to complete (must include start position at index 0)
	 * @param sliceSize - Ignored (swapped CAP always uses halved)
	 * @returns The complete circular sequence with all beats
	 */
	executeCAP(sequence: BeatData[], sliceSize: SliceSize): BeatData[] {
		console.log("🔀 Executing Strict Swapped CAP (always halved)");
		console.log(`📊 Input sequence length: ${sequence.length} beats`);

		// Validate the sequence
		this._validateSequence(sequence);

		// Remove start position (index 0) for processing
		const startPosition = sequence.shift();
		if (!startPosition) {
			throw new Error("Sequence must have a start position");
		}

		// Calculate how many beats to generate (always doubles for swapped)
		const sequenceLength = sequence.length;
		const entriesToAdd = sequenceLength; // Always halved = doubles the sequence
		console.log(`➕ Will generate ${entriesToAdd} additional beats (swapped)`);

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

			console.log(`✅ Generated swapped beat ${nextBeat.beatNumber}: ${nextBeat.letter || "unknown"}`);
		}

		// Re-insert start position at the beginning
		sequence.unshift(startPosition);

		console.log(`🎉 Swapped CAP complete! Final sequence length: ${sequence.length} beats`);
		return sequence;
	}

	/**
	 * Validate that the sequence can perform a swapped CAP
	 * Requirement: swapped_position(start_position) === end_position
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

		// Check if the (start, end) pair is valid for swapping
		const key = `${startPos},${endPos}`;

		if (!SWAPPED_CAP_VALIDATION_SET.has(key)) {
			const expectedEnd = SWAPPED_POSITION_MAP[startPos as GridPosition];
			throw new Error(
				`Invalid position pair for swapped CAP: ${startPos} → ${endPos}. ` +
					`For a swapped CAP from ${startPos}, the sequence must end at ${expectedEnd}.`
			);
		}

		console.log(`✅ Validation passed: ${startPos} → ${endPos} is valid for swapped CAP`);
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
			`🔍 Swapping beat ${beatNumber} with beat ${previousMatchingBeat.beatNumber} (letter: ${previousMatchingBeat.letter})`
		);

		// Debug: Log the previous beat's end position (where we're starting from)
		console.log(
			`📍 Previous beat ${previousBeat.beatNumber}: endPosition=${previousBeat.endPosition}`,
			{
				blueEndLoc: previousBeat.motions[MotionColor.BLUE]?.endLocation,
				redEndLoc: previousBeat.motions[MotionColor.RED]?.endLocation
			}
		);

		// Debug: Log the matching beat's data (what we're swapping from)
		console.log(
			`📍 Matching beat ${previousMatchingBeat.beatNumber}: startPos=${previousMatchingBeat.startPosition}, endPos=${previousMatchingBeat.endPosition}`,
			{
				blueStartLoc: previousMatchingBeat.motions[MotionColor.BLUE]?.startLocation,
				blueEndLoc: previousMatchingBeat.motions[MotionColor.BLUE]?.endLocation,
				redStartLoc: previousMatchingBeat.motions[MotionColor.RED]?.startLocation,
				redEndLoc: previousMatchingBeat.motions[MotionColor.RED]?.endLocation
			}
		);

		// Create the swapped motions first
		const blueMotion = this._createSwappedMotion(
			MotionColor.BLUE,
			previousBeat,
			previousMatchingBeat.motions[MotionColor.RED] // Use RED from matching beat
		);
		const redMotion = this._createSwappedMotion(
			MotionColor.RED,
			previousBeat,
			previousMatchingBeat.motions[MotionColor.BLUE] // Use BLUE from matching beat
		);

		// CRITICAL: Recalculate the actual grid positions from the hand locations
		// The swapped map is just a validation - we need to derive positions from actual hand locations
		const actualStartPosition = this.gridPositionDeriver.getGridPositionFromLocations(
			blueMotion.startLocation,
			redMotion.startLocation
		);
		const actualEndPosition = this.gridPositionDeriver.getGridPositionFromLocations(
			blueMotion.endLocation,
			redMotion.endLocation
		);

		console.log(
			`📍 New beat ${beatNumber}: ` +
			`startPosition=${actualStartPosition} (from blue=${blueMotion.startLocation}, red=${redMotion.startLocation}), ` +
			`endPosition=${actualEndPosition} (from blue=${blueMotion.endLocation}, red=${redMotion.endLocation})`
		);

		// Create the new beat with swapped attributes (BLUE ↔ RED)
		// Note: We swap the color assignments - blue gets red's data and vice versa
		const newBeat: BeatData = {
			...previousMatchingBeat,
			id: `beat-${beatNumber}`,
			beatNumber,
			startPosition: actualStartPosition,
			endPosition: actualEndPosition,
			motions: {
				[MotionColor.BLUE]: blueMotion,
				[MotionColor.RED]: redMotion,
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
	 * Get the swapped position
	 */
	private _getSwappedPosition(previousMatchingBeat: BeatData): GridPosition | null {
		const endPos = previousMatchingBeat.endPosition;

		if (!endPos) {
			throw new Error("Previous matching beat must have an end position");
		}

		const swappedPosition = SWAPPED_POSITION_MAP[endPos as GridPosition];

		if (!swappedPosition) {
			throw new Error(`No swapped position found for ${endPos}`);
		}

		console.log(`📍 Swapped position: ${endPos} → ${swappedPosition}`);

		return swappedPosition;
	}

	/**
	 * Create swapped motion data for the new beat
	 * Uses the opposite color's matching motion attributes
	 */
	private _createSwappedMotion(
		color: MotionColor,
		previousBeat: BeatData,
		matchingMotion: any // This is from the OPPOSITE color in the matching beat
	): any {
		const previousMotion = previousBeat.motions[color];

		if (!previousMotion || !matchingMotion) {
			throw new Error(`Missing motion data for ${color}`);
		}

		console.log(
			`🔀 [${color}] Creating swapped motion:`,
			{
				matchingMotionColor: matchingMotion.color,
				previousMotionEndLoc: previousMotion.endLocation,
				matchingMotionEndLoc: matchingMotion.endLocation,
				matchingMotionType: matchingMotion.motionType,
				matchingPropRotDir: matchingMotion.rotationDirection
			}
		);

		// CRITICAL: We must explicitly set the color to match THIS motion,
		// not copy it from the opposite color's matching motion!
		// We want Blue to DO what Red did, but still BE Blue.
		const swappedMotion = {
			...matchingMotion,
			color, // FIXED: Set to THIS motion's color, not matchingMotion's color
			startLocation: previousMotion.endLocation,
			endLocation: matchingMotion.endLocation, // Keep same end location from swapped motion
			// motionType, rotationDirection, turns all come from matchingMotion (opposite color)
			// Start orientation will be set by orientationCalculationService
			// End orientation will be calculated by orientationCalculationService
		};

		console.log(
			`✅ [${color}] Swapped motion result:`,
			{
				color: swappedMotion.color,
				startLoc: swappedMotion.startLocation,
				endLoc: swappedMotion.endLocation,
				motionType: swappedMotion.motionType
			}
		);

		return swappedMotion;
	}
}
