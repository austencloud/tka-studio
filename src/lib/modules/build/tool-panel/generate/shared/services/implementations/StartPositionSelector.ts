/**
 * Start Position Selector Implementation
 *
 * Selects random start positions for sequence generation.
 * Extracted from SequenceGenerationService for single responsibility.
 */
import type { BeatData, GridMode, ILetterQueryHandler } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IBeatConverterService, IPictographFilterService } from "../contracts";
import type { IStartPositionSelector } from "../contracts/IStartPositionSelector";

@injectable()
export class StartPositionSelector implements IStartPositionSelector {
  constructor(
    @inject(TYPES.ILetterQueryHandler)
    private letterQueryHandler: ILetterQueryHandler,
    @inject(TYPES.IPictographFilterService)
    private pictographFilterService: IPictographFilterService,
    @inject(TYPES.IBeatConverterService)
    private beatConverterService: IBeatConverterService
  ) {}

  /**
   * Select a random start position
   */
  async selectStartPosition(gridMode: GridMode): Promise<BeatData> {
    const allOptions = await this.letterQueryHandler.getAllPictographVariations(gridMode);
    const startPositions = this.pictographFilterService.filterStartPositions(allOptions);
    const startPictograph = this.pictographFilterService.selectRandom(startPositions);
    return this.beatConverterService.convertToBeat(startPictograph, 0);
  }
}
