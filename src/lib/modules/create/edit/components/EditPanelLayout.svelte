<!--
EditPanelLayout.svelte - Responsive Container Query Layout for Edit Panel

Uses modern 2025 patterns:
- Svelte 5 runes ($state, $derived) for reactivity
- CSS Container Queries for responsive layouts
- Proportional scaling based on available space
- No resize observers needed!

Layout Modes (determined by container size):
1. pictograph-top-cards-2col: Pictograph top, cards side-by-side (Z Fold folded)
2. pictograph-top-cards-stacked: Pictograph top, cards stacked (tall narrow)
3. pictograph-left-cards-right: Pictograph left, cards right (landscape wide)
4. all-stacked: All 3 stacked vertically (very narrow)
-->
<script lang="ts">
  import { Pictograph } from "$shared";
  import type { BeatData } from "$shared";
  import { onMount, onDestroy } from "svelte";
  import MainAdjustmentPanel from "./MainAdjustmentPanel.svelte";

  // Props
  let {
    selectedBeatIndex,
    selectedBeatData,
    onOrientationChanged,
    onTurnAmountChanged,
  } = $props<{
    selectedBeatIndex: number | null;
    selectedBeatData: BeatData | null;
    onOrientationChanged: (color: string, orientation: string) => void;
    onTurnAmountChanged: (color: string, turnAmount: number) => void;
  }>();

  // Component references for imperative API
  let mainAdjustmentPanelRef = $state<MainAdjustmentPanel | null>(null);
  let containerElement = $state<HTMLDivElement | null>(null);

  // Container width detection for simplified layout mode
  let containerWidth = $state(0);
  let resizeObserver: ResizeObserver | null = null;

  // Determine if we should use simplified layout based on container width
  // Narrow portrait (Z Fold 344px): <= 500px uses simplified always-visible controls
  const useSimplifiedLayout = $derived(
    containerWidth > 0 && containerWidth <= 500
  );

  // Expose getSelectedArrow method to parent
  export function getSelectedArrow(): string | null {
    return mainAdjustmentPanelRef?.getSelectedArrow() ?? null;
  }

  // Create beat data with any additional flags needed for pictograph display
  const beatDataForPictograph = $derived(() => {
    if (!selectedBeatData) return null;
    return {
      ...selectedBeatData,
      // Add any additional display properties if needed
    };
  });

  // Observe container width to detect narrow layouts
  onMount(() => {
    if (containerElement) {
      resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          containerWidth = entry.contentRect.width;
        }
      });
      resizeObserver.observe(containerElement);
    }
  });

  onDestroy(() => {
    if (resizeObserver) {
      resizeObserver.disconnect();
    }
  });
</script>

<!--
Container query aware layout
The container will change layout based on its OWN size, not viewport
-->
<div
  class="edit-panel-layout"
  data-testid="edit-panel-layout"
  bind:this={containerElement}
>
  <!-- Pictograph Display -->
  <div class="pictograph-container" data-testid="pictograph-container">
    {#if beatDataForPictograph()}
      <div class="pictograph-wrapper">
        <Pictograph pictographData={beatDataForPictograph()} />
      </div>
    {:else}
      <div class="pictograph-placeholder">
        <p>No beat selected</p>
      </div>
    {/if}
  </div>

  <!-- Adjustment Controls -->
  <div class="adjustment-container" data-testid="adjustment-container">
    <MainAdjustmentPanel
      bind:this={mainAdjustmentPanelRef}
      {selectedBeatIndex}
      {selectedBeatData}
      {onOrientationChanged}
      {onTurnAmountChanged}
      {useSimplifiedLayout}
    />
  </div>
</div>

<style>
  /*
   * Container Query Setup
   * The .edit-panel-layout establishes a container context
   * All child layouts respond to THIS container's size, not viewport
   */
  .edit-panel-layout {
    /* Establish container query context */
    container-type: inline-size;
    container-name: edit-panel;

    /* Fill parent (EditSlidePanel content area) */
    width: 100%;
    height: 100%;

    /* CSS Grid for flexible layouts */
    display: grid;
    gap: var(--spacing-md, 16px);
    padding: var(--spacing-md, 16px);
    background: transparent;

    /* Default layout: Pictograph top (grows), controls bottom (fixed) */
    grid-template-columns: 1fr;
    grid-template-rows: 1fr auto;
    grid-template-areas:
      "pictograph"
      "adjustment";

    /* Center everything horizontally */
    place-items: center;
    align-content: start;
  }

  /* Pictograph Container - grows to fill available space */
  .pictograph-container {
    grid-area: pictograph;
    display: flex;
    align-items: center;
    justify-content: center;

    /* Fill available space */
    width: 100%;
    height: 100%;
    max-width: 100%;
    overflow: hidden;
  }

  .pictograph-wrapper {
    /* Pictograph scales to fit available space */
    width: 100%;
    height: 100%;
    max-width: min(400px, 90vw);
    max-height: 400px;
    aspect-ratio: 1; /* Keep square */
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .pictograph-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 150px;
    color: var(--muted-foreground);
    font-size: var(--font-size-sm);
  }

  /* Adjustment Container */
  .adjustment-container {
    grid-area: adjustment;
    overflow-y: auto;
    overflow-x: hidden;
    width: 100%;
    max-width: 600px; /* Constrain controls width */
    /* Ensure controls have minimum space and proper scrolling */
    min-height: 0;
    display: flex;
    flex-direction: column;
  }

  /*
   * CONTAINER QUERIES - Responsive Layouts Based on Panel Size
   * These respond to the edit-panel container's width, not viewport!
   */

  /*
   * Layout 1: Narrow panels (< 500px) - Typical mobile/portrait
   * Pictograph top with comfortable spacing, controls below
   */
  @container edit-panel (max-width: 500px) {
    .edit-panel-layout {
      gap: var(--spacing-sm, 12px);
      padding: var(--spacing-sm, 12px);
    }

    .pictograph-wrapper {
      max-width: min(320px, 85vw);
      max-height: 320px;
    }
  }

  /*
   * Layout 2: Medium panels (500-700px)
   * More breathing room
   */
  @container edit-panel (min-width: 500px) and (max-width: 700px) {
    .edit-panel-layout {
      gap: var(--spacing-md, 16px);
      padding: var(--spacing-md, 16px);
    }

    .pictograph-wrapper {
      max-width: 350px;
      max-height: 350px;
    }
  }

  /*
   * Layout 3: Wide panels (700px+)
   * Side-by-side layout - pictograph left, controls right
   */
  @container edit-panel (min-width: 700px) {
    .edit-panel-layout {
      grid-template-columns: minmax(300px, 400px) 1fr;
      grid-template-rows: 1fr;
      grid-template-areas: "pictograph adjustment";
      gap: var(--spacing-lg, 24px);
      padding: var(--spacing-lg, 24px);
      align-items: start;
    }

    .pictograph-wrapper {
      max-width: 400px;
      max-height: 400px;
    }

    .adjustment-container {
      /* Full height in side-by-side */
      height: 100%;
    }
  }
</style>
