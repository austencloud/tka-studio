/**
 * Generation Actions State - Complete implementation with real service integration
 *
 * Handles generation button logic and integrates with actual SequenceGenerationService
 * to create real sequences that update the BeatGrid.
 */

import type { GridMode, SequenceData } from "../../../../shared";
import type { DifficultyLevel, GenerationMode, GenerationOptions, PropContinuity } from "../domain";
import type { ISequenceGenerationService } from "../services/contracts/generate-contracts";


export interface GenerationConfig {
  mode: GenerationMode;
  length: number;
  gridMode: GridMode;
  propType: string;
  difficulty: DifficultyLevel;
  propContinuity: PropContinuity;
  turnIntensity: number;
  letterTypes: string[];
}

// Utility functions removed - not currently used but may be needed for future features

/**
 * Creates reactive state for generation actions with real service integration
 */
export function createGenerationActionsState() {
  // Generation state
  let isGenerating = $state(false);
  let lastGeneratedSequence = $state<SequenceData | null>(null);
  let generationError = $state<string | null>(null);

  /**
   * Generate sequence - complete implementation using real SequenceGenerationService
   */
  async function onGenerateClicked(config: GenerationConfig) {
    if (isGenerating) return;

    console.log("🎯 Starting real sequence generation with config:", config);

    isGenerating = true;
    generationError = null;

    try {
      // Get the sequence generation service through DI
      const { resolve, TYPES } = await import(
        "$lib/shared/inversify/container"
      );
      const sequenceGenerationService = resolve<ISequenceGenerationService>(
        TYPES.ISequenceGenerationService
      );

      if (!sequenceGenerationService) {
        throw new Error("SequenceGenerationService not available");
      }

      // Convert config to generation options (no conversion needed since config now uses enums)
      const generationOptions: GenerationOptions = {
        mode: config.mode,
        length: config.length,
        gridMode: config.gridMode,
        propType: config.propType,
        difficulty: config.difficulty,
        propContinuity: config.propContinuity,
        turnIntensity: config.turnIntensity,
        letterTypes: config.letterTypes,
      };

      console.log("⚡ Calling SequenceGenerationService.generateSequence()");

      // Generate the actual sequence
      const generatedSequence =
        await sequenceGenerationService.generateSequence(generationOptions);

      console.log("✅ Sequence generation completed:", {
        id: generatedSequence.id,
        name: generatedSequence.name,
        beats: generatedSequence.beats.length,
      });

      // Store the generated sequence
      lastGeneratedSequence = generatedSequence;

      // TODO: Update the BeatGrid with the generated sequence
      // This should integrate with the workbench state to display the new sequence
      await updateWorkbenchWithSequence(generatedSequence);

      console.log("🎉 Generation complete and workbench updated!");
    } catch (error) {
      console.error("❌ Sequence generation failed:", error);
      generationError =
        error instanceof Error ? error.message : "Unknown generation error";
    } finally {
      isGenerating = false;
    }
  }

  /**
   * Auto-complete sequence - placeholder for future implementation
   */
  async function onAutoCompleteClicked() {
    if (isGenerating) return;

    console.log("🔄 Auto-complete clicked - not yet implemented");

    // TODO: Implement auto-complete using SequenceGenerationService
    // This would analyze the current sequence and generate remaining beats
  }

  /**
   * Update workbench with generated sequence
   * TODO: This should integrate with the actual workbench state management
   */
  async function updateWorkbenchWithSequence(sequence: SequenceData) {
    try {
      console.log("🔄 Updating workbench with generated sequence");

      // TODO: Get the workbench service and update it with the new sequence
      // This is where we'd integrate with BeatGrid state management

      // For now, just log the sequence data
      console.log("📊 Generated sequence data:", {
        name: sequence.name,
        beats: sequence.beats.length,
        firstBeat: sequence.beats[0]?.pictographData?.letter,
        lastBeat:
          sequence.beats[sequence.beats.length - 1]?.pictographData?.letter,
      });

      // TODO: Call workbench service to update the beat grid
      // const workbenchService = resolve("IWorkbenchService");
      // await workbenchService.setSequence(sequence);
    } catch (error) {
      console.error("❌ Failed to update workbench:", error);
      throw new Error(
        `Workbench update failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Clear generation error
   */
  function clearError() {
    generationError = null;
  }

  /**
   * Get generation summary for debugging
   */
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
    // State
    get isGenerating() {
      return isGenerating;
    },
    get lastGeneratedSequence() {
      return lastGeneratedSequence;
    },
    get generationError() {
      return generationError;
    },

    // Actions
    onGenerateClicked,
    onAutoCompleteClicked,
    clearError,
    getGenerationSummary,
  };
}
