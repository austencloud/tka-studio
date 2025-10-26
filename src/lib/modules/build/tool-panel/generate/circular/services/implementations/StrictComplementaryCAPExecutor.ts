/**
 * Strict Complementary CAP Executor
 *
 * Executes the strict complementary CAP (Circular Arrangement Pattern) by:
 * 1. Taking a partial sequence (always first half - no quartering)
 * 2. Using complementary letters (opposite motion types)
 * 3. Generating the remaining beats to complete the circular pattern
 *
 * The complementary transformation works by:
 * - Using complementary letters (A↔B, D↔E, G↔H, etc.)
 * - Flipping motion types (PRO ↔ ANTI)
 * - Flipping prop rotation directions (CLOCKWISE ↔ COUNTER_CLOCKWISE)
 * - Keeping positions the same (sequence returns to start position)
 * - Maintaining the same hand locations
 *
 * IMPORTANT: Slice size is ALWAYS halved (no user choice like STRICT_ROTATED)
 * IMPORTANT: End position must equal start position for complementary CAPs
 */

import type { BeatData } from "$build/workbench";
import { MotionColor, MotionType, RotationDirection, type IGridPositionDeriver } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IOrientationCalculationService } from "../../../shared/services/contracts";
import {
    COMPLEMENTARY_CAP_VALIDATION_SET,
    getComplementaryLetter,
} from "../../domain/constants/strict-cap-position-maps";
import type { SliceSize } from "../../domain/models/circular-models";

@injectable()
export class StrictComplementaryCAPExecutor {
	constructor(
		@inject(TYPES.IOrientationCalculationService)
		private orientationCalculationService: IOrientationCalculationService,
		@inject(TYPES.IGridPositionDeriver)
		private gridPositionDeriver: IGridPositionDeriver
	) {}

	/**
	 * Execute the strict complementary CAP
	 *
	 * @param sequence - The partial sequence to complete (must include start position at index 0)
	 * @param sliceSize - Ignored (complementary CAP always uses halved)
	 * @returns The complete circular sequence with all beats
	 */
	executeCAP(sequence: BeatData[], sliceSize: SliceSize): BeatData[] {
		console.log("🎨 Executing Strict Complementary CAP (always halved)");
		console.log(`📊 Input sequence length: ${sequence.length} beats`);

		// Validate the sequence
		this._validateSequence(sequence);

		// Remove start position (index 0) for processing
		const startPosition = sequence.shift();
		if (!startPosition) {
			throw new Error("Sequence must have a start position");
		}

		// Calculate how many beats to generate (always doubles for complementary)
		const sequenceLength = sequence.length;
		const entriesToAdd = sequenceLength; // Always halved = doubles the sequence
		console.log(`➕ Will generate ${entriesToAdd} additional beats (complementary)`);

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

			console.log(`✅ Generated complementary beat ${nextBeat.beatNumber}: ${nextBeat.letter || "unknown"}`);
		}

		// Re-insert start position at the beginning
		sequence.unshift(startPosition);

		console.log(`🎉 Complementary CAP complete! Final sequence length: ${sequence.length} beats`);
		return sequence;
	}

	/**
	 * Validate that the sequence can perform a complementary CAP
	 * Requirement: end_position === start_position (returns to start)
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

		// Check if the (start, end) pair is valid for complementary (must be same)
		const key = `${startPos},${endPos}`;

		if (!COMPLEMENTARY_CAP_VALIDATION_SET.has(key)) {
			throw new Error(
				`Invalid position pair for complementary CAP: ${startPos} → ${endPos}. ` +
					`For a complementary CAP, the sequence must end at the same position it started (${startPos}).`
			);
		}

		console.log(`✅ Validation passed: ${startPos} → ${endPos} is valid for complementary CAP`);
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
			`🔍 Creating complementary beat ${beatNumber} from beat ${previousMatchingBeat.beatNumber} (letter: ${previousMatchingBeat.letter})`
		);

		// Get complementary letter
		const complementaryLetter = this._getComplementaryLetter(previousMatchingBeat);

		// Create the new beat with complementary attributes
		const newBeat: BeatData = {
			...previousMatchingBeat,
			id: `beat-${beatNumber}`,
			beatNumber,
			letter: complementaryLetter as any,
			startPosition: previousBeat.endPosition ?? null,
			endPosition: previousMatchingBeat.endPosition, // Same as matching beat
			motions: {
				[MotionColor.BLUE]: this._createComplementaryMotion(
					MotionColor.BLUE,
					previousBeat,
					previousMatchingBeat
				),
				[MotionColor.RED]: this._createComplementaryMotion(
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
	 * Get complementary letter
	 */
	private _getComplementaryLetter(previousMatchingBeat: BeatData): string {
		const letter = previousMatchingBeat.letter;

		if (!letter) {
			throw new Error("Previous matching beat must have a letter");
		}

		const complementaryLetter = getComplementaryLetter(letter);

		console.log(`🔤 Complementary letter: ${letter} → ${complementaryLetter}`);

		return complementaryLetter;
	}

	/**
	 * Create complementary motion data for the new beat
	 * Flips motion type (PRO ↔ ANTI) and prop rotation direction
	 */
	private _createComplementaryMotion(
		color: MotionColor,
		previousBeat: BeatData,
		previousMatchingBeat: BeatData
	): any {
		const previousMotion = previousBeat.motions[color];
		const matchingMotion = previousMatchingBeat.motions[color];

		if (!previousMotion || !matchingMotion) {
			throw new Error(`Missing motion data for ${color}`);
		}

		// Flip the motion type (PRO ↔ ANTI)
		const complementaryMotionType = this._getComplementaryMotionType(matchingMotion.motionType);

		// Flip the prop rotation direction (FIXED: use rotationDirection not propRotationDirection)
		const originalPropRotDir = matchingMotion.rotationDirection;
		const complementaryPropRotDir = this._getComplementaryPropRotDir(matchingMotion.rotationDirection);

		console.log(
			`🔄 [${color}] Prop rotation complementary: ${originalPropRotDir} → ${complementaryPropRotDir}`
		);

		// Create complementary motion
		const complementaryMotion = {
			...matchingMotion,
			motionType: complementaryMotionType,
			startLocation: previousMotion.endLocation,
			endLocation: matchingMotion.endLocation, // Same as matching beat
			rotationDirection: complementaryPropRotDir,
			// Start orientation will be set by orientationCalculationService
			// End orientation will be calculated by orientationCalculationService
		};

		console.log(
			`📦 [${color}] Complementary motion created:`,
			{
				motionType: complementaryMotion.motionType,
				startLoc: complementaryMotion.startLocation,
				endLoc: complementaryMotion.endLocation,
				rotationDir: complementaryMotion.rotationDirection,
			}
		);

		return complementaryMotion;
	}

	/**
	 * Get complementary motion type (flip PRO ↔ ANTI)
	 * Other motion types (FLOAT, DASH, STATIC) remain unchanged
	 */
	private _getComplementaryMotionType(motionType: MotionType): MotionType {
		if (motionType === MotionType.PRO) {
			return MotionType.ANTI;
		} else if (motionType === MotionType.ANTI) {
			return MotionType.PRO;
		}

		// FLOAT, DASH, STATIC stay the same
		return motionType;
	}

	/**
	 * Get complementary prop rotation direction (flip CLOCKWISE ↔ COUNTER_CLOCKWISE)
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
