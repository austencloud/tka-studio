/**
 * Partial Sequence Generator Implementation
 *
 * Generates partial sequences for circular mode (CAP preparation).
 * Extracted from SequenceGenerationService - EXACT original logic preserved.
 */
import type { BeatData, IGridPositionDeriver, ILetterQueryHandler } from "$shared";
import { RotationDirection } from "$shared/pictograph/shared/domain/enums/pictograph-enums";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { GenerationOptions } from "../../../shared/domain/models/generate-models";
import { PropContinuity } from "../../../shared/domain/models/generate-models";
import type {
    IBeatConverterService,
    IOrientationCalculationService,
    IPictographFilterService,
    ISequenceMetadataService,
    ITurnManagementService,
} from "../../../shared/services/contracts";
import type { IPartialSequenceGenerator } from "../contracts/IPartialSequenceGenerator";

@injectable()
export class PartialSequenceGenerator implements IPartialSequenceGenerator {
  constructor(
    @inject(TYPES.ILetterQueryHandler)
    private letterQueryHandler: ILetterQueryHandler,
    @inject(TYPES.IPictographFilterService)
    private pictographFilterService: IPictographFilterService,
    @inject(TYPES.IBeatConverterService)
    private beatConverterService: IBeatConverterService,
    @inject(TYPES.ITurnManagementService)
    private turnManagementService: ITurnManagementService,
    @inject(TYPES.ISequenceMetadataService)
    private metadataService: ISequenceMetadataService,
    @inject(TYPES.IGridPositionDeriver)
    private gridPositionDeriver: IGridPositionDeriver,
    @inject(TYPES.IOrientationCalculationService)
    private orientationCalculationService: IOrientationCalculationService
  ) {}

