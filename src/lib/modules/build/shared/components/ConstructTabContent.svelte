<!--
  ConstructTabContent.svelte

  Pure UI component that displays StartPositionPicker or OptionPicker
  based on the current sequence state. Receives all state and handlers as props.
-->
<script lang="ts">
	import { GridMode, type PictographData } from "$shared";
	import { fade } from "svelte/transition";
	import { OptionViewer, StartPositionPicker } from "../../construct";
	import type { SimplifiedStartPositionState } from "../../construct/start-position-picker/state/start-position-state.svelte";

  // Props - simplified with unified service
  let {
    shouldShowStartPositionPicker,
    startPositionState,
    onOptionSelected,
    currentSequence = [],
    isUndoingOption = false,
    onStartPositionNavigateToAdvanced,
    onStartPositionNavigateToDefault,
    isSideBySideLayout = () => false,
    onOpenFilters = () => {},
    onCloseFilters = () => {},
    isContinuousOnly = false,
    isFilterPanelOpen = false,
    onToggleContinuous = () => {},
  } = $props<{
    shouldShowStartPositionPicker: boolean;
    startPositionState?: SimplifiedStartPositionState | null;
    onOptionSelected: (option: PictographData) => Promise<void>;
    currentSequence?: PictographData[];
    isUndoingOption?: boolean;
    onStartPositionNavigateToAdvanced?: () => void;
    onStartPositionNavigateToDefault?: () => void;
    isSideBySideLayout?: () => boolean;
    onOpenFilters?: () => void;
    onCloseFilters?: () => void;
    isContinuousOnly?: boolean;
    isFilterPanelOpen?: boolean;
    onToggleContinuous?: (value: boolean) => void;
  }>();
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
              startPositionState={startPositionState}
              onNavigateToAdvanced={onStartPositionNavigateToAdvanced}
              onNavigateToDefault={onStartPositionNavigateToDefault}
              {isSideBySideLayout}
            />
          <!-- Option Grid -->
          {:else}
            <OptionViewer
              {onOptionSelected}
              {currentSequence}
              currentGridMode={startPositionState?.currentGridMode || GridMode.DIAMOND}
              {isSideBySideLayout}
              {isUndoingOption}
              {onOpenFilters}
              {onCloseFilters}
              {isContinuousOnly}
              {isFilterPanelOpen}
              {onToggleContinuous}
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
    min-height: 0;
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
