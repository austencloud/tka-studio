/**
 * Swapped Complementary CAP Executor
 *
 * Executes the swapped-complementary CAP (Circular Arrangement Pattern) by combining:
 * 1. SWAPPED: Blue does what Red did, Red does what Blue did
 * 2. COMPLEMENTARY: Flip letters, flip motion types (PRO↔ANTI), flip prop rotation (CW↔CCW)
 *
 * This creates a sequence where:
 * - Colors are swapped (Blue performs Red's actions and vice versa)
 * - Letters are complementary (A↔B, D↔E, etc.)
 * - Motion types are flipped (PRO↔ANTI)
 * - Prop rotation directions are flipped (CW↔CCW)
 * - Locations stay the same (returns to starting position)
 *
 * IMPORTANT: Slice size is ALWAYS halved (no quartering)
 * IMPORTANT: End position must equal start position (returns to start)
 */

import type { BeatData } from "$create/shared/workspace-panel";
import type { Letter } from "$shared";
import type { IGridPositionDeriver } from "$shared";
import { MotionColor, MotionType, RotationDirection } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IOrientationCalculationService } from "../../../shared/services/contracts";
import {
  COMPLEMENTARY_CAP_VALIDATION_SET,
  getComplementaryLetter,
} from "../../domain/constants/strict-cap-position-maps";
import type { SliceSize } from "../../domain/models/circular-models";

@injectable()
export class SwappedComplementaryCAPExecutor {
  constructor(
    @inject(TYPES.IOrientationCalculationService)
    private orientationCalculationService: IOrientationCalculationService,
    @inject(TYPES.IGridPositionDeriver)
    private gridPositionDeriver: IGridPositionDeriver
  ) {}

  /**
   * Execute the swapped-complementary CAP
   *
   * @param sequence - The partial sequence to complete (must include start position at index 0)
   * @param sliceSize - Ignored (swapped-complementary CAP always uses halved)
   * @returns The complete circular sequence with all beats
   */
  executeCAP(sequence: BeatData[], sliceSize: SliceSize): BeatData[] {
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

    // Generate the new beats
    const generatedBeats: BeatData[] = [];
    let lastBeat = sequence[sequence.length - 1]!;
    const nextBeatNumber = lastBeat.beatNumber + 1;

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
    }

    // Re-insert start position at the beginning
    sequence.unshift(startPosition);

    return sequence;
  }

  /**
   * Validate that the sequence can perform a swapped-complementary CAP
   * Requirement: end_position === start_position (returns to start)
   */
  private _validateSequence(sequence: BeatData[]): void {
    if (sequence.length < 2) {
      throw new Error(
        "Sequence must have at least 2 beats (start position + 1 beat)"
      );
    }

    const startPos = sequence[0]!.startPosition;
    const endPos = sequence[sequence.length - 1]!.endPosition;

    if (!startPos || !endPos) {
      throw new Error("Sequence beats must have valid start and end positions");
    }

    // Check if the (start, end) pair is valid for swapped-complementary (must return to start)
    const key = `${startPos},${endPos}`;

    if (!COMPLEMENTARY_CAP_VALIDATION_SET.has(key)) {
      throw new Error(
        `Invalid position pair for swapped-complementary CAP: ${startPos} → ${endPos}. ` +
          `For a swapped-complementary CAP, the sequence must end at the same position it started (${startPos}).`
      );
    }
  }

  /**
   * Create a new CAP entry by transforming a previous beat with SWAP + COMPLEMENTARY
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

    // Get complementary letter
    const complementaryLetter =
      this._getComplementaryLetter(previousMatchingBeat);

    // Create the new beat with swapped and complementary attributes
    // KEY: Blue gets attributes from Red's matching beat (SWAP)
    //      Red gets attributes from Blue's matching beat (SWAP)
    //      Then motion types and rotations are flipped (COMPLEMENTARY)
    const newBeat: BeatData = {
      ...previousMatchingBeat,
      id: `beat-${beatNumber}`,
      beatNumber,
      letter: complementaryLetter, // COMPLEMENTARY
      startPosition: previousBeat.endPosition ?? null,
      endPosition: previousMatchingBeat.endPosition ?? null, // Same as matching beat (returns to start), handle undefined
      motions: {
        // SWAP: Blue does what Red did, with complementary transformation
        [MotionColor.BLUE]: this._createSwappedComplementaryMotion(
          MotionColor.BLUE,
          previousBeat,
          previousMatchingBeat,
          true // isSwapped = true (use opposite color's data)
        ),
        // SWAP: Red does what Blue did, with complementary transformation
        [MotionColor.RED]: this._createSwappedComplementaryMotion(
          MotionColor.RED,
          previousBeat,
          previousMatchingBeat,
          true // isSwapped = true (use opposite color's data)
        ),
      },
    };

    // Update orientations
    const beatWithStartOri =
      this.orientationCalculationService.updateStartOrientations(
        newBeat,
        previousBeat
      );
    const finalBeat =
      this.orientationCalculationService.updateEndOrientations(
        beatWithStartOri
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

    return sequence[arrayIndex]!;
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
  private _getComplementaryLetter(previousMatchingBeat: BeatData): Letter {
    const letter = previousMatchingBeat.letter;

    if (!letter) {
      throw new Error("Previous matching beat must have a letter");
    }

    const complementaryLetter = getComplementaryLetter(
      letter as string
    ) as Letter;

    return complementaryLetter;
  }

  /**
   * Create swapped-complementary motion data for the new beat
   * Combines color swapping with complementary transformations
   */
  private _createSwappedComplementaryMotion(
    color: MotionColor,
    previousBeat: BeatData,
    previousMatchingBeat: BeatData,
    isSwapped: boolean
  ): any {
    const previousMotion = previousBeat.motions[color];

    // SWAP: Get the opposite color's motion data
    const oppositeColor =
      color === MotionColor.BLUE ? MotionColor.RED : MotionColor.BLUE;
    const matchingMotion = isSwapped
      ? previousMatchingBeat.motions[oppositeColor]
      : previousMatchingBeat.motions[color];

    if (!previousMotion || !matchingMotion) {
      throw new Error(`Missing motion data for ${color}`);
    }

    // COMPLEMENTARY: Flip the motion type (PRO ↔ ANTI)
    const complementaryMotionType = this._getComplementaryMotionType(
      matchingMotion.motionType
    );

    // COMPLEMENTARY: Flip the prop rotation direction
    const complementaryPropRotDir = this._getComplementaryPropRotDir(
      matchingMotion.rotationDirection
    );

    // Create swapped-complementary motion
    const swappedComplementaryMotion = {
      ...matchingMotion,
      color, // IMPORTANT: Preserve the color (Blue stays Blue, Red stays Red)
      motionType: complementaryMotionType, // Flipped
      startLocation: previousMotion.endLocation,
      endLocation: matchingMotion.endLocation, // Same location
      rotationDirection: complementaryPropRotDir, // Flipped
      // Start orientation will be set by orientationCalculationService
      // End orientation will be calculated by orientationCalculationService
    };

    return swappedComplementaryMotion;
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
  private _getComplementaryPropRotDir(
    propRotDir: RotationDirection
  ): RotationDirection {
    if (propRotDir === RotationDirection.CLOCKWISE) {
      return RotationDirection.COUNTER_CLOCKWISE;
    } else if (propRotDir === RotationDirection.COUNTER_CLOCKWISE) {
      return RotationDirection.CLOCKWISE;
    }

    // NO_ROTATION stays NO_ROTATION
    return propRotDir;
  }
}
