/**
 * Generation Actions State - Reactive wrapper for generation orchestration
 *
 * Delegates complex generation logic to IGenerationOrchestrationService.
 * Manages reactive state and workbench animation updates.
 */

import type { SequenceState } from "$build/shared/state";
import type { SequenceData } from "$shared";
// Import resolve and TYPES directly from inversify module (not through $shared barrel export)
import { resolve } from "../../../../shared/inversify";
import { TYPES } from "../../../../shared/inversify/types";
import type { GenerationOptions } from "../shared/domain";
import type { IGenerationOrchestrationService } from "../shared/services/contracts";

export function createGenerationActionsState(
  sequenceState?: SequenceState,
  getIsSequential?: () => boolean
) {
  let isGenerating = $state(false);
  let lastGeneratedSequence = $state<SequenceData | null>(null);
  let generationError = $state<string | null>(null);
  let orchestrationService: IGenerationOrchestrationService | null = null;

  async function onGenerateClicked(options: GenerationOptions) {
    if (isGenerating) return;

    isGenerating = true;
    generationError = null;

    try {
      if (!orchestrationService) {
        orchestrationService = resolve<IGenerationOrchestrationService>(
          TYPES.IGenerationOrchestrationService
        );
      }

      const generatedSequence = await orchestrationService.generateSequence(options);
      lastGeneratedSequence = generatedSequence;
      await updateWorkbenchWithSequence(generatedSequence);

    } catch (error) {
      generationError =
        error instanceof Error ? error.message : "Unknown generation error";
      console.error("❌ Generation failed:", error);
    } finally {
      isGenerating = false;
    }
  }

  async function onAutoCompleteClicked() {
    if (isGenerating) return;
    // TODO: Implement auto-complete using orchestration service
  }

  async function updateWorkbenchWithSequence(sequence: SequenceData) {
    try {
      if (!sequenceState) return;

      const hasExistingSequence = sequenceState.getCurrentBeats().length > 0;

      if (hasExistingSequence) {
        window.dispatchEvent(new CustomEvent('clear-sequence-animation'));
        await new Promise(resolve => setTimeout(resolve, 300));
      }

      const isSequential = getIsSequential?.() ?? false;

      // Dispatch BEFORE updating sequence to prepare BeatGrid for animation
      window.dispatchEvent(new CustomEvent('prepare-sequence-animation', {
        detail: {
          isSequential,
          beatCount: sequence.beats.length
        }
      }));

      sequenceState.setCurrentSequence(sequence);

    } catch (error) {
      throw new Error(
        `Workbench update failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  function clearError() {
    generationError = null;
  }

  function getGenerationSummary() {
    return {
      isGenerating,
      hasLastGenerated: lastGeneratedSequence !== null,
      lastGeneratedName: lastGeneratedSequence?.name || null,
      lastGeneratedBeats: lastGeneratedSequence?.beats.length || 0,
      hasError: generationError !== null,
      errorMessage: generationError,
    };
  }

  return {
    get isGenerating() {
      return isGenerating;
    },
    get lastGeneratedSequence() {
      return lastGeneratedSequence;
    },
    get generationError() {
      return generationError;
    },
    onGenerateClicked,
    onAutoCompleteClicked,
    clearError,
    getGenerationSummary,
  };
}