  /**
   * Generate a partial sequence ending at a specific position
   * Implements WordLengthCalculator logic from legacy system
   *
   * EXACT ORIGINAL LOGIC FROM SequenceGenerationService._generatePartialSequenceToPosition
   */
  async generatePartialSequence(
    startPos: any,
    endPos: any,
    sliceSize: any,
    options: GenerationOptions
  ): Promise<BeatData[]> {
    const { SliceSize } = await import("../../domain/models/circular-models");

    // Step 1: Create Type 6 static start position beat (beat 0)
    // Use the same approach as StartPositionService to create a proper Type 6 motion
    const { MotionType, MotionColor, Orientation, RotationDirection, PropType, Letter, GridPosition } = await import("$shared");
    const { createMotionData, createPictographData } = await import("$shared");

    // Get hand locations for this start position
    const [blueLocation, redLocation] = this.gridPositionDeriver.getGridLocationsFromPosition(startPos);

    // Determine the letter based on the position
    let letter: any;
    if (startPos === GridPosition.ALPHA1 || startPos === GridPosition.ALPHA2) {
      letter = Letter.ALPHA;
    } else if (startPos === GridPosition.BETA5 || startPos === GridPosition.BETA4) {
      letter = Letter.BETA;
    } else {
      letter = Letter.GAMMA;
    }

    // Create Type 6 static motions (both hands stay in place)
    const blueMotion = createMotionData({
      motionType: MotionType.STATIC,
      startLocation: blueLocation,
      endLocation: blueLocation,
      startOrientation: Orientation.IN,
      endOrientation: Orientation.IN,
      rotationDirection: RotationDirection.NO_ROTATION,
      turns: 0,
      color: MotionColor.BLUE,
      isVisible: true,
      propType: PropType.STAFF,
      arrowLocation: blueLocation
    });

    const redMotion = createMotionData({
      motionType: MotionType.STATIC,
      startLocation: redLocation,
      endLocation: redLocation,
      startOrientation: Orientation.IN,
      endOrientation: Orientation.IN,
      rotationDirection: RotationDirection.NO_ROTATION,
      turns: 0,
      color: MotionColor.RED,
      isVisible: true,
      propType: PropType.STAFF,
      arrowLocation: redLocation
    });

    // Create the start position pictograph
    const startPictograph = createPictographData({
      id: `start-${startPos}`,
      letter,
      startPosition: startPos,
      endPosition: startPos,
      motions: {
        [MotionColor.BLUE]: blueMotion,
        [MotionColor.RED]: redMotion
      }
    });

    const startBeat = this.beatConverterService.convertToBeat(startPictograph, 0);
    const sequence: BeatData[] = [startBeat];

    // Now get all options for generating the rest of the sequence
    const allOptions = await this.letterQueryHandler.getAllPictographVariations(options.gridMode);

    // Step 2: Calculate word length (legacy formula)
    // word_length = length // 2 for halved, length // 4 for quartered
    // This is the total REAL BEATS we need in the partial sequence (excluding start position)
    // The start position (beatNumber 0) is not counted toward the user's requested length
    const wordLength = sliceSize === SliceSize.HALVED
      ? Math.floor(options.length / 2)
      : Math.floor(options.length / 4);

    console.log(`📊 Word calculation: length=${options.length}, sliceSize=${sliceSize}, wordLength=${wordLength}`);

    // Step 3: Generate beats to fill the partial sequence
    // Total REAL BEATS needed: wordLength
    // We already have the start position (beatNumber 0) which is NOT counted
    // We need to generate: wordLength total beats
    // But the last beat must end at the required position, so:
    // - Generate (wordLength - 1) intermediate beats freely
    // - Generate 1 final beat that ends at required position
    const intermediateBeatsCount = Math.max(0, wordLength - 1); // Can be 0 if wordLength is 1
    const beatsToGenerate = intermediateBeatsCount;
    const level = this.metadataService.mapDifficultyToLevel(options.difficulty);
    const turnIntensity = options.turnIntensity || 1;

    // Calculate turn allocation for the beats we're generating
    const turnAllocation = await this._allocateTurns(beatsToGenerate, level, turnIntensity);

    // Determine rotation directions
    const { blueRotationDirection, redRotationDirection } = this._determineRotationDirections(
      options.propContinuity
    );

    // Generate intermediate beats (not constrained to end position)
    for (let i = 0; i < beatsToGenerate; i++) {
      const nextBeat = await this._generateNextBeat(
        sequence,
        level,
        turnAllocation.blue[i],
        turnAllocation.red[i],
        options.propContinuity || PropContinuity.CONTINUOUS,
        blueRotationDirection,
        redRotationDirection,
        options.letterTypes || ["Dual-Shift"],
        options.gridMode
      );
      sequence.push(nextBeat);
      console.log(`✅ Generated intermediate beat ${i + 1}: ${nextBeat.letter}`);
    }

    // Step 4: Add final beat that must end at required endPos
    const lastBeat = sequence[sequence.length - 1];
    let finalMoves = allOptions.filter((p: any) =>
      p.startPosition === lastBeat.endPosition && p.endPosition === endPos
    );

    console.log(`🎯 Found ${finalMoves.length} moves from ${lastBeat.endPosition} to ${endPos}`);

    // Apply the same filters as intermediate beats to respect continuity setting
    finalMoves = this.pictographFilterService.filterByContinuity(finalMoves, lastBeat);
    console.log(`🔄 After continuity filter: ${finalMoves.length} options`);

    if (options.propContinuity === PropContinuity.CONTINUOUS) {
      finalMoves = this.pictographFilterService.filterByRotation(
        finalMoves,
        blueRotationDirection,
        redRotationDirection
      );
      console.log(`🔄 After rotation filter: ${finalMoves.length} options`);
    }

    finalMoves = this.pictographFilterService.filterByLetterTypes(
      finalMoves,
      options.letterTypes || ["Dual-Shift"]
    );
    console.log(`🔄 After letter type filter: ${finalMoves.length} options`);

    if (finalMoves.length === 0) {
      throw new Error(
        `No valid move from ${lastBeat.endPosition} to required end position ${endPos} ` +
        `that respects continuity=${options.propContinuity} and letter type constraints. ` +
        `This combination may not be possible with the current settings.`
      );
    }

    const finalPictograph = this.pictographFilterService.selectRandom(finalMoves);
    let finalBeat = this.beatConverterService.convertToBeat(finalPictograph, sequence.length);

    // Set turns if level 2 or 3
    const finalTurnIndex = Math.min(sequence.length - 1, turnAllocation.blue.length - 1);
    if (level === 2 || level === 3) {
      this.turnManagementService.setTurns(
        finalBeat,
        turnAllocation.blue[finalTurnIndex],
        turnAllocation.red[finalTurnIndex]
      );
    }

    // Update orientations
    finalBeat = this.orientationCalculationService.updateStartOrientations(finalBeat, lastBeat);
    this.turnManagementService.updateDashStaticRotationDirections(
      finalBeat,
      options.propContinuity || PropContinuity.CONTINUOUS,
      blueRotationDirection,
      redRotationDirection
    );
    finalBeat = this.orientationCalculationService.updateEndOrientations(finalBeat);

    sequence.push(finalBeat);
    console.log(`🎯 Generated final beat ending at required position: ${finalBeat.letter} → ${endPos}`);

    return sequence;
  }

