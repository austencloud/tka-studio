/**
 * Mirrored Complementary CAP Executor
 *
 * Executes the mirrored-complementary CAP (Circular Arrangement Pattern) by combining:
 * 1. MIRRORED: Mirror locations vertically (E↔W), flip prop rotation (CW↔CCW)
 * 2. COMPLEMENTARY: Flip letters (A↔B), flip motion types (PRO↔ANTI), flip prop rotation (CW↔CCW)
 *
 * This creates a sequence where:
 * - Letters are flipped (complementary effect)
 * - Motion types are flipped (PRO ↔ ANTI) (complementary effect)
 * - Locations are mirrored vertically across the north-south axis (mirrored effect)
 * - **Prop rotation directions stay THE SAME** (both transformations flip rotation, so they CANCEL OUT)
 *
 * IMPORTANT: Slice size is ALWAYS halved (no quartering)
 * IMPORTANT: End position must be vertical mirror of start position
 */

import type { BeatData } from "$create/shared/workspace-panel";
import type { Letter } from "$shared";
import type { IGridPositionDeriver } from "$shared";
import { MotionColor, MotionType } from "$shared";
import { TYPES } from "$shared/inversify/types";
import type {
  GridLocation,
  GridPosition,
} from "$shared/pictograph/grid/domain/enums/grid-enums";
import { inject, injectable } from "inversify";
import type { IOrientationCalculationService } from "../../../shared/services/contracts";
import type { IComplementaryLetterService } from "../../../shared/services/contracts";
import {
  MIRRORED_COMPLEMENTARY_VALIDATION_SET,
  VERTICAL_MIRROR_LOCATION_MAP,
  VERTICAL_MIRROR_POSITION_MAP,
} from "../../domain/constants/strict-cap-position-maps";
import type { SliceSize } from "../../domain/models/circular-models";

@injectable()
export class MirroredComplementaryCAPExecutor {
  constructor(
    @inject(TYPES.IOrientationCalculationService)
    private orientationCalculationService: IOrientationCalculationService,
    @inject(TYPES.IGridPositionDeriver)
    private gridPositionDeriver: IGridPositionDeriver,
    @inject(TYPES.IComplementaryLetterService)
    private complementaryLetterService: IComplementaryLetterService
  ) {}

  /**
   * Execute the mirrored-complementary CAP
   *
   * @param sequence - The partial sequence to complete (must include start position at index 0)
   * @param sliceSize - Ignored (mirrored-complementary CAP always uses halved)
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
   * Validate that the sequence can perform a mirrored-complementary CAP
   * Requirement: end_position must be vertical mirror of start_position
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

    // Check if the (start, end) pair is valid for mirrored-complementary
    const key = `${startPos},${endPos}`;

    if (!MIRRORED_COMPLEMENTARY_VALIDATION_SET.has(key)) {
      throw new Error(
        `Invalid position pair for mirrored-complementary CAP: ${startPos} → ${endPos}. ` +
          `For a mirrored-complementary CAP, the end position must be the vertical mirror of start position.`
      );
    }
  }

  /**
   * Create a new CAP entry by transforming a previous beat with MIRROR + COMPLEMENTARY
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

    // Get the complementary letter (COMPLEMENTARY effect)
    if (!previousMatchingBeat.letter) {
      throw new Error("Previous matching beat must have a letter");
    }
    const complementaryLetter =
      this.complementaryLetterService.getComplementaryLetter(
        previousMatchingBeat.letter as string
      ) as Letter;

    // Get the mirrored end position (MIRRORED effect)
    const mirroredEndPosition = this._getMirroredPosition(previousMatchingBeat);

    // Create the new beat with mirrored-complementary attributes
    // KEY: Motion type is flipped (COMPLEMENTARY)
    //      Locations are mirrored (MIRRORED)
    //      Rotation direction STAYS THE SAME (both transformations flip, so they cancel)
    const newBeat: BeatData = {
      ...previousMatchingBeat,
      id: `beat-${beatNumber}`,
      beatNumber,
      letter: complementaryLetter, // COMPLEMENTARY: Flip letter
      startPosition: previousBeat.endPosition ?? null,
      endPosition: mirroredEndPosition, // MIRRORED: Flip position
      motions: {
        [MotionColor.BLUE]: this._createMirroredComplementaryMotion(
          MotionColor.BLUE,
          previousBeat,
          previousMatchingBeat
        ),
        [MotionColor.RED]: this._createMirroredComplementaryMotion(
          MotionColor.RED,
          previousBeat,
          previousMatchingBeat
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
   * Get the vertical mirrored position
   */
  private _getMirroredPosition(
    previousMatchingBeat: BeatData
  ): GridPosition | null {
    const endPos = previousMatchingBeat.endPosition;

    if (!endPos) {
      throw new Error("Previous matching beat must have an end position");
    }

    const mirroredPosition =
      VERTICAL_MIRROR_POSITION_MAP[endPos as GridPosition];

    if (!mirroredPosition) {
      throw new Error(`No mirrored position found for ${endPos}`);
    }

    return mirroredPosition;
  }

  /**
   * Create mirrored-complementary motion data for the new beat
   * Combines location mirroring with motion type flipping
   * **IMPORTANT**: Rotation direction stays the SAME (two flips cancel out)
   */
  private _createMirroredComplementaryMotion(
    color: MotionColor,
    previousBeat: BeatData,
    previousMatchingBeat: BeatData
  ): any {
    const previousMotion = previousBeat.motions[color];
    const matchingMotion = previousMatchingBeat.motions[color];

    if (!previousMotion || !matchingMotion) {
      throw new Error(`Missing motion data for ${color}`);
    }

    // Mirror the end location vertically (MIRRORED effect)
    const mirroredEndLocation = this._getMirroredLocation(
      matchingMotion.endLocation as GridLocation
    );

    // Flip the motion type (COMPLEMENTARY effect)
    const originalMotionType = matchingMotion.motionType;
    const complementaryMotionType = this._getComplementaryMotionType(
      matchingMotion.motionType
    );

    // IMPORTANT: Rotation direction stays the SAME (both transformations flip, so they cancel)
    const rotationDirection = matchingMotion.rotationDirection;

    // Create mirrored-complementary motion
    const mirroredComplementaryMotion = {
      ...matchingMotion,
      color, // Preserve the color
      motionType: complementaryMotionType, // COMPLEMENTARY: Flip motion type
      startLocation: previousMotion.endLocation,
      endLocation: mirroredEndLocation, // MIRRORED: Flip location
      rotationDirection: rotationDirection, // NO CHANGE: Both flips cancel out
      // Start orientation will be set by orientationCalculationService
      // End orientation will be calculated by orientationCalculationService
    };

    return mirroredComplementaryMotion;
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
}
