<!--
StartPositionPicker.svelte - Simplified version with advanced variations
Shows 3 start positions (Alpha, Beta, Gamma) with toggle to view all 16 variations
-->
<script lang="ts">
  import type { IHapticFeedbackService, PictographData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  import { createSimplifiedStartPositionState } from "../state/start-position-state.svelte";
  import AdvancedStartPositionPicker from "./AdvancedStartPositionPicker.svelte";
  import PictographGrid from "./PictographGrid.svelte";
  import SimpleAdvancedToggle from "./SimpleAdvancedToggle.svelte";

  // Props - receive navigation callbacks and layout detection
  const {
    onNavigateToAdvanced,
    onNavigateToDefault,
    isSideBySideLayout = () => false,
  } = $props<{
    onNavigateToAdvanced?: () => void;
    onNavigateToDefault?: () => void;
    isSideBySideLayout?: () => boolean;
  }>();

  // Create simplified state
  const pickerState = createSimplifiedStartPositionState();

  // State for showing advanced picker
  let showAdvancedPicker = $state(false);

  // Track if animation is in progress
  let isAnimating = $state(false);

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
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

  // Handle back from advanced picker (for back button in advanced picker)
  function handleBackToDefault() {
    // Trigger navigation haptic feedback for back button
    hapticService?.trigger("navigation");
    handleToggleView(false);
  }

  // Handle grid mode change in advanced picker
  function handleGridModeChange(gridMode: any) {
    pickerState.loadAllVariations(gridMode);
  }
</script>

<div class="start-pos-picker" data-testid="start-position-picker">
  <!-- Toggle between simple and advanced views -->
  <div class="toggle-container">
    <SimpleAdvancedToggle
      isAdvanced={showAdvancedPicker}
      onToggle={handleToggleView}
    />
  </div>

  <!-- Use {#key} to ensure only one view exists at a time during transitions -->
  {#key showAdvancedPicker}
    <div class="picker-view" in:fade={{ duration: 250, delay: 250 }} out:fade={{ duration: 250 }}>
      {#if showAdvancedPicker}
        <!-- Advanced picker with all 16 variations -->
        <AdvancedStartPositionPicker
          pictographDataSet={pickerState.allVariations}
          selectedPictograph={pickerState.selectedPosition}
          currentGridMode={pickerState.currentGridMode}
          onPictographSelect={handlePositionSelect}
          onGridModeChange={handleGridModeChange}
          onBack={handleBackToDefault}
          {isSideBySideLayout}
          {isAnimating}
        />
      {:else}
        <!-- Default picker with 3 positions -->
        <!-- Header text -->
        <div class="picker-header">
          <h2 class="picker-title">Choose your start position!</h2>
        </div>

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
    padding: 20px 0;
    position: relative;
    container-type: inline-size;
  }

  .picker-view {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }

  .picker-header {
    position: absolute;
    top: 40%;
    left: 50%;
    transform: translate(-50%, -120px); /* Position above the centered grid */
    text-align: center;
    width: 100%;
    max-width: 100%;
    padding: 0 10px;
    box-sizing: border-box;
    z-index: 10; /* Ensure it floats above the grid */
  }

  .picker-title {
    margin: 0;
    font-family: "Monotype Corsiva", cursive, serif;
    /* Increased font sizes for more prominence */
    font-size: clamp(1.3rem, 3vw + 0.4rem, 2.4rem);
    font-weight: 400;
    color: var(--text-color, #ffffff);
    white-space: nowrap;
    font-style: italic;
    line-height: 1.1;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .toggle-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 16px 0;
    width: 100%;
    z-index: 20;
  }

  .grid-container {
    width: 100%;
    height: 100%; /* Take full height */
    display: flex;
    justify-content: center;
    align-items: center;
    /* Grid is now centered in the full available space */
  }

  /* Container-based responsive adjustments */
  @container (max-width: 600px) {
    .picker-title {
      font-size: clamp(1.1rem, 2.6vw + 0.3rem, 2rem);
    }

    .picker-header {
      transform: translate(-50%, -100px); /* Closer on medium screens */
    }
  }

  @container (max-width: 400px) {
    .picker-title {
      font-size: clamp(1.4rem, 2.4vw + 0.25rem, 1.7rem);
      white-space: normal;
      line-height: 1.2;
    }

    .picker-header {
      transform: translate(-50%, -80px); /* Even closer on small screens */
    }
  }

  @container (max-width: 300px) {
    .picker-title {
      font-size: clamp(0.9rem, 2.2vw + 0.2rem, 1.4rem);
    }

    .picker-header {
      padding: 0 5px;
      transform: translate(-50%, -70px); /* Very close on tiny screens */
    }
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

  /* Large screens - more prominent sizing */
  @media (min-width: 1200px) {
    .picker-title {
      font-size: clamp(1.6rem, 3.2vw + 0.5rem, 2.8rem);
    }

    .picker-header {
      transform: translate(-50%, -140px); /* A bit more spacing on large screens */
    }
  }
</style>
