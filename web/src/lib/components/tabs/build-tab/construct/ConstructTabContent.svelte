<!--
  ConstructTabContent.svelte

  Construct tab content component extracted from ConstructTab.
  Handles the conditional logic for showing either StartPositionPicker or OptionPicker
  based on the current sequence state.
-->
<script lang="ts">
	import OptionPickerContainer from './option-picker/OptionPickerContainer.svelte';
	import StartPositionPicker from './start-position-picker/StartPositionPicker.svelte';
  import { constructTabEventService } from "$services/implementations/construct/ConstructTabEventService";
  import type { PictographData } from "$services/interfaces/domain-types";

  // Import fade transition for smooth switching
  import { getSettings } from "$lib/state/app-state.svelte";
  import { fade } from "svelte/transition";
  // CRITICAL FIX: Also watch the singleton sequence state for updates
  // This ensures we react to changes made by the coordination service
  import { resolve } from "$lib/services/bootstrap";
  import { createSequenceState } from "$lib/state/sequence/sequence-state.svelte";

  // Get service from DI container and create component-scoped state
  const sequenceStateService = resolve(
    "ISequenceStateService"
  ) as import("$lib/services/interfaces/sequence-state-interfaces").ISequenceStateService;
  const sequenceState = createSequenceState(sequenceStateService);

  // TODO: Implement proper state synchronization with new DI pattern

  // Initialize component coordination using effect instead of onMount
  $effect(() => {
    try {
      constructTabEventService().setupComponentCoordination();
    } catch (error) {
      console.error(
        "ConstructTabContent: Error setting up component coordination:",
        error
      );
    }
  });

  // Reactive state from store
  let shouldShowStartPositionPicker = $derived.by(() => {
    // Use the new sequence state
    const currentSequence = sequenceState.currentSequence;
    const shouldShow =
      !currentSequence || !currentSequence.startingPositionBeat;

    console.log("🔍 ConstructTabContent: shouldShowStartPositionPicker check", {
      hasSequence: !!currentSequence,
      hasStartingPositionBeat: !!currentSequence?.startingPositionBeat,
      shouldShow,
    });

    return shouldShow;
  });
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

  async function handleStartPositionSelected(position: any) {
    try {
      // Use the event service to handle start position selection
      await constructTabEventService().handleStartPositionSelected(position);
    } catch (error) {
      console.error("❌ Error handling start position selection:", error);
    }
  }
</script>

<div class="construct-tab-content" data-testid="construct-tab-content">
  <!-- Start Position Picker -->
  {#if shouldShowStartPositionPicker}
    <div class="content-container" in:contentIn out:contentOut>
      <div class="panel-content">
        <StartPositionPicker {sequenceState} />
      </div>
    </div>
  {/if}

  <!-- Option Picker - Always mounted to receive events, but hidden when start position picker is shown -->
  <div
    class="content-container"
    class:hidden={shouldShowStartPositionPicker}
    in:contentIn
    out:contentOut
  >
    <div class="panel-content transparent-scroll">
      <OptionPickerContainer onOptionSelected={handleOptionSelected} />
    </div>
  </div>
</div>

<style>
  .construct-tab-content {
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

  .content-container.hidden {
    display: none;
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
