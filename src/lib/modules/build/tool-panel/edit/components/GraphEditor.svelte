<!-- GraphEditor.svelte - Professional Graph Editor ported from desktop -->
<script lang="ts">
  import type { BeatData, IHapticFeedbackService } from "$shared";
  import { Pictograph, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import MainAdjustmentPanel from "./MainAdjustmentPanel.svelte";

  let hapticService: IHapticFeedbackService;

  // Props - sequence state and optional external data
  const {
    selectedBeatIndex,
    selectedBeatData,
    onArrowSelected: _onArrowSelected,
  }: {
    selectedBeatIndex: number | null;
    selectedBeatData: BeatData | null;
    onBeatModified?: (beatIndex: number, beatData: BeatData) => void;
    onArrowSelected?: (arrowData: {
      color: string;
      orientation?: string;
      turn_amount?: number;
      type: string;
    }) => void;
    onVisibilityChanged?: (isVisible: boolean) => void;
  } = $props();

  // Component references
  let pictographComponent = $state<Pictograph>();
  let adjustmentPanel = $state<MainAdjustmentPanel>();

  // Internal state
  let errorMessage = $state<string | null>(null);

  // Handle orientation changes
  function handleOrientationChanged(color: string, orientation: string) {
    try {
      const orientationData = {
        color,
        orientation,
        type: "orientation_change",
      };
      _onArrowSelected?.(orientationData);
      console.log(
        `Graph Editor: ${color} orientation changed to ${orientation}`
      );

      // Trigger pictograph update immediately
      if (selectedBeatData && pictographComponent) {
        // Pictograph is reactive - no manual update needed
        console.log("Pictograph will update reactively");
      }
    } catch (error) {
      console.error("Error handling orientation change:", error);
      errorMessage = "Failed to update orientation";
    }
  }

  // Handle turn amount changes
  function handleTurnAmountChanged(color: string, turnAmount: number) {
    try {
      const turnData = {
        color,
        turn_amount: turnAmount,
        type: "turn_change",
      };
      _onArrowSelected?.(turnData);
      console.log(
        `Graph Editor: ${color} turn amount changed to ${turnAmount}`
      );
    } catch (error) {
      console.error("Error handling turn amount change:", error);
      errorMessage = "Failed to update turn amount";
    }
  }

  // Update components when beat data changes
  $effect(() => {
    if (selectedBeatIndex !== null && selectedBeatData) {
      console.log("🎭 GraphEditor: Beat data updated", {
        beatIndex: selectedBeatIndex,
        isBlank: selectedBeatData.isBlank,
        beatData: selectedBeatData
      });

      // Pictograph updates reactively via props
      // No manual update needed

      // Update adjustment panel
      if (adjustmentPanel) {
        adjustmentPanel.setBeatData(selectedBeatIndex, selectedBeatData);
      }
    } else if (selectedBeatData && selectedBeatData.beatNumber === 0) {
      // Handle start position selection
      console.log("🎭 GraphEditor: Start position data updated", {
        beatData: selectedBeatData
      });

      // Update adjustment panel for start position
      if (adjustmentPanel) {
        adjustmentPanel.setBeatData(-1, selectedBeatData); // Use -1 as special index for start position
      }
    } else {
      console.log("🎭 GraphEditor: No beat selected or no beat data", {
        selectedBeatIndex,
        selectedBeatData
      });
    }
  });

  // Clear error message after 5 seconds
  $effect(() => {
    if (errorMessage) {
      const timeout = setTimeout(() => {
        errorMessage = null;
      }, 5000);

      return () => clearTimeout(timeout);
    }
    return undefined;
  });

  function handleCloseError() {
    hapticService?.trigger("selection");
    errorMessage = null;
  }

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });
</script>

