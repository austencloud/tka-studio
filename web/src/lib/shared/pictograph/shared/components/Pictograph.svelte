<!--
Pictograph.svelte - Unified Pictograph Component with Svelte 5 Snippets

Modern unified component that consolidates state management and SVG rendering.
Uses Svelte 5 snippets for better organization and eliminates prop drilling.

ARCHITECTURE:
- createPictographState: Handles all pictograph state management with Svelte 5 runes
- Snippets: Organize SVG rendering logic (empty state, loading, overlays)
- Direct component integration: No artificial separation between state and rendering
-->
<script lang="ts">
  import {
    BeatNumber,
    EmptyStateIndicator,
    GridMode,
    ReversalIndicators,
    type PictographData,
  } from "$shared";
  import { onMount } from "svelte";
  import { resolve, TYPES } from "../../../inversify";
  import ArrowSvg from "../../arrow/rendering/components/ArrowSvg.svelte";
  import GridSvg from "../../grid/components/GridSvg.svelte";
  import type { IGridModeDeriver } from "../../grid/services/contracts";
  import PropSvg from "../../prop/components/PropSvg.svelte";
  import { TKAGlyph } from "../../tka-glyph";
  import { createPictographState } from "../state/pictograph-state.svelte";

  // Enhanced Props interface - includes beat-specific properties for rendering
  let {
    pictographData = null,
    beatNumber = null,
    isStartPosition = false,
    isSelected = false,
    blueReversal = false,
    redReversal = false,
    showBeatNumber = true
  } = $props<{
    pictographData?: PictographData | null;
    beatNumber?: number | null;
    isStartPosition?: boolean;
    isSelected?: boolean;
    blueReversal?: boolean;
    redReversal?: boolean;
    showBeatNumber?: boolean;
  }>();

  // =============================================================================
  // STATE MANAGEMENT (using pictograph-state.svelte.ts)
  // =============================================================================

  // Create pictograph state with reactive data management
  const pictographState = createPictographState(pictographData);

  // Update state when props change
  $effect(() => {
    pictographState.updatePictographData(pictographData);
  });

  // =============================================================================
  // SVG RENDERING STATE (previously in PictographSvg)
  // =============================================================================

  // Loading coordination state
  let loadedComponents = $state(new Set<string>());

  // Track if all components are loaded for coordinated display
  const allComponentsLoaded = $derived(() => {
    if (!pictographState.hasValidData) return false;

    // Required components: grid only (props and arrows are pre-loaded by parent)
    const requiredComponents = ["grid"];

    return requiredComponents.every((component) =>
      loadedComponents.has(component)
    );
  });

  // Derive grid mode from pictograph data using Svelte 5 runes
  const gridMode = $derived(
    (() => {
      if (
        !pictographState.effectivePictographData ||
        !pictographState.effectivePictographData.motions?.blue ||
        !pictographState.effectivePictographData.motions?.red
      ) {
        return GridMode.DIAMOND; // Default fallback
      }

      try {
        const gridModeService = resolve<IGridModeDeriver>(
          TYPES.IGridModeDeriver
        );
        return gridModeService.deriveGridMode(
          pictographState.effectivePictographData.motions.blue,
          pictographState.effectivePictographData.motions.red
        );
      } catch (error) {
        console.warn("Failed to derive grid mode, using default:", error);
        return GridMode.DIAMOND; // Fallback to default on error
      }
    })()
  );

  // Standard pictograph viewBox
  const viewBox = "0 0 950 950";

  // =============================================================================
  // EVENT HANDLERS
  // =============================================================================

  // Enhanced component loading handler
  function handleComponentLoaded(componentName: string) {
    loadedComponents.add(componentName);
    loadedComponents = new Set(loadedComponents); // Trigger reactivity
    pictographState.handleComponentLoaded(componentName);
  }

  function handleComponentError(componentName: string, error: string) {
    pictographState.handleComponentError(componentName, error);
  }

  // =============================================================================
  // LIFECYCLE & EFFECTS
  // =============================================================================

  // Calculate arrow and prop positions when component mounts
  onMount(async () => {
    await pictographState.calculateArrowPositions();
    await pictographState.calculatePropPositions();
  });
