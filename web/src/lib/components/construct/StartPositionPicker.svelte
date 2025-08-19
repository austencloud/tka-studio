<!-- StartPositionPicker.svelte - Modern implementation updated for proper OptionPicker integration -->
<script lang="ts">
  import type { BeatData } from "$domain/BeatData";
  import type { PictographData } from "$domain/PictographData";
  import { GridMode } from "$domain/enums";
  import { resolve } from "$services/bootstrap";
  import type { IPictographRenderingService } from "$services/interfaces/pictograph-interfaces";
  import type { IStartPositionService } from "$services/interfaces/application-interfaces";
  import { onMount } from "svelte";

  // Extracted utilities (keeping original functionality intact)
  import {
    extractEndPosition,
    createStartPositionData,
    storeStartPositionData,
    storePreloadedOptions,
  } from "./start-position/utils/StartPositionUtils";

  // UI Components
  import LoadingState from "./start-position/ui/LoadingState.svelte";
  import ErrorState from "./start-position/ui/ErrorState.svelte";
  import PictographGrid from "./start-position/ui/PictographGrid.svelte";
  import TransitionOverlay from "./start-position/ui/TransitionOverlay.svelte";

  // Props using runes
  const { gridMode = "diamond" } = $props<{
    gridMode?: "diamond" | "box";
  }>();

  // Runes-based reactive state (replacing legacy stores)
  let startPositionPictographs = $state<PictographData[]>([]);
  let selectedStartPos = $state<PictographData | null>(null);
  let isLoading = $state(true);
  let loadingError = $state(false);
  let isTransitioning = $state(false);

  // Modern services (replacing legacy service calls)
  let startPositionService = $state<IStartPositionService | null>(null);
  let pictographRenderingService = $state<IPictographRenderingService | null>(
    null
  );

  // Resolve services when container is ready
  $effect(() => {
    try {
      // Try to resolve services, but handle gracefully if container not ready
      if (!startPositionService) {
        try {
          startPositionService = resolve("IStartPositionService");
        } catch {
          // Container not ready yet, will retry on next effect run
          return;
        }
      }
      if (!pictographRenderingService) {
        try {
          pictographRenderingService = resolve("IPictographRenderingService");
        } catch {
          // Container not ready yet, will retry on next effect run
          return;
        }
      }
    } catch (error) {
      console.error("StartPositionPicker: Failed to resolve services:", error);
      // Services will remain null and component will handle gracefully
    }
  });

  // Load available start positions (modernized from legacy)
  async function loadStartPositions() {
    isLoading = true;
    loadingError = false;

    try {
      // Use modern service to get start positions
      if (!startPositionService) {
        throw new Error("StartPositionService not available");
      }
      const startPositions =
        await startPositionService.getDefaultStartPositions(gridMode);
      startPositionPictographs = startPositions;
    } catch (error) {
      console.error("❌ Error loading start positions:", error);
      loadingError = true;
      startPositionPictographs = [];
    } finally {
      isLoading = false;
    }
  }

  // Handle start position selection (modernized from legacy with proper data format)
  async function handleSelect(startPosPictograph: PictographData) {
    console.log(
      "🚀 StartPositionPicker: handleSelect called with parameter:",
      startPosPictograph
    );
    console.log(
      "🚀 StartPositionPicker: Parameter type:",
      typeof startPosPictograph
    );
    console.log(
      "🚀 StartPositionPicker: Parameter is null/undefined?",
      startPosPictograph == null
    );

    try {
      console.log(
        "🚀 StartPositionPicker: User clicked start position:",
        startPosPictograph?.id
      );
      console.log(
        "🚀 StartPositionPicker: Full pictograph data:",
        startPosPictograph
      );

      // Show transition state
      isTransitioning = true;
      console.log("🚀 StartPositionPicker: Setting isTransitioning = true");

      // **CRITICAL: Create the data format that OptionPicker expects**
      // Based on legacy analysis, OptionPicker looks for:
      // 1. localStorage 'startPosition' with endPosition field
      // 2. Proper pictograph data structure

      // Extract end position from the pictograph data
      console.log(
        "🚀 StartPositionPicker: About to extract end position from:",
        startPosPictograph
      );
      const endPosition = extractEndPosition(startPosPictograph);
      console.log(
        "🚀 StartPositionPicker: Extracted end position:",
        endPosition
      );

      // Create start position data in the format the OptionPicker expects (like legacy)
      const startPositionData = createStartPositionData(
        startPosPictograph,
        endPosition
      );

      // Create start position beat data for internal use
      const startPositionBeat: BeatData = {
        id: crypto.randomUUID(),
        beat_number: 0,
        duration: 1.0,
        blue_reversal: false,
        red_reversal: false,
        isBlank: false,
        pictograph_data: startPosPictograph,
        metadata: {
          endPosition: endPosition,
        },
      };

      // Update selected state
      selectedStartPos = startPosPictograph;

      // **CRITICAL: Save to localStorage in the format OptionPicker expects**
      storeStartPositionData(startPositionData);

      // **NEW: Preload options BEFORE triggering the transition**
      // This ensures options are ready when the option picker fades in
      try {
        console.log(
          "🚀 StartPositionPicker: Starting preload options for seamless transition..."
        );

        // Import and use the OptionDataService to preload options
        console.log("🚀 StartPositionPicker: Importing OptionDataService...");
        const { OptionDataService } = await import(
          "$services/implementations/OptionDataService"
        );
        console.log(
          "🚀 StartPositionPicker: Creating OptionDataService instance..."
        );
        const optionDataService = new OptionDataService();
        console.log(
          "🚀 StartPositionPicker: Initializing OptionDataService..."
        );
        await optionDataService.initialize();

        console.log(
          "🚀 StartPositionPicker: Getting next options from end position:",
          endPosition
        );
        const preloadedOptions =
          await optionDataService.getNextOptionsFromEndPosition(
            endPosition,
            gridMode === "diamond" ? GridMode.DIAMOND : GridMode.BOX,
            {}
          );

        console.log(
          `✅ StartPositionPicker: Preloaded ${preloadedOptions?.length || 0} options for seamless transition`
        );

        // Store the preloaded options so OptionPicker can use them immediately
        storePreloadedOptions(preloadedOptions || []);
      } catch (preloadError) {
        console.warn(
          "🚨 StartPositionPicker: Failed to preload options, will load normally:",
          preloadError
        );
        // Continue with normal flow even if preload fails
      }

      // Use modern service to set start position
      if (startPositionService) {
        console.log(
          "🚀 StartPositionPicker: Calling startPositionService.setStartPosition"
        );
        await startPositionService.setStartPosition(startPositionBeat);
        console.log(
          "🚀 StartPositionPicker: startPositionService.setStartPosition completed"
        );
      }

      // **CRITICAL: Emit event that coordination service is listening for**
      // NOTE: We only use event dispatching, not callback, to avoid duplicate handling
      console.log(
        "🚀 StartPositionPicker: Dispatching start-position-selected event"
      );
      const event = new CustomEvent("start-position-selected", {
        detail: {
          startPosition: startPositionData,
          endPosition: endPosition,
          isTransitioning: true,
          preloadedOptions: true, // Signal that options are preloaded
        },
        bubbles: true,
      });
      document.dispatchEvent(event);
      console.log(
        "🚀 StartPositionPicker: Event dispatched - coordination service should handle the rest"
      );

      // Clear transition state after a short delay to allow UI to update
      setTimeout(() => {
        isTransitioning = false;
        console.log("🚀 StartPositionPicker: Cleared isTransitioning state");
      }, 500);
    } catch (error) {
      console.error(
        "🚨 StartPositionPicker: Error selecting start position:",
        error
      );
      if (error instanceof Error) {
        console.error("🚨 StartPositionPicker: Error stack:", error.stack);
        console.error("🚨 StartPositionPicker: Error details:", {
          message: error.message,
          name: error.name,
          startPosPictograph: startPosPictograph,
        });
      }
      isTransitioning = false;
      // Consider showing an error message to the user
      alert(
        `Failed to select start position: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  // Initialize on mount
  onMount(() => {
    loadStartPositions();
  });

  // Reload when grid mode changes
  $effect(() => {
    if (gridMode) {
      loadStartPositions();
    }
  });

  // CRITICAL FIX: Listen for sequence state changes to clear transition state
  import { sequenceStateService } from "$lib/services/SequenceStateService.svelte";

  $effect(() => {
    const currentSequence = sequenceStateService.currentSequence;

    // If a sequence with startPosition exists and we're transitioning, clear the transition
    if (currentSequence && currentSequence.startPosition && isTransitioning) {
      console.log(
        "🚀 StartPositionPicker: Sequence with start position detected, clearing transition state"
      );
      isTransitioning = false;
    }
  });
</script>

<div class="start-pos-picker" data-testid="start-position-picker">
  {#if isLoading}
    <LoadingState />
  {:else if loadingError}
    <ErrorState />
  {:else if startPositionPictographs.length === 0}
    <ErrorState
      message="No valid start positions found for the current configuration."
      hasRefreshButton={false}
    />
  {:else}
    <PictographGrid
      pictographs={startPositionPictographs}
      selectedPictograph={selectedStartPos}
      onPictographSelect={handleSelect}
    />
  {/if}

  <!-- Loading overlay during transition -->
  {#if isTransitioning}
    <TransitionOverlay />
  {/if}
</div>

<style>
  .start-pos-picker {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    padding: var(--spacing-lg);
    background: transparent;
    position: relative;
  }
</style>