<div class="graph-editor" data-testid="graph-editor">
  <!-- Error display -->
  {#if errorMessage}
    <div class="error-banner">
      <span>⚠️ {errorMessage}</span>
      <button onclick={handleCloseError}>×</button>
    </div>
  {/if}

  <!-- Main content area -->
  <div class="graph-content">
    <!-- Top section: Pictograph Display (65% height) -->
    <div class="pictograph-section">
      <!-- Remove Beat Button now handled by ButtonPanel in BuildTab -->

      <div class="pictograph-display">
        {#if selectedBeatData && !selectedBeatData.isBlank}
          <div class="pictograph-wrapper">
            <Pictograph
              bind:this={pictographComponent}
              pictographData={selectedBeatData}
            />
          </div>
        {:else}
          <div class="no-pictograph">
            <div class="placeholder-icon">🎭</div>
            <p>Select a beat to view its pictograph</p>
          </div>
        {/if}
      </div>
    </div>

    <!-- Bottom section: Adjustment Panel (35% height) -->
    <div class="adjustment-section">
      <MainAdjustmentPanel
        bind:this={adjustmentPanel}
        {selectedBeatIndex}
        {selectedBeatData}
        onOrientationChanged={handleOrientationChanged}
        onTurnAmountChanged={handleTurnAmountChanged}
      />
    </div>
  </div>
</div>

<style>
  .graph-editor {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    overflow: hidden;
    backdrop-filter: blur(10px);
    min-height: 400px;
  }

  .error-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-sm) var(--spacing-md);
    background: rgba(255, 0, 0, 0.1);
    border-bottom: 1px solid rgba(255, 0, 0, 0.3);
    color: var(--destructive);
    font-size: var(--font-size-sm);
  }

  .error-banner button {
    background: none;
    border: none;
    color: var(--destructive);
    cursor: pointer;
    font-size: var(--font-size-lg);
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .graph-content {
    flex: 1;
    /* Modern 2025 CSS Grid - zero gap, content fills naturally */
    display: grid;
    grid-template-rows: 1fr auto;
    gap: 0; /* No gap - pictograph grows to fill */
    align-items: stretch;
    min-height: 0;
    container-type: size; /* Enable container queries for intelligent sizing */
  }

  .pictograph-section {
    /* Fill all available space above adjustment section */
    width: 100%;
    min-height: 0;
    display: grid;
    place-items: center; /* Center pictograph in available space */
    container-type: size; /* Enable container queries on this section */
    /* Section expands vertically until pictograph reaches max size */
  }

  .pictograph-display {
    /* Size naturally based on container - no artificial constraints */
    width: 100%;
    height: 100%;
    display: grid;
    place-items: center;
    container-type: size;
  }

  /* Pictograph wrapper - 2025 intelligent container-aware sizing */
  .pictograph-display :global(.pictograph-wrapper) {
    /* Use container queries to be as large as possible while fitting */
    width: min(95cqw, 95cqh);
    aspect-ratio: 1 / 1;
    max-width: 100cqw;
    max-height: 100cqh;
    container-type: size;

    /* Smooth animation when size changes (e.g., when control panels expand/collapse) */
    /* Use all-properties transition to catch container query changes */
    transition: all var(--transition-normal);
    will-change: width, height;
  }

  /* Ensure pictograph respects wrapper constraints */
  .pictograph-display :global(.pictograph-wrapper .pictograph) {
    width: 100%;
    height: 100%;
    /* Override Pictograph's default 0.2s transition to match wrapper's 0.3s */
    transition: all var(--transition-normal) !important;
  }

  .pictograph-display :global(svg) {
    width: 100%;
    height: 100%;
    /* Ensure SVG also transitions smoothly */
    transition: all var(--transition-normal);
  }

  .no-pictograph {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: var(--muted-foreground);
    gap: var(--spacing-md);
  }

  .placeholder-icon {
    font-size: 3rem;
    opacity: 0.5;
  }

  .no-pictograph p {
    margin: 0;
    font-size: var(--font-size-md);
  }

  .adjustment-section {
    /* Grid gives this only the space it needs (auto row) */
    width: 100%;
    display: flex;
    flex-direction: column;
    border-radius: var(--border-radius);
    overflow: visible; /* Allow content to be fully visible */
    justify-self: stretch; /* Fill grid cell horizontally */
    align-self: end; /* Stick to bottom of container */
    /* Max height prevents turn controls from dominating */
    max-height: 300px;
    container-type: inline-size; /* Enable container queries for child components */
  }

  /* Mobile adjustments - only adjust control heights, grid handles the rest */
  @media (max-width: 768px) {
    .adjustment-section {
      max-height: 280px; /* More compact to give pictograph more space */
    }
  }

  @media (max-width: 480px) {
    .adjustment-section {
      max-height: 320px; /* More space for touch-friendly controls */
    }
  }
</style>
