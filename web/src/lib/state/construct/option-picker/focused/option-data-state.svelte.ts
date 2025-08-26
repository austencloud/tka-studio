/**
 * Option Data State - Pure Svelte 5 Runes
 *
 * Handles raw data management, service integration, and end position calculation.
 * Extracted from lines 45-180 of optionPickerRunes.svelte.ts
 */

import { GridMode } from "$lib/domain";
import type { PictographData } from "$lib/domain/PictographData";
import type { IPositionMapper } from "$lib/services/interfaces/movement/IPositionMapper";
import { resolve } from "$services/bootstrap";

/**
 * Helper function to compute endPosition from motion data
 */
function getEndPosition(pictographData: PictographData): string | null {
  if (pictographData.motions?.blue && pictographData.motions?.red) {
    const positionService = resolve("IPositionMapper") as IPositionMapper;
    const position = positionService.getPositionFromLocations(
      pictographData.motions.blue.endLocation,
      pictographData.motions.red.endLocation
    );
    return position?.toString() || null;
  }
  return null;
}

export function createOptionDataState() {
  // ===== Core Data State =====
  let sequenceData = $state<PictographData[]>([]);
  let optionsData = $state<PictographData[]>([]);
  let selectedPictograph = $state<PictographData | null>(null);

  // ===== Actions =====

  /**
   * Load options from services based on sequence data
   */
  async function loadOptionsFromServices(
    sequence: PictographData[]
  ): Promise<PictographData[]> {
    let nextOptions: PictographData[] = [];

    if (sequence && sequence.length > 0) {
      const lastBeat = sequence[sequence.length - 1];
      const endPosition = getEndPosition(lastBeat);

      if (endPosition && typeof endPosition === "string") {
        console.log(
          `🎯 Option Picker: Filtering options for end position: ${endPosition}`
        );

        // Get services through DI
        const { ILetterQueryServiceInterface } = await import(
          "$lib/services/di/interfaces/codex-interfaces"
        );
        const letterQueryService = resolve(ILetterQueryServiceInterface);
        const { IOptionFilteringServiceInterface } = await import(
          "$lib/services/di/registration/shared-services"
        );
        const optionFilteringService = resolve(
          IOptionFilteringServiceInterface
        );

        // Get ALL pictograph variations from CSV (like desktop algorithm) and filter by start position
        const allPictographs =
          await letterQueryService.getAllPictographVariations(GridMode.DIAMOND);
        nextOptions = optionFilteringService.filterByStartPosition(
          allPictographs,
          endPosition
        );

        console.log(
          `✅ Option Picker: Found ${nextOptions.length} options that start from ${endPosition}`
        );
      } else {
        console.warn("No end position found in sequence");
      }
    } else {
      // For empty sequence, try to get start position from localStorage
      const startPositionData = localStorage.getItem("startPosition");
      if (startPositionData) {
        const startPosition = JSON.parse(startPositionData);
        const endPosition =
          typeof startPosition.endPosition === "string"
            ? startPosition.endPosition
            : null;
        if (endPosition) {
          console.log(
            `🎯 Option Picker: Filtering options for start position end: ${endPosition}`
          );

          // Get services through DI
          const { ILetterQueryServiceInterface } = await import(
            "$lib/services/di/interfaces/codex-interfaces"
          );
          const letterQueryService = resolve(ILetterQueryServiceInterface);
          const { IOptionFilteringServiceInterface } = await import(
            "$lib/services/di/registration/shared-services"
          );
          const optionFilteringService = resolve(
            IOptionFilteringServiceInterface
          );

          // Get ALL pictograph variations from CSV (like desktop algorithm) and filter by start position
          const allPictographs =
            await letterQueryService.getAllPictographVariations(
              GridMode.DIAMOND
            );
          nextOptions = optionFilteringService.filterByStartPosition(
            allPictographs,
            endPosition
          );

          console.log(
            `✅ Option Picker: Found ${nextOptions.length} options that start from ${endPosition}`
          );
        }
      }
    }

    // If we got no options, log a warning but don't treat it as an error
    if (!nextOptions || nextOptions.length === 0) {
      console.warn("No options available for the current sequence");
    }

    return nextOptions || [];
  }

  function setSequence(seq: PictographData[]): void {
    sequenceData = seq;
  }

  function setOptions(opts: PictographData[]): void {
    optionsData = opts;
  }

  function selectOption(option: PictographData): void {
    selectedPictograph = option;

    // Dispatch custom events
    if (typeof document !== "undefined") {
      const beatAddedEvent = new CustomEvent("beat-added", {
        detail: { beat: option },
        bubbles: true,
      });
      document.dispatchEvent(beatAddedEvent);

      const optionSelectedEvent = new CustomEvent("option-selected", {
        detail: { option },
        bubbles: true,
      });
      document.dispatchEvent(optionSelectedEvent);
    }
  }

  function reset(): void {
    optionsData = [];
    sequenceData = [];
    selectedPictograph = null;
  }

  // ===== Return Interface =====
  return {
    // Getters
    get sequence() {
      return sequenceData;
    },
    get options() {
      return optionsData;
    },
    get selectedOption() {
      return selectedPictograph;
    },

    // Actions
    loadOptionsFromServices,
    setSequence,
    setOptions,
    selectOption,
    reset,
  };
}

export type OptionDataState = ReturnType<typeof createOptionDataState>;
