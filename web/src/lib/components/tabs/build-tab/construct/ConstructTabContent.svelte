<!--
  ConstructTabContent.svelte

  Pure UI component that displays StartPositionPicker or OptionPicker
  based on the current sequence state. Receives all state and handlers as props.
-->
<script lang="ts">
  import type { PictographData } from "$domain";
  import OptionPickerContainer from "./option-picker/OptionPickerContainer.svelte";
  import StartPositionPicker from "./start-position-picker/StartPositionPicker.svelte";
  // Import fade transition for smooth switching
  import { getSettings } from "$state";
  import { fade } from "svelte/transition";

  // Props - simplified with unified service
  let { shouldShowStartPositionPicker, onOptionSelected } = $props<{
    shouldShowStartPositionPicker: boolean;
    onOptionSelected: (option: PictographData) => Promise<void>;
  }>();

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
</script>

<div class="construct-tab-content" data-testid="construct-tab-content">
  <!-- Start Position Picker -->
  {#if shouldShowStartPositionPicker}
    <div class="content-container" in:contentIn out:contentOut>
      <div class="panel-content">
        <StartPositionPicker />
      </div>
    </div>
  {/if}

  <div
    class="content-container"
    class:hidden={shouldShowStartPositionPicker}
    in:contentIn
    out:contentOut
  >
    <div class="panel-content transparent-scroll">
      <OptionPickerContainer {onOptionSelected} />
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
