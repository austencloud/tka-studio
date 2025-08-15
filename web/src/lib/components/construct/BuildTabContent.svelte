<!--
	BuildTabContent.svelte

	Build tab content component extracted from ConstructTab.
	Handles the conditional logic for showing either StartPositionPicker or OptionPicker
	based on the current sequence state.
-->
<script lang="ts">
  import { constructTabEventService } from "$services/implementations/ConstructTabEventService";
  import type { BeatData, PictographData } from "$services/interfaces";
  import { resolve } from "$services/bootstrap";
  import { createSequenceState } from "$lib/state/sequenceState.svelte";
  import { createConstructTabState } from "$lib/state/construct-tab-state.svelte";
  import OptionPickerContainer from "./OptionPickerContainer.svelte";
  import StartPositionPicker from "./StartPositionPicker.svelte";
  // Import fade transition for smooth switching
  import { GridMode } from "$domain/enums";
  import { getSettings } from "$lib/state/appState.svelte";
  import { OptionDataService } from "$services/implementations/OptionDataService";
  import { fade } from "svelte/transition";

  console.log("🎯 BuildTabContent script is being processed");

  // Create component-scoped state using factory functions
  const sequenceService = resolve("ISequenceService") as any; // TODO: Fix typing
  const sequenceState = createSequenceState(sequenceService);
  const constructTabState = createConstructTabState(sequenceState);

  // CRITICAL FIX: Also watch the singleton sequence state for updates
  // This ensures we react to changes made by the coordination service
  import { sequenceStateService } from "$lib/services/SequenceStateService.svelte";

  // Sync the component-scoped state with singleton state when it changes
  $effect(() => {
    const singletonSequence = sequenceStateService.currentSequence;
    const componentSequence = sequenceState.currentSequence;

    // If singleton has a different sequence, update component state
    if (singletonSequence && singletonSequence.id !== componentSequence?.id) {
      console.log("🔄 Syncing component sequence state with singleton state");
      sequenceState.setCurrentSequence(singletonSequence);
    }
  });

  // Simple debugging
  console.log("🎯 constructTabState available:", !!constructTabState);

  // Initialize component coordination using effect instead of onMount
  $effect(() => {
    console.log(
      "🎯 BuildTabContent: $effect called - setting up component coordination"
    );
    try {
      constructTabEventService.setupComponentCoordination();
      console.log("✅ BuildTabContent: Component coordination setup complete");
    } catch (error) {
      console.error(
        "❌ BuildTabContent: Error setting up component coordination:",
        error
      );
    }
  });

  // Reactive state from store
  let shouldShowStartPositionPicker = $derived(
    constructTabState.shouldShowStartPositionPicker
  );
  let currentSequence = $derived(sequenceState.currentSequence);
  let gridMode = $derived(constructTabState.gridMode);
  let settings = $derived(getSettings());

  // Add debugging for the reactive values
  $effect(() => {
    console.log(
      "🔍 BuildTabContent shouldShowStartPositionPicker:",
      shouldShowStartPositionPicker
    );
    console.log(
      "🔍 BuildTabContent currentSequence exists:",
      !!currentSequence
    );
    console.log(
      "🔍 BuildTabContent currentSequence.start_position exists:",
      !!currentSequence?.start_position
    );
    console.log(
      "🔍 BuildTabContent singleton sequence exists:",
      !!sequenceStateService.currentSequence
    );
    console.log(
      "🔍 BuildTabContent singleton start_position exists:",
      !!sequenceStateService.currentSequence?.start_position
    );
  });

  // Preload all options for default start positions when component loads
  let isPreloading = $state(false);
  let preloadingComplete = $state(false);

  $effect(() => {
    // Only preload once when component first loads and we should show start position picker
    if (shouldShowStartPositionPicker && !preloadingComplete && !isPreloading) {
      preloadAllDefaultOptions();
    }
  });

  async function preloadAllDefaultOptions() {
    try {
      isPreloading = true;
      console.log(
        "🚀 Preloading ALL options for ALL default start positions..."
      );

      // Get the start position service to fetch default start positions
      const startPositionService = resolve("IStartPositionService") as {
        getDefaultStartPositions: (
          gridMode: GridMode
        ) => Promise<PictographData[]>;
      };
      const defaultStartPositions =
        await startPositionService.getDefaultStartPositions(
          gridMode === "diamond" ? GridMode.DIAMOND : GridMode.BOX
        );

      // Create and initialize option data service
      const optionDataService = new OptionDataService();
      await optionDataService.initialize();

      // Preload options for all default start positions
      const allPreloadedOptions: Record<string, PictographData[]> = {};

      for (const startPos of defaultStartPositions) {
        try {
          // Extract end position (similar to how StartPositionPicker does it)
          const endPosition = extractEndPosition(startPos);

          // Load options for this start position
          const options = await optionDataService.getNextOptionsFromEndPosition(
            endPosition,
            gridMode === "diamond" ? GridMode.DIAMOND : GridMode.BOX,
            {}
          );

          // Store with end position as key for quick lookup
          allPreloadedOptions[endPosition] = options || [];
          console.log(
            `✅ Preloaded ${options?.length || 0} options for start position: ${endPosition}`
          );
        } catch (error) {
          console.warn(
            `Failed to preload options for start position:`,
            startPos,
            error
          );
        }
      }

      // Store all preloaded options in localStorage
      localStorage.setItem(
        "all_preloaded_options",
        JSON.stringify(allPreloadedOptions)
      );
      preloadingComplete = true;

      console.log(
        `🎉 Successfully preloaded options for ${Object.keys(allPreloadedOptions).length} start positions`,
        {
          startPositions: Object.keys(allPreloadedOptions),
          totalOptions: Object.values(allPreloadedOptions).reduce(
            (sum, opts) => sum + opts.length,
            0
          ),
        }
      );
    } catch (error) {
      console.error(
        "❌ Failed to preload default start position options:",
        error
      );
    } finally {
      isPreloading = false;
    }
  }

  // Helper function to extract end position from pictograph (same logic as StartPositionPicker)
  function extractEndPosition(pictograph: PictographData): string {
    try {
      // Extract end position based on motion data
      const blueMotion = pictograph.motions?.blue;
      const redMotion = pictograph.motions?.red;

      if (blueMotion && redMotion) {
        const blueEndLoc = blueMotion.end_loc || blueMotion.start_loc;
        const blueEndOri = blueMotion.end_ori || blueMotion.start_ori;
        const redEndLoc = redMotion.end_loc || redMotion.start_loc;
        const redEndOri = redMotion.end_ori || redMotion.start_ori;

        return `${blueEndLoc}_${blueEndOri}-${redEndLoc}_${redEndOri}`;
      }

      // Fallback to ID-based extraction
      if (pictograph.id) {
        const match = pictograph.id.match(/start-pos-(.+)/);
        return match?.[1] ?? "alpha1_alpha1-0";
      }

      return "alpha1_alpha1-0";
    } catch (error) {
      console.warn("Failed to extract end position:", error);
      return "alpha1_alpha1-0";
    }
  }

  // Transition functions that respect animation settings - same as main interface
  const contentOut = (node: Element) => {
    const animationsEnabled = settings.animationsEnabled !== false;
    return fade(node, {
      duration: animationsEnabled ? 250 : 0,
    });
  };

  const contentIn = (node: Element) => {
    const animationsEnabled = settings.animationsEnabled !== false;
    return fade(node, {
      duration: animationsEnabled ? 300 : 0,
      delay: animationsEnabled ? 250 : 0, // Wait for out transition
    });
  };

  // Event handlers
  async function handleStartPositionSelected(startPosition: BeatData) {
    console.log(
      "🎯 BuildTabContent: handleStartPositionSelected called with:",
      startPosition.pictograph_data?.id
    );
    try {
      await constructTabEventService.handleStartPositionSelected(startPosition);
      console.log(
        "✅ BuildTabContent: constructTabEventService.handleStartPositionSelected completed"
      );
    } catch (error) {
      console.error(
        "❌ BuildTabContent: Error in handleStartPositionSelected:",
        error
      );
    }
  }

  async function handleOptionSelected(option: PictographData) {
    await constructTabEventService.handleOptionSelected(option);
  }