</script>

{#snippet loadingPlaceholder()}
  <g class="loading-placeholder" opacity="0.3">
    <rect width="950" height="950" fill="#f3f4f6" />
    <text
      x="475"
      y="475"
      text-anchor="middle"
      dominant-baseline="middle"
      font-family="Arial, sans-serif"
      font-size="24"
      fill="#6b7280"
    >
      Loading...
    </text>
  </g>
{/snippet}







<!-- =============================================================================
     MAIN CONTAINER
     ============================================================================= -->
<div
  class="pictograph"
  class:loading={pictographState.isLoading}
  class:loaded={pictographState.isLoaded}
  class:has-error={pictographState.errorMessage}
>
  <svg
    width="100%"
    height="100%"
    {viewBox}
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label={pictographState.hasValidData ? "Pictograph" : "Empty Pictograph"}
  >
    <!-- Background -->
    <rect width="950" height="950" fill="white" />

    {#if pictographState.hasValidData}
      <!-- Show loading placeholder until all components are loaded -->
      {#if !allComponentsLoaded}
        {@render loadingPlaceholder()}
      {/if}

      <!-- Grid (always rendered first) -->
      <GridSvg
        {gridMode}
        onLoaded={() => handleComponentLoaded("grid")}
        onError={(error) => handleComponentError("grid", error)}
      />

      <!-- Props (rendered first so arrows appear on top) -->
      {#each pictographState.motionsToRender as { color, motionData } (color)}
        {#if pictographState.effectivePictographData && pictographState.propAssets[color] && pictographState.propPositions[color]}
          <PropSvg
            {motionData}
            propAssets={pictographState.propAssets[color]}
            propPosition={pictographState.propPositions[color]}
            showProp={pictographState.showProps}
          />
        {/if}
      {/each}

      <!-- Arrows (rendered after props) -->
      {#each pictographState.motionsToRender as { color, motionData } (color)}
        {#if pictographState.effectivePictographData && pictographState.arrowAssets[color] && pictographState.arrowPositions[color]}
          <ArrowSvg
            {motionData}
            arrowAssets={pictographState.arrowAssets[color]}
            arrowPosition={pictographState.arrowPositions[color]}
            shouldMirror={pictographState.arrowMirroring[color] || false}
            showArrow={pictographState.showArrows}
          />
        {/if}
      {/each}

      <!-- Letter/Glyph overlay -->
      {#if pictographState.displayLetter}
        <TKAGlyph letter={pictographState.displayLetter} turnsTuple="(s, 0, 0)" />
      {/if}

      <!-- Beat number overlay -->
      <BeatNumber
        {beatNumber}
        {showBeatNumber}
        {isStartPosition}
        hasValidData={pictographState.hasValidData}
      />

      <!-- Reversal indicators -->
      <ReversalIndicators
        {blueReversal}
        {redReversal}
        hasValidData={pictographState.hasValidData}
      />
    {:else}
      <!-- Empty state -->
      <EmptyStateIndicator
        {beatNumber}
        hasValidData={pictographState.hasValidData}
      />
    {/if}
  </svg>
</div>

<!-- =============================================================================
     STYLES (unified container and SVG styles)
     ============================================================================= -->
<style>
  .pictograph {
    position: relative;
    border-radius: 0; /* Remove border radius so pictographs touch */
    transition: all 0.2s ease;
    background: white;
    border: none; /* Remove border to maximize content space */
    width: 100%;
    height: 100%;
    display: block;
    margin: 0; /* Remove any margin */
    padding: 0; /* Remove any padding */
  }

  .pictograph.loading {
    opacity: 0.8;
  }

  .pictograph.has-error {
    border-color: #ef4444;
  }

  /* SVG styles (from PictographSvg) */
  svg {
    display: block;
    box-sizing: border-box;
  }

  :global(.component-loading) {
    opacity: 0.5;
    animation: pulse 1s infinite;
  }

  @keyframes pulse {
    0% {
      opacity: 0.5;
    }
    50% {
      opacity: 0.8;
    }
    100% {
      opacity: 0.5;
    }
  }
</style>
