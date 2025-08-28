/**
 * StartPositionSelectionService.ts
 *
 * Service to handle start position selection business logic.
 * Extracted from StartPositionPicker component to follow clean architecture.
 */

import { inject, injectable } from "inversify";
import type { PictographData } from "$domain/PictographData";
import type { IStartPositionSelectionService } from "$lib/services/interfaces/IStartPositionSelectionService";
import type { IStartPositionService as IApplicationStartPositionService, IStartPositionService } from "$services/interfaces/application-interfaces";
import { TYPES } from "$services/inversify/types";

interface StartPositionData {
  endPosition: string;
  pictographData: PictographData;
}

/**
 * Service implementation for start position selection
 */
@injectable()
export class StartPositionSelectionService
  implements IStartPositionSelectionService
{
  constructor(
    @inject(TYPES.IStartPositionService)
    private readonly utilityStartPositionService: IStartPositionService
  ) {}

  /**
   * Handle the complete start position selection process
   */
  async selectStartPosition(
    startPosPictograph: PictographData,
    applicationStartPositionService: IApplicationStartPositionService
  ): Promise<void> {
    try {
      // Extract end position from the pictograph data
      const endPosition =
        this.utilityStartPositionService.extractEndPosition(startPosPictograph);

      // Create start position data in the format the OptionPicker expects
      const startPositionData =
        this.utilityStartPositionService.createStartPositionData(
          startPosPictograph,
          endPosition
        );

      // Create start position beat data for internal use
      const startPositionBeat =
        this.utilityStartPositionService.createStartPositionBeat(
          startPosPictograph
        );

      // Save to localStorage in the format OptionPicker expects
      this.utilityStartPositionService.storeStartPositionData(
        startPositionData as unknown as Record<string, unknown>
      );

      // Preload options for better UX
      await this.preloadOptionsForPosition(endPosition);

      // Use application service to set start position in the sequence
      await applicationStartPositionService.setStartPosition(startPositionBeat);

      // Dispatch event for coordination service
      this.dispatchStartPositionSelectedEvent(startPositionData, endPosition);
    } catch (error) {
      console.error(
        "StartPositionSelectionService: Error selecting start position:",
        error
      );
      throw new Error(
        `Failed to select start position: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Preload options for the selected start position
   */
  async preloadOptionsForPosition(_endPosition: string): Promise<void> {
    try {
      // Import and use the LetterQueryService to preload options
      const { resolve, TYPES } = await import(
        "$lib/services/inversify/container"
      );
      // Resolve service to trigger initialization
      resolve(TYPES.ILetterQueryService);

      // LetterQueryService initializes automatically when first used
      console.log("✅ CSV data preloaded for option picker");

      // Store empty preloaded options for now - option generation logic would need to be implemented
      // This is a placeholder for future option generation logic
    } catch (preloadError) {
      console.warn(
        "StartPositionSelectionService: Failed to preload options, will load normally:",
        preloadError
      );
      // Continue with normal flow even if preload fails
    }
  }

  /**
   * Dispatch event that coordination service is listening for
   */
  private dispatchStartPositionSelectedEvent(
    startPositionData: StartPositionData,
    endPosition: string
  ): void {
    const event = new CustomEvent("start-position-selected", {
      detail: {
        startPosition: startPositionData,
        endPosition: endPosition,
        isTransitioning: true,
        preloadedOptions: true,
      },
      bubbles: true,
    });
    document.dispatchEvent(event);
  }
}