  /**
   * Allocate turns for the sequence
   * EXACT ORIGINAL LOGIC FROM SequenceGenerationService._allocateTurns
   */
  private async _allocateTurns(
    beatsToGenerate: number,
    level: number,
    turnIntensity: number
  ): Promise<{ blue: (number | "fl")[]; red: (number | "fl")[] }> {
    const { TurnIntensityManagerService } = await import("../../../shared/services/implementations/TurnIntensityManagerService");
    const turnManager = new TurnIntensityManagerService(beatsToGenerate, level, turnIntensity);
    return turnManager.allocateTurnsForBlueAndRed();
  }

  /**
   * Determine rotation directions based on prop continuity
   * EXACT ORIGINAL LOGIC FROM SequenceGenerationService._determineRotationDirections
   */
  private _determineRotationDirections(propContinuity?: PropContinuity): {
    blueRotationDirection: string;
    redRotationDirection: string;
  } {

    if (propContinuity === PropContinuity.CONTINUOUS) {
      return {
        blueRotationDirection: this.pictographFilterService.selectRandom([
          RotationDirection.CLOCKWISE,
          RotationDirection.COUNTER_CLOCKWISE,
        ]),
        redRotationDirection: this.pictographFilterService.selectRandom([
          RotationDirection.CLOCKWISE,
          RotationDirection.COUNTER_CLOCKWISE,
        ]),
      };
    }

    return { blueRotationDirection: "", redRotationDirection: "" };
  }

  /**
   * Generate next beat - orchestrates filtering and conversion
   * EXACT ORIGINAL LOGIC FROM SequenceGenerationService._generateNextBeat
   */
  private async _generateNextBeat(
    sequence: BeatData[],
    level: number,
    turnBlue: number | "fl",
    turnRed: number | "fl",
    propContinuity: PropContinuity,
    blueRotationDirection: string,
    redRotationDirection: string,
    letterTypes: string[],
    gridMode: any
  ): Promise<BeatData> {
    // Get all options
    const allOptions = await this.letterQueryHandler.getAllPictographVariations(gridMode);
    console.log(`📋 Loaded ${allOptions.length} option variations`);

    // Apply filters
    let filteredOptions = allOptions;
    const lastBeat = sequence.length > 0 ? sequence[sequence.length - 1] : null;

    filteredOptions = this.pictographFilterService.filterByContinuity(filteredOptions, lastBeat);

    if (propContinuity === PropContinuity.CONTINUOUS) {
      filteredOptions = this.pictographFilterService.filterByRotation(
        filteredOptions,
        blueRotationDirection,
        redRotationDirection
      );
      console.log(`🔄 Filtered for rotation: ${filteredOptions.length} options`);
    }

    filteredOptions = this.pictographFilterService.filterByLetterTypes(filteredOptions, letterTypes);

    if (filteredOptions.length === 0) {
      throw new Error("No valid options available after filtering");
    }

    // Random selection
    const selectedOption = this.pictographFilterService.selectRandom(filteredOptions);
    console.log(`🎯 Selected option: ${selectedOption.letter}`);

    // Convert to beat
    let nextBeat = this.beatConverterService.convertToBeat(selectedOption, sequence.length);

    // Set turns if level 2 or 3
    if (level === 2 || level === 3) {
      this.turnManagementService.setTurns(nextBeat, turnBlue, turnRed);
      console.log(`🎲 Set turns: blue=${turnBlue}, red=${turnRed}`);
    }

    // Update orientations
    if (sequence.length > 0) {
      nextBeat = this.orientationCalculationService.updateStartOrientations(
        nextBeat,
        sequence[sequence.length - 1]
      );
    }

    this.turnManagementService.updateDashStaticRotationDirections(
      nextBeat,
      propContinuity,
      blueRotationDirection,
      redRotationDirection
    );

    nextBeat = this.orientationCalculationService.updateEndOrientations(nextBeat);

    return nextBeat;
  }
}
