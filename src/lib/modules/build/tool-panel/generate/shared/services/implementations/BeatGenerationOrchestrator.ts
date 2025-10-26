/**
 * Beat Generation Orchestrator Implementation
 *
 * Orchestrates the core beat-by-beat generation loop.
 * Extracted from SequenceGenerationService for single responsibility.
 */
import type { BeatData, ILetterQueryHandler } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import { PropContinuity } from "../../domain/models/generate-models";
import type {
  IBeatConverterService,
  IOrientationCalculationService,
  IPictographFilterService,
  ITurnManagementService,
} from "../contracts";
import type { BeatGenerationOptions, IBeatGenerationOrchestrator } from "../contracts/IBeatGenerationOrchestrator";

@injectable()
export class BeatGenerationOrchestrator implements IBeatGenerationOrchestrator {
  constructor(
    @inject(TYPES.ILetterQueryHandler)
    private letterQueryHandler: ILetterQueryHandler,
    @inject(TYPES.IPictographFilterService)
    private pictographFilterService: IPictographFilterService,
    @inject(TYPES.IBeatConverterService)
    private beatConverterService: IBeatConverterService,
    @inject(TYPES.ITurnManagementService)
    private turnManagementService: ITurnManagementService,
    @inject(TYPES.IOrientationCalculationService)
    private orientationCalculationService: IOrientationCalculationService
  ) {}

  /**
   * Generate multiple beats for a sequence
   */
  async generateBeats(
    sequence: BeatData[],
    count: number,
    options: BeatGenerationOptions
  ): Promise<BeatData[]> {
    const generatedBeats: BeatData[] = [];

    for (let i = 0; i < count; i++) {
      console.log(`⚡ Generating beat ${i + 1}/${count}`);

      const nextBeat = await this.generateNextBeat(
        sequence,
        options,
        options.turnAllocation.blue[i],
        options.turnAllocation.red[i]
      );

      sequence.push(nextBeat);
      generatedBeats.push(nextBeat);
      console.log(`✅ Generated beat ${i}: ${nextBeat.letter}`);
    }

    return generatedBeats;
  }

  /**
   * Generate next beat - orchestrates filtering and conversion
   */
  async generateNextBeat(
    sequence: BeatData[],
    options: BeatGenerationOptions,
    turnBlue: number | "fl",
    turnRed: number | "fl"
  ): Promise<BeatData> {
    // Get all options
    const allOptions = await this.letterQueryHandler.getAllPictographVariations(options.gridMode);
    console.log(`📋 Loaded ${allOptions.length} option variations`);

    // Apply filters
    let filteredOptions = allOptions;
    const lastBeat = sequence.length > 0 ? sequence[sequence.length - 1] : null;

    filteredOptions = this.pictographFilterService.filterByContinuity(filteredOptions, lastBeat);

    if (options.propContinuity === PropContinuity.CONTINUOUS) {
      filteredOptions = this.pictographFilterService.filterByRotation(
        filteredOptions,
        options.blueRotationDirection,
        options.redRotationDirection
      );
      console.log(`🔄 Filtered for rotation: ${filteredOptions.length} options`);
    }

    filteredOptions = this.pictographFilterService.filterByLetterTypes(filteredOptions, options.letterTypes);

    if (filteredOptions.length === 0) {
      throw new Error("No valid options available after filtering");
    }

    // Random selection
    const selectedOption = this.pictographFilterService.selectRandom(filteredOptions);
    console.log(`🎯 Selected option: ${selectedOption.letter}`);

    // Convert to beat
    let nextBeat = this.beatConverterService.convertToBeat(selectedOption, sequence.length);

    // Set turns if level 2 or 3
    if (options.level === 2 || options.level === 3) {
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
      options.propContinuity,
      options.blueRotationDirection,
      options.redRotationDirection
    );

    nextBeat = this.orientationCalculationService.updateEndOrientations(nextBeat);

    return nextBeat;
  }
}
