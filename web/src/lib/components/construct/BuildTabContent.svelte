<!--
  BuildTabContent.svelte

  Build tab content component extracted from ConstructTab.
  Handles the conditional logic for showing either StartPositionPicker or OptionPicker
  based on the current sequence state.
-->
<script lang="ts">
  import { constructTabEventService } from "$services/implementations/ConstructTabEventService";
  import type { PictographData } from "$services/interfaces/domain-types";
  import { resolve } from "$services/bootstrap";
  import { createSequenceState } from "$lib/state/sequence-state.svelte";
  import { createConstructTabState } from "$lib/state/construct-tab-state.svelte";
  import OptionPickerContainer from "./OptionPickerContainer.svelte";
  import StartPositionPicker from "./StartPositionPicker.svelte";
  // Import fade transition for smooth switching
  import { getSettings } from "$lib/state/appState.svelte";
  import { fade } from "svelte/transition";

  // Create component-scoped state using factory functions - lazily
  let sequenceService: any = $state(null);
  let sequenceState: any = $state(null);
  let constructTabState: any = $state(null);

  // Initialize services when container is ready
  $effect(() => {
    try {
      if (!sequenceService) {
        sequenceService = resolve("ISequenceService");

        // Create state managers once service is available
        if (sequenceService && !sequenceState) {
          sequenceState = createSequenceState(sequenceService);
          constructTabState = createConstructTabState(sequenceState);
        }
      }
    } catch (error) {
      console.error("BuildTabContent: Error initializing services:", error);
    }
  });

  // CRITICAL FIX: Also watch the singleton sequence state for updates
  // This ensures we react to changes made by the coordination service
  import { sequenceStateService } from "$lib/services/SequenceStateService.svelte";

  // Sync the component-scoped state with singleton state when it changes
  $effect(() => {
    if (!sequenceState) return; // Wait for state to be initialized

    const singletonSequence = sequenceStateService.currentSequence;
    const componentSequence = sequenceState.currentSequence;

    // If singleton has a different sequence, update component state
    if (singletonSequence && singletonSequence.id !== componentSequence?.id) {
      sequenceState.setCurrentSequence(singletonSequence);
    }

    // IMPORTANT: Also sync when startPosition changes
    if (
      singletonSequence &&
      componentSequence &&
      singletonSequence.id === componentSequence.id &&
      singletonSequence.startPosition !== componentSequence.startPosition
    ) {
      sequenceState.setCurrentSequence(singletonSequence);
    }
  });

  // Initialize component coordination using effect instead of onMount
  $effect(() => {
    try {
      constructTabEventService().setupComponentCoordination();
    } catch (error) {
      console.error(
        "BuildTabContent: Error setting up component coordination:",
        error
      );
    }
  });

  // Reactive state from store
  let shouldShowStartPositionPicker = $derived.by(() => {
    // CRITICAL FIX: Use singleton state directly for immediate reactivity
    const singletonSequence = sequenceStateService.currentSequence;
    const shouldShow = !singletonSequence || !singletonSequence.startPosition;

    return shouldShow;
  });
  let gridMode = $derived(constructTabState?.gridMode || "radial");
  let settings = $derived(getSettings());

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
  async function handleOptionSelected(option: PictographData) {
    await constructTabEventService().handleOptionSelected(option);
  }
</script>

<div class="build-tab-content" data-testid="build-tab-content">
  <!-- Start Position Picker -->
  {#if shouldShowStartPositionPicker}
    <div class="content-container" in:contentIn out:contentOut>
      <div class="panel-content">
        <StartPositionPicker {gridMode} />
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
