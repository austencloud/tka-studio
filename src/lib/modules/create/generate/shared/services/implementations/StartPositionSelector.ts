/**
 * Start Position Selector Implementation
 *
 * Selects random start positions for sequence generation.
 * Extracted from SequenceGenerationService for single responsibility.
 */
import type { ILetterQueryHandler, IArrowPositioningOrchestrator } from "$shared";
import type { BeatData, GridMode } from "$shared";
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
    private beatConverterService: IBeatConverterService,
    @inject(TYPES.IArrowPositioningOrchestrator)
    private arrowPositioningOrchestrator: IArrowPositioningOrchestrator
  ) {}

  /**
   * Select a random start position
   */
  async selectStartPosition(gridMode: GridMode): Promise<BeatData> {
    const allOptions =
      await this.letterQueryHandler.getAllPictographVariations(gridMode);
    const startPositions =
      this.pictographFilterService.filterStartPositions(allOptions);
    const startPictograph =
      this.pictographFilterService.selectRandom(startPositions);

    let startBeat = this.beatConverterService.convertToBeat(
      startPictograph,
      0,
      gridMode
    );

    // 🎯 CRITICAL FIX: Calculate arrow placements for start position
    // This ensures start position arrows have correct positions instead of default (0, 0)
    const updatedPictographData =
      await this.arrowPositioningOrchestrator.calculateAllArrowPoints(
        startBeat
      );
    startBeat = { ...startBeat, ...updatedPictographData };

    return startBeat;
  }
}
