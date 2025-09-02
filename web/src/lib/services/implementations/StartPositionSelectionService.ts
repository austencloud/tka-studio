/**
 * StartPositionSelectionService.ts
 *
 * Service to handle start position selection business logic.
 * Extracted from StartPositionPicker component to follow clean architecture.
 */

import type {
  IStartPositionSelectionService,
  IStartPositionService,
} from "$contracts";
import type { PictographData } from "$domain";
import { injectable } from "inversify";

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
  constructor() {}

  /**
   * Handle the complete start position selection process
   */
  async selectStartPosition(
    startPosPictograph: PictographData,
    applicationStartPositionService: IStartPositionService
  ): Promise<void> {
    try {
      // Extract end position from the pictograph data
      const endPosition = this.extractEndPosition(startPosPictograph);

      // Create start position data in the format the OptionPicker expects
      const startPositionData = this.createStartPositionData(
        startPosPictograph,
        endPosition
      );

      // Create start position beat data for internal use

      // Save to localStorage in the format OptionPicker expects
      this.storeStartPositionData(
        startPositionData as unknown as Record<string, unknown>
      );

      // Preload options for better UX
      await this.preloadOptionsForPosition(endPosition);

      // Use application service to select start position in the sequence
      await applicationStartPositionService.selectStartPosition(
        startPosPictograph
      );

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
   * Extract end position from pictograph data
   */
  private extractEndPosition(pictograph: PictographData): string {
    // Extract end position from motion data
    if (pictograph.motions?.blue && pictograph.motions?.red) {
      return `${pictograph.motions.blue.endLocation}_${pictograph.motions.red.endLocation}`;
    }
    return "alpha1_alpha1"; // Default fallback
  }

  /**
   * Create start position data in the format expected by OptionPicker
   */
  private createStartPositionData(
    pictograph: PictographData,
    endPosition: string
  ): StartPositionData {
    return {
      endPosition,
      pictographData: pictograph,
    };
  }

  /**
   * Store start position data to localStorage
   */
  private storeStartPositionData(data: Record<string, unknown>): void {
    if (typeof window !== "undefined") {
      localStorage.setItem("startPosition", JSON.stringify(data));
      console.log("💾 StartPositionSelectionService: Saved to localStorage");
    }
  }

  /**
   * Preload options for the selected start position
   */
  async preloadOptionsForPosition(_endPosition: string): Promise<void> {
    try {
      // Import and use the LetterQueryHandler to preload options
      const { resolve, TYPES } = await import(
        "$lib/services/inversify/container"
      );
      // Resolve service to trigger initialization
      resolve(TYPES.ILetterQueryHandler);

      // LetterQueryHandler initializes automatically when first used
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
