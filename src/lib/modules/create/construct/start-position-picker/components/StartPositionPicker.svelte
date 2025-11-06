<!--
StartPositionPicker.svelte - Simplified version with advanced variations
Shows 3 start positions (Alpha, Beta, Gamma) with toggle to view all 16 variations
-->
<script lang="ts">
  import type {
    GridMode,
    IHapticFeedbackService,
    PictographData,
  } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  import {
    createSimplifiedStartPositionState,
    type SimplifiedStartPositionState,
  } from "../state/start-position-state.svelte";
  import AdvancedStartPositionPicker from "./AdvancedStartPositionPicker.svelte";
  import PictographGrid from "./PictographGrid.svelte";
  import ConstructPickerHeader from "../../shared/components/ConstructPickerHeader.svelte";

  // Props - receive navigation callbacks and layout detection
  const {
    startPositionState,
    onNavigateToAdvanced,
    onNavigateToDefault,
    isSideBySideLayout = () => false,
  } = $props<{
    startPositionState?: SimplifiedStartPositionState | null;
    onNavigateToAdvanced?: () => void;
    onNavigateToDefault?: () => void;
    isSideBySideLayout?: () => boolean;
  }>();

  // Create simplified state
  const pickerState =
    startPositionState ?? createSimplifiedStartPositionState();

  // State for showing advanced picker
  let showAdvancedPicker = $state(false);

  // Track if animation is in progress
  let isAnimating = $state(false);

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Expose state for parent components
  export function isShowingAdvanced() {
    return showAdvancedPicker;
  }

  export function goBackToDefault() {
    handleBackToDefault();
  }

  // Handle position selection
  async function handlePositionSelect(position: PictographData) {
    // Trigger selection haptic feedback for start position selection
    hapticService?.trigger("selection");

    await pickerState.selectPosition(position);
  }

  // Handle toggle between simple and advanced
  function handleToggleView(isAdvanced: boolean) {
    // Trigger haptic feedback
    hapticService?.trigger("selection");

    // Start animation
    isAnimating = true;

    if (isAdvanced) {
      showAdvancedPicker = true;
      pickerState.loadAllVariations(pickerState.currentGridMode);
      onNavigateToAdvanced?.();
    } else {
      showAdvancedPicker = false;
      onNavigateToDefault?.();
    }

    // End animation after transition completes
    setTimeout(() => {
      isAnimating = false;
    }, 600);
  }

  // Handle return to the default picker (exposed for external triggers)
  function handleBackToDefault() {
    // Trigger navigation haptic feedback for returning to default
    hapticService?.trigger("selection");
    handleToggleView(false);
  }

  // Handle grid mode change in advanced picker
  async function handleGridModeChange(gridMode: GridMode) {
    await pickerState.loadPositions(gridMode);
    await pickerState.loadAllVariations(gridMode);
  }
</script>

<div class="start-pos-picker" data-testid="start-position-picker">
  <ConstructPickerHeader
    variant="start"
    currentGridMode={pickerState.currentGridMode}
    isAdvanced={showAdvancedPicker}
    isSideBySideLayout={isSideBySideLayout()}
    onToggleAdvanced={handleToggleView}
    onGridModeChange={handleGridModeChange}
  />

  <!-- Use {#key} to ensure only one view exists at a time during transitions -->
  {#key showAdvancedPicker}
    <div
      class="picker-view"
      in:fade={{ duration: 250, delay: 250 }}
      out:fade={{ duration: 250 }}
    >
      {#if showAdvancedPicker}
        <!-- Advanced picker with all 16 variations -->
        <AdvancedStartPositionPicker
          pictographDataSet={pickerState.allVariations}
          selectedPictograph={pickerState.selectedPosition}
          currentGridMode={pickerState.currentGridMode}
          onPictographSelect={handlePositionSelect}
          {isSideBySideLayout}
          {isAnimating}
        />
      {:else}
        <!-- Always show the pictograph grid - no loading/error states needed -->
        <div class="grid-container">
          <PictographGrid
            pictographDataSet={pickerState.positions}
            selectedPictograph={pickerState.selectedPosition}
            onPictographSelect={handlePositionSelect}
            {isAnimating}
          />
        </div>
      {/if}
    </div>
  {/key}
</div>

<style>
  .start-pos-picker {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    min-height: 300px;
    position: relative;
    container-type: inline-size;
  }

  .picker-view {
    display: flex;
    flex-direction: column;
    flex: 1;
    width: 100%;
    position: relative;
  }

  .grid-container {
    width: 100%;
    height: 100%; /* Take full height */
    display: flex;
    justify-content: center;
    align-items: center;
    /* Grid is now centered in the full available space */
  }

  /* Traditional media queries as fallback */
  @media (max-width: 768px) {
    .start-pos-picker {
      padding: 16px 0;
    }
  }

  @media (max-width: 480px) {
    .start-pos-picker {
      padding: 12px 0;
    }
  }
</style>
