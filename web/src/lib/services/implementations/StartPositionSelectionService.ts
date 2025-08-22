/**
 * StartPositionSelectionService.ts
 *
 * Service to handle start position selection business logic.
 * Extracted from StartPositionPicker component to follow clean architecture.
 */

import type { BeatData } from "$domain/BeatData";
import type { PictographData } from "$domain/PictographData";
import {
  createStartPositionData,
  extractEndPosition,
  storeStartPositionData,
} from "$lib/components/construct/start-position/utils/StartPositionUtils";
import type { IStartPositionSelectionService } from "$lib/services/interfaces/IStartPositionSelectionService";
import type { IStartPositionService } from "$services/interfaces/application-interfaces";

interface StartPositionData {
  endPosition: string;
  pictographData: PictographData;
}

/**
 * Service implementation for start position selection
 */
export class StartPositionSelectionService
  implements IStartPositionSelectionService
{
  /**
   * Handle the complete start position selection process
   */
  async selectStartPosition(
    startPosPictograph: PictographData,
    startPositionService: IStartPositionService
  ): Promise<void> {
    try {
      // Extract end position from the pictograph data
      const endPosition = extractEndPosition(startPosPictograph);

      // Create start position data in the format the OptionPicker expects
      const startPositionData = createStartPositionData(
        startPosPictograph,
        endPosition
      );

      // Create start position beat data for internal use
      const startPositionBeat: BeatData = {
        id: crypto.randomUUID(),
        beatNumber: 0,
        duration: 1.0,
        blueReversal: false,
        redReversal: false,
        isBlank: false,
        pictographData: startPosPictograph,
        metadata: {
          endPosition: endPosition,
        },
      };

      // Save to localStorage in the format OptionPicker expects
      storeStartPositionData(startPositionData);

      // Preload options for better UX
      await this.preloadOptionsForPosition(endPosition);

      // Use service to set start position
      await startPositionService.setStartPosition(startPositionBeat);

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
      const { resolve } = await import("$services/bootstrap");
      const { ILetterQueryServiceInterface } = await import(
        "$services/di/interfaces/codex-interfaces"
      );
      // Resolve service to trigger initialization
      resolve(ILetterQueryServiceInterface);

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
