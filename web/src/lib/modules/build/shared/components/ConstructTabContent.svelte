<!--
  ConstructTabContent.svelte

  Pure UI component that displays StartPositionPicker or OptionPicker
  based on the current sequence state. Receives all state and handlers as props.
-->
<script lang="ts">
	import type { PictographData } from "$shared";
// Import fade transition for smooth switching
  import { fade } from "svelte/transition";
  import { OptionGrid, StartPositionPicker } from "../../construct";

  // Props - simplified with unified service
  let { shouldShowStartPositionPicker, onOptionSelected, currentSequence = [] } = $props<{
    shouldShowStartPositionPicker: boolean;
    onOptionSelected: (option: PictographData) => Promise<void>;
    currentSequence?: PictographData[];
  }>();



  // Transition functions - animations are always enabled
  const contentOut = (node: Element) => {
    return fade(node, {
      duration: 250,
    });
  };

  const contentIn = (node: Element) => {
    return fade(node, {
      duration: 300,
      delay: 250, // Wait for out transition
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
      <OptionGrid {onOptionSelected} {currentSequence} />
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
    overflow: visible;
    height: 100%;
    width: 100%;
  }

  .content-container.hidden {
    display: none;
  }

  .panel-content {
    flex: 1;
    overflow: hidden; /* Changed from visible to hidden to enable proper scrolling */
    min-height: 0; /* Important for flex child to enable scrolling */
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