</script>

<div class="build-tab-content" data-testid="build-tab-content">
  <!-- Start Position Picker -->
  {#if shouldShowStartPositionPicker}
    <div class="content-container" in:contentIn out:contentOut>
      <div class="panel-content">
        <StartPositionPicker
          {gridMode}
          onStartPositionSelected={handleStartPositionSelected}
        />
      </div>
    </div>
  {/if}

  <!-- Option Picker -->
  {#if !shouldShowStartPositionPicker}
    <div class="content-container" in:contentIn out:contentOut>
      <div class="panel-content transparent-scroll">
        <OptionPickerContainer onOptionSelected={handleOptionSelected} />
      </div>
    </div>
  {/if}
</div>

<style>
  .build-tab-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    height: 100%;
    width: 100%;
    position: relative; /* Needed for absolute positioning of content */
  }

  .content-container {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    height: 100%;
    width: 100%;
  }

  .panel-content {
    flex: 1;
    overflow: auto;
    padding: var(--spacing-lg);
  }

  .panel-content.transparent-scroll {
    background: transparent;
  }

  /* Hide scrollbars for transparent scroll area while maintaining functionality */
  .panel-content.transparent-scroll::-webkit-scrollbar {
    width: 8px;
  }

  .panel-content.transparent-scroll::-webkit-scrollbar-track {
    background: transparent;
  }

  .panel-content.transparent-scroll::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
  }

  .panel-content.transparent-scroll::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
  }
</style>
