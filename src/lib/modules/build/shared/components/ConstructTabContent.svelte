<!--
  ConstructTabContent.svelte

  Pure UI component that displays StartPositionPicker or OptionPicker
  based on the current sequence state. Receives all state and handlers as props.
-->
<script lang="ts">
	import type { PictographData } from "$shared";
	import { fade } from "svelte/transition";
	import { OptionViewer, StartPositionPicker } from "../../construct";
  import type { SimplifiedStartPositionState } from "../../construct/start-position-picker/state/start-position-state.svelte";

  // Props - simplified with unified service
  let {
    shouldShowStartPositionPicker,
    startPositionState,
    onOptionSelected,
    currentSequence = [],
    isClearingSequence = false,
    isUndoingOption = false,
    onStartPositionNavigateToAdvanced,
    onStartPositionNavigateToDefault,
    isSideBySideLayout = () => false,
  } = $props<{
    shouldShowStartPositionPicker: boolean;
    startPositionState?: SimplifiedStartPositionState | null;
    onOptionSelected: (option: PictographData) => Promise<void>;
    currentSequence?: PictographData[];
    isClearingSequence?: boolean;
    isUndoingOption?: boolean;
    onStartPositionNavigateToAdvanced?: () => void;
    onStartPositionNavigateToDefault?: () => void;
    isSideBySideLayout?: () => boolean;
  }>();

  // Reference to StartPositionPicker for external control
  let startPositionPickerRef: any = $state(null);

  // Expose method to go back in start position picker
  export function handleStartPositionPickerBack() {
    if (startPositionPickerRef) {
      startPositionPickerRef.goBackToDefault();
      return true; // Handled
    }
    return false; // Not handled
  }
</script>

<div class="construct-tab-content" data-testid="construct-tab-content">
  <!-- Main Content (always visible) -->
  <div class="content-container">
    <div class="panel-content transparent-scroll">
      <!-- Use {#key} for smooth transitions between pickers -->
      {#key shouldShowStartPositionPicker}
        <div
          class="picker-transition-wrapper"
          in:fade={{ duration: 250, delay: 250 }}
          out:fade={{ duration: 250 }}
        >
          <!-- Start Position Picker -->
          {#if shouldShowStartPositionPicker}
            <StartPositionPicker
              bind:this={startPositionPickerRef}
              startPositionState={startPositionState}
              onNavigateToAdvanced={onStartPositionNavigateToAdvanced}
              onNavigateToDefault={onStartPositionNavigateToDefault}
              {isSideBySideLayout}
            />
          <!-- Option Grid (default) -->
          {:else}
            <OptionViewer
              {onOptionSelected}
              {currentSequence}
              {isClearingSequence}
              {isSideBySideLayout}
              {isUndoingOption}
            />
          {/if}
        </div>
      {/key}
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



  .panel-content {
    flex: 1;
    overflow: hidden; /* Changed from visible to hidden to enable proper scrolling */
    min-height: 0; /* Important for flex child to enable scrolling */
    position: relative; /* Positioning context for transition wrapper */
  }

  .panel-content.transparent-scroll {
    background: transparent;
  }

  .picker-transition-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
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
